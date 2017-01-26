title: Android单元测试与模拟测试
date: 2016-11-30 00:40:03
permalink: 2016/05/15/android_test
tags:
- 单元测试
- 模拟测试
- UI测试
- 稳定性
- Android

---

> 测试驱动式编程(Test-Driven-Development)在RoR中已经是非常普遍的开发模式，是一种十分可靠、优秀的编程思想，可是在Android领域中这块还没有普及，今天主要聊聊Android中的单元测试与模拟测试及其常用的一些库。

<!-- more -->

## I. 测试与基本规范

#### 1. 为什么需要测试?

- 为了稳定性，能够明确的了解是否正确的完成开发。
- 更加易于维护，能够在修改代码后保证功能不被破坏。
- 集成一些工具，规范开发规范，使得代码更加稳定( 如通过 phabricator differential 发diff时提交需要执行的单元测试，在开发流程上就可以保证远端代码的稳定性)。

#### 2. 测什么?

- 一般单元测试:
  - 列出想要测试覆盖的异常情况，进行验证。
  - 性能测试。
- 模拟测试: 根据需求，测试用户真正在使用过程中，界面的反馈与显示以及一些依赖系统架构的组件的应用测试。

#### 3. 需要注意

- 考虑可读性，对于方法名使用表达能力强的方法名，对于测试范式可以考虑使用一种规范, 如 RSpec-style。方法名可以采用一种格式，如: `[测试的方法]_[测试的条件]_[符合预期的结果]`。
- 不要使用逻辑流关键字(If/else、for、do/while、switch/case)，在一个测试方法中，如果需要有这些，拆分到单独的每个测试方法里。
- 测试真正需要测试的内容，需要覆盖的情况，一般情况只考虑验证输出（如某操作后，显示什么，值是什么）。
- 考虑耗时，Android Studio默认会输出耗时。
- 不需要考虑测试`private`的方法，将`private`方法当做黑盒内部组件，测试对其引用的`public`方法即可；不考虑测试琐碎的代码，如`getter`或者`setter`。
- 每个单元测试方法，应没有先后顺序；尽可能的解耦对于不同的测试方法，不应该存在Test A与Test B存在时序性的情况。

#### 4. 创建测试

- 选择对应的类
- 将光标停留在类名上
- 按下`ALT + ENTER`
- 在弹出的弹窗中选择`Create Test`

## II. Android Studio中的单元测试与模拟测试

> control + shift + R (Android Studio 默认执行单元测试快捷键)。

### 1. 本地单元测试

> 直接在开发机上面进行运行测试。
> 在没有依赖或者仅仅只需要简单的Android库依赖的情况下，有限考虑使用该类单元测试。

`./gradlew test`

通过添加以下脚本到对应module的`build.gradle`中，以便于在终端中也可以直接查看单元测试的各类测试信息:

```groovy
android {
  ...
  testOptions.unitTests.all {
    testLogging {
      events 'passed', 'skipped', 'failed', 'standardOut', 'standardError'
      outputs.upToDateWhen { false }
      showStandardStreams = true
    }
  }
}
```

#### 代码存储

> 如果是对应不同的flavor或者是build type，直接在test后面加上对应后缀(如对应名为`myFlavor`的单元测试代码，应该放在`src/testMyFlavor/java`下面)。

`src/test/java`

#### Google官方推荐引用

```groovy
dependencies {
    // Required -- JUnit 4 framework，用于单元测试，google官方推荐
    testCompile 'junit:junit:4.12'
    // Optional -- Mockito framework，用于模拟架构，google官方推荐
    testCompile 'org.mockito:mockito-core:1.10.19'
}
```

#### JUnit

##### Annotation

| Annotation | 描述
| --- | ---
| `@Test public void method()` | 定义所在方法为`单元测试方法`
| `@Test (expected = Exception.class)` | 如果所在方法没有抛出`Annotation`中的`Exception.class`->失败
| `@Test(timeout=100)` | 如果方法耗时超过`100`毫秒->失败
| `@Test(expected=Exception.class)` | 如果方法抛了Exception.class类型的异常->通过
| `@Before public void method()` | 这个方法在每个测试之前执行，用于准备测试环境(如: 初始化类，读输入流等)
| `@After public void method()` | 这个方法在每个测试之后执行，用于清理测试环境数据
| `BeforeClass public static void method()` | 这个方法在所有测试开始之前执行一次，用于做一些耗时的初始化工作(如: 连接数据库)
| `AfterClass public static void method()` | 这个方法在所有测试结束之后执行一次，用于清理数据(如: 断开数据连接)
| `@Ignore`或者`@Ignore("Why disabled")` | 忽略当前测试方法，一般用于测试方法还没有准备好，或者太耗时之类的
| `@FixMethodOrder(MethodSorters.NAME_ASCENDING) public class TestClass{}`  | 使得该测试方法中的所有测试都按照方法中的字母顺序测试
| `Assume.assumeFalse(boolean condition)` | 如果满足`condition`，就不执行对应方法

### 2. 模拟测试

> 需要运行在Android设备或者虚拟机上的测试。

> 主要用于测试: 单元(Android SDK层引用关系的相关的单元测试)、UI、应用组件集成测试(Service、Content Provider等)。

`./gradlew connectedAndroidTest`

#### 代码存储:

`src/androidTest/java`

#### Google官方推荐引用

```groovy
dependencies {
    androidTestCompile 'com.android.support:support-annotations:23.0.1'
    androidTestCompile 'com.android.support.test:runner:0.4.1'
    androidTestCompile 'com.android.support.test:rules:0.4.1'
    // Optional -- Hamcrest library
    androidTestCompile 'org.hamcrest:hamcrest-library:1.3'
    // Optional -- UI testing with Espresso
    androidTestCompile 'com.android.support.test.espresso:espresso-core:2.2.1'
    // Optional -- UI testing with UI Automator
    androidTestCompile 'com.android.support.test.uiautomator:uiautomator-v18:2.1.1'
}
```

#### 常见的UI测试

> 需要模拟Android系统环境。

##### 主要三点:

1. UI加载好后展示的信息是否正确。
2. 在用户某个操作后UI信息是否展示正确。
3. 展示正确的页面供用户操作。

#### Espresso

> 谷歌官方提供用于UI交互测试

```java
import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayed;
import static android.support.test.espresso.matcher.ViewMatchers.withId;

// 对于Id为R.id.my_view的View: 触发点击，检测是否显示
onView(withId(R.id.my_view)).perform(click())               
                            .check(matches(isDisplayed()));
// 对于文本打头是"ABC"的View: 检测是否没有Enable
onView(withText(startsWith("ABC"))).check(matches(not(isEnabled()));
// 按返回键
pressBack();
// 对于Id为R.id.button的View: 检测内容是否是"Start new activity"
onView(withId(R.id.button)).check(matches(withText(("Start new activity"))));
// 对于Id为R.id.viewId的View: 检测内容是否不包含"YYZZ"
onView(withId(R.id.viewId)).check(matches(withText(not(containsString("YYZZ")))));
// 对于Id为R.id.inputField的View: 输入"NewText"，然后关闭软键盘
onView(withId(R.id.inputField)).perform(typeText("NewText"), closeSoftKeyboard());
// 对于Id为R.id.inputField的View: 清除内容
onView(withId(R.id.inputField)).perform(clearText());
```

##### 启动一个打开`Activity`的`Intent`

```java
@RunWith(AndroidJUnit4.class)
public class SecondActivityTest {
    @Rule
    public ActivityTestRule<SecondActivity> rule =
            new ActivityTestRule(SecondActivity.class, true,
                                  // 这个参数为false，不让SecondActivity自动启动
                                  // 如果为true，将会在所有@Before之前启动，在最后一个@After之后关闭
                                  false);
    @Test
    public void demonstrateIntentPrep() {
        Intent intent = new Intent();
        intent.putExtra("EXTRA", "Test");
        // 启动SecondActivity并传入intent
        rule.launchActivity(intent);
        // 对于Id为R.id.display的View: 检测内容是否是"Text"
        onView(withId(R.id.display)).check(matches(withText("Test")));
    }
}
```

##### 异步交互

建议关闭设备中"设置->开发者选项中"的动画，因为这些动画可能会是的Espresso在检测异步任务的时候产生混淆: 窗口动画缩放(Window animation scale)、过渡动画缩放(Transition animation scale)、动画程序时长缩放(Animator duration scale)。

> 针对`AsyncTask`，在测试的时候，如触发点击事件以后抛了一个`AsyncTask`任务，在测试的时候直接`onView(withId(R.id.update)).perform(click())`，然后直接进行检测，此时的检测就是在`AsyncTask#onPostExecute`之后。

```java
// 通过实现IdlingResource，block住当非空闲的时候，当空闲时进行检测，非空闲的这段时间处理异步事情
public class IntentServiceIdlingResource implements IdlingResource {
    ResourceCallback resourceCallback;
    private Context context;

    public IntentServiceIdlingResource(Context context) { this.context = context; }

    @Override public String getName() { return IntentServiceIdlingResource.class.getName(); }

    @Override public void registerIdleTransitionCallback( ResourceCallback resourceCallback) { this.resourceCallback = resourceCallback; }

    @Override public boolean isIdleNow() {
      // 是否是空闲
      // 如果IntentService 没有在运行，就说明异步任务结束，IntentService特质就是启动以后处理完Intent中的事务，理解关闭自己
        boolean idle = !isIntentServiceRunning();
        if (idle && resourceCallback != null) {
          // 回调告知异步任务结束
            resourceCallback.onTransitionToIdle();
        }
        return idle;
    }

    private boolean isIntentServiceRunning() {
        ActivityManager manager = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
        // Get all running services
        List<ActivityManager.RunningServiceInfo> runningServices = manager.getRunningServices(Integer.MAX_VALUE);
        // check if our is running
        for (ActivityManager.RunningServiceInfo info : runningServices) {
            if (MyIntentService.class.getName().equals(info.service.getClassName())) {
                return true;
            }
        }
        return false;
    }
}

// 使用IntentServiceIdlingResource来测试，MyIntentService服务启动结束这个异步事务，之后的结果。
@RunWith(AndroidJUnit4.class)
public class IntegrationTest {

    @Rule
    public ActivityTestRule rule = new ActivityTestRule(MainActivity.class);
    IntentServiceIdlingResource idlingResource;

    @Before
    public void before() {
        Instrumentation instrumentation = InstrumentationRegistry.getInstrumentation();
        Context ctx = instrumentation.getTargetContext();
        idlingResource = new IntentServiceIdlingResource(ctx);
        // 注册这个异步监听
        Espresso.registerIdlingResources(idlingResource);

    }
    @After
    public void after() {
        // 取消注册这个异步监听
        Espresso.unregisterIdlingResources(idlingResource);

    }

    @Test
    public void runSequence() {
        // MainActivity中点击R.id.action_settings这个View的时候，会启动MyIntentService
        onView(withId(R.id.action_settings)).perform(click());
        // 这时候IntentServiceIdlingResource#isIdleNow会返回false，因为MyIntentService服务启动了
        // 这个情况下，这里会block住.............
        // 直到IntentServiceIdlingResource#isIdleNow返回true，并且回调了IntentServiceIdlingResource#onTransitionToIdle
        // 这个情况下，继续执行，这时我们就可以测试异步结束以后的情况了。
        onView(withText("Broadcast")).check(matches(notNullValue()));
    }
}

```

##### 自定义匹配器

```java
// 定义
public static Matcher<View> withItemHint(String itemHintText) {
  checkArgument(!(itemHintText.equals(null)));
  return withItemHint(is(itemHintText));
}

public static Matcher<View> withItemHint(final Matcher<String> matcherText) {
  checkNotNull(matcherText);
  return new BoundedMatcher<View, EditText>(EditText.class) {

    @Override
    public void describeTo(Description description) {
      description.appendText("with item hint: " + matcherText);
    }

    @Override
    protected boolean matchesSafely(EditText editTextField) {
      // 取出hint，然后比对下是否相同
      return matcherText.matches(editTextField.getHint().toString());
    }
  };
}

// 使用
onView(withItemHint("test")).check(matches(isDisplayed()));
```

## III. 拓展工具

#### 1. AssertJ Android

> [square/assertj-android](https://github.com/square/assertj-android)
> 极大的提高可读性。

```java
import static org.assertj.core.api.Assertions.*;

// 断言: view是GONE的
assertThat(view).isGone();

MyClass test = new MyClass("Frodo");
MyClass test1 = new MyClass("Sauron");
MyClass test2 = new MyClass("Jacks");

List<MyClass> testList = new ArrayList<>();
testList.add(test);
testList.add(test1);

// 断言: test.getName()等于"Frodo"
assertThat(test.getName()).isEqualTo("Frodo");
// 断言: test不等于test1并且在testList中
assertThat(test).isNotEqualTo(test1)
                 .isIn(testList);
// 断言: test.getName()的字符串，是由"Fro"打头，以"do"结尾，忽略大小写会等于"frodo"
assertThat(test.getName()).startsWith("Fro")
                            .endsWith("do")
                            .isEqualToIgnoringCase("frodo");
// 断言: testList有2个数据，包含test，test1，不包含test2
assertThat(list).hasSize(2)
                .contains(test, test1)
                .doesNotContain(test2);

// 断言: 提取testList队列中所有数据中的成员变量名为name的变量，并且包含name为"Frodo"与"Sauron"
//      并且不包含name为"Jacks"
assertThat(testList).extracting("name")
                    .contains("Frodo", "Sauron")
                    .doesNotContain("Jacks");
```

#### 2. Hamcrest

> [JavaHamcrest](https://github.com/hamcrest/JavaHamcrest)
> 通过已有的通配方法，快速的对代码条件进行测试
> `org.hamcrest:hamcrest-junit:(version)`

```java
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.equalTo;

// 断言: a等于b
assertThat(a, equalTo(b));
assertThat(a, is(equalTo(b)));
assertThat(a, is(b));
// 断言: a不等于b
assertThat(actual, is(not(equalTo(b))));

List<Integer> list = Arrays.asList(5, 2, 4);
// 断言: list有3个数据
assertThat(list, hasSize(3));
// 断言: list中有5,2,4，并且顺序也一致
assertThat(list, contains(5, 2, 4));
// 断言: list中包含5,2,4
assertThat(list, containsInAnyOrder(2, 4, 5));
// 断言: list中的每一个数据都大于1
assertThat(list, everyItem(greaterThan(1)));
// 断言: fellowship中包含有成员变量"race"，并且其值不是ORC
assertThat(fellowship, everyItem(hasProperty("race", is(not((ORC))))));
// 断言: object1中与object2相同的成员变量都是相同的值
assertThat(object1, samePropertyValuesAs(object2));

Integer[] ints = new Integer[] { 7, 5, 12, 16 };
// 断言: 数组中包含7,5,12,16
assertThat(ints, arrayContaining(7, 5, 12, 16));

```

##### 几个主要的匹配器:

| Mather | 描述
| --- | ---
| `allOf` | 所有都匹配
| `anyOf` | 任意一个匹配
| `not` | 不是
| `equalTo` | 对象等于
| `is` | 是
| `hasToString` | 包含`toString`
| `instanceOf`,`isCompatibleType` | 类的类型是否匹配
| `notNullValue`,`nullValue` | 测试null
| `sameInstance` | 相同实例
| `hasEntry`,`hasKey`,`hasValue` | 测试`Map`中的`Entry`、`Key`、`Value`
| `hasItem`,`hasItems` | 测试集合(`collection`)中包含元素
| `hasItemInArray` | 测试数组中包含元素
| `closeTo` | 测试浮点数是否接近指定值
| `greaterThan`,`greaterThanOrEqualTo`,`lessThan`,`lessThanOrEqualTo` | 数据对比
| `equalToIgnoringCase` | 忽略大小写字符串对比
| `equalToIgnoringWhiteSpace` | 忽略空格字符串对比
| `containsString`,`endsWith`,`startsWith`,`isEmptyString`,`isEmptyOrNullString` | 字符串匹配

##### 自定义匹配器

```java
// 自定义
import org.hamcrest.Description;
import org.hamcrest.TypeSafeMatcher;

public class RegexMatcher extends TypeSafeMatcher<String> {
    private final String regex;

    public RegexMatcher(final String regex) { this.regex = regex; }
    @Override
    public void describeTo(final Description description) { description.appendText("matches regular expression=`" + regex + "`"); }

    @Override
    public boolean matchesSafely(final String string) { return string.matches(regex); }


    // 上层调用的入口
    public static RegexMatcher matchesRegex(final String regex) {
        return new RegexMatcher(regex);
    }
}

// 使用
String s = "aaabbbaaa";
assertThat(s, RegexMatcher.matchesRegex("a*b*a"));
```
#### 3. Mockito

> [Mockito](https://code.google.com/archive/p/mockito/)
> Mock对象，控制其返回值，监控其方法的调用。
> `org.mockito:mockito-all:(version)`

```java
// import如相关类
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;

// 创建一个Mock的对象
 MyClass test = mock(MyClass.class);

// 当调用test.getUniqueId()的时候返回43
when(test.getUniqueId()).thenReturn(43);
// 当调用test.compareTo()传入任意的Int值都返回43
when(test.compareTo(anyInt())).thenReturn(43);
// 当调用test.compareTo()传入的是Target.class类型对象时返回43
when(test.compareTo(isA(Target.class))).thenReturn(43);
// 当调用test.close()的时候，抛IOException异常
doThrow(new IOException()).when(test).close();
// 当调用test.execute()的时候，什么都不做
doNothing().when(test).execute();

// 验证是否调用了两次test.getUniqueId()
verify(test, times(2)).getUniqueId();
// 验证是否没有调用过test.getUniqueId()
verify(test, never()).getUniqueId();
// 验证是否至少调用过两次test.getUniqueId()
verify(test, atLeast(2)).getUniqueId();
// 验证是否最多调用过三次test.getUniqueId()
verify(test, atMost(3)).getUniqueId();
// 验证是否这样调用过:test.query("test string")
verify(test).query("test string");


// 通过Mockito.spy() 封装List对象并返回将其mock的spy对象
List list = new LinkedList();
List spy = spy(list);

// 指定spy.get(0)返回"foo"
doReturn("foo").when(spy).get(0);

assertEquals("foo", spy.get(0));
```

##### 对访问方法时，传入参数进行快照

```java
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import static org.junit.Assert.assertEquals;

@Captor
private ArgumentCaptor<Integer> captor;

@Test
public void testCapture(){
  MyClass test = mock(MyClass.class);

  test.compareTo(3, 4);
  verify(test).compareTo(captor.capture(), eq(4));

  assertEquals(3, (int)captor.getValue());


  // 需要特别注意，如果是可变数组(vargars)参数，如方法 test.doSomething(String... params)
  // 此时是使用ArgumentCaptor<String>，而非ArgumentCaptor<String[]>
  ArgumentCaptor<String> varArgs = ArgumentCaptor.forClass(String.class);
  test.doSomething("param-1", "param-2");
  verify(test).doSomething(varArgs.capture());

  // 这里直接使用getAllValues()而非getValue()，来获取可变数组参数的所有传入参数
  assertThat(varArgs.getAllValues()).contains("param-1", "param-2");
}
```

##### 对于静态的方法的Mock:

可以使用 [PowerMock](https://github.com/jayway/powermock/wiki/MockitoUsage):

> `org.powermock:powermock-api-mockito:(version)` & `org.powermock:powermock-module-junit4:(version)`(For `PowerMockRunner.class`)

```java

@RunWith(PowerMockRunner.class)
@PrepareForTest({StaticClass1.class, StaticClass2.class})
public class MyTest {

  @Test
  public void testSomething() {
    // mock完静态类以后，默认所有的方法都不做任何事情
    mockStatic(StaticClass1.class);
    when(StaticClass1.getStaticMethod()).andReturn("anything");

    // 验证是否StaticClass1.getStaticMethod()这个方法被调用了一次
    verifyStatic(time(1));
    StaticClass1.getStaticMethod();

    when(StaticClass1.getStaticMethod()).andReturn("what ever");

    // 验证是否StaticClass2.getStaticMethod()这个方法被至少调用了一次
    verifyStatic(atLeastOnce());
    StaticClass2.getStaticMethod();

    // 通过任何参数创建File的实力，都直接返回fileInstance对象
    whenNew(File.class).withAnyArguments().thenReturn(fileInstance);
  }
}

```

或者是封装为非静态，然后用Mockito:

```java
class FooWraper{
  void someMethod() {
    Foo.someStaticMethod();
  }
}
```

#### 4. Robolectric

> [Robolectric](http://robolectric.org/)
> 让模拟测试直接在开发机上完成，而不需要在Android系统上。所有需要使用到系统架构库的，如(`Handler`、`HandlerThread`)都需要使用Robolectric，或者进行模拟测试。

主要是解决模拟测试中耗时的缺陷，模拟测试需要安装以及跑在Android系统上，也就是需要在Android虚拟机或者设备上面，所以十分的耗时。基本上每次来来回回都需要几分钟时间。针对这类问题，业界其实已经有了一个现成的解决方案: Pivotal实验室推出的[Robolectric](http://robolectric.org/)。通过使用Robolectrict模拟Android系统核心库的`Shadow Classes`的方式，我们可以像写本地测试一样写这类测试，并且直接运行在工作环境的JVM上，十分方便。

#### 5. Robotium

> [RobotiumTech/robotium](https://github.com/robotiumtech/robotium)
> (Integration Tests)模拟用户操作，事件流测试。

```java

@RunWith(RobolectricTestRunner.class)
@Config(constants = BuildConfig.class)
public class MyActivityTest{

  @Test
  public void doSomethingTests(){
    // 获取Application对象
    Application application = RuntimeEnvironment.application;

    // 启动WelcomeActivity
    WelcomeActivity activity = Robolectric.setupActivity(WelcomeActivity.class);
    // 触发activity中Id为R.id.login的View的click事件
    activity.findViewById(R.id.login).performClick();

    Intent expectedIntent = new Intent(activity, LoginActivity.class);
    // 在activity之后，启动的Activity是否是LoginActivity
    assertThat(shadowOf(activity).getNextStartedActivity()).isEqualTo(expectedIntent);
  }
}
```

通过模拟用户的操作的行为事件流进行测试，这类测试无法避免需要在虚拟机或者设备上面运行的。是一些用户操作流程与视觉显示强相关的很好的选择。

#### 6. Test Butler

> [linkedin/test-butler](https://github.com/linkedin/test-butler)
> 避免设备/模拟器系统或者环境的错误，导致测试的失败。

通常我们在进行UI测试的时候，会遇到由于模拟器或者设备的错误，如系统的crash、ANR、或是未预期的Wifi、CPU罢工，或者是锁屏，这些外再环境因素导致测试不过。Test-Butler引入就是避免这些环境因素导致UI测试不过。

> 该库被[谷歌官方推荐过](https://www.youtube.com/watch?v=aHcmsK9jfGU)，并且收到谷歌工程师的Review。

## IV. 拓展思路

#### 1. Android Robots

> [Instrumentation Testing Robots - Jake Wharton](https://realm.io/news/kau-jake-wharton-testing-robots/)

假如我们需要测试: 发送 $42 到 "foo@bar.com"，然后验证是否成功。

##### 通常的做法

![](/img/android-test_1.png)

![](/img/android-test_2.png)

##### Robot思想

在写真正的UI测试的时候，只需要关注要测试什么，而不需要关注需要怎么测试，换句话说就是让测试逻辑与View或Presenter解耦，而与数据产生关系。

首先通过封装一个Robot去处理How的部分:

![](/img/android-test_3.png)

然后在写测试的时候，只关注需要测试什么:

![](/img/android-test_4.png)

最终的思想原理

![](/img/android-test_5.png)

---

- 文章创建时间: 2016-5-15，[本文迭代日志](https://github.com/Jacksgong/Blog/commits/master/source/_posts/android_test.md)。

---

本文已经发布到JackBlog公众号，可请直接访问: [Android单元测试与模拟测试 - JacksBlog](https://mp.weixin.qq.com/s?__biz=MzIyMjQxMzAzOA==&mid=2247483680&idx=1&sn=a81f0b86696f243bf32c032fc7b09574)

---

- [Building Local Unit Tests](http://developer.android.com/training/testing/unit-testing/local-unit-tests.html)
- [Testing the Android way](https://www.bignerdranch.com/blog/testing-the-android-way/)
- [timber中的单元测试实例](https://github.com/JakeWharton/timber/blob/master/timber/src/test/java/timber/log/TimberTest.java)
- [timber/build.gradle](https://github.com/JakeWharton/timber/blob/master/timber/build.gradle)
- [A BDD (RSpec-like) testing library for Java](http://stackoverflow.com/questions/30675748/a-bdd-rspec-like-testing-library-for-java)
- [Open Sourcing Test Butler](https://engineering.linkedin.com/blog/2016/08/introducing-and-open-sourcing-test-butler--reliable-android-test)
- [Unit Testing with JUnit -Tutorial](http://www.vogella.com/tutorials/JUnit/article.html)
- [Unit tests with Mockito - Tutorial](http://www.vogella.com/tutorials/Mockito/article.html)
- [Using Hamcrest for testing - Tutorial](http://www.vogella.com/tutorials/Hamcrest/article.html)
- [Testing with AssertJ assertions - Tutorial](http://www.vogella.com/tutorials/AssertJ/article.html)
- [Android user interface testing with Espresso - Tutorial](http://www.vogella.com/tutorials/AndroidTestingEspresso/article.html)
- [chiuki/espresso-samples](https://github.com/chiuki/espresso-samples)
- [Mock static methods from multiple class using PowerMock](http://stackoverflow.com/questions/10327612/mock-static-methods-from-multiple-class-using-powermock)
- [rest-assured/rest-assured](https://github.com/rest-assured/rest-assured)
- [skyscreamer/JSONassert](https://github.com/skyscreamer/JSONassert)
- [Mastering the Terminal side of Android development](https://medium.com/@cesarmcferreira/mastering-the-terminal-side-of-android-development-e7520466c521#.e5vt3p3vl)

---

> © 2012 - 2016, Jacksgong(blog.dreamtobe.cn). Licensed under the Creative Commons Attribution-NonCommercial 3.0 license (This license lets others remix, tweak, and build upon a work non-commercially, and although their new works must also acknowledge the original author and be non-commercial, they don’t have to license their derivative works on the same terms). http://creativecommons.org/licenses/by-nc/3.0/

---
