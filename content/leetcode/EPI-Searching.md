Title: EPI-Searching
Date: 2020-04-10 19:20
Modified: 2020-04-10 20:20
Category: LeetCode
Tags: EPI, c++
Slug: epi-Searching

很久很久以前，有人刷题不做记录，没刷过Searching。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还没刷过Searching。

[TOC]

## Searching

这里主要考虑有序存储在数组中的静态数据。



### Binary search

Binary search看起来比较简单，实现起来还是容易产生bug的，比如下面这个(我压根没注意过数值问题)

```c++
int bsearch(int t, const vector<int>& A) {
  int L = 0, U = A.size() - 1;
  while (L <= U) {
    int M = (L + U) / 2;
    if (A[M] < t) {
      L = M + 1;
    } else if (A[M] == t) {
      return M;
    } else {
      U = M - 1;
    }
  }
  return -1;
}
```

产生bug的在`M = (L + U) / 2`， 有可能会导致overflow，改成`M = L + (U - L) /2`能避免这个问题。



### Boot camp



```c++
struct Student {
  string name;
  double grade_point_average;
};

const static function<bool(const Student&, const Student&)> CompGPA = [] (const Student& a, const Student& b) {
  if (a.grade_point_average != b.grade_point_average) {
    return a.grade_point_average > b.grade_point_average;
  }
  return a.name < b.name;
}


bool SearchStudent(const vector<Student>& students, const Student& target, const function<bool(const Student&, const Student&)>& comp_GPA) {
  return binary_search(students.begin(), students.end(), target, comp_GPA);
}
```



### Tips

- Binary search 不仅可以用在有序数组中， 还可以搜索整数或实数的interval
- 如果排序后的操作比排序本身更快，尝试使用部分排序的方法
- 考虑时间和空间的tradeoff



### 库函数

```c++
// <algorithm>
.find(A.begin(), A.end(), target);
.binary_search(begin, end, target); //return bool
.lower_bound(begin, end, target); 
.upper_bound(begin, end, target);

```





### Search a sorted array for first occurrence of k

类似与二分查找，不过这里需要查找第一次出现的位置，更改一下判断条件。

```c++
int SearchFirstOfK(const vector<int>& A, int k) {
  // TODO - you fill in here.
  int L = 0, U = A.size() - 1;
  while (L <= U) {
      int M = L + (U - L) / 2;
      if (A[M] == k && (M == 0 || A[M-1] != k)) {
          return M;
      }
      else if (A[M] < k) {
          L = M + 1;
      } else {
          U = M - 1;
      }
  }
  return -1;
}
```



### Search a sorted array for entry equal to its index

返回有序数组中的一个数值等于下标的元素。

直接迭代也是能求解的，利用类似二分的做法可以进一步降低时间复杂度。注意数组是有序的，index之间的最小差异是1.

```c++
int SearchEntryEqualToItsIndex(const vector<int>& A) {
  // TODO - you fill in here.
  int L = 0, U = A.size() - 1;
  while (L <= U) {
      int M = L + (U - L) / 2;
      if (A[M] == M) {
          return M;
      } else if (A[M] > M) {
          // 值大于index 向左查找
          U = M - 1;
      } else {
          L = M + 1;
      }
  }
  return -1;
}
```



### Search a cyclically sorted array

cyclically sorted array: shift 后变得有序

要求实现$O(\log n)$的算法查找数组中的最小元素.

这个用二分也是可以做的, 关键在于如何定位到要查找的元素以及如何更新上下界.



```c++
int SearchSmallest(const vector<int>& A) {
  // TODO - you fill in here.
  int L = 0, U = A.size() - 1;
  int M = -1;
  while (L <= U) {
      M = L + (U - L) / 2; //向下取整 M>= L && M < U
      if (A[M] >= A[U]) { // 尖峰在右半部份
          L = M + 1;  // 例如[3][1]时，L将前进1， 保证M为最小值
      } else if (A[M] < A[L]){ //尖峰在左半部分
          U = M; //只更新到M的位置 如果等于M-1可能会跳过最小值
      } else {
          return L;
      }
  }
  return M;
}
```



### Compute the integer square root

给定一个整数$k$, 找出最大的整数$x$使得$x^2\leq k$.

直接迭代的话,时间复杂度是$O(n)$, 将这个问题转为在$[1, k]$区间上的二分查找问题可以降低时间复杂度.

```c++
int SquareRoot(int k) {
  // TODO - you fill in here.
  int L = 1, U = k;
  while (L <= U) {
      long M = L + (U - L) / 2;
      long prod = M * M;
      if (prod > k) {
          U = M - 1;
      } else if (prod <= k) { // 要求计算<=k的值
          L = M + 1;
      }
  }
  return L - 1;
}
```



### Compute the real square root

这个可以用牛顿法求解, 将求$x$的平方根问题转为求方程的根.

假设结果为$k$, 令$f(k)=k^2-x$



```c++
double SquareRoot(double x) {
  // TODO - you fill in here.
  bool less_one = x < 1;
  if (less_one) {
      x = 1. / x;
  }
  double L = 1, U = x, k = 0;
  while (abs(L - U) > 1e-8) {
      k = L + (U - L) / 2;
      double l_res = f(L, x), r_res = f(U, x), mid_res = f(k, x);
      if (l_res * mid_res < 0) {
          U = k;
      } else {
          L = k;
      }
  }
  k = L + (U - L) / 2;
  if (less_one) {
      k = 1. / k;
  }
  return k;
}
```



## Generalized search

下面的问题不再考虑二分查找

> For example, they focus on tradeoffs between RAM and computation time, avoid wasted comparisons when searching for the minimum and maximum simultaneously, use randomization to perform elimination efficiently, use bit-level manipulations to identify missing elements, etc.

### Search in a 2D sorted array

给一个排序的2D数组(按行列非递减), 查找指定元素是否在数组内.



~~这个在LeetCode上做过, ~~ 这题要是想降低时间复杂度的话, 要注意两点

- 如果(x, y)位置的值大于目标值val, 所有(y+)列的元素都大于val
- 如果(x, y)位置的值小于目标值, 则当前行的所有(y-)元素都小于val



```c++
bool MatrixSearch(const vector<vector<int>>& A, int x) {
  // TODO - you fill in here.
  if (A.empty()) {
      return false;
  }
  int row = 0, max_col = A[0].size() - 1;
  // 从右上角搜索到左下角
  while (row < A.size()) {
      for (int col = max_col; col >= 0; --col) {
          if (A[row][col] == x) {
              return true;
          }
          if (x > A[row][col]) {
              break;
          }
          if (x < A[row][col]) {
              max_col = col - 1;
          }
      }
      ++row;
  }
  return false;
}
```





### Find the min and max simultaneously

需要在少于$2(n-1)$次比较下查找序列中的最小值和最大值.



如果朴素地比较, 每过一个元素需要进行两次比较. 通过先将两个元素比较得到较大较小值, 再与最大值和最小值分别比较, 将两个元素四次比较降低到两个元素三次比较.



```c++
MinMax FindMinMax(const vector<int>& A) {
  // TODO - you fill in here.
  if (A.size() <= 1) {
      return {A.front(), A.front()};
  }
  std::pair<int, int> global_min_max = std::minmax(A[0], A[1]);
  for (int i = 2; i + 1 < A.size(); ++i) {
      auto local_min_max = std::minmax(A[i], A[i+1]);
      global_min_max.first = std::min(local_min_max.first, global_min_max.first);
      global_min_max.second = std::max(local_min_max.second, global_min_max.second);
  }
  if (A.size() % 2 != 0) {
      global_min_max.first = std::min(A.back(), global_min_max.first);
      global_min_max.second = std::max(A.back(), global_min_max.second);
  }
  return {global_min_max.first, global_min_max.second};
}
```





### Find the kth largest element

如果排序的话, 时间复杂度为$O(n\log n)$, 用最大堆的时间复杂度为$O(n\log k)$.



类似与快排的partition, 只是划分后并不继续对每个区间进行排序.

```c++
int PartitionAroundPivot(int left, int right, int pivot_idx, vector<int>* A_ptr) {
    vector<int> & A = *A_ptr;
    int pivot_value = A[pivot_idx];
    int new_pivot_idx = left;
    std::swap(A[right], A[pivot_idx]);
    for (int i = left; i < right; ++i) {
        if (A[i] > pivot_value) {
            std::swap(A[i], A[new_pivot_idx++]);
        }
    }
    std::swap(A[right], A[new_pivot_idx]); // swap pivot back
    return new_pivot_idx;
}

// The numbering starts from one, i.e., if A = [3, 1, -1, 2] then
// FindKthLargest(1, A) returns 3, FindKthLargest(2, A) returns 2,
// FindKthLargest(3, A) returns 1, and FindKthLargest(4, A) returns -1.
int FindKthLargest(int k, vector<int>* A_ptr) {
  // TODO - you fill in here.
  vector<int> & A = *A_ptr;
  int left = 0, right = A.size() - 1;
  std::default_random_engine gen((std::random_device())());
  while (left <= right) {
      int pivot_idx = std::uniform_int_distribution<int>{left, right}(gen);
      int new_pivot_idx = PartitionAroundPivot(left, right, pivot_idx, &A);
      if (new_pivot_idx == k - 1) {
          return A[new_pivot_idx];
      } else if (new_pivot_idx  < k - 1) {
          left = new_pivot_idx + 1;
      } else {
          right = new_pivot_idx - 1;
      }
  }
  return 0;
}
```



### Find the missing IP address

查找32bit序列中的缺失值，假设有无限制的硬盘空间，却只有MB级别的RAM。

