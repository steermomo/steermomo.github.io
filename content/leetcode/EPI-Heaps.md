Title: EPI-Heaps
Date: 2020-04-07 19:20
Modified: 2020-04-07 20:20
Category: LeetCode
Tags: EPI, c++
Slug: epi-Heaps

很久很久以前，有人刷题不做记录，没刷过Heaps。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还没刷过Heaps。

[TOC]

## Heaps

Heaps又可以称为优先队列，是一个特化的二叉树(完全二叉树)。

Heap中一个结点的键值需要大于等于其子树中的键值。

一个最大堆插入时间复杂度为 $O(\log n)$，查找最大值为$O(1)$, 删除最大值为$O(\log n)$.

 

### Tips

- 当需要操心最大值,最小值且不需要快速查找删除时,使用heap
- 当需要查找k个最大(最小)元素时, 可以使用最小(最大)堆.



### Heap libraries

> A priority queue is a container adaptor that provides constant time lookup of the largest (by default) element, at the expense of logarithmic insertion and extraction.
>
> A user-provided `Compare` can be supplied to change the ordering, e.g. using std::greater<T> would cause the smallest element to appear as the [top()](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/container/priority_queue/top.html).
>
> Working with a `priority_queue` is similar to managing a [heap](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/algorithm/make_heap.html) in some random access container, with the benefit of not being able to accidentally invalidate the heap.

```c++
// priority_queue
//std::priority_queue
// 定义
template<
    class T, // 数据类型
    class Container = std::vector<T>, //priority_queue 容器
    class Compare = std::less<typename Container::value_type> // 比较符
> class priority_queue;
.push();
.top();
.pop();
```





### Merge sorted files

问题场景：有500个文件，每个文件包含一个公司的股票交易信息，每次交易编码成一行：123211，APPL，30，456.12，分别表示自从交易日至今的时间、股票代码、股票的股数(shares)、单价。

要去将这500个文件合并成单个文件，按照时间增序排列。



这个有些类似有序列表的合并, 每次取每个500个文件头中最小的那个插入到结果中. 只是要同时维护500个文件的当前位置有些困难.



这里就直接看EPI的解析了. 给出的代码实现挺好的, 在堆内保存vector的迭代器, 将比较操作定义为迭代器指向的值之间的大小比较.

这样每个vector都有对应的iterator记录当前读取的位置. heap的排序特性会自动将当前最小值对应的iterator调整到堆首.

时间复杂度为$O(n\log k)$

```c++
struct IteratorCurrentAndEnd{
    // 比较迭代器指向的值
    bool operator>(const IteratorCurrentAndEnd& that) {
        return *current > *that.current;
    }
    vector<int>::const_iterator current;
    vector<int>::const_iterator end;
};
vector<int> MergeSortedArrays(const vector<vector<int>>& sorted_arrays) {
  // TODO - you fill in here.
  std::priority_queue<IteratorCurrentAndEnd, vector<IteratorCurrentAndEnd>, std::greater<>>
  min_heap;
  // 保存每个数组的迭代器
  for (const vector<int>& sorted_array: sorted_arrays) {
      if (!sorted_array.empty()) {
          min_heap.emplace(IteratorCurrentAndEnd{sorted_array.cbegin(), sorted_array.cend()});
      }
  }

  vector<int> ret;
  while (!min_heap.empty()) {
      // 取出当前最小元素对应的迭代器
      auto smallest_array = min_heap.top();
      min_heap.pop();
      if (smallest_array.current != smallest_array.end) {
          // 对应的数组非空
          ret.emplace_back(*smallest_array.current);
          min_heap.emplace(IteratorCurrentAndEnd{std::next(smallest_array.current), smallest_array.end});
      }
  }
  return ret;
}
```



###  Sort an increasing-decreasing array

k increasing-decreasing array: 数组中的元素递增递减再递增...共k次



直接排序的方法时间复杂度为$O(n \log n)$. 这样就没有利用到元素有递增递减的特性.

至于怎么用到这个特性呢...我也不知道, 没做过



Solution: 先将递减的序列翻转, 也变成递增的序列. 这样就得到了一组都递增的子数组, 然后就类似上一题的操作.



```c++
vector<int> SortKIncreasingDecreasingArray(const vector<int>& A) {
  // TODO - you fill in here.
  vector<vector<int>> sorted_subarrays;
  typedef enum {INCREASING, DECREASING} SubarrayType;
  SubarrayType subarray_type = INCREASING;
  int start_idx = 0;
  for (int i = 1; i <= A.size(); ++i) {
      // 状态发生变化或到达尾部
      if (i == A.size() || (A[i-1] < A[i] && subarray_type == DECREASING)
        || (A[i-1] >= A[i] && subarray_type == INCREASING)) {
          if (subarray_type == INCREASING) {
              // 递增的序列直接添加进ret
              sorted_subarrays.emplace_back(A.cbegin()+start_idx, A.cbegin()+i);
          } else {
              // 将递减的序列翻转后再添加到ret
              sorted_subarrays.emplace_back(A.crbegin() + A.size() - i, A.crbegin() + A.size() - start_idx);
          }
          subarray_type = subarray_type == INCREASING ? DECREASING : INCREASING;
          start_idx = i;
      }
  }
  return MergeSortedArrays(sorted_subarrays);
}
```





### Sort an almost-sorted array

问题背景: 由于延时等原因,服务器按时间接收的数据在顺序上可能会有些许的漂移. 给一个数组,其中元素距离其正确的位置距离不会超过k, 将其排序.



...

不会, 看解析

...

这个要用到元素距离正确位置的距离不会超过k这个特性. 在一共读入k+1个元素的情况下, 这个集合中的最小值一定也是后续元素的最小值. 因此就能确定这个值的位置.

因为每次都需要读入一个数, 并获得当前集合的最小值, 这里需要使用最小堆来实现.

时间复杂度为$O(n \log k)$, 空间复杂度为$O(k)$

```c++
vector<int> SortApproximatelySortedData(
    vector<int>::const_iterator sequence_begin,
    const vector<int>::const_iterator& sequence_end, int k) {
  // TODO - you fill in here.
  std::priority_queue<int , vector<int>, std::greater<int>> min_heap;
  int cnt = 0;
  // 先存入k+1个数
  while (sequence_begin != sequence_end && cnt < k + 1) {
      int val = *sequence_begin;
      min_heap.emplace(val);
      ++sequence_begin;
  }
  vector<int> ret;
  // 每新读取一个数， 当前堆的最小值就是正确排序的最小值
  while (sequence_begin != sequence_end) {
      int val = min_heap.top();
      min_heap.pop();
      ret.emplace_back(val);
      min_heap.emplace(*sequence_begin);
      ++sequence_begin;
  }
  // 将堆中的剩余元素追加到结果中
  while (!min_heap.empty()) {
      int val = min_heap.top();
      ret.emplace_back(val);
      min_heap.pop();
  }
  return ret;
}
```



### Compute the k closest stars

Milky Way銀河系



计算在银河系中距离地球最近的k颗星球.

这个还是比较简单的, 只是需要用最大堆来处理.

```c++
vector<Star> FindClosestKStars(vector<Star>::const_iterator stars_begin,
                               const vector<Star>::const_iterator& stars_end,
                               int k) {
    // TODO - you fill in here.
    std::priority_queue<Star, vector<Star>, std::less<>> max_heap;
    int cnt = 0;
    while (stars_begin != stars_end && cnt < k) {
        ++cnt;
        max_heap.emplace(*stars_begin);
        ++stars_begin;
    }
    while (stars_begin != stars_end) {
        max_heap.emplace(*stars_begin);
        max_heap.pop(); // pop 最大元素
        ++stars_begin;
    }
    vector<Star> ret;
    while (!max_heap.empty()) {
        ret.emplace_back(max_heap.top());
        max_heap.pop();
    }
  return ret;
}
```





### Compute the median of online data

 计算一个流中元素的中位数.

这里是需要保存历史数据的, 如果是用数组顺序保存, 每次插入一个元素都需要查找一次中位数.

中位数的特点是将数值集合分成两个大小均等的部分, 那么就可以用一个最大堆和一个最小堆来分别表示这两个部分. 每次读取一个新元素, 就依次从这两个堆里过一遍.

```c++
vector<double> OnlineMedian(vector<int>::const_iterator sequence_begin,
                            const vector<int>::const_iterator &sequence_end) {
    // TODO - you fill in here.
    // 最小堆存储较大的那半部份数  最大堆存储较小的那部份
    std::priority_queue<int, vector<int>, std::greater<>> min_heap;
    std::priority_queue<int, vector<int>, std::less<>> max_heap;
    vector<double> ret;
    while (sequence_begin != sequence_end) {
        min_heap.emplace(*sequence_begin++);
        max_heap.emplace(min_heap.top());
        min_heap.pop();
        // 偶数个元素情况下， 两个堆大小将会相等， 否则最小堆将会多一个元素
        if (max_heap.size() > min_heap.size()) {
            min_heap.emplace(max_heap.top());
            max_heap.pop();
        }
        ret.emplace_back(max_heap.size() == min_heap.size() ?
                         0.5 * max_heap.top() + 0.5 * min_heap.top() :
                         min_heap.top());
    }
    return ret;
}
```





### Compute the k largest elements in a max-heap

在不改变堆存储的情况下获取k个最大的元素.

如果对堆进行排序,则改变了堆存储.

这里利用最大堆的性质: 结点的值大于等于所有子树中结点的值, 同时堆是一个完全二叉树, 在数组的存储结构中父子结点很容易索引.

那么根结点包含最大的元素, 第二大的则是根结点的左右孩子中较大者, 第三大的又是前述子结点的子结点中较大者. 

如果手写判断将会十分麻烦,  刚好在上面的操作中又一直有取集合的最大值,另开一个堆来完成元素的排列比较方便.



EPI的写法中使用了`std::function<bool(HeapEntry, HeapEntry)>`来完成队列的类型指定. 

在`priority_queue`的定义中, `Compare`对象需要是一个class

```c++
template<
    class T,
    class Container = std::vector<T>,
    class Compare = std::less<typename Container::value_type>
> class priority_queue;
```

不能直接传入`lambda`函数. 在模板中指定了`Compare`后,  通过构造函数赋值比较函数

```c++
explicit priority_queue(const Compare& compare) 
    : priority_queue(compare, Container()) { }
```



```c++
vector<int> KLargestInBinaryHeap(const vector<int>& A, int k) {
  // TODO - you fill in here.
  if (k <= 0) {
      return {};
  }
  struct HeapEntry {
      int idx, val;
  };
  std::priority_queue<HeapEntry, vector<HeapEntry>, std::function<bool(HeapEntry, HeapEntry)>>
    candidate_max_heap([] (const HeapEntry& a, const HeapEntry& b) {return a.val < b.val;});
  // 放入根结点
  candidate_max_heap.emplace(HeapEntry{0, A[0]});
  vector<int> ret;
  // 取出k个最大的数
  for (int i = 0; i < k; ++i) {
      int candidate_idx = candidate_max_heap.top().idx;
      ret.emplace_back(A[candidate_idx]);
      candidate_max_heap.pop();

      int left_idx = candidate_idx * 2 + 1;
      if (left_idx < A.size()) {
          candidate_max_heap.emplace(HeapEntry{left_idx, A[left_idx]});
      }
      int right_idx = candidate_idx * 2 + 2;
      if (right_idx < A.size()) {
          candidate_max_heap.emplace(HeapEntry{right_idx, A[right_idx]});
      }
  }
  return ret;
}
```

