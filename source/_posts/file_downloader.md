title: FileDownloader
date: 2015-12-23 11:18:03
permalink: 2015/12/23/file_downloader
tags:
- Download
- Parallel
- Serial
- Project

---

> 已开源 [lingochamp/FileDownloader](https://github.com/lingochamp/FileDownloader)

- [中文迭代日志](https://github.com/lingochamp/FileDownloader/blob/master/CHANGELOG.md)
- [中文说明文档](https://github.com/lingochamp/FileDownloader/blob/master/README-zh.md)
- [Wiki](https://github.com/lingochamp/FileDownloader/wiki)
- [问题讨论区](https://github.com/lingochamp/FileDownloader/issues)

<!-- more -->

---

## 简述所解决问题

系统提供的DownloadManager由于是考虑系统层面所有应用公用，不够灵活。

## 特征

- 支持 独立进程/非独立进程
- 灵活
- 高并发
- 稳定

## Demo

![](/img/filedownloader-serial_tasks_demo.gif)
![](/img/filedownloader-parallel_tasks_demo.gif)
![](/img/filedownloader-tasks_manager_demo.gif)
![](/img/filedownloader-mix_tasks_demo.gif)
![](/img/filedownloader-avoid_drop_frames1.gif)
