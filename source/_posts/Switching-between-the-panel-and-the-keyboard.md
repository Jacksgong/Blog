title: Switching between the panel and the keyboard in Wechat
date: 2015-02-07 07:47:03
updated: 2015-02-07 07:47:03
permalink: 2015/02/07/Switching-between-the-panel-and-the-keyboard/
categories:
- Android UI交互
tags:
- keybord
- Android
- Panel
- Wechat
- 优化

---

>Somebody ask me, why there are no layout jumping in wechat when switching between the panel and the keyboard?

>It's very simple.

>Just 2 cases under 2 rules.

<!--more-->

### Precondition

- Definition android:windowSoftInputMode as adjustSize for Activity in AndroidManifest xml.
- Already calculated keybord height.


### Case 1: switching from the panel to the keyboard

#### Rule:

To ensure that gone(or providing zero height) panel during keyboard squeeze layout trigger layout real remeasuring smaller height and redrawing.

### Case 2: switching from the keyboard to the panel

#### Rule:
To ensure that switching panel to display(visible&valid height) from hidden(gone|no height) state is in the keybord hiding trigger layout real remeasuring more high and redrawing period.


### In a word

- No trigger layout remeasure & redraw by panel.
- Readjusting panel height during keybord trigger layout remeasuring new height.

>any suggestions and questions, welcome to follow post comment.

---
