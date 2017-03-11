title: php mysql学习之简单留言板
date: 2013-01-08 08:35:03
permalink: 2013/01/08/php-mysql学习之简单留言板
tags:
- mysql
- php
- sql
- 留言板

---

![](/img/php-mysql-1.jpg)

数据库中的内容:

![](/img/php-mysql-2.jpg)

<!--more-->
`index.php`:

```
<meta http-equiv="Content-Type" content="text/html; charset=gbk">
<?php
include("IncDB.php");
$result=mysqli_query($link,"SELECT * FROM intd");
$row=mysqli_fetch_row($result);
while($row)
{
     echo "ID: ".$row[0]." 姓名: ".$row[1]." 时间: ".$row[3]."<br />";
     echo $row[2];
     echo "<hr /><br />";
     $row=mysqli_fetch_row($result);
}
mysqli_close($link);
?>


<form method="POST" action="InsetToDB.php">
昵称:<input type="text" size="8"; name="name">
   <p>内容:<textarea rows="5" name="text" cols="60"></textarea>
   </p>
   <p><input type="submit" value="提交" name="B1"><input type="reset" value="重置" name="B2"></p>
</form>
```

`IncDB.php`:

```
<?php
//error_reporting(E_ALL ^ E_WARNING);
$link=mysqli_connect('127.0.0.1','root','');
if(!$link)
{
   die("<center>出错啦:1!</center>");

}

if(!mysqli_select_db($link,'guestbook'))
{
   die("<center>出错啦:2!</center>");
   }


?>
```

`InsetToDB.php`:

```
<?php
include("IncDB.php");
$name=addslashes($_POST['name']);
$text=addslashes($_POST['text']);
$sql = "INSERT INTO `intd` (`id`, `name`, `text`, `datetime`) VALUES (NULL, '$name', '$text', now());";
//$sql="INSERT INTO `intd` ( , `name` , `text`,`datetime` ) VALUES ( ,'$name','$text',now())";
if(mysqli_query($link,$sql))
{
   echo "留言成功！";
   echo "<meta http-equiv="refresh" content="1;URL=index.php">";
   }
else
   echo "留言失败！";

mysqli_close($link);
?>
```

数据库为：guestbook
并且初始化执行：

```
CREATE TABLE `intd` (
`id` int(11) NOT NULL auto_increment,
`name` varchar(255) character set utf8 collate utf8_bin NOT NULL,
`text` text character set utf8 collate utf8_bin NOT NULL,
`datetime` datetime NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=gb2312 AUTO_INCREMENT=11 ;
```

---
