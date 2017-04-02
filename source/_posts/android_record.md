title: Android简单录音
date: 2015-10-23 11:18:03
updated: 2015-10-23 11:18:03
permalink: 2015/10/23/android_record
categories:
- Android最佳实践
tags:
- Record
- MediaRecorder
- Android

---

## I. 通过系统自带的录音进行录音

#### 存在问题

- [可能无效](http://www.grokkingandroid.com/checking-intent-availability/)
- 默认放到sdcard根目录

<!-- more -->

```
Intent intent =
      new Intent(MediaStore.Audio.Media.RECORD_SOUND_ACTION);
if (isAvailable(getApplicationContext(), intent)) {
   startActivityForResult(intent,
         REQUESTCODE_RECORDING);
}

public static boolean isAvailable(Context ctx, Intent intent) {
   final PackageManager mgr = ctx.getPackageManager();
   List<ResolveInfo> list =
      mgr.queryIntentActivities(intent,
         PackageManager.MATCH_DEFAULT_ONLY);
   return list.size() > 0;
}

protected void onActivityResult(int requestCode,
      int resultCode, Intent intent) {
   if (requestCode == REQUESTCODE_RECORDING) {
      if (resultCode == RESULT_OK) {
         Uri audioUri = intent.getData();
         // make use of this MediaStore uri
         // e.g. store it somewhere
      }
      else {
         // react meaningful to problems
      }
   }
   else {
      super.onActivityResult(requestCode,
            resultCode, intent);
   }
}
```

## II. 通过MediaRecorder进行自己应用内录音

#### 需要注意:

1. `java.lang.IllegalStateException`: `prepare()`失败或者其他一些关机步骤失败了还继续执行导致。
2. `mediarecorder went away with unhandled events`，不用担心，这个只是告知你调用`release()`的时候还在录音或者还在队列中。
3. `Fatal signal 11 (SIGSEGV)`: 这个是`release()`以后，还在使用这个MediaRecorder对象，或者是还没有`prepare()`过就调用了`reset()`，这个错误会直接导致应用重启。


```
MediaRecorder recorder = null;

private void startRecording(File file) {
    //为了考虑到旧的recorder对象可能出现过错误，因此直接重新创建不通过reset复用旧的
   if (recorder != null) {
      recorder.release();
   }
   // step1. Create a MediaRecorder object
   recorder = new MediaRecorder();
   // step2. State the source to use
   recorder.setAudioSource(AudioSource.MIC);
   // step3. Set the file format
   recorder.setOutputFormat(OutputFormat.THREE_GPP);
   // step4. Set the Encoding
   recorder.setAudioEncoder(AudioEncoder.AMR_WB);
   recorder.setOutputFile(file.getAbsolutePath());
   try {
      // step5. Prepare a file
      recorder.prepare();
      // step6. Start recording
      recorder.start();
   } catch (IOException e) {
      Log.e("giftlist", "io problems while preparing [" +
            file.getAbsolutePath() + "]: " + e.getMessage());
   }
}

private void stopRecording() {
   if (recorder != null) {
      recorder.stop();
      recorder.release();
      recorder = null;
   }
}

@Override
protected void onPause() {
   super.onPause();
   if (recorder != null) {
      recorder.release();
      recorder = null;
   }
}
```

---

- [Recording Audio using Android’s MediaRecorder Framework](http://www.grokkingandroid.com/recording-audio-using-androids-mediarecorder-framework/)

---
