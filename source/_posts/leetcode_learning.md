title: LeetCode算法题学习笔记
date: 2019-02-22 11:36:03
updated: 2019-02-22
categories:
- 笔记
tags:
- leetcode
- Programing

---

{% note info %} 一方面是想要开阔思路以及做一些思维的练习，另一方面也是做了几题觉得挺有意思的还有需要提高公司面试人员筛选的准确度，而LeetCode.com本身也是深受海内外科技行业的认可，因此持续化的做点LeetCode学习笔记。{% endnote %}

<!-- more -->

主要目标是能过拓宽思路，不要求量，只要求每道题都有自己的思考，并且能够提高做题效率，想必刚开始是很磨叽的过程，说句实话，作为常年实糙的我，算法基础真心有很大的提高空间。

## List旋转

> https://leetcode.com/articles/rotate-list/
> Given a linked list, rotate the list to the right by k places, where k is non-negative.

题干案例就不再摘抄了，题目链接有，这是一个四星半的题目，感觉是我膨胀了吗？n年没有做算法题，居然以拿到就有思路，砰砰砰就写了一片代码。

思路:

```
// k < n
tail --> n-k-1
head --> n-k
// k >= n
tail --> n-(k mod n)-1
head --> n-(k mod n)
```

回头来看，思路是正确的，我的实现就不贴了，总之相对于标准答案还有优化空间，反思下:

这是一个linked list，我的做法是先在图上画出需要找出的几个关键的`Node`，然后求出链表长度；分别求出`k<n`以及`k>=n`两种情况下head与tail的index(其中还遇到`k>=n`的时候发现当`k%n=0`时的case特殊处理)，然后再分别找出几个点进行断`newTail`与拼接`oldTail`，返回`newHead`。相比与标准答案有明显的几个问题:

1. 其实当`k<n`的时候: `n-(k mod n) = n-k`；这里我没有做深究，通过这个可以简化后续的代码可读性
2. 这是一个`linked list`，我为什么需要先求出`index`，直接从列表找到关键的node进行处理就行了嘛
3. 虽然有一个special case是原顺序不变，但是显然先将整个liked list组为一个ring然后再进行统一的算法处理会更加可读

摘抄一遍标准答案以作为反思:

```
public Node rotateList(Node headNode, k){
  if (headNode == null) return null;
  if (headNode.next == null) return null;

  // find oldTail and set as ring
  Node oldTail = headNode;
  int n = 1;
  while (oldTail.next != null){
    oldTail = oldTail.next;
    n++;
  }
  oldTail.next = headNode;

  // tail --> n-(k mod n) -1
  // head --> n-(k mod n)
  Node newTail = headNode;
  for ( int i = 0; i < n - k%n -1; i++){
    newTail = newTail.next;
  }
  Node newHead = newTail.next;

  // break ring
  newTail.next = null;

  return newHead;
}
```

## Pascal Triangle

> https://leetcode.com/explore/learn/card/recursion-i/251/scenario-i-recurrence-relation/1644/
> 帕斯卡三角形就是: 最左与左右都是1，其余的是上面两个数相加得到。要求第i行第j列值是多少。

这个主要是递归的。


思路:

这种题目呢先画图，然后找到base case与recurrence relation formula

这里的base case很明显: 当`j=1 or i=j`时 $f(i,j) = 1$
它的`recurrence relation formula`就是: $f(i, j) = f(i-1, j-1) + f(i-1, j)$

如果觉得抽象，可以自己随便画一个三角形，然后取一个值带入分解。

因此这个最简单的方法就是:

```
public static void getPascalTriangleValue(int i, int j) {
  if (j == 1 || j == i ) return 1;
  return getPascalValue(i - 1, j - 1 ) + getPascalValue(i -1, j);
}
```

> 求一个Pascal Triangle

```
class Solution {
    public List<List<Integer>> generate(int numRows) {
        final List<List<Integer>> pascalTriangle = new ArrayList<>();
        for (int i = 1; i <= numRows; i++) {
            final List<Integer> newRow = new ArrayList<>();
            pascalTriangle.add(newRow);
            for (int j = 1; j <=i; j++) {
                newRow.add(getPascalTriangleValue(i, j));
            }
        }
        return pascalTriangle;
    }

    public static int getPascalTriangleValue(int i, int j) {
        // not triangle error
        //if (j > i || j < 1) throw new RuntimeException("not pascal triangle with row[" + i "] and column["+ j + "]");
        if (j==1 || i==j) return 1;
        return getPascalTriangleValue(i-1, j-1) + getPascalTriangleValue(i-1, j);
    }
}
```

这个稍微思考下，应该是可以优化的，因为其实在递归的时候，就已经把前面的值都拿到了，只不过我们应该怎么把这些值利用好。

```
public static void recursionPascalTriangle(List<List<Integer>> pascalTriangle, i, j){
    rowIndex = i - 1;
    columnIndex = j - 1;

    rowList = pascalTriangle.get(rowIndex);
    if (rowList == null){
      rowList = new ArrayList<Integer>(i);
      pascalTriangle.add(rowIndex, rowList)
    }

    if (j == 1 || j == i) {
      rowList.add(columnIndex, 1);
    } else {
      recursionPascalTriangle(pascalTriangle, i-1, j-1);
      recursionPascalTriangle(pascalTriangle, i-1, j);
      preRowList = pascalTriangle.get(rowIndex -1);

      rowList.add(columnIndex, preRowList.get(columnIndex - 1) + preRowList.get(columnIndex))
    }
}
```

上面这个的正确解法应该是从上到下递归:

```
iterate(List<List<Integer>> pascalTriangle, int row, int maxRow){
  if (row > maxRow) return;
  // .... calculate this row from pre row

  iterate(pascalTriangle, row+1, maxRow)
}
```

但是上面这个做法显然有问题，而最简单的方法其实就是:

```
class Solution {
  public static List<List<Integer>> generate(int numRows) {
    // if (numRows < 0) not accept
    final List<List<Integer>> pascalTriangle = new ArrayList<>();
    if (numRows == 0) return pascalTriangle;

    List<Integer> preRow = new ArrayList<>();
    preRow.add(1);
    pascalTriangle.add(preRow);
    if (numRows == 1) return pascalTriangle;

    for (int i = 1; i < numRows; i++) {
      final List<Integer> newRow = new ArrayList<>(i + 1);
      pascalTriangle.add(newRow);
      newRow.add(1);
      for (int j = 1; j< i; j++){
        newRow.add(preRow.get(j-1) + preRow.get(j))
      }
      newRow.add(1);
      preRow = newRow;
    }

    return pascalTriangle;
  }
}
```

> 尽量小的额外空间使用，求第k+1行的帕斯卡三角值:

根据题干建议是使用额外空间是$O(k)$，因此这里很明显是只有存储一个第`k`行的缓存，因此就一个递归不断缓存复用即可。

```
class Solution {
    public List<Integer> getRow(int rowIndex) {
        return iterate(new ArrayList<>(), 1, rowIndex+1);
    }

    public static List<Integer> iterate(List<Integer> preRowList, int row, int maxRow) {
        if (row > maxRow) return preRowList;

        final List<Integer> rowList = new ArrayList<>(row);
        rowList.add(1);

        // not first row
        if (row > 1) {
            for (int j = 1; j < row - 1; j ++) {
                rowList.add(preRowList.get(j-1) + preRowList.get(j));
            }
            rowList.add(1);
        }

        return iterate(rowList, row + 1, maxRow);
    }
}
```

上面这个答案在提交之后做了一点改动，主要是要对特殊值处理需要做完后review，比如之前的答案中将`rowIndex == 0`的case拿出来单独处理，几种解法后混淆在里面导致特殊值错误。
但是还有更简单的做法，最简单的做法其实并不是用递归，而是使用遍历，这样可以减少赋值次数:

```
class Solution {
  public List<Integer> getRow(int rowIndex){
    final List<Integer> rowList = new ArrayList<>();

    final int[] previous = new int[rowIndex + 1];

    for(int i = 0; i <= rowIndex; i++) {
      for(int j = i; j >=0; j--) {
        if(j == i || j == 0) {
          previous[j] = 1;
        } else {
          // previous[j-1] and previous[j] now is the pre row values;
          previous[j] += previous[j-1];
        }
      }
    }

    for (int i=0; i <= rowIndex; i++){
      rowList.add(previous[i]);
    }

    return rowList;
  }
}
```

分别用递归与遍历的方式对链表反转:

通过前面的练习，这里其实就已经可以做到可以说是十分的顺手的，首先思考下公式:

很显然: $f(next) = f(pre)$
而终止点: $head = null$

OK，那么这边再通过画图就可以得知遍历的话，我们必然需要有三点: `pre`，`cur`，`next`，主要是先备份`next`，然后将`cur.next`指向`pre`，然后循环。
而递归的话，截止点是 $cur == null$的时候将$pre$返回回去，然后这边每次都是往前指向就ok了。

```
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) { val = x; }
 * }
 */
class Solution {
    public ListNode reverseList(ListNode head) {
        // base case: head.next = null
        // formula: f(next) = f(pre)

        //return reverseListIterate(head);
        return reverseListRecursive(null, head);
    }

    public ListNode reverseListIterate(ListNode head){
        ListNode pre = null;
        ListNode cur = head;
        ListNode next = head.next;

        while(cur != null) {
            next = cur.next;
            cur.next = pre;

            pre = cur;
            cur = next;
        }

        return pre;
    }

    public ListNode reverseListRecursive(ListNode pre, ListNode cur) {
        if (cur == null) return pre;

        ListNode next = cur.next;
        cur.next = pre;
        return reverseListRecursive(cur, next);
    }
}
```

不过这道题做下来依然存在几个问题:

1. special case没有处理，这个在写之前有考虑的，但是想着先把方法写出来然后再做这块，结果就忘了，这个以后要特别注意
2. 其实可以利用`head.next`来代替上面算法的`pre`来节省一个`ListNode`的空间

因此优化后如下:

```
public ListNode reverseListIterate(ListNode head){
  if (head == null || head.next == null) {
    return head;
  }

  ListNode newHead = head;
  ListNode next = head.next;

  while(next != null){
    // for mark next.next, finally to null
    head.next = next.next;

    next.next = newHead;

    newHead = next;
    next = head.next;
  }

  return newHead;
}
```

不过考虑到可读性，其实我的做法也不错，仅仅只是多了一个`next`的备份可读性就提高了很多。

## Fibonacci Numbers

> https://leetcode.com/explore/learn/card/recursion-i/255/recursion-memoization/1661/

通过缓存、递归等方式来实现计算出第n个Fibonacci Number: `F(n)`

我们已知这个的公式: `F(n) = F(n-2) - F(n-1)`
并且Base Case: `F(0) = 0`; `F(1) = 1`

```
class Solution {
    private final HashMap<Integer, Integer> cachedMap = new HashMap<>();
    public int fib(int n) {
        if (n <= 1) return n;

        if (cachedMap.containsKey(n)) return cachedMap.get(n);

        final int value = fib(n - 2) + fib(n - 1);
        cachedMap.put(n, value);
        return value;
    }
}
```
唯一一点需要思考的是，先`n-2`还是先`n-1`，如果是先`n-2`的话，这边是否是能够避免多余计算，其实没有关系，无论哪一个都是会确保只计算一次，简单推演下会把抽象的问题形象化:

```
5,

          4             3
    3         2      2     1
  2    1  
1   0
```

不过这道题如果抛开递归，最佳的方法(少了调用栈的开销):

```
class Solution {
    public int fib(int n) {
        if (n <= 1) return n;
        final int[] f = new int[n + 1];
        f[0] = 0;
        f[1] = 1;
        for (int i = 2; i <= n; i++ ) f[i] = f[i - 1] + f[i - 2];
        return f[n];
    }
}
```

因此。。这道题，哈哈哈哈哈。
