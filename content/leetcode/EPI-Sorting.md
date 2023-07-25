Title: EPI-Sorting
Date: 2020-04-19 19:20
Modified: 2020-04-19 20:20
Category: LeetCode
Tags: EPI, cpp
Slug: epi-Sorting

很久很久以前，有人刷题不做记录，没刷过Sorting。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还没刷过Sorting。

[TOC]

## Sorting

对于小型数组（10-），插入排序更容易实现，速度更快。

如果是一小部分不同的元素，(如0-255), 计数排序更适合.

如果有大量重复的元素,可以将其串到BST中.



大多数排序是不稳定的, 精心实现的归并排序可以实现稳定排序.



大多数排序都基于元素的两两比较.



### 库函数

```c++
//sort() 数组排序
//list::sort() 链表排序


```

- `sort()`和`list::sort()`都需要实现运算符重载`operator<()`或指定比较函数

排序问题有两种:

- 使用排序使后续的算法更简单
  - 使用库函数即可
- 实现自定义的排序要求
  - 使用BST, heap,索引数组等.



### Compute the intersection of two sorted arrays

A natural implementation for a search engine is to retrieve documents that match the set of words in a query by maintaining an inverted index. Each page is assigned an integer identifier , its document - ID . An inverted index is a mapping that takes a word w and returns a sorted array of page - ids which contain zv the sort order could be , for example , the page rank in descending order. When a query contains multiple words , the search engine finds the sorted array for each word and then computes the intersection of these arrays these are the pages containing all the words in the query . The most computationally intensive step of doing this is finding the intersection of the sorted arrays .



Write a program which takes as input two sorted arrays , and returns a new array containing elements that are present in both of the input arrays . The input arrays may have duplicate entries , but the returned array should be free of duplicates . For example , the input is ( 2 , 3 , 3 , 5 , 5 , 6 , 7 , 7 , 8 , 12 ) and ( 5 , 5 , 6 , 8, 8, 9, 10 , 10 ) , your output should be ( 5 , 6, 8 ) .



倒排索引中的交叉项查找。

这个就类似之前的有序链表的归并。

```c++
vector<int> IntersectTwoSortedArrays(const vector<int>& A,
                                     const vector<int>& B) {
  // TODO - you fill in here.
  vector<int> ret;
  int a_st = 0, b_st = 0;
  while (a_st < A.size() && b_st < B.size()) {
      if (A[a_st] == B[b_st] && (ret.empty() || ret.back() != A[a_st])) {
          ret.emplace_back(A[a_st]);
          ++a_st, ++b_st;
      } else if (A[a_st] < B[b_st]) {
          ++a_st;
      } else {
          ++b_st;
      }
  }
  return ret;
}
```



### Merge two sorted arrays

这个就是上一题的翻版，假设A的尾部有足够的空间容纳B中的元素， 将有序数组AB合并到A中。



首先将A的元素都搬移到A的尾部，留出头部的操作空间。(如果从尾部先排序大元素的话,这一步可以避免)

时间复杂度为$O(m+n)$

```c++
void MergeTwoSortedArrays(vector<int>& A, int m, const vector<int>& B, int n) {
  // TODO - you fill in here.
  int st = m - 1, ed = A.size() - 1;
  while (st >= 0) {
      A[ed--] = A[st--];
  }
  //ed 指向空位置
  int A_st = ed + 1, B_st = 0, A_curr = 0;
  while (A_st < A.size() && B_st < B.size()) {
      if (A[A_st] <= B[B_st]) {
          A[A_curr++] = A[A_st++];
      } else {
          A[A_curr++] = B[B_st++];
      }
  }
  while (A_st < A.size()) {
      A[A_curr++] = A[A_st++];
  }
  while (B_st < B.size()) {
      A[A_curr++] = B[B_st++];
  }
  return;
}
```



从尾部开始合并，可以避免刚开始时对A数组的搬移操作

```c++
void MergeTwoSortedArrays(vector<int>& A, int m, const vector<int>& B, int n) {
  // TODO - you fill in here.
  int A_curr = m + n - 1, A_st = m - 1, B_st = n - 1;
  while (A_st >= 0 && B_st >= 0) {
      if (A[A_st] >= B[B_st]) {
          A[A_curr--] = A[A_st--];
      } else {
          A[A_curr--] = B[B_st--];
      }
  }
  while (B_st >= 0) {
      A[A_curr--] = B[B_st--];
  }
  return;
}
```



### Computing the h-index

无题



### Remove first-name duplicates

Design an efficient algorithm for removing all first - name duplicates from an array . For example , if the input is ( ( Ian , Botham ) , ( David , Gower ) , ( Ian , Bell ) , ( Ian , Chappell ) ) , one result could be (( Ian , Bell ), ( David , Gower ) ) ; ( ( David , Gower ), ( Ian , Botham ) ) would also be acceptable .

Hint: Bring equal items close together .



跟之前的合并也是类似的，先做排序后剔除相同的项目。

```c++
void EliminateDuplicate(vector<Name>* names) {
  // TODO - you fill in here.
  vector<Name>& name_ref = *names;
  std::sort(name_ref.begin(), name_ref.end());
  int l_idx = 0, r_idx = 1;
  while (r_idx < name_ref.size()) {
      if (name_ref[r_idx].first_name == name_ref[l_idx].first_name) {
          ++r_idx;
      } else {
          name_ref[++l_idx] = name_ref[r_idx++];
      }
  }
  if (l_idx == name_ref.size() - 1) {
      return;
  }
  int residual = name_ref.size() - l_idx - 1;
  while (residual-- > 0) {
      name_ref.pop_back();
  }
  return;
}
```



EPI给了一个用`std::unique`去重的方法. 根据文档的说明, 这是C++17及C++20才支持的功能. 我用的Clion目前只配置了C++11, 就不折腾了.

> Eliminates all but the first element from every consecutive group of equivalent elements from the range `[first, last)` and returns a past-the-end iterator for the new *logical*end of the range.
>
> Removing is done by shifting the elements in the range in such a way that elements to be erased are overwritten. Relative order of the elements that remain is preserved and the *physical* size of the container is unchanged. Iterators pointing to an element between the new *logical* end and the *physical* end of the range are still dereferenceable, but the elements themselves have unspecified values. A call to `unique` is typically followed by a call to a container's `erase` method, which erases the unspecified values and reduces the *physical* size of the container to match its new *logical* size.



### Render a calendar

Consider the problem of designing an online calendaring application . One compo nent of the design is to render the calendar , i .e. , display it visually .

Suppose each day consists of a number of events , where an event is specified as a start time and a finish time. Individual events for a day are to be rendered as nonoverlapping rectangular regions whose sides are parallel to the X - and Y - axes. Let the X - axis correspond to time. If an event starts at time b and ends at time e , the upper and lower sides of its corresponding rectangle must be at b and e , respectively . Figure 14.1 represents a set of events.



Write a program that takes a set of events , and determines the maximum number of events that take place concurrently .



找出日程安排中最多同时发生的事件数量。

~~我不太知道怎么处理这个问题。~~

看了解析之后，知道是没有分析好问题，老是想着要把时间堆叠成示意图中的方式。

恰当的方法是把时间的start和finish两个时间节点拆分开，然后按照时间点排序，同时start事件排在finish事件前。这样遇到一个start就将计数加1，遇到一个finish就将计数减1.





```c++
struct Event {
  int start, finish;
};

struct EndPoint {
    bool operator<(const EndPoint& e) const{
        // 将时间靠前的拍在前面 如果时间相同 将start 排在 end 前面
        return this->time != e.time ? this->time < e.time : (this->isStart && !e.isStart);
    }
    int time;
    bool isStart;
};
int FindMaxSimultaneousEvents(const vector<Event>& A) {
  // TODO - you fill in here.
  vector<EndPoint> E;
  for (auto &each : A) {
      E.push_back({each.start, true});
      E.push_back({each.finish, false});
  }
  //按照时间排序
  std::sort(E.begin(), E.end());

  int max_event_cnt = 0, event_cnt = 0;
  for (auto &each : E) {
      if (each.isStart) {
          ++event_cnt;
          max_event_cnt = std::max(event_cnt, max_event_cnt);
      } else {
          --event_cnt;
      }
  }
  return max_event_cnt;
}
```





### Merging intervals

Suppose the time during the day that a person is busy is stored as a set of disjoint time intervals. If an event is added to the person ' s calendar , the set of busy times may need to be updated .

In the abstract , we want a way to add an interval to a set of disjoint intervals and represent the new set as a set of disjoint intervals. For example , if the initial set of intervals is [ - 4 , - 1 ] , [ 0 , 2 ] , [ 3 , 6 ] , [ 7 , 9 ] , [ 11 , 12 ] , [ 14 , 17 ] , and the added interval is [ 1 , 8 ] , the result is [ - 4 , - 1 ] , [ 0 , 9 ] , [ 11 , 12 ] , [ 14 , 17 ] .

Write a program which takes as input an array of disjoint closed intervals with integer endpoints , sorted by increasing order of left endpoint , and an interval to be added , and returns the union of the intervals in the array and the added interval. Your result should be expressed as a union of disjoint intervals sorted by left endpoint .

Hint What is the union of two closed intervals?



在不相交的区间集合中插入一个新的区间，计算出合并后的区间。



这个有点像上一题的日程安排。将区间的两个端点拆开排序，然后从左到右遍历。

在遍历的过程中有些像括号的匹配：

+ 如果是单个区间，那么遇到一个left后就会遇到right，提取出一个区间
+ 如果是多个区间有交叉，对left的个数进行计数，只有left的个数等于right的个数，才算是一个完整的区间。



```c++
struct Interval {
  int left, right;
};
struct EndPoint {
    bool operator<(const EndPoint& e) const {
        return point != e.point ? point < e.point : (isLeft && !e.isLeft);
    }
    int point;
    bool isLeft;
};
vector<Interval> AddInterval(const vector<Interval>& disjoint_intervals,
                             Interval new_interval) {
  // TODO - you fill in here.
  vector<EndPoint> E;
  for (auto &each: disjoint_intervals) {
      E.push_back({each.left, true});
      E.push_back({each.right, false});
  }
  E.push_back({new_interval.left, true});
  E.push_back({new_interval.right, false});

  std::sort(E.begin(), E.end());

  vector<Interval> ret;
  bool is_new_interval = true;
  int st = 0, left_cnt = 0;
  for (auto &each : E) {
      if (each.isLeft) {
          ++left_cnt;
          if (is_new_interval) {
              st = each.point;
              is_new_interval = false;
          }
      } else {
          --left_cnt;
      }
      if (left_cnt == 0) {
          ret.push_back({st, each.point});
          is_new_interval = true;
      }
  }
  return ret;
}
```

.... 我这个时间复杂度是$O(n\log n)$, 如果输入的区间已经是有序排列, 可以将时间复杂度降低到$O(n)$.



### Compute the union of intervals

In this problem we consider sets of intervals with integer endpoints ; the intervals may be open or closed at either end. We want to compute the union of the intervals in such sets.

这题又涉及到区间开闭的问题。

在解决方法上可以照搬上一题的代码，也是将区间的端点拆开排序。因为有区间开闭的问题， 需要根据情况讨论排序条件。



```c++
struct Interval {
  struct Endpoint {
    bool is_closed;
    int val;
  };

  Endpoint left, right;
};

struct Point {
    bool operator<(const Point& p) const {
//        return val != p.val ? val < p.val : (is_left && !p.is_left);
        if (val != p.val) {
            return val < p.val;
        }
        // 元素相等 两个都是开区间
        if (!is_closed && !p.is_closed) {
            // 一前一后 将right 放在left前
            return !is_left && p.is_left;
        }

        // 元素相等 一开一闭 都是right 开区间放前
        if (!is_left && !p.is_left) {
            return !is_closed && p.is_closed;
        }
        // 元素相等 一开一闭 都是left 闭区间放前
        if (is_left && p.is_left) {
            return is_closed && !p.is_closed;
        }
        // 元素相等 一开一闭 left放在right前
        return is_left && !p.is_left;
    }
    int val;
    bool is_left;
    bool is_closed;
};
vector<Interval> UnionOfIntervals(vector<Interval> intervals) {
  // TODO - you fill in here.
  vector<Point> P;
  for (auto &each : intervals) {
      P.push_back({each.left.val, true, each.left.is_closed});
      P.push_back({each.right.val, false, each.right.is_closed});
  }
  std::sort(P.begin(), P.end());
  vector<Interval> ret;

  bool is_new_intervals = true, left_closed = false;
  int left_idx = 0, left_cnt = 0;
  for (auto &each : P) {
    if (each.is_left) {
        ++left_cnt;
        if (is_new_intervals) {
            left_idx = each.val;
            left_closed = each.is_closed;
            is_new_intervals = false;
        }
    } else {
        --left_cnt;
    }
    if (left_cnt == 0) {
        ret.push_back({{left_closed, left_idx},{each.is_closed, each.val}});
        is_new_intervals = true;
    }
  }
  return ret;
}
```



### Partitioning and sorting an array with many repeated entries

Suppose you need to reorder the elements of a very large array so that equal elements appear together . For example , if the array is ( b , a , c , b , d , a , b , d ) then ( a , a , b , b , b , c , d , d ) is an acceptable reordering , as is ( d, d , c , a,a , b , b , b ) .

If the entries are integers , this reordering can be achieved by sorting the array . If the number of distinct integers is very small relative to the size of the array , an efficient approach to sorting the array is to count the number of occurrences of each distinct integer and write the appropriate number of each integer , in sorted order , to the array . When array entries are objects , with multiple fields , only one of which is to be used as a key , the problem is harder to solve.

You are given an array of student objects . Each student has an integer - valued age field that is to be treated as a key . Rearrange the elements of the array so that students of equal age appear together . The order in which different ages appear is not important . How would your solution change if ages have to appear in sorted order?

Hint Count the number of students for each age .

将学生对象按照年龄进行聚类。

因为年龄集中在某个区间内，对全部的学生进行排序需要$O(n\log n)$的时间复杂度. 排序的信息也不是必要的.

下面的做法是$O(n)$的时间复杂度, 但是也用了$O(n)$的空间.

```c++
void GroupByAge(vector<Person>* people) {
  // TODO - you fill in here
  vector<Person>& p_ref = *people;
  std::unordered_map<int, vector<string>> age_to_name;
  for (auto &each: p_ref) {
      age_to_name[each.age].emplace_back(each.name);
  }
  int c_idx = 0;
  for (auto &each : age_to_name) {
      for (auto &name: each.second) {
          p_ref[c_idx++] = {each.first, name};
      }

  }
  return;
}
```



为了将操作改为原地置换，需要另外一个table记录每个age的offset。这样每次找到一个年龄的对象，将其置换到指定的offset上去。



```c++
void GroupByAge(vector<Person>* people) {
  // TODO - you fill in here
  vector<Person>& p_ref = *people;
  std::unordered_map<int, int> age_to_cnt;
  for (auto &each: p_ref) {
      ++age_to_cnt[each.age];
  }
  std::unordered_map<int, int> age_to_offset;
  int offset = 0;
  for (auto &each : age_to_cnt) {
      age_to_offset[each.first] = offset;
      offset += each.second;
  }

  int c_idx = 0;
  while (!age_to_offset.empty()) {
      // 将from 的元素替换到to
      auto from = age_to_offset.begin();
      // 找到from处年龄对应的offset位置的元素的年龄
      auto to = age_to_offset.find(p_ref[from->second].age);
      // 上一步找到两个年龄的offset, 将from替换到to， 此时to位置的元素处于正确的位置， 而from未必
      std::swap(p_ref[from->second], p_ref[to->second]);

      --age_to_cnt[to->first];
      if (age_to_cnt[to->first] > 0) {
          ++age_to_offset[to->first];
      } else {
          age_to_offset.erase(to->first);
      }
  }
  return;
}
```



### Team photo day---1

You are a photographer for a soccer meet. You will be taking pictures of pairs of opposing teams. All teams have the same number of players . A team photo consists of a front row of players and a back row of players . A player in the back row must be taller than the player in front of him , as illustrated in Figure 14.3. All players in a row must be from the same team.

Design an algorithm that takes as input two teams and the heights of the players in the teams and checks if it is possible to place players to take the photo subject to the placement constraint.



 ~~这个题不允许排序...虽然可以开新空间复制元素后排序。~~

.....

居然就是复制后排序...

<img src="{static}/images/what.jfif" style="max-width: 80%">

```c++
  // Checks if team0 can be placed in front of team1.
  static bool ValidPlacementExists(const Team& team0, const Team& team1) {
    // TODO - you fill in here.
    auto team0_sort(team0.players_);
    auto team1_sort(team1.players_);
    std::sort(team0_sort.begin(), team0_sort.end());
    std::sort(team1_sort.begin(), team1_sort.end());
    for (int i = 0; i < team0_sort.size(); ++i) {
        if (!(team0_sort[i] < team1_sort[i])) {
            return false;
        }
    }
    return true;
  }
```



### Implement a fast sorting algorithm for lists

Implement a routine which sorts lists efficiently . It should be a stable sort , i .e. , the relative positions of equal elements must remain unchanged .

Hint: In what respects are lists superior to arrays ?



快排可以原地操作，但不是稳定排序。归并排序是稳定排序，但需要额外的空间。对于数组来说，这两个条件不能同时满足。



对于链表来说，可以使用归并排序来保证稳定性，同时对链表的合并可以原地操作。



```c++
shared_ptr<ListNode<int>> MergeTwoSortList(shared_ptr<ListNode<int>> L0, shared_ptr<ListNode<int>> L1) {
    auto dummy_head = make_shared<ListNode<int>>(ListNode<int>{0, nullptr});

    auto ptr = dummy_head;
    while (L0 && L1) {
        if (L0->data < L1->data) {
            ptr->next = L0;
            L0 = L0->next;
        } else {
            ptr->next = L1;
            L1 = L1->next;
        }
        ptr = ptr->next;
    }
    if (L0 == nullptr) {
        ptr->next = L1;
    } else {
        ptr->next = L0;
    }
    return dummy_head->next;
}

shared_ptr<ListNode<int>> StableSortList(shared_ptr<ListNode<int>> L) {
  // TODO - you fill in here.
  if (L == nullptr || L->next == nullptr) {
      return L;
  }
  // 用快慢指针找到链表中点
  shared_ptr<ListNode<int>> pre_slow = nullptr, slow = L, fast = L;
  while (fast && fast->next) {
      pre_slow = slow;
      fast = fast->next->next;
      slow = slow->next;
  }
  // 断开链表
  pre_slow->next = nullptr;
  // 递归归并排序
  return MergeTwoSortList(StableSortList(L), StableSortList(slow));
}
```



### Compute a salary threshold

You are working in the finance office for ABC corporation . ABC needs to cut payroll expenses to a specified target . The chief executive officer wants to do this by putting a cap on last year ' s salaries. Every employee who earned more than the cap last year will be paid the cap this year ; employees who earned no more than the cap will see no change in their salary .

For example , if there were five employees with salaries last year were \$ 90 ,\$ 30 , \$ 100 , \$ 40 , and \$ 20 , and the target payroll this year is \$ 210 , then 60 is a suitable salary cap , since 60 + 30 + 60 + 40 + 20 = 210.



公司要扣钱了，计划从薪水比较高的人中收割，凡是薪水高于cap的，只发cap，为了使总支出达到target_payroll。



我本来是用了一个table去记录高于xx的薪水有多少人，然后让cap从0到maximum迭代。

在实际操作上，一个是>多少在hash table中不可操作,另一是cap是浮点数, 没法迭代.

恰当的方式是对salary排序后, 每次让cap跳一个层级.

```c++
double FindSalaryCap(int target_payroll, vector<int> current_salaries) {
  // TODO - you fill in here.
  std::sort(current_salaries.begin(), current_salaries.end());
  // 当前cap下的薪水和
  double unadjusted_salary_sum = 0.;
  for (int i = 0; i < current_salaries.size(); ++i) {
      // cap以上的薪水和
      const double adjusted_salary_sum = current_salaries[i] * (current_salaries.size() - i);
      if (unadjusted_salary_sum + adjusted_salary_sum >= target_payroll) {
          return (target_payroll - unadjusted_salary_sum) / (current_salaries.size() - i);
      }
      unadjusted_salary_sum += current_salaries[i];
  }
  return -1;
}
```

