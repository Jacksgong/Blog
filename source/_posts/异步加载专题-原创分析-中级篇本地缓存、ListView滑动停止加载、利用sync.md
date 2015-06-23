title: 【异步加载专题】【原创分析】中级篇-各类架构与线程数控制
date: 2012-12-31 08:35:03
tags:
- Android
- ListView
- synchronized
- 异步加载
- 文件结构
- 本地缓存

---

> 本文分析此源码(源码作者也许叫cindy吧）：http://s.yunio.com/Wd8Nxm

![](/img/async-1.png)

<!--more-->

> 本项目非常值得分析的一点除了它的异步加载外，还有它良好的文件结构：
固定的临时文件夹创建放在MyApp(继承于Application）（如备注，当application/package被创建时，此函数被实例化:

```
package cindy.android.test.synclistview;
 
import java.io.File;
 
import android.app.Application;
import android.os.Environment;
 
public class MyApp extends Application{
//will cause that class to be instantiated for you when the process for your application/package is created...
	//create cache on install application
	@Override
	public void onCreate() {
		// TODO Auto-generated method stub
		super.onCreate();
		File f = new File(Environment.getExternalStorageDirectory()+"/TestSyncListView/");
		if(!f.exists()){
			f.mkdir();
		}
	}
 
}
```

当然了，需要在AndroidManifest.xml中定义：

```
........
```

Log记录做一个类，这样即可以统一管理TAG也可以清晰的通过此类明白自己项目会涉及到问题.并且统一管理对应的显示规则：

```
package cindy.android.test.synclistview;
 
import android.content.Context;
import android.util.Log;
import android.widget.Toast;
 
public class DebugUtil {
    public static final String TAG = "DebugUtil";
    public static final boolean DEBUG = true;
     //for debug show log.
    public static void toast(Context context,String content){
        Toast.makeText(context, content, Toast.LENGTH_SHORT).show();
    }
 
    public static void debug(String tag,String msg){
        if (DEBUG) {
            Log.d(tag, msg);
        }
    }
 
    public static void debug(String msg){
        if (DEBUG) {
            Log.d(TAG, msg);
        }
    }
 
    public static void error(String tag,String error){
        Log.e(tag, error);
    }
 
    public static void error(String error){
        Log.e(TAG, error);
    }
}
```

本项目封装了入口Activity的父类：

```
package cindy.android.test.synclistview;
 
import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.Window;
import android.widget.Toast;
 
public abstract class AbstructCommonActivity extends Activity  {
 
	//Main Activity's Parent
	//Window Feature_no_Title
	//Hanlder to Show some tip.
	private MyHandler handler = new MyHandler();
 
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
	}
 
	protected void handleOtherMessage(int flag){
 
	}
 
	public void sendMessage(int flag) {
		handler.sendEmptyMessage(flag);
	}
 
	public void sendMessageDely(int flag,long delayMillis){
		handler.sendEmptyMessageDelayed(flag, delayMillis);
	}
 
	public void showToast(String toast_message){
		handler.toast_message = toast_message;
		sendMessage(MyHandler.SHOW_STR_TOAST);
	}
 
	public void showToast(int res){
		handler.toast_res = res;
		sendMessage(MyHandler.SHOW_RES_TOAST);
	}
 
	private class MyHandler extends Handler {
		public static final int SHOW_STR_TOAST = 0;
		public static final int SHOW_RES_TOAST = 1;
 
		private String toast_message=null;
		private int toast_res;
 
		@Override
		public void handleMessage(Message msg) {
			if (!Thread.currentThread().isInterrupted()) {
				switch (msg.what) {
					case SHOW_STR_TOAST:
						Toast.makeText(getBaseContext(), toast_message, 1).show();
						break;
					case SHOW_RES_TOAST:
						Toast.makeText(getBaseContext(), toast_res, 1).show();
						break;
					default:
						handleOtherMessage(msg.what);
				}
			}
		}
 
	}
}
```

通过这个统一管理了主要的一些Toast简化代码量的同时也清晰了项目会遇到的一些需要给用户提示的情况，并且定义了整体的布局。这是一个很好的方法。

由于加载是从网络上来的，需要延时是难免的。通过ProgressBar来下意识用户等候是常用方法，本项目作者将整个延时等待的load框架封装出来：

```
package cindy.android.test.synclistview;
 
import android.content.Context;
import android.util.AttributeSet;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
import android.widget.TextView;
 
public class LoadStateView extends RelativeLayout{
	//Loading RelativeLayout
	ProgressBar progBar;
 
	LinearLayout downLoadErrMsgBox;
 
	TextView downLoadErrText;
 
	Button btnListLoadErr;
 
	public LoadStateView(Context context, AttributeSet attrs) {
		super(context, attrs);
		// TODO Auto-generated constructor stub
	}
 
	@Override
	protected void onFinishInflate() {
		// TODO Auto-generated method stub
		super.onFinishInflate();
		progBar = (ProgressBar) findViewById(R.id.progBar);
		downLoadErrMsgBox = (LinearLayout) findViewById(R.id.downLoadErrMsgBox);
		downLoadErrText = (TextView) findViewById(R.id.downLoadErrText);
		btnListLoadErr = (Button) findViewById(R.id.btnListLoadErr);
	}
 
	public void startLoad(){
		downLoadErrMsgBox.setVisibility(View.GONE);
		progBar.setVisibility(View.VISIBLE);
	}
 
	public void stopLoad(){
		progBar.setVisibility(View.GONE);
	}
 
	public void showError(){
		downLoadErrMsgBox.setVisibility(View.VISIBLE);
		progBar.setVisibility(View.GONE);
	}
 
	public void showEmpty(){
		downLoadErrMsgBox.setVisibility(View.VISIBLE);
		progBar.setVisibility(View.GONE);
	}
 
	public void setOnReloadClickListener(OnClickListener onReloadClickListener){
		btnListLoadErr.setOnClickListener(onReloadClickListener);
	}
}
```

这样很好的对加载框架进行控制，隐藏了方法，同时使可读性增强。

下面我们进入本项目的分析：
我们先按管理分析下作者的思路：
如果加载成功隐藏加载框架，失败显示按钮与有关文字 -> 滑动如果处于闲置状态进行加载对应范围内的图片.
首先我们看看入口Activity:

```
package cindy.android.test.synclistview;
 
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
 
public class TestListViewActivity extends AbstructCommonActivity
	implements AdapterView.OnItemClickListener{
 
	ListView viewBookList;
 
	BookItemAdapter adapter;
 
	//ViewGroup listFolder;
 
	LoadStateView loadStateView;
 
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);
		viewBookList = (ListView) findViewById(R.id.viewBookList);
		adapter = new BookItemAdapter(this,viewBookList);
		loadStateView = (LoadStateView) findViewById(R.id.downloadStatusBox);
 
		loadStateView.setOnReloadClickListener(new View.OnClickListener() {
 
			@Override
			public void onClick(View v) {
				reload();
			}
		});
		//listFolder = (ViewGroup) getLayoutInflater().inflate(R.layout.load_more, null);
		//viewBookList.addFooterView(listFolder);
		viewBookList.setAdapter(adapter);
		viewBookList.setOnItemClickListener(this);
		reload();
	}
 
	private void reload(){
		adapter.clean();
		loadStateView.startLoad();
		new Thread(new Runnable(){
			@Override
			public void run() {
				try {
					Thread.sleep(2*1000);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				loadDate();
				sendMessage(REFRESH_LIST);
//				sendMessageDely(LOAD_IMAGE, 500);
			}
		}).start();
	}
 
	public void loadDate(){
		for(int i=0;i&lt;10;i++){
			adapter.addBook("吞噬星空"+i,
			"http://www.pfwx.com/bookinfo/11/11000.html",
			"http://www.pfwx.com/files/article/image/11/11000/11000s.jpg");
 
			adapter.addBook("仙逆"+i,
			"http://www.pfwx.com/bookinfo/9/9760.html",
			"http://www.pfwx.com/files/article/image/9/9760/9760s.jpg");
 
			adapter.addBook("武动乾坤"+i,
			"http://www.pfwx.com/bookinfo/13/13939.html",
			"http://www.pfwx.com/files/article/image/13/13939/13939s.jpg");
 
			adapter.addBook("凡人修仙传"+i,
			"http://www.pfwx.com/bookinfo/3/3237.html",
			"http://www.pfwx.com/files/article/image/3/3237/3237s.jpg");
 
			adapter.addBook("遮天"+i,
			"http://www.pfwx.com/bookinfo/11/11381.html",
			"http://www.pfwx.com/files/article/image/11/11381/11381s.jpg");
		}
	}
 
	@Override
	public void onItemClick(AdapterView&lt;?&gt; arg0, View arg1, int arg2, long arg3) {
 
	}
 
	private static final int REFRESH_LIST = 0x10001;
	private static final int SHOW_LOAD_STATE_VIEW = 0x10003;
	private static final int HIDE_LOAD_STATE_VIEW = 0x10004;
 
	@Override
	protected void handleOtherMessage(int flag) {
		switch (flag) {
		case REFRESH_LIST:
			adapter.notifyDataSetChanged();
			loadStateView.stopLoad();
			if(adapter.getCount() == 0){
				loadStateView.showEmpty();
			}
			break;
		case SHOW_LOAD_STATE_VIEW:
			loadStateView.startLoad();
			break;
		case HIDE_LOAD_STATE_VIEW:
			loadStateView.stopLoad();
			break;
 
		default:
			break;
		}
	}
 
}
```

继承自封装好的Activity。
创建一个adapter对象：

```
adapter = new BookItemAdapter(this,viewBookList);
```

下面我们来看下BookItemAdapter:

```
package cindy.android.test.synclistview;
 
import java.util.Vector;
 
import android.content.Context;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
 
public class BookItemAdapter extends BaseAdapter{
	//Main List Adapter
	private LayoutInflater mInflater;
	private Context mContext;
	private Vector mModels = new Vector();
	private ListView mListView;
	SyncImageLoader syncImageLoader;
 
	public BookItemAdapter(Context context,ListView listView){
		mInflater = LayoutInflater.from(context);
		syncImageLoader = new SyncImageLoader();
		mContext = context;
		mListView = listView;
 
		mListView.setOnScrollListener(onScrollListener);
	}
 
	public void addBook(String book_name,String out_book_url,String out_book_pic){
		BookModel model = new BookModel();
		model.book_name =book_name;
		model.out_book_url = out_book_url;
		model.out_book_pic = out_book_pic;
		mModels.add(model);
	}
 
	public void clean(){
		mModels.clear();
	}
 
	@Override
	public int getCount() {
		// TODO Auto-generated method stub
		return mModels.size();
	}
 
	@Override
	public Object getItem(int position) {
		if(position &gt;= getCount()){
			return null;
		}
		return mModels.get(position);
	}
 
	@Override
	public long getItemId(int position) {
		// TODO Auto-generated method stub
		return position;
	}
 
	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		if(convertView == null){
			convertView = mInflater.inflate(R.layout.book_item_adapter, null);
		}
		BookModel model = mModels.get(position);
		convertView.setTag(position);
		ImageView iv = (ImageView) convertView.findViewById(R.id.sItemIcon);
		TextView sItemTitle =  (TextView) convertView.findViewById(R.id.sItemTitle);
		TextView sItemInfo =  (TextView) convertView.findViewById(R.id.sItemInfo);
		sItemTitle.setText(model.book_name);
		sItemInfo.setText(model.out_book_url);
		iv.setBackgroundResource(R.drawable.rc_item_bg);
		syncImageLoader.loadImage(position,model.out_book_pic,imageLoadListener);
		return  convertView;
	}
 
	SyncImageLoader.OnImageLoadListener imageLoadListener = new SyncImageLoader.OnImageLoadListener(){
 
		@Override
		public void onImageLoad(Integer t, Drawable drawable) {
			//BookModel model = (BookModel) getItem(t);
			View view = mListView.findViewWithTag(t);
			if(view != null){
				ImageView iv = (ImageView) view.findViewById(R.id.sItemIcon);
				iv.setBackgroundDrawable(drawable);
			}
		}
		@Override
		public void onError(Integer t) {
			BookModel model = (BookModel) getItem(t);
			View view = mListView.findViewWithTag(model);
			if(view != null){
				ImageView iv = (ImageView) view.findViewById(R.id.sItemIcon);
				iv.setBackgroundResource(R.drawable.rc_item_bg);
			}
		}
 
	};
 
	public void loadImage(){
		int start = mListView.getFirstVisiblePosition();
		int end =mListView.getLastVisiblePosition();
		if(end &gt;= getCount()){
			end = getCount() -1;
		}
		syncImageLoader.setLoadLimit(start, end);
		syncImageLoader.unlock();
	}
 
	AbsListView.OnScrollListener onScrollListener = new AbsListView.OnScrollListener() {
 
		@Override
		public void onScrollStateChanged(AbsListView view, int scrollState) {
			switch (scrollState) {
				case AbsListView.OnScrollListener.SCROLL_STATE_FLING:
					DebugUtil.debug("SCROLL_STATE_FLING");
					syncImageLoader.lock();
					break;
				case AbsListView.OnScrollListener.SCROLL_STATE_IDLE:
					DebugUtil.debug("SCROLL_STATE_IDLE");
					loadImage();
					//loadImage();
					break;
				case AbsListView.OnScrollListener.SCROLL_STATE_TOUCH_SCROLL:
					syncImageLoader.lock();
					break;
 
				default:
					break;
			}
 
		}
 
		@Override
		public void onScroll(AbsListView view, int firstVisibleItem,
				int visibleItemCount, int totalItemCount) {
			// TODO Auto-generated method stub
 
		}
	};
}
```

此Adapter在构造时还获得了对应的ListView
我们可以看到

```
mListView.setOnScrollListener(onScrollListener);
```

我们看下onScrollListener:

```
AbsListView.OnScrollListener onScrollListener = new AbsListView.OnScrollListener() {
 
		@Override
		public void onScrollStateChanged(AbsListView view, int scrollState) {
			switch (scrollState) {
				case AbsListView.OnScrollListener.SCROLL_STATE_FLING:
					DebugUtil.debug("SCROLL_STATE_FLING");
					syncImageLoader.lock();
					break;
				case AbsListView.OnScrollListener.SCROLL_STATE_IDLE:
					DebugUtil.debug("SCROLL_STATE_IDLE");
					loadImage();
					//loadImage();
					break;
				case AbsListView.OnScrollListener.SCROLL_STATE_TOUCH_SCROLL:
					syncImageLoader.lock();
					break;
 
				default:
					break;
			}
 
		}
 
		@Override
		public void onScroll(AbsListView view, int firstVisibleItem,
				int visibleItemCount, int totalItemCount) {
			// TODO Auto-generated method stub
 
		}
	};
```

这里主要就是当滑动闲置的时候解锁加载.我们深入看下：

```
package cindy.android.test.synclistview;
 
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.ref.SoftReference;
import java.net.URL;
import java.util.HashMap;
 
import android.graphics.drawable.Drawable;
import android.os.Environment;
import android.os.Handler;
 
public class SyncImageLoader {
	//Sync Image Loader
	//Message Load Image
	//
	private Object lock = new Object();
 
	private boolean mAllowLoad = true;
 
	private boolean firstLoad = true;
 
	private int mStartLoadLimit = 0;
 
	private int mStopLoadLimit = 0;
 
	final Handler handler = new Handler();
 
	private HashMap&lt;String, SoftReference&gt; imageCache = new HashMap&lt;String, SoftReference&gt;();
 
	public interface OnImageLoadListener {
		public void onImageLoad(Integer t, Drawable drawable);
		public void onError(Integer t);
	}
 
	public void setLoadLimit(int startLoadLimit,int stopLoadLimit){
		if(startLoadLimit &gt; stopLoadLimit){
			return;
		}
		mStartLoadLimit = startLoadLimit;
		mStopLoadLimit = stopLoadLimit;
	}
 
	public void restore(){
		mAllowLoad = true;
		firstLoad = true;
	}
 
	public void lock(){
		mAllowLoad = false;
		firstLoad = false;
	}
 
	public void unlock(){
		mAllowLoad = true;
		synchronized (lock) {
			lock.notifyAll(); //wake up all waiting thread.
		}
	}
 
	public void loadImage(Integer t, String imageUrl,
			OnImageLoadListener listener) {
		final OnImageLoadListener mListener = listener;
		final String mImageUrl = imageUrl;
		final Integer mt = t;
 
		new Thread(new Runnable() {
 
			@Override
			public void run() {
				if(!mAllowLoad){
					DebugUtil.debug("prepare to load");
					synchronized (lock) {
						try {
							lock.wait();
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
					}
				}
 
				if(mAllowLoad &amp;&amp; firstLoad){
					loadImage(mImageUrl, mt, mListener);
				}
 
				if(mAllowLoad &amp;&amp; mt &lt;= mStopLoadLimit &amp;&amp; mt &gt;= mStartLoadLimit){
					loadImage(mImageUrl, mt, mListener);
				}
			}
 
		}).start();
	}
 
	private void loadImage(final String mImageUrl,final Integer mt,final OnImageLoadListener mListener){
 
		if (imageCache.containsKey(mImageUrl)) {
            SoftReference softReference = imageCache.get(mImageUrl);
            final Drawable d = softReference.get();
            if (d != null) {
            	handler.post(new Runnable() {
    				@Override
    				public void run() {
    					if(mAllowLoad){
    						mListener.onImageLoad(mt, d);
    					}
    				}
    			});
                return;
            }
        }
		try {
			final Drawable d = loadImageFromUrl(mImageUrl);
			if(d != null){
                imageCache.put(mImageUrl, new SoftReference(d));
			}
			handler.post(new Runnable() {
				@Override
				public void run() {
					if(mAllowLoad){
						mListener.onImageLoad(mt, d);
					}
				}
			});
		} catch (IOException e) {
			handler.post(new Runnable() {
				@Override
				public void run() {
					mListener.onError(mt);
				}
			});
			e.printStackTrace();
		}
	}
 
	public static Drawable loadImageFromUrl(String url) throws IOException {
		DebugUtil.debug(url);
		if(Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED)){
			//if local SD CARD usable create local ache in SD card.
			File f = new File(Environment.getExternalStorageDirectory()+"/TestSyncListView/"+MD5.getMD5(url));
			if(f.exists()){
				FileInputStream fis = new FileInputStream(f);
				Drawable d = Drawable.createFromStream(fis, "src");
				return d;
			}
			URL m = new URL(url);
			InputStream i = (InputStream) m.getContent();
			DataInputStream in = new DataInputStream(i);
			FileOutputStream out = new FileOutputStream(f);
			byte[] buffer = new byte[1024];
			int   byteread=0;
			while ((byteread = in.read(buffer)) != -1) {
				out.write(buffer, 0, byteread);
			}
			in.close();
			out.close();
			Drawable d = Drawable.createFromStream(i, "src");
			return loadImageFromUrl(url);
		}else{
			//if local SD CARD unusable only get Drawable from input stream.
			URL m = new URL(url);
			InputStream i = (InputStream) m.getContent();
			Drawable d = Drawable.createFromStream(i, "src");
			return d;
		}
 
	}
}
```

可以清晰的看到只有当mAllowLoad与firstLoad同为true或者mAllowLoad与获得的position在当前界面的时候调用loadImage:

```
private void loadImage(final String mImageUrl,final Integer mt,final OnImageLoadListener mListener){
 
		if (imageCache.containsKey(mImageUrl)) {
            SoftReference softReference = imageCache.get(mImageUrl);
            final Drawable d = softReference.get();
            if (d != null) {
            	handler.post(new Runnable() {
    				@Override
    				public void run() {
    					if(mAllowLoad){
    						mListener.onImageLoad(mt, d);
    					}
    				}
    			});
                return;
            }
        }
		try {
			final Drawable d = loadImageFromUrl(mImageUrl);
			if(d != null){
                imageCache.put(mImageUrl, new SoftReference(d));
			}
			handler.post(new Runnable() {
				@Override
				public void run() {
					if(mAllowLoad){
						mListener.onImageLoad(mt, d);
					}
				}
			});
		} catch (IOException e) {
			handler.post(new Runnable() {
				@Override
				public void run() {
					mListener.onError(mt);
				}
			});
			e.printStackTrace();
		}
	}
```

这里的imageCache是一个哈希表
private HashMap&lt;String, SoftReference&gt; imageCache = new HashMap&lt;String, SoftReference&gt;();
我们可以很清晰的看到当通过图片的url地址可以在哈希表中找到直接从哈希表中得到对应的软引用（不会被随意回收，不过当内存吃紧返回00mb的时候会被回收）.如果此时允许加载，调用OnImageLoadListener的onImageLoad对应的接口：
此接口在BookItemAdapter中进行了实现：

```
SyncImageLoader.OnImageLoadListener imageLoadListener = new SyncImageLoader.OnImageLoadListener(){
 
		@Override
		public void onImageLoad(Integer t, Drawable drawable) {
			//BookModel model = (BookModel) getItem(t);
			View view = mListView.findViewWithTag(t);
			if(view != null){
				ImageView iv = (ImageView) view.findViewById(R.id.sItemIcon);
				iv.setBackgroundDrawable(drawable);
			}
		}
		@Override
		public void onError(Integer t) {
//			BookModel model = (BookModel) getItem(t);
			View view = mListView.findViewWithTag(t);
			if(view != null){
				ImageView iv = (ImageView) view.findViewById(R.id.sItemIcon);
				iv.setBackgroundResource(R.drawable.rc_item_bg);
			}
		}
 
	};
```

很显然这里通过传入的position可以得到对应item的View我们可以看下BookItemAdapter中的getView

```
convertView.setTag(position);
```

确实是将对应的position设置为其tag.
回到SyncImageLoader的private void loadImage(final String mImageUrl,final Integer mt,final OnImageLoadListener mListener):
当在哈希表中找不到对应的软引用，则通过loadImageFromUrl获得：

```
public static Drawable loadImageFromUrl(String url) throws IOException {
		DebugUtil.debug(url);
		if(Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED)){
			//if local SD CARD usable create local ache in SD card.
			File f = new File(Environment.getExternalStorageDirectory()+"/TestSyncListView/"+MD5.getMD5(url));
			if(f.exists()){
				FileInputStream fis = new FileInputStream(f);
				Drawable d = Drawable.createFromStream(fis, "src");
				return d;
			}
			URL m = new URL(url);
			InputStream i = (InputStream) m.getContent();
			DataInputStream in = new DataInputStream(i);
			FileOutputStream out = new FileOutputStream(f);
			byte[] buffer = new byte[1024];
			int   byteread=0;
			while ((byteread = in.read(buffer)) != -1) {
				out.write(buffer, 0, byteread);
			}
			in.close();
			out.close();
			Drawable d = Drawable.createFromStream(i, "src");
			return loadImageFromUrl(url);
		}else{
			//if local SD CARD unusable only get Drawable from input stream.
			URL m = new URL(url);
			InputStream i = (InputStream) m.getContent();
			Drawable d = Drawable.createFromStream(i, "src");
			return d;
		}
 
	}
```

此函数从网络上获得图片并创建对应Drawable.如果sd卡可用:
如果对应缓存文件存在（已经缓存），则直接从缓存文件中取得，否则从网路上读取后，创建缓存文件(同样以MD5加密形式命名）。
如果不sdcard不可用直接从网络上读取.
返回Drawable.
通过所返回的Drawable 判断是否调用onImageLoad接口或是onError接口（显示默认图片）。

在之前我们已经了解到如果SCROLL_STATE_IDLE的时候进行加载，我们看下它的调用：

```
case AbsListView.OnScrollListener.SCROLL_STATE_IDLE:
					DebugUtil.debug("SCROLL_STATE_IDLE");
					loadImage();
					//loadImage();
					break;
```

对应的loadImage():

```
public void loadImage(){
		int start = mListView.getFirstVisiblePosition();
		int end =mListView.getLastVisiblePosition();
		if(end &gt;= getCount()){
			end = getCount() -1;
		}
		syncImageLoader.setLoadLimit(start, end);
		syncImageLoader.unlock();
	}
```

这里的把当前界面的第一个item的position与最后一个item的position传给syncImageLoader，然后进行解锁：

```
public void unlock(){
		mAllowLoad = true;
		synchronized (lock) {
			lock.notifyAll(); //wake up all waiting thread.
		}
	}
```

此时getView中各种加载，这里的加载条件与方法上面已经知道了。
其它的，入口的reload和刷新的作用一样.重新刷新一遍。
