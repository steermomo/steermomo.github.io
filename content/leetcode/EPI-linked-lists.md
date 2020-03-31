Title: EPI-Linked-Lists
Date: 2020-03-27 18:20
Modified: 2020-03-27 18:20
Category: LeetCode
Tags: EPI, c++
Slug: epi-code-linked-lists



很久很久以前，有人刷题不做记录，从Array刷到Linked-Lists，刷了几年还是在刷Linked-Lists。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还是在刷Linked-Lists。



[toc]



## Linked-Lists

EPI的代码都在用`shared_ptr`, 跟之前写的风格完全不一样...



### 结构定义

```c++
template <typename T>
struct ListNode {
	T data;
  shared_ptr<ListNode<T>> next;
}
```

有两种类型的链表题目

- 自己实现链表
  - 搜索
  - 插入
  - 删除
- 使用库函数



tips

- 单链表通常使用两个指针，指针相邻或是快慢指针



标准库中的List

```c++
// list 双向链表
.push_front();
.emplace_front();
.pop_front();
.push_back();
.emplace_back();
.pop_back();

splice(L1.end(), L2);
reverse();
sort();
// forward_list
.push_front();
.emplace_front();
.pop_front();
.insert_after(L.end(), val);
.emplace_after(L.end(), val);
.erase_after(L.begin());

splice_after(L1.end(), L2);
reverse();
sort();

```





### Merge two sorted lists

列表合并倒是比较简单，还真没用过`shared_ptr`来处理这种情况。

```c++
//sorted_lists_merge.cc

void AppendNode(shared_ptr<ListNode<int>> *node, shared_ptr<ListNode<int>> *tail) {
    (*tail)->next = *node;
    *tail = *node; // update tail
    (*node) = (*node)->next;
}
shared_ptr<ListNode<int>> MergeTwoSortedLists(shared_ptr<ListNode<int>> L1,
                                              shared_ptr<ListNode<int>> L2) {
  // TODO - you fill in here.
  shared_ptr<ListNode<int>> dummy_head(new ListNode<int>);
  auto tail = dummy_head;

  while (L1 && L2) {
      AppendNode(L1->data <= L2->data ? &L1 : &L2, &tail);
  }
  tail->next = L1 ? L1 : L2;
  return dummy_head->next;
}
```



### Reverse a single sublist

将单向链表中从s到f(闭区间)位置的链表反转。

```c++
shared_ptr<ListNode<int>> ReverseSublist(shared_ptr<ListNode<int>> L, int start,
                                         int finish) {
  // TODO - you fill in here.
  if (start >= finish) {
      return L;
  }
  auto dummy_head = make_shared<ListNode<int>>(ListNode<int>{0, L});
  auto sublist_head = dummy_head;
  int k = 1;
  // 这里有dummy head  k的值从head开始
  while (k++ < start) {
      sublist_head = sublist_head->next;
  }
  auto sublist_iter = sublist_head->next;
  while (start++ < finish) {
      auto temp = sublist_iter->next;
      sublist_iter->next = temp->next;
      temp->next = sublist_head->next;
      sublist_head->next = temp;
  }
  return dummy_head->next;
}
```





### Test for cyclicity

测试单向链表中是否有环，并找到环开始的结点。

BF的解法是用两个循环套两个指针，外层每次移动一次，内层移动一圈，时间复杂度是O(n^2).

用快慢指针将优化为线性时间复杂度。

慢指针每次前进1，快指针每次前进2，如果链表中有环的话，快指针进入环后会追上慢指针(快指针与慢指针的距离每次减小1)。探测出环后，让其中一个指针继续环绕一圈，计算出环的长度clen。  从头开始设置两个指针，其中一个先走clen，然后两个指针同时前进，因为两个指针的距离相差一个clen，当第一个指针第一次环绕一圈后，第二个指针刚好进入环，两个指针相遇。



```c++
shared_ptr<ListNode<int>> HasCycle(const shared_ptr<ListNode<int>>& head) {
  // TODO - you fill in here.
  shared_ptr<ListNode<int>> slow = head, fast = head;
  while (fast && fast->next) {
      slow = slow->next;
      fast = fast->next->next;
      if (slow == fast) { // find cycle
          // 计算圈长
          int cycle_len = 0;
          do {
              ++cycle_len;
              fast = fast->next;
          }while (slow != fast);
          // cycle 指针先前进cycle len
          auto cycle_advance_iter = head;
          while (cycle_len--) {
              cycle_advance_iter = cycle_advance_iter->next;
          }
          // 两指针同时前进
          auto iter = head;
          while (iter != cycle_advance_iter) {
              iter = iter->next;
              cycle_advance_iter = cycle_advance_iter->next;
          }
          return iter;
      }
  }
  return nullptr;
}
```



### Test for overlapping lists---lists are cycle-free

找出两个单向链表的交界结点。 两个链表如果有相交的结点，从该结点到尾部都是共享的！(单向链表无法再分叉)

将两个链表尾部对其，从最短链表的位置开始遍历，直到遇到相交的位置。



```c++
int Length(shared_ptr<ListNode<int>> L) {
    int  length = 0;
    while (L) {
        ++length;
        L = L->next;
    }
    return length;
}
void AdvanceByK(shared_ptr<ListNode<int>> *L, int k) {
    while (k--) {
        (*L) = (*L)->next;
    }
}
shared_ptr<ListNode<int>> OverlappingNoCycleLists(
    shared_ptr<ListNode<int>> l0, shared_ptr<ListNode<int>> l1) {
  // TODO - you fill in here.
  int l0_len = Length(l0), l1_len = Length(l1);  // 计算长度
  AdvanceByK(l0_len > l1_len ? &l0 : &l1, abs(l0_len - l1_len)); // 将较长的链表头前进，直至两个链表长度相等
  while (l0 && l0 != l1) {
      l0 = l0->next;
      l1 = l1->next;
  }
  return l0;
}
```



### Test for overlapping lists---lists may have cycles

如果用O(n)的空间复杂度，直接用hash表判断已访问过的结点就能直接找到重叠区间的起点。

通过分情况讨论来降低空间复杂度：

- 两个链表都不含环，用上一题的方法判断即可
- 一个含环，另一个不含，则两个链表不会有重叠的部分
- 两个都含环，且是同一个环，这样又分两种子情况：
  - 在进入环之前已经开始合并
  - 在进入环之后才有合并

将问题分解后，可以分别用之前的写过的方法求解。



```c++
int Distance(shared_ptr<ListNode<int>> a, shared_ptr<ListNode<int>> b) {
    int dis = 0;
    while (a != b) {
        a = a->next;
        ++dis;
    }
    return dis;
}
shared_ptr<ListNode<int>> OverlappingLists(shared_ptr<ListNode<int>> l0,
                                           shared_ptr<ListNode<int>> l1) {
  // TODO - you fill in here.
  auto root0 = HasCycle(l0), root1 = HasCycle(l1);
  if (!root0 && !root1) {
      // 两个都无环
      return OverlappingNoCycleLists(l0, l1);
  }
  else if ((!root0 && root1) || (root0 && !root1)) {
      // 只有一个有环，肯定不会相交
      return nullptr;
  }

  auto temp = root0;
  do {
      temp = temp->next;
  } while (temp != root0 && temp != root1);

  if (temp != root1) {
      // 两个都有环，且环不相交
      return nullptr;
  }

  // 类似无环判断时判断两链表相交，需要先计算出距离
  int stem0_length = Distance(l0, root0), stem1_length = Distance(l1, root1);  // 计算两个链表到各自环的距离
  AdvanceByK(stem0_length > stem1_length ? &l0 : &l1, abs(stem0_length - stem1_length));

  while (l0 != l1 && l0 != root0 && l1 != root1) {
      l0 = l0->next;
      l1 = l1->next;
  }

  if (l0 == l1) {
      // l1 == l2 说明在入环之前两个指针相遇，相交点在环外
      return l1;
  }
  else {
      // 另外两种情况下，返回任意一个入环点均可
      return root0;
  }
  
  return nullptr;
}
```





### Delete a node from a singly linked list

在单向链表中删除指针指向的结点(保证待删除的不是尾结点)。

删除当前结点需要更新前结点的next域。题目保证了删除的不是未结点，可通过删除后继结点，并将其值复制到当前位置的方式，变相实现删除。

```c++
// Assumes node_to_delete is not tail.
void DeletionFromList(const shared_ptr<ListNode<int>>& node_to_delete) {
  // TODO - you fill in here.
  node_to_delete->data = node_to_delete->next->data; // copy data
  node_to_delete->next = node_to_delete->next->next;
  return;
}
```





### Remove the kth last element from a list

删除链表中的倒数第k个元素，不允许记录链表的长度信息。

用双指针处理这种问题，让快指针比慢指针快k，这样快指针到达尾部时，慢指针刚好是倒数k个。

```c++
// Assumes L has at least k nodes, deletes the k-th last node in L.
shared_ptr<ListNode<int>> RemoveKthLast(const shared_ptr<ListNode<int>>& L,
                                        int k) {
  // TODO - you fill in here.
  // 头结点为了方便处理删除
  auto dummy_head = make_shared<ListNode<int>>(0, L);
  // 双指针
  auto fast = L, slow = dummy_head;
  // 将fast与slow的间距设为k+1 (slow指向前结点，所以多了1)
  while (k--) {
      fast = fast->next;
  }
  while (fast) {
      fast = fast->next;
      slow = slow->next;
  }
  slow->next = slow->next->next;
  return dummy_head->next;
}
```



### Remove duplicates from a sorted list

这个也可以用双指针试试



```c++
shared_ptr<ListNode<int>> RemoveDuplicates(const shared_ptr<ListNode<int>>& L) {
  // TODO - you fill in here.
  // 刚开始忘记检查空指针的情况，EPI的写法更顺畅一点。
  if (!L || !L->next) {
      return L;
  }
  auto fast = L->next, slow = L;
  while (fast && slow) {
      if (fast->data == slow->data) {
          slow->next = fast->next;
          fast = fast->next;
          continue;
      }
      else {
          fast = fast->next;
          slow = slow->next;
      }
  }
//  auto iter = L;
//  while (iter) {
//      auto next_dist = iter->next;
//      while (next_dist && next_dist->data == iter->data) {
//          next_dist = next_dist->next;
//      }
//      iter->next = next_dist;
//      iter = next_dist;
//  }
  return L;
}
```



### Implement cyclic right shift for singly linked lists

将单链表向右平移k。  

平移k意味着最后的k项将被移动到表头的位置, 用双指针确定倒数第k项的位置。



```c++
int Length(shared_ptr<ListNode<int>> L) {
    int length = 0;
    while (L) {
        ++length;
        L = L->next;
    }
    return length;
}
shared_ptr<ListNode<int>> CyclicallyRightShiftList(shared_ptr<ListNode<int>> L,
                                                   int k) {
  // TODO - you fill in here.
  int list_len = Length(L);
  if (list_len == 0) {
      return nullptr;
  }
  k = k % list_len; // > len 次的平移等价于在n内平移
  auto dummy_head = make_shared<ListNode<int>>(ListNode<int>{0, L});
  auto fast = dummy_head, slow = dummy_head; // 均指向前结点
  while (k--) {
      fast = fast->next;
  }
  while (fast->next) {
      fast = fast->next;
      slow = slow->next;
  }
  fast->next = dummy_head->next; // 尾部应该指向原来的头部
  dummy_head->next = slow->next; // 链表头更新为指向后k个元素的首结点
  slow->next = nullptr; // 中间断开
  return dummy_head->next;
}
```



### Implement even-odd merge

将链表中的偶数位置的结点排在前，奇数位置的结点排在后.

创建两个链表头，按当前位置的奇偶将元素分别放到不同的表中。

头结点真的好用！！

```c++
shared_ptr<ListNode<int>> EvenOddMerge(const shared_ptr<ListNode<int>>& L) {
  // TODO - you fill in here.
    auto even_head = make_shared<ListNode<int>>(ListNode<int>{0, nullptr});
  auto odd_head = make_shared<ListNode<int>>(ListNode<int>{0, nullptr});

  bool even_idx = true;
  auto iter = L, even_iter = even_head, odd_iter = odd_head;
  while (iter) {
      if (even_idx) {
          even_iter->next = iter;
          even_iter = even_iter->next;
      }
      else {
          odd_iter->next = iter;
          odd_iter = odd_iter->next;
      }
      iter = iter->next;
      even_idx = !even_idx;
  }
  even_iter->next = odd_head->next, odd_iter->next = nullptr;
  return even_head->next;
}
```





### Test whether a singly linked list is palindromic

如果按照数组那种判断方法，因为不能随机访问，需要O(n^2)的时间复杂度。

使用快慢指针找到链表的中部位置， 将后半部分翻转，然后从前到后依次比较是否相等。

如果有要求不能改变链表的顺序的话，将后半部分再翻转一次即可。

```c++
shared_ptr<ListNode<int>> ReverseL(shared_ptr<ListNode<int>> L) {
    auto dummy_head = make_shared<ListNode<int>>(ListNode<int>{0, L});
    auto fast = dummy_head->next;
    shared_ptr<ListNode<int>> slow = nullptr;
    while (fast) {
        auto temp = fast->next;
        fast->next = slow;
        slow = fast;
        fast = temp;
    }
    return slow;
}
bool IsLinkedListAPalindrome(shared_ptr<ListNode<int>> L) {
  // TODO - you fill in here.
  if (L == nullptr) {
      return true;
  }

  auto slow = L, fast = L;
  // 当L的长度为偶数时，slow指向另一个半的前结点，当L的长度为奇数时，slow刚好指向中间的结点
  while (fast && fast->next) {
      fast = fast->next->next;
      slow = slow->next;
  }
  auto left = L, right = ReverseL(slow->next);
  while (left && right) {
      if (left->data != right->data) {
          return false;
      }
      left = left->next, right = right->next;
  }
  return true;
}
```





### Implement list pivoting

将小于k的排在k的左边，大于k的排在k的右边。有点类似之前的even-odd merge。

将三种情况的结点分别存放到3个链表中，在合并的时候需要考虑相等的元素不一定存在。不过头结点的存在大大降低了合并的难度。

```c++
shared_ptr<ListNode<int>> ListPivoting(const shared_ptr<ListNode<int>>& l,
                                       int x) {
  // TODO - you fill inhere.
  auto less_head = make_shared<ListNode<int>>(ListNode<int>{0, nullptr});
  auto greater_head = make_shared<ListNode<int>>(ListNode<int>{0, nullptr});
  auto eq_head = make_shared<ListNode<int>>(ListNode<int>{0, nullptr});
  auto l_iter = less_head, g_iter = greater_head, eq_iter = eq_head, iter = l;
  while (iter) {
      if (iter->data < x) {
          l_iter->next = iter;
          l_iter = l_iter->next;
      }
      else if (iter->data == x) {
          eq_iter->next = iter;
          eq_iter = eq_iter->next;
      }
      else {
          g_iter->next = iter;
          g_iter = g_iter->next;
      }
      iter = iter->next;
  }
  
  l_iter->next = eq_head->next == nullptr ? greater_head->next : eq_head->next; // 相等的元素不一定存在
  eq_iter->next = greater_head->next;
  g_iter->next = nullptr;
  return less_head->next;
}
```





### Add list-based integers

链表版本的大数求和，有之前数组的版本，这个写起来也比较容易。

```c++
shared_ptr<ListNode<int>> AddTwoNumbers(shared_ptr<ListNode<int>> L1,
                                        shared_ptr<ListNode<int>> L2) {
  // TODO - you fill in here.
  shared_ptr<ListNode<int>> dummy_head = make_shared<ListNode<int>>(ListNode<int>{0, nullptr});
  auto iter = dummy_head;
  int carry = 0;
  // 同时前进两个链表指针
  while (L1 && L2) {
      int val = L1->data + L2->data + carry;
      if (val > 9) {
          val = val - 10;
          carry = 1;
      }
      else {
          carry = 0;
      }
      // 创建新结点
      iter->next = make_shared<ListNode<int>>(ListNode<int>{val, nullptr});
      iter = iter->next;
      L1 = L1->next;
      L2 = L2->next;
  }
  // 处理尾部剩余数值
  auto tail = L1 ? L1 : L2;
  iter->next = tail; // iter指向前结点
  while (carry) {
      if (iter->next == nullptr) {
          iter->next = make_shared<ListNode<int>>(ListNode<int>{carry, nullptr});
          carry = 0;
      }
      else if (iter->next->data >= 9) {
              iter->next->data = 0;
              carry = 1;
              iter = iter->next;
      }
      else {
          iter->next->data += carry;
          carry = 0;
      }
  }
  return dummy_head->next;
}
```

