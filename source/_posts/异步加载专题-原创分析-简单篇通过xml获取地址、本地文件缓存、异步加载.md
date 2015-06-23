title: [异步加载专题][原创分析]简单篇通过xml获取地址、本地文件缓存、异步加载
date: 2012-12-31 08:35:03
tags:
- xml
- 异步加载
- Android

---

> 本文分析该内容：http://l5.yunpan.cn/lk/QkvuDuuCFWS89

首先我们看下作者的思路：

创建缓存目录 ->; 通过一个线程进行获取xml文件内容  ->; 对获取的xml文件进行解析获取所有的图片id、图片名称、图片地址 -> 在线程中通过Handler的Message创建listview的adapter -> 在adapter中实现异步加载图片资源.

<!--more-->
//下一篇将分析：[异步加载专题][原创分析]中级篇本地缓存、ListView滑动停止加载、利用synchronized控制线程数机制、很好的文件结构
下面我们开始分析MainActivity:

```
package com.example.synctask;
 
import java.io.File;
import java.util.List;
 
import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.widget.ListView;
 
public class MainActivity extends Activity {
	protected static final int SUCCESS_GET_CONTACT = 0;
	private ListView mListView;
	private ImageAdapter mAdapter;
	private File cache;
 
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
 
        mListView = (ListView) findViewById(R.id.listView);
 
        //创建缓存目录，系统一运行就得创建缓存目录的，
        cache = new File(Environment.getExternalStorageDirectory(), "cache");
 
        if(!cache.exists()){
        	cache.mkdirs();
        }
 
        //获取数据，主UI线程是不能做耗时操作的，所以启动子线程来做
        new Thread(){
        	public void run() {
        		ContactService service = new ContactService();
        		List<contact> contacts = null;
				try {
					contacts = service.getContactAll();
				} catch (Exception e) {
					e.printStackTrace();
				}
				//子线程通过Message对象封装信息，并且用初始化好的，
				//Handler对象的sendMessage()方法把数据发送到主线程中，从而达到更新UI主线程的目的
        		Message msg = new Message();
        		msg.what = SUCCESS_GET_CONTACT;
        		msg.obj = contacts;
        		mHandler.sendMessage(msg);
        	};
        }.start();
    }
 
    private Handler mHandler = new Handler(){
		public void handleMessage(android.os.Message msg) {
			if(msg.what == SUCCESS_GET_CONTACT){
				List<contact> contacts = (List<contact>) msg.obj;
				mAdapter = new ImageAdapter(getApplicationContext(),contacts,cache);
				mListView.setAdapter(mAdapter);
			}
		};
	};
 
    @Override
    protected void onDestroy() {
    	super.onDestroy();
    	//清空缓存
    	File[] files = cache.listFiles();
    	for(File file :files){
    		file.delete();
    	}
    	cache.delete();
    }
}
```

其中Contact用于存储从xml中读取到的对象类型：

```
package com.example.synctask;
 
public class Contact {
	int id;
	String image;
	String name;
 
	public Contact() {
		super();
	}
	public Contact(int id, String image, String name) {
		this.id = id;
		this.image = image;
		this.name = name;
	}
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getImage() {
		return image;
	}
	public void setImage(String image) {
		this.image = image;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
 
}
```

ContactService 用于获取网络资源:

```
package com.example.synctask;
 
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
 
 
import org.xmlpull.v1.XmlPullParser;
 
import android.graphics.Bitmap;
import android.net.Uri;
import android.util.Xml;
 
public class ContactService {
 
	/*
	 * 从服务器上获取数据
	 */
	public List<contact> getContactAll() throws Exception {
		List<contact> contacts = null;
		String Parth = "http://xxx.dreamtobe.cn:8080/xxx/list.xml";
		URL url = new URL(Parth);
		HttpURLConnection conn = (HttpURLConnection) url.openConnection();
		conn.setConnectTimeout(30000);
		conn.setReadTimeout(30000);
		conn.setRequestMethod("GET");
		if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
			InputStream is = conn.getInputStream();
			// 这里获取数据直接放在XmlPullParser里面解析
			contacts = xmlParser(is);
			return contacts;
		} else {
			return null;
		}
	}
 
	// 这里并没有下载图片下来，而是把图片的地址保存下来了
	private List<contact> xmlParser(InputStream is) throws Exception {
		List<contact> contacts = null;
		Contact contact = null;
		XmlPullParser parser = Xml.newPullParser();
		parser.setInput(is, "UTF-8");
		int eventType = parser.getEventType();
		while ((eventType = parser.next()) != XmlPullParser.END_DOCUMENT) {
			switch (eventType) {
			case XmlPullParser.START_TAG:
				if (parser.getName().equals("contacts")) {
					contacts = new ArrayList<contact>();
				} else if (parser.getName().equals("contact")) {
					contact = new Contact();
					contact.setId(Integer.valueOf(parser.getAttributeValue(0)));
				} else if (parser.getName().equals("name")) {
					contact.setName(parser.nextText());
				} else if (parser.getName().equals("image")) {
					contact.setImage(parser.getAttributeValue(0));
				}
				break;
 
			case XmlPullParser.END_TAG:
				if (parser.getName().equals("contact")) {
					contacts.add(contact);
				}
				break;
			}
		}
		return contacts;
	}
 
	/*
	 * 从网络上获取图片，如果图片在本地存在的话就直接拿，如果不存在再去服务器上下载图片
	 * 这里的path是图片的地址
	 */
	public Uri getImageURI(String path, File cache) throws Exception {
		String name = MD5.getMD5(path) + path.substring(path.lastIndexOf("."));
		File file = new File(cache, name);
		// 如果图片存在本地缓存目录，则不去服务器下载
		if (file.exists()) {
			return Uri.fromFile(file);//Uri.fromFile(path)这个方法能得到文件的URI
		} else {
			// 从网络上获取图片
			URL url = new URL(path);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setConnectTimeout(5000);
			conn.setRequestMethod("GET");
			conn.setDoInput(true);
			if (conn.getResponseCode() == 200) {
 
				InputStream is = conn.getInputStream();
				FileOutputStream fos = new FileOutputStream(file);
				byte[] buffer = new byte[1024];
				int len = 0;
				while ((len = is.read(buffer)) != -1) {
					fos.write(buffer, 0, len);
				}
				is.close();
				fos.close();
				// 返回一个URI对象
				return Uri.fromFile(file);
			}
		}
		return null;
	}
}
```

其中MainActivity中的线程：

```
//获取数据，主UI线程是不能做耗时操作的，所以启动子线程来做
        new Thread(){
        	public void run() {
        		ContactService service = new ContactService();
        		List<contact> contacts = null;
				try {
					contacts = service.getContactAll();
				} catch (Exception e) {
					e.printStackTrace();
				}
				//子线程通过Message对象封装信息，并且用初始化好的，
				//Handler对象的sendMessage()方法把数据发送到主线程中，从而达到更新UI主线程的目的
        		Message msg = new Message();
        		msg.what = SUCCESS_GET_CONTACT;
        		msg.obj = contacts;
        		mHandler.sendMessage(msg);
        	};
        }.start();
```

先通过

```
contacts = service.getContactAll();
```

获得解析后的所有的Contact.
通过Hanlder的Message

```
Message msg = new Message();
        		msg.what = SUCCESS_GET_CONTACT;
        		msg.obj = contacts;
        		mHandler.sendMessage(msg);
```

发送到

```
private Handler mHandler = new Handler(){
		public void handleMessage(android.os.Message msg) {
			if(msg.what == SUCCESS_GET_CONTACT){
				List<contact> contacts = (List<contact>) msg.obj;
				mAdapter = new ImageAdapter(getApplicationContext(),contacts,cache);
				mListView.setAdapter(mAdapter);
			}
		};
	};
```

在handleMessage中创建ListView的Adapter.
在ImageAdapter中：

```
@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		// 1获取item,再得到控件
		// 2 获取数据
		// 3绑定数据到item
		ViewHolder holder = null;
		if (convertView == null) {
			holder = new ViewHolder();
 
			convertView = mInflater.inflate(R.layout.item, null);
 
			holder.iv_header = (ImageView) convertView.findViewById(R.id.imageView);
			holder.tv_name = (TextView) convertView.findViewById(R.id.textView);
 
			convertView.setTag(holder);
		}else {
			holder = (ViewHolder)convertView.getTag();
		}
 
		Contact contact = contacts.get(position);
 
		// 异步的加载图片 (线程池 + Handler ) ---> AsyncTask
		asyncloadImage(holder.iv_header, contact.image);
 
		holder.tv_name.setText(contact.name);
 
		return convertView;
	}
```

调用asyncloadImage顾名思义异步加载图片:

```
private void asyncloadImage(ImageView iv_header, String path) {
		ContactService service = new ContactService();
		AsyncImageTask task = new AsyncImageTask(service, iv_header);
		task.execute(path);
	}
```

在其中创建联网下载图片的对象service传入以AsyncTask 为父类（暂且理解为可以更新UI的线程）的task对象.

```
private final class AsyncImageTask extends AsyncTask<string, Integer, Uri> {
 
		private ContactService service;
		private ImageView iv_header;
 
		public AsyncImageTask(ContactService service, ImageView iv_header) {
			this.service = service;
			this.iv_header = iv_header;
		}
 
		// 后台运行的子线程子线程
		@Override
		protected Uri doInBackground(String... params) {
			try {
				return service.getImageURI(params[0], cache);
			} catch (Exception e) {
				e.printStackTrace();
			}
			return null;
		}
 
		// 这个放在在ui线程中执行
		@Override
		protected void onPostExecute(Uri result) {
			super.onPostExecute(result);
			// 完成图片的绑定
			if (iv_header != null && result != null) {
				iv_header.setImageURI(result);
			}
		}
	}
```

我们可以清晰的看到：
此类在:protected void onPostExecute(Uri result)是需要传入一个Uri类型的值得。
而protected Uri doInBackground(String… params)的返回值恰好是Uri(通过后面我们可以清晰的了解到，这个值就是传递给onPostExecute的）。
而这个线程的请求应该是通过：task.execute(path);
我们看下protected Uri doInBackground(String… params)

```
// 后台运行的子线程子线程
		@Override
		protected Uri doInBackground(String... params) {
			try {
				return service.getImageURI(params[0], cache);
			} catch (Exception e) {
				e.printStackTrace();
			}
			return null;
		}
```

这个在后台运行的子线程子线程调通过getImageURI返回获取Uri.
我们看下：getImageURI:
```
/*
	 * 从网络上获取图片，如果图片在本地存在的话就直接拿，如果不存在再去服务器上下载图片
	 * 这里的path是图片的地址
	 */
	public Uri getImageURI(String path, File cache) throws Exception {
		String name = MD5.getMD5(path) + path.substring(path.lastIndexOf("."));
		File file = new File(cache, name);
		// 如果图片存在本地缓存目录，则不去服务器下载
		if (file.exists()) {
			return Uri.fromFile(file);//Uri.fromFile(path)这个方法能得到文件的URI
		} else {
			// 从网络上获取图片
			URL url = new URL(path);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setConnectTimeout(5000); //5000毫秒 请求无连接直接返回Timeout
			conn.setRequestMethod("GET"); //通过get请求
			conn.setDoInput(true);
			if (conn.getResponseCode() == 200) {
 
				InputStream is = conn.getInputStream();
				FileOutputStream fos = new FileOutputStream(file);
				byte[] buffer = new byte[1024];
				int len = 0;
				while ((len = is.read(buffer)) != -1) {
					fos.write(buffer, 0, len);
				}
				is.close();
				fos.close();
				// 返回一个URI对象
				return Uri.fromFile(file);
			}
		}
		return null;
	}
```

这里已经备注的很清晰了，需要提到的是这里通过MD5来加密了获取到的图片的名字.
就是项目中涉及到的：

```
package com.example.synctask;
 
import java.security.MessageDigest;
import java.util.Iterator;
 
public class MD5 {
	public static String getMD5(String content) {
		try {
			MessageDigest digest = MessageDigest.getInstance("MD5");
			digest.update(content.getBytes());
			return getHashString(digest);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}
 
	public static String getHashString(MessageDigest digest) {
		StringBuilder builder = new StringBuilder();
		for (byte b : digest.digest()) {
			builder.append(Integer.toHexString((b >> 4) & 0xf));
			builder.append(Integer.toHexString(b & 0xf));
 
		}
		return builder.toString();
	}
}
```

此时更新ui

```
// 这个放在在ui线程中执行
		@Override
		protected void onPostExecute(Uri result) {
			super.onPostExecute(result);
			// 完成图片的绑定
			if (iv_header != null && result != null) {
				iv_header.setImageURI(result);
			}
		}
```

至此简单的异步加载就实现了。