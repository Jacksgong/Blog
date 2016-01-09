title: Notification最佳实践
date: 2016-01-09 15:30:03
tags:
- Notification
- 最佳实践

---



> 视频: [Respecting User Attention: Notification Best Practices (Android Dev Summit 2015)](https://www.youtube.com/watch?v=WzRSpZpw2wg)

> CODE: https://goo.gl/NfwEiY

> 主要讲解如何正确姿势使用Notification

<!-- more -->

## I. Don't annoy the user

```
// 之所以用NotifcationCompat，因为这个可以直接兼容到API4
new NotificationCompat.Builder(this)
    .setSmallIcon(...)
    .setContentTitle(senderName)
    .setContentText(msgText)
    .setCategory(
        // CATEGORY_ALARM(alarms or timers), REMINDER(user requested reminder),EVENT,MESSAGE,CALL,EMAIL,SOCIAL,RECOMMENDATION(TV?)
    )
    .build();
```

## II. Respect the user

![](/img/notification_best_practise-1.png)

```
// MAX(time-critical tasks, incoming calls, turn-by-turn directions)
// HIGH(important communications, chats, texts, important emails)
// LOW(not time sensitive, social broadcasts)
// MIN(contextual or background infomation, recommendations wechther), not show when locked screen
// setPriority
NotificationCompat.PRIORITY_
```

#### 同id的notification, 声音、振动、ticker 仅第一次
```java
NotificationCompat.Builder builder =
    new NotificationCompat.Builder(c)
        // Set this flag if you would only like the sound, vibrate and ticker to be played if the notification is not already showing.
        .setOnlyAlertOnce(true)
        .setProgress(100, 50, false);
```

#### notification一段时间后自动干掉

> 好吧。只是用了alarm service

```
ctxt.getSystemService(Context.ALARM_SERVICE)
    .set(AlarmManager.ELAPSED_REALTIME,
        SystemClock.elapsedRealtime() + ONE_HOUR,
        makeCancelAllPendingIntent(ctxt));
```

#### Peak

> conditaion: PRIORITY_HIGH && (sound || vibration)

## III. Empower user

> 长按通知以后进入自定义设置页面

```
<activity android:name="SettingsActivity"
        android:label="@string/app_name">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name=
            "android.intent.category.DEFAULT" />
        <category android:anme=
            "android.intent.category.NOTIFICATION_PREFERENCES" />
    </intent-filter>
</activity>
```

作者顺便推广了一把通过`PreferenceFragment`与`Preference xml`很简单就实现一个设置页面.

#### Add more actionable button on Notification

```
new NotificationCompat.Builder(this)
    .setSamllIcon(...)
    .setContentTitle(title)
    .setContentText(text)
    .addAction(R.drawable.ic_answer,
        getString(R.string.call_answer),
        answerPendingIntent)
    .addAction(R.drawable.ic_ignore,
        getString(R.string.call_ignore),
        ignorePendingIntent)
    .build();
```

![](/img/notification_best_practise-2.png)

```
new Notification.Builder(this)
    .setSmallIcon(...)
    .setContentTitle(title)
    .setContentText(text)
    // started in Jelly Bean
    .setStyle(
        new Notification.BigPictureStyle()
        .bigPicture(photoBitmap))
    .build();

    // rich text?
    .setStyle(
        new Notification.BigTextStyle()
            .bigText(longText))
    .build();
```

多端同步，如果一端的notification被干掉，同步到其他端也将其干掉。


#### onGoing Notification

> 用户无法划掉

- startForeground()
- incoming calls
- prefer snooze-and-repost pattern

需要给用户可以划掉/干掉的机会

如：音乐播放器在播放的时候无法划掉，在暂停/停止的时候，允许用户划掉(改优先级)(Google Music目前的做法)
如: SSH/VPN连接在连接上的时候无法划掉，但是提供Action断开链接就自动干掉

## IV. Delight the user

两种用户:

1. 从来都不开声音，要不只开振动
2. 始终都开通知声音，并且喜欢去设置声音类型针对不同的应用

#### 设置通知声音

```
<RingtonePreference
    android:persistent="true"
    android:key="sms_sound"
    android:denpendency="sms_enable"
    android:ringtoneType="notification"
    android:title="@string/sms_sound" />
```

```
SharedPreferences prefs = PreferenceManager
    .getDefaultSharedPreferences(context);
String url = prefs.getString(SOUND, null);
if(uri != null){
    builder.setSound(Uri.parse(uri));
}
```

## V. Connect them to the people they love

系统提供指定联系人（星标） ，其余联系人不打扰的模式，因此我们可以在不请求获取联系人权限的情况下通过以下的方式进行对通知绑定

```
new Notification.Builder(this)
    .setSmallIcon(...)
    .setLargeIcon(...)
    .setContentTilte(senderName)
    .setContentText(msgText)
    .addAction(...)
    // email
    .addPerson(Uri.fromParts("mailto",
        "igzhenjie@gmail.com", null)
        .toString())
    .build();

    // tel
    .addPerson(Uri.fromParts("tel",
        "1(617) 555-1212", null)
        .toString())
```

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
