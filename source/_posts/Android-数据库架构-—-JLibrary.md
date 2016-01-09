title: Android 数据库架构 — JLibrary
date: 2014-09-06 08:35:03
tags:
- 数据库
- 架构
- Android
- JLibrary
- 项目

---

> 刚开始维护GITHUB多多指教，本项目源码地址：https://github.com/Jacksgong/Android-Database-Construct

始末
-------

由于做一些小项目的时候，在创建数据库、创建表、执行表操作等数据库相关代码编写的时候进行了优化，统一了架构，因此分享出来。
ps: 目前架构基于ContentProvier

<!--more-->
架构分布
-------

 1. BaseContentProvider  负责数据库的规范
 2. BaseTableFields 规范数据表 字段(默认字段：`_id`, `createAt`, `modifiedAt`)
 3. BaseTableHelper 负责数据表 规范(表名、主键、默认查询结果排序、表创建、表升级)
 4. BaseTableOperator 提供常用数据表的操作以及操作规范(某人已带功能：插入、更新、删除、搜索、数量、是否存在）
 5. CustomTableHelper 常用表规范(默认查询结果排列顺序、默认主键）

通过Sample来介绍使用
-------

 - 首先Sample中我们创建了一个SampleDB，通过集成BaseContentProvider来快速创建。
 - 其次我们创建了UserInfoTable，并且为其提供了基本的数据库操作


####**1. 创建SampleDB数据库**(注意在AndroidManifest.xml中申明ContentProvider)

```
public class SampleDB extends BaseContentProvider {

public final static String DATABASE_NAME = "sample.db";

public final static String AUTHORITY = "sampledb";

public final static int DATABASE_VERSION = 1;

public SampleDB() {
	super(AUTHORITY);
}

@Override
protected HashMap<String, BaseTableHelper> createAllTableHelper() {
	final HashMap<String, BaseTableHelper> hashMap = new HashMap<String, BaseTableHelper>();

 需要提供各表的Helper
	final UserInfoHelper userInfoHelper = UserInfoHelper.getImpl();
	hashMap.put(userInfoHelper.getTableName(), userInfoHelper);

	return hashMap;
}

@Override
protected String getDatabaseName() {
	return DATABASE_NAME;
}

@Override
protected int getDatabaseVersion() {
	return DATABASE_VERSION;
}

}
```

####**2. UserInfo表字段**(name, sex, age)

```
public class UserInfoFields extends BaseTableFields {

	public final static String NAME = "name";
	public final static String SEX = "sex";
	public final static String AGE = "age";

	public UserInfoFields() {

	}

	public UserInfoFields(final Cursor c) {
		super(c);
	}

	public void setName(final String name) {
		put(NAME, name);
	}

	public String getName() {
		return (String) get(NAME);
	}

	public void setSex(final String sex) {
		put(SEX, sex);
	}

	public String getSex() {
		return (String) get(SEX);
	}

	public void setAge(final String age) {
		put(AGE, age);
	}

	public String getAge() {
		return (String) get(AGE);
	}

	@Override
	public void put(Cursor c) {
		if (c == null || c.isClosed() || c.isAfterLast()) {
			return;
		}

		set_Id(c.getInt(c.getColumnIndexOrThrow(_ID)));
		setName(c.getString(c.getColumnIndexOrThrow(NAME)));
		setSex(c.getString(c.getColumnIndexOrThrow(SEX)));
		setAge(c.getString(c.getColumnIndexOrThrow(AGE)));
	}

}
```

####**3. UserInfo表规范**

```
public class UserInfoHelper extends CustomTableHelper {

	public final static String TABLE_NAME = "user_info";

	private final static class ClassHolder {
		private final static UserInfoHelper INSTANCE = new UserInfoHelper();
	}

	public static UserInfoHelper getImpl() {
		return ClassHolder.INSTANCE;
	}

	@Override
	public String getTableName() {
		return TABLE_NAME;
	}

	@Override
	public void onDataBaseCreate(SQLiteDatabase db) {
		final String create = getCustomCreatePre() + UserInfoFields.NAME + " TEXT," + UserInfoFields.SEX + " TEXT," + UserInfoFields.AGE + " TEXT);";
		db.execSQL(create);
	}

}
```

####**4. UserInfo表操作**(实现下面，就已经带有了这些功能：插入、更新、删除、搜索、数量、是否存在)

```
public class UserInfoOperator extends BaseTableOperator<UserInfoFields, UserInfoHelper> {

	private final static class ClassHolder {
		private final static UserInfoOperator INSTANCE = new UserInfoOperator(SampleApplication.getContext(), UserInfoHelper.getImpl());
	}

	public static UserInfoOperator getImpl() {
		return ClassHolder.INSTANCE;
	}

	public UserInfoOperator(Context context, UserInfoHelper helper) {
		super(context, helper);
	}

	@Override
	public Uri getUri() {
		return getTableHelper().getContentUri(SampleDB.AUTHORITY);
	}

	@Override
	protected List<UserInfoFields> createColumns(Cursor c) {
		if (c == null || c.isClosed() || c.isAfterLast()) {
			return null;
		}

		List<UserInfoFields> list = new ArrayList<UserInfoFields>();
		for (c.moveToFirst(); !c.isAfterLast(); c.moveToNext()) {
			list.add(new UserInfoFields(c));
		}

		return list;
	}

}
```

---

> © 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
