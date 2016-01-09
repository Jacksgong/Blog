title: Android Messenger 进程通信
date: 2013-12-14 08:35:03
tags:
- 分析
- 进程通信
- Android

---

今天通过以前写的简单的代码，分享通过Messenger 完成跨进成通信的使用，大神等请绕行。

> 接的外包越来越复杂，使我不得不急需从以前凌乱的成型的、未成型的项目中整理出一些主要的框架 – 2013. 中旬。

<!--more-->
也是由于一般来说Messenger相比AIDL是把所有的请求都放到一个请求队列，逐一处理，无法支持同时处理并且Messenger仅仅只是通过传递message进行通讯，所以所有的操作只能在对方的Handle中处理，对于架构来说也不是很好，所以最近再次整理的时候需要将这些替换为AIDL通信，但是Messenger通信比较简单，还是很值得mark的，因此，先上当初写的拙码：

———— 服务端： SocketServer:

```
package cn.dreamtobe.service;
import android.app.Service;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.os.Messenger;
import cn.dreamtobe.net.SocketHandle;
import cn.dreamtobe.net.SocketHandle.SocketHandleCallBack;
import cn.dreamtobe.order.CmdOrder;
import cn.dreamtobe.utils.LogUtils;
import cn.dreamtobe.utils.Util;
/**
 *
 * @author 振杰
 *
 */
public class SocketService extends Service implements Runnable {
 private ServiceHandle mHandle = new ServiceHandle();
 private SocketHandle mSocketHandle = null;
 private volatile boolean mbStop = false;
 private final String mHostIp = Util.getSocketHostIP();
 private final int mPort = Util.getSocketPort();
 // 客服端Messenger
 private Messenger mcMessenger = null;
 // 服务端Messenger
 private Messenger msMessenger = new Messenger(mHandle);
 private LogUtils mLogUtils = LogUtils.getInstance();
 private class ServiceHandle extends Handler {
  @Override
  public void handleMessage(Message msg) {
   super.handleMessage(msg);
   switch (msg.what) {
   case CmdOrder.CMD_SERVICE_STOP:
    mbStop = true;
    stopSelf();
    break;
   case CmdOrder.CMD_MESSAGE_SEND:
    mcMessenger = msg.replyTo;
    Bundle bundle = msg.getData();
    String sendMsg = bundle.getString("client");
    sendString(sendMsg);
   default:
    break;
   }
  }
 }
 private Message mSendMsg = null;
 // 答复客服端
 private void replyClient(int cmd, String replyMsg) {
  if (mSendMsg == null) {
   mSendMsg = new Message();
  }
  mSendMsg.what = cmd;
  Bundle bundle = new Bundle();
  bundle.putString("socketservice", replyMsg);
  mSendMsg.setData(bundle);
  try {
   mcMessenger.send(mSendMsg);
  } catch (Exception e) {
  }
 }
 // 发送String 给服务器
 private void sendString(String sendMsg) {
  mLogUtils.NetSendLog("socket服务请求发送: " + sendMsg);
  mSocketHandle.SendString(sendMsg);
 }
 @Override
 public IBinder onBind(Intent intent) {
  mLogUtils.SysLog("Socket Service onBind");
  return msMessenger.getBinder();
 }
 @Override
 public void onCreate() {
  super.onCreate();
  mSocketHandle = new SocketHandle(mHostIp, mPort, mCallBack);
  mSocketHandle.start();
  mLogUtils.SysLog("Socket Service onCreate");
 }
 @Override
 public void onDestroy() {
  super.onDestroy();
  mSocketHandle.stop();
  mLogUtils.SysLog("Socket Service onDestroy");
 }
 @Override
 public void run() {
  if (!mbStop) {
  }
 }
 private SocketHandleCallBack mCallBack = new SocketHandleCallBack() {
  @Override
  public void SucceedSendString() {
   // TODO Auto-generated method stub
  }
  @Override
  public void SucceedReconnect() {
   // TODO Auto-generated method stub
  }
  @Override
  public void ReConnectFailOnSendString() {
   // TODO Auto-generated method stub
  }
  @Override
  public void FailReconnect() {
   // TODO Auto-generated method stub
  }
  @Override
  public void ErrorOnSendString() {
   // TODO Auto-generated method stub
  }
  @Override
  public void BeginReConnect() {
   // TODO Auto-generated method stub
  }
  @Override
  public void BackMessage(String msg) {
   if (mcMessenger == null) {
    return;
   }
   replyClient(CmdOrder.CMD_MESSAGE_RECEIVE, msg);
  }
 };
}
```

——————– BaseActivity:

```
package cn.dreamtobe.activity;
import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.os.Messenger;
import android.os.RemoteException;
import cn.dreamtobe.order.CmdOrder;
import cn.dreamtobe.tool.GlobalTool;
import cn.dreamtobe.utils.LogUtils;
import cn.dreamtobe.utils.VariUtils;
/**
 *
 * @author 振杰
 *
 */
public abstract class BaseActivity extends Activity {
 private static MyHandler mHandler = null;
 private static int mnBaseAct = 0;
 /**
  * 客户端Messenger
  */
 protected Messenger mcMessenger = null;
 /**
  * 服务端Messenger
  */
 protected Messenger msMessenger = null;
 private static BaseActivity mCurBaseActivity = null;
 private LogUtils mLogUtils = LogUtils.getInstance();
 private boolean mIsBind = false;
 @Override
 public void onCreate(Bundle savedInstanceState) {
  super.onCreate(savedInstanceState);
  mnBaseAct++;
  preConfigure();
  if (mHandler == null) {
   mHandler = new MyHandler();
  }
  VariUtils.gCurActivity = this;
  mCurBaseActivity = this;
  configure();
  initUtils();
  initControl();
  initUI();
 }
 protected void preConfigure() {
 }
 public void BindService() {
  if (!mIsBind) {
   mLogUtils
     .SysLog(this.getClass().toString() + " Bind SocketService");
   mIsBind = bindService(new Intent(VariUtils.SocketServiceAction),
     mSerConn, BIND_AUTO_CREATE);
  }
 }
 public void unBindService() {
  if (mIsBind) {
   mLogUtils.SysLog(this.getClass().toString()
     + " unBind SocketService");
   unbindService(mSerConn);
   mIsBind = false;
  }
 }
 @Override
 protected void onResume() {
  super.onResume();
  VariUtils.gCurActivity = this;
  mCurBaseActivity = this;
 }
 @Override
 protected void onDestroy() {
  super.onDestroy();
  unBindService();
  if (--mnBaseAct == 0) {
  }
 }
 protected abstract void configure();
 protected abstract void initUtils();
 protected abstract void initControl();
 protected abstract void initUI();
 public void sendMessage(int flag) {
  mHandler.sendEmptyMessage(flag);
 }
 public void sendMessageDely(int flag, long delayMillis) {
  mHandler.sendEmptyMessageDelayed(flag, delayMillis);
 }
 public void sendMessage(Message msg) {
  mHandler.sendMessage(msg);
 }
 protected void ToastShow(String message) {
  mHandler.toast_message = message;
  mHandler.sendEmptyMessage(MyHandler.SHOW_STR_TOAST);
 }
 private static class MyHandler extends Handler {
  public static final int SHOW_STR_TOAST = 0;
  private String toast_message = null;
  @Override
  public void handleMessage(Message msg) {
   if (!Thread.currentThread().isInterrupted()) {
    switch (msg.what) {
    case SHOW_STR_TOAST:
     GlobalTool.showCustomToast(mCurBaseActivity, toast_message,
       1);
     break;
    default:
     mCurBaseActivity.handleOtherMessage(msg);
     break;
    }
   }
  }
 }
 /**
  * 处理Handle
  *
  * @param msg
  */
 protected abstract void handleOtherMessage(Message msg);
 private ServiceConnection mSerConn = new ServiceConnection() {
  @Override
  public void onServiceDisconnected(ComponentName name) {
   mLogUtils.SysLog("ServiceUnConnected");
   // msMessenger = null;
  }
  @Override
  public void onServiceConnected(ComponentName name, IBinder service) {
   mLogUtils.SysLog("ServiceConnected");
   msMessenger = new Messenger(service);// get the object of remote
             // service
   mcMessenger = new Messenger(mHandler);// initial the object of local
             // service
  }
 };
 protected Message mSendMsg = null;
 public void sendSocketServiceMsg(int cmd, String msg) {
  if (msMessenger == null) {
   return;
  }
  if (mSendMsg == null) {
   mSendMsg = new Message();
   mSendMsg.replyTo =  mcMessenger ;
  }
  mSendMsg.what = cmd;
  Bundle mBundle = new Bundle();
  mBundle.putString("client", msg);
  mSendMsg.setData(mBundle);
  try {
   msMessenger.send(mSendMsg);
   if (cmd == CmdOrder.CMD_SERVICE_STOP) {
    msMessenger = null;
   }
  } catch (RemoteException e) {
   mLogUtils
     .SysLogE("error on Send to SocketService: " + e.toString());
   e.printStackTrace();
  }
 }
}
```

虽然我也想忽略一切直接分析Messenger，但是，这里还是提下，其中所有Socket有关的机制都封装在SocketHandle当中，其中一些主要的反馈通过接口SocketHandleCallBack在SocketService中实现。
那么，透过代码，我们可以看到在SocketService与BaseActivity中都有：

```
/**
  * 客户端Messenger
  */
 protected Messenger mcMessenger= null;
 /**
  * 服务端Messenger
  */
 protected Messenger msMessenger = null;
 ```

 对于SocketService（下称为Service端）而言mcMessenger来自BaseActivity（下称为Client端）：mcMessenger = msg.replyTo; 而msMessenger 为Service端通过传入对应处理的Handle创建，所有的客服端发过来的有关处理都在这个Handle中处理。

 ```
 private class ServiceHandle extends Handler {
  @Override
  public void handleMessage(Message msg) {
   super.handleMessage(msg);
   switch (msg.what) {
   case CmdOrder.CMD_SERVICE_STOP:
    mbStop = true;
    stopSelf();
    break;
   case CmdOrder.CMD_MESSAGE_SEND:
    mcMessenger = msg.replyTo;
    Bundle bundle = msg.getData();
    String sendMsg = bundle.getString("client");
    sendString(sendMsg);
   default:
    break;
   }
  }
 }
 ```

 并且在onBind时，返回Service端Messenger的IBinder:

 ```
 @Override
 public IBinder onBind(Intent intent) {
  mLogUtils.SysLog("Socket Service onBind");
  return msMessenger.getBinder();
 }
 ```

 对于Client端而言，mcMessenger的创建类似与msMessenger ，也是通过传入对应处理的Handle创建，而msMessenger是通过连接成功以后传入参数IBinder进行创建，还有一点值得注意的是，在发送message给Service端时，将message的replyTo赋值为mcMessenger，别忘了我们在Service端时是如何取得Client端的Messenger进行通信的:

 ```
 /**
  * 处理Handle
  *
  * @param msg
  */
 protected abstract void handleOtherMessage(Message msg);
 private ServiceConnection mSerConn = new ServiceConnection() {
  @Override
  public void onServiceDisconnected(ComponentName name) {
   mLogUtils.SysLog("ServiceUnConnected");
   // msMessenger = null;
  }
  @Override
  public void onServiceConnected(ComponentName name, IBinder service) {
   mLogUtils.SysLog("ServiceConnected");
   msMessenger = new Messenger(service);// get the object of remote
             // service
   mcMessenger = new Messenger(mHandler);// initial the object of local
             // service
  }
 };
 protected Message mSendMsg = null;
 public void sendSocketServiceMsg(int cmd, String msg) {
  if (msMessenger == null) {
   return;
  }
  if (mSendMsg == null) {
   mSendMsg = new Message();
   mSendMsg.replyTo = mcMessenger;
  }
  mSendMsg.what = cmd;
  Bundle mBundle = new Bundle();
  mBundle.putString("client", msg);
  mSendMsg.setData(mBundle);
  try {
   msMessenger.send(mSendMsg);
   if (cmd == CmdOrder.CMD_SERVICE_STOP) {
    msMessenger = null;
   }
  } catch (RemoteException e) {
   mLogUtils
     .SysLogE("error on Send to SocketService: " + e.toString());
   e.printStackTrace();
  }
 }
 ```

 至此，已经简单的通过Messenger完成进程间通信。

---

> © 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
