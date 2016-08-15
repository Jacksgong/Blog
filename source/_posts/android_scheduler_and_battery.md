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

- 简单易用。
- 稳定高效。

## II. AlarmManager:

> 利用系统层级的闹钟服务(持有Wake lock)。

> 如果需要精确的定时任务，这个是最佳选择。

<!-- more -->

#### 1. 功能

- 在大概的时间间隔 运行/重复执行 指定任务。
- 指定精确的时间间隔执行任务。

#### 2. 特征

- 注册以后，无论是自己的应用进程是否存在/组件是否存在，都会正常执行。
- 所有注册的闹钟服务都会在系统重启后复位，因此如果需要保证任务，就需要注册RECEIVE_BOOT_COMPLETE，保证重启后，可以重新将任务注册到闹钟服务中。
- AlarmManager处理的是一个PendingIntent，因此通常是启动一个服务，进行处理事务。

#### 3. 备注

- 官方不建议网络请求相关的使用AlarmManager。
- 考虑到电量损耗，建议非特殊情况使用 大概时间的方式，这样Android会尽量让几个任务打包在一起执行，防止频繁的唤起手机。

## III. Job Scheduler:

> [JobScheduler官方文档](https://developer.android.com/reference/android/app/job/JobScheduler.html)

> 建议网络相关任务放到Job Scheduler。

> 系统重启以后，任务会依然保留在Job Scheduler当中。

> 只有在Api21或以上的系统支持


#### 1. 优势

- 更节省电量
- 更高效
- 更易用

#### 2. 明确的指定特定场景下执行(JobInfo):

> 由于是将多个任务打包在一个场景下执行，因此执行有略微的延后；并且有期限，如果在期限内还没有满足特定情况，系统会将这些任务加入队列，并且随后会进行执行。

1. 设备开始充电
2. 空闲
3. 连接上网络
4. 断开网络

#### 3. 接口类型

```
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

## IV. GCM

> GCM Netwrok Manager实际上在 Api 21 或以上也是使用了 Job Scheduler，在此之前的版本使用的是Google Play Service中实现Job Scheduler的功能。

> 在[GCMNetworkManager](https://developers.google.com/android/reference/com/google/android/gms/gcm/GcmNetworkManager)中有很多利于省点的规则。

#### 1. 接口类型

- 通过 `OneoffTask.Builder()`与`PeriodicTask.Builder()`创建任务。
- `GcmTaskService#onRunTask(TaskParams params)`是在后台线程执行的。

> 触发场景与JobInfo中的一样。

## V. Sync Adapter

> [Transferring Data Using Sync Adapters](https://developer.android.com/training/sync-adapters/index.html)

![](/img/android-scheduler_syncs-adapter.png)

> - 通常是用于同步较多的数据。
> - 也许这是Job Scheduler API 21前比较好的替代品。

同步服务端与本地设备中的数据。

#### 1. 特征

- 利于大数据同步。
- 不需要依赖Google Play Service。
- 省电稳定。
- 用户可以通过设置中主动查看同步的时间，以及触发同步，或者关闭同步。
- API 7 或以上。

#### 2. 备注

- 可绑定一个账户。
- 通过提供ContentProvider，并且与服务端同步的数据库。
- 只有在存在网络的时候才触发同步。

#### 2. 在一定的场景下触发同步

> 尽可能的打包所有需要同步的任务在一个周期中执行，以此来进行尽可能的节省手机电量。

- 服务端/设备端数据发生变化。
- 手机闲置时。
- 一天。
- 如果同步失败，会放到同步失败的队列中，在尽可能的时候进行同步。


## VI. Doze Mode

### Deep Doze Mode

> API 23中直接称其为Doze Mode。

> 无论Target SDK是多少，只要设备是Android API 23或以上会启用该模式。

#### 1. 特征

- 旨在: 在用户离开设备以后，尽可能的减少手机电量的消耗。
- 开发人员并不需要做特殊的适配，但是会对上面提到的所有Schedule的方式(Job Scheduler、AlarmManager、Syncs Adapter)进行影响。

通过移动窗口打包任务请求，并且间隔时间会越来越久。

![](/img/android-scheduler_deep-doze.png)

#### 2. 进入条件

会同时满足以下情况过后一段时间(大约30分钟)以后生效:

- 手机没有在充电
- 屏幕被关闭
- 手机各方状态保持稳定

> 退出条件是，进入条件中任意条件状态发生变化。

#### 3. 在两个处理窗口之间的手机状态

1. 对所有应用拒绝网络访问。
2. 所有JobScheduler、Sync-Adapter、AlarmManager的任务都会被延后到窗口中执行。
3. 系统会拒绝所有来自应用的`WAKE-LOCK`
4. 停止所有Wifi以及GPS扫描
5. 减少位置事件从设备检测WiFi热点。

### Light Doze Mode

> API 24 或以上会启用该模式

#### 1. 特征

- 相比Deep Doze Mode，打包任务的频率会更高些

![](/img/android-scheduler_light-doze.png)

#### 2. 进入条件

会同事满足以下情况后一段时间(大约几分钟)以后生效:

- 手机没有在充电
- 屏幕被关闭
- 处于稳定状态/不稳定状态

或者在以下的条件:

- 处于Deep Doze Mode
- 屏幕关闭
- 手机没有在充电
- 手机不再处于稳定状态

#### 3. 退出条件

- 屏幕打开
- 手机开始充电
- 进入Deep Doze Mode

#### 4. 在两个处理窗口之间的手机状态

- 对所有应用拒绝网络访问。
- 所有JobScheduler与Sync-Adapter的任务都会被延后到窗口中执行。
- 不会对AlarmManager中的任务进行影响，但是将无网络访问（如果你的任务需要网络访问，是时候改用JobScheduler或Sync-Adapter，保证在任务窗口执行会有网络）

### 中断/避开Doze

> 以下所有情况，Google官方都建议不在特殊情景，不要去使用，由于中断了省电的规则。

#### 1. AlarmManager

- 指定需要精确时间的事件: `setAndAllowWhileIdle()`、`setExactAndAllowWhileIdle()`。但是在非窗口期间并不解除无网络访问的限制，并且只有10s的时间给予处理。
- 指定闹钟事件`AlarmManager.setAlarmClock()`的事件会在闹钟结束前，令系统短暂的完全退出Doze模式，并且正常处理事件，系统为了突显该闹钟事件，将会在status bar上显示物理闹钟的icon。

#### 2. FCM/GCM

> (Firebase Cloud Messaging，旧版中称为Google Cloud Messaging(GCM))。

FCM/GCM中高优先级的任务配置中(`"priority" : "high"`) 的消息，在Doze模式下可以正常及时到达。

#### 3. 白名单

> [白名单官方文档](https://developer.android.com/training/monitoring-device-state/doze-standby.html#support_for_other_use_cases)


> [官方建议可考虑加入白名单的情况](https://developer.android.com/training/monitoring-device-state/doze-standby.html#whitelisting-cases)

- 主动请求加入白名单，用户同一以后加入白名单;
- 用户也可以主动将App从白名单中删除或添加应用;
- 应用可以通过`isIgnoringBatteryOptimizations()`来获知是否在白名单中;
- 白名单的应用可以访问网络与持有有效的WAKELOKE，但是其他Doze的约束依然存在(如延后的Job Scheduler、Syncs-Adapter、AlarmManager);

白名单的请求方式:

- 通过[ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS](https://developer.android.com/reference/android/provider/Settings.html#ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS)打开电量优化页面，用户可以通过搜索来关闭应用的电量优化，以此加入白名单。
- 先持有[REQUEST_IGNORE_BATTERY_OPTIMIZATIONS](https://developer.android.com/reference/android/Manifest.permission.html#REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)权限，然后通过启动Intent[ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS](https://developer.android.com/reference/android/provider/Settings.html#ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)直接弹出Dialog让用户关闭应用的电量优化，以此加入白名单。

#### 4. 特殊情况

前台服务(foreground-service)将不会受到Doze模式影响。

### Doze模式测试

> Google官方提供了一些adb命令用于测试Doze模式，而非需要通过等待来进入Doze模式的。

#### 1. 进入Doze模式

- 准备一台系统是在Android Nougat Devloper Preview4或以上版本的设备。
- 将其连接连接到电脑。
- 通过 `adb shell dumpsys battery unplug` 命令让设备进入未连接充电的模式。
- 通过 `adb shell dumpsys deviceidle step [light|deep]` 强行进入Doze模式。

> 退出Doze模式，让手机恢复正常需要复位充电模式: `adb shell dumpsys battery reset`。

#### 2. 其他指令

- 获取设备状态 `adb shell dumpsys deviceidle get [light|deep|force|screen|charging|network]`。

在Android Nougat Developer Preview 4中，Doze模式的状态周期是:

```
Light: ACTIVE -> IDLE -> IDLE_MAINTENANCE -> OVERRIDE
Deep: ACTIVE -> IDLE_PENDING -> SENSING -> LOCATING -> IDLE -> IDLE_MAINTENANCE
```

---

- [Choosing the Right Background Scheduler in Android](https://www.bignerdranch.com/blog/choosing-the-right-background-scheduler-in-android/)
- [Diving into Doze Mode for Developers](https://www.bignerdranch.com/blog/diving-into-doze-mode-for-developers/)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
