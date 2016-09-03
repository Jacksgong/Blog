title: Android后台调度任务与省电
date: 2016-08-15 09:07:03
tags:
- Android
- Scheduler
- Job Scheduler
- Syncs-Adapter
- AlarmManager
- Doze Mode

---

## I. Handler:

> 在进程存活的期间有效使用, Google官方推荐使用。
> 相关机制可以参见: [Android Handler Looper机制](http://blog.dreamtobe.cn/2016/03/11/android_handler_looper/)

- 简单易用。
- 稳定高效。

## II. AlarmManager:

> 利用系统层级的闹钟服务(持有`Wake Lock`)。

<!-- more -->

#### 1. 使用场景

> 在大概的时间间隔(重复)运行指定任务。
> 在精确的时间间隔(重复)运行指定任务。

- 需要精确的定时(重复)任务，如闹钟。
- 非网络访问的，大概时间间隔的定时(重复)任务。
- Google官方不建议网络请求相关的业务使用`AlarmManager`。

#### 2. 特征

- 运行在系统的闹钟服务上的，注册以后，无论是自己的应用进程或组件是否存在，都会正常运作。
- 所有注册的闹钟服务都会在系统重启后复位，因此如果需要保证任务，就需要注册`RECEIVE_BOOT_COMPLETE`广播，确保重启后，可以重新将任务注册到闹钟服务中。
- `AlarmManager`处理的是一个`PendingIntent`。
- 考虑到电量损耗，建议非特殊情况使用大概时间间隔的规则，这样Android会尽量让几个任务打包在一起执行，防止频繁的唤起手机。

## III. Job Scheduler:

> [JobScheduler官方文档](https://developer.android.com/reference/android/app/job/JobScheduler.html)

#### 1. 使用场景

> 在指定特定场景下执行指定任务

- Google官方建议网络请求相关业务放到`Job Scheduler`，由于其的省电的特性。
- 一些与特定场景(`JobInfo`)绑定的任务。

#### 2. 特征

- `Job Scheduler`只有在`Api21`或以上的系统支持。
- `Job Scheduler`是将多个任务打包在一个场景下执行。
- 在系统重启以后，任务会依然保留在`Job Scheduler`当中，因此不需要监听系统启动状态重复设定。
- 如果在一定期限内还没有满足特定执行所需情况，`Job Scheduler`会将这些任务加入队列，并且随后会进行执行。

#### 3. 接口类型

```java
boolean onStartJob(JobParams params) {
    // 开始执行
    // 注意这个方法是在主线程执行的，如果是耗时操作请抛到独立线程中
    // jobFinished(JobParameters params) // 在完成任务并且决定是否还需要定时执行更多任务
    // return 是否是在独立现在还有事务要执行
}

void onStopJob(){
    // 用于清理数据，在结束任务后被回调。
}
```

## IV. GCM(FCM)

> GCM Network Manager实际上在 Api 21 或以上也是使用了 Job Scheduler，在此之前的版本使用的是Google Play Service中实现Job Scheduler的功能。
> 在[GCMNetworkManager](https://developers.google.com/android/reference/com/google/android/gms/gcm/GcmNetworkManager)中有很多利于省电的规则。
> 在中国内地，该服务被墙，无法正常使用。

#### 1. 使用场景

- 实时消息推送。
- 非实时消息推送。

#### 2. 特征

- 系统级别维护的长链接，十分稳定。

#### 3. 接口类型

- 通过 `OneoffTask.Builder()`与`PeriodicTask.Builder()`创建任务。
- `GcmTaskService#onRunTask(TaskParams params)`是在后台线程执行的。

## V. Sync Adapter

> [Transferring Data Using Sync Adapters](https://developer.android.com/training/sync-adapters/index.html)

![](/img/android-scheduler_syncs-adapter.png)

#### 1. 使用场景

> 用于同步服务端与本地设备中的数据。

- 通常是用于同步较多的数据，如系统联系人信息、Dropbox等。

#### 2. 特征

- 省电稳定。
- 可绑定一个账户。
- 利于大数据同步。
- 通过提供`ContentProvider`，可以快捷的与服务端同步的数据库。
- 只有在存在网络的时候才触发同步。
- 不需要依赖Google Play Service。
- 用户可以通过设置中主动查看同步的时间，以及触发同步，或者关闭同步。
- `Sync Adapter`在`API7`或以上就可以使用，因此在一些场景下这是`Job Scheduler`在`API21`之前比较好的替代品。

#### 3. 在一定的场景下触发同步

> 尽可能的打包所有需要同步的任务在一个周期中执行，以此来进行尽可能的节省手机电量。

- 服务端或设备端数据发生变化。
- 手机闲置时。
- 一天。
- 如果同步失败，会放到同步失败的队列中，在尽可能的时候进行同步。

## VI. Doze Mode

### Deep Doze Mode

> `API23`中直接称其为`Doze Mode`。

#### 1. 特征

> **旨在**: 在用户离开设备以后，尽可能的减少手机电量的消耗。

- 无论应用指定的`Target SDK`是多少，只要设备是`Android 6`或以上会启用该模式。
- 开发人员并不需要做特殊的适配，但是会对上面提到的所有Schedule的方式(`Job Scheduler`、`AlarmManager`、`Syncs Adapter`)产生影响。

> 所有任务周期通过移动窗口打包任务执行，并且间隔时间会越来越久。

![](/img/android-scheduler_deep-doze.png)

#### 2. 进入条件

会同时满足以下情况一段时间(大约30分钟)以后生效:

- 手机没有在充电
- 屏幕被关闭
- 手机各方状态保持稳定

> 退出条件是，进入条件中任意条件状态发生变化。

#### 3. 在两个处理窗口之间的手机状态

1. 对所有应用拒绝网络访问。
2. 所有`JobScheduler`、`Sync-Adapter`、`AlarmManager`的任务都会被延后到窗口中执行。
3. 系统会拒绝所有来自应用的`Wake Lock`
4. 停止所有Wifi以及GPS扫描
5. 减少位置事件从设备检测WiFi热点。

### Light Doze Mode

> `Android 7`或以上会启用该模式。

#### 1. 特征

- 相比`Deep Doze Mode`，打包执行任务的频率会更高些。

![](/img/android-scheduler_light-doze.png)

#### 2. 进入条件

会同时满足以下情况一段时间(大约几分钟)以后生效:

- 手机没有在充电
- 屏幕被关闭
- 处于稳定状态/不稳定状态

或者在`Deep Doze Mode`的情况下同时满足以下条件下生效:

- 屏幕关闭
- 手机没有在充电
- 手机不再处于稳定状态

#### 3. 退出条件

- 屏幕打开
- 手机开始充电
- 进入`Deep Doze Mode`

#### 4. 在两个处理窗口之间的手机状态

- 对所有应用拒绝网络访问。
- 所有`JobScheduler`与`Sync Adapter`的任务都会被延后到窗口中执行。
- 不会对`AlarmManager`中的任务进行影响，但是将无网络访问（如果你的任务需要网络访问，是时候改用`JobScheduler`或`Sync Adapter`了，这样才会保证在任务窗口执行会有网络）

### 中断/避开Doze

> 以下所有情况，Google官方都建议不在特殊情景，不要去使用，由于中断了Doze Mode的省电规则。

#### 1. AlarmManager

- 在精确的时间间隔中运行的任务: `setAndAllowWhileIdle()`、`setExactAndAllowWhileIdle()`。但是在非窗口期间并不解除无网络访问的限制，并且只有10s的时间给予处理。
- 指定闹钟事件`AlarmManager.setAlarmClock()`的事件会在闹钟结束前，令系统短暂的完全退出Doze模式，并且正常处理事件，系统为了突显该闹钟事件，将会在系统的`Status Bar`上显示物理闹钟的ICON。

#### 2. FCM/GCM

> (Firebase Cloud Messaging，旧版中称为Google Cloud Messaging(GCM))。

FCM/GCM中高优先级的任务配置中(`"priority" : "high"`) 的消息，在Doze模式下可以正常及时到达。

#### 3. 白名单

> [白名单官方文档](https://developer.android.com/training/monitoring-device-state/doze-standby.html#support_for_other_use_cases)
> [官方建议可考虑加入白名单的情况](https://developer.android.com/training/monitoring-device-state/doze-standby.html#whitelisting-cases)

- 主动请求加入白名单，用户同意以后才加入白名单;
- 用户也可以主动将应用从白名单中删除或将应用添加到白名单中;
- 应用可以通过`isIgnoringBatteryOptimizations()`来获知是否在白名单中;
- 白名单的应用可以访问网络与持有有效的`Wake Lock`，但是其他`Doze`的约束依然存在(如延后的`Job Scheduler`、`Syncs-Adapter`、`AlarmManager`);

白名单的请求方式:

- 通过[ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS](https://developer.android.com/reference/android/provider/Settings.html#ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS)打开电量优化页面，用户可以通过搜索来关闭应用的电量优化，以此加入白名单。
- 先持有[REQUEST_IGNORE_BATTERY_OPTIMIZATIONS](https://developer.android.com/reference/android/Manifest.permission.html#REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)权限，然后通过启动Intent[ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS](https://developer.android.com/reference/android/provider/Settings.html#ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)直接弹出Dialog让用户关闭应用的电量优化，以此加入白名单。

#### 4. 特殊情况

前台服务(`Foreground Service`)将不会受到`Doze`模式影响。

### Doze模式测试

> Google官方提供了一些adb命令用于测试`Doze`模式，而非需要通过等待来进入`Doze`模式的。

#### 1. 进入Doze模式

- 准备一台系统是在`Android Nougat Developer Preview4`或以上版本的设备。
- 将其连接连接到电脑。
- 通过执行`adb shell dumpsys battery unplug`命令让设备进入未连接充电的模式。
- 通过执行`adb shell dumpsys deviceidle step [light|deep]`强行进入`Doze`模式。

> 退出`Doze`模式，让手机恢复正常需要复位充电模式:`adb shell dumpsys battery reset`。

#### 2. 其他指令

- 获取设备状态:`adb shell dumpsys deviceidle get [light|deep|force|screen|charging|network]`。

在`Android Nougat Developer Preview 4`中，`Doze`模式的状态周期是:

```
Light: ACTIVE -> IDLE -> IDLE_MAINTENANCE -> OVERRIDE
Deep: ACTIVE -> IDLE_PENDING -> SENSING -> LOCATING -> IDLE -> IDLE_MAINTENANCE
```

---

本文已经发布到JackBlog公众号，可请直接访问: [Android后台调度任务与省电 - JacksBlog](http://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483685&idx=1&sn=7f548740be9dd4e5b8849b861cb75ec7)

---

- [Choosing the Right Background Scheduler in Android](https://www.bignerdranch.com/blog/choosing-the-right-background-scheduler-in-android/)
- [Diving into Doze Mode for Developers](https://www.bignerdranch.com/blog/diving-into-doze-mode-for-developers/)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
