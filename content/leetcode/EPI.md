Title: EPI-Array
Date: 2020-03-26 18:20
Modified: 2020-03-26 18:20
Category: LeetCode
Tags: EPI, c++
Slug: epi-code-array



很久很久以前，有人刷题不做记录，从Array刷到Array，刷了几年还是在刷Array。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还是在刷Array。

## Array



###　数组的基本语法

```c++
//alloc
array<int, 3> A = {1,2,3};
vector<int> A = {1, 2, 3};
vector<int> sub_A(A.begin(), A.begin()+5);

//2d
array<array<int, 2>, 2> A={};
vector<vector<int>> A;

//
A.push_back();
A.emplace_back();

//algorithm
binary_search(A.begin(), A.end(), 42);
lower_bound(A.begin(), A.end(), 42);
upper_bound(A.begin(), A.end(), 42);
fill(A.begin(), A.end(), 42);
swap(x, y);
min_element(A.begin(), A.end());
max_element(A.begin(), A.end());
reverse(A.begin(), A.end());
rotate(A.begin(), A.begin()+shift, A.end()); //Performs a left rotation on a range of elements.
sort(A.begin(), A.end());
```



### Bootcamp: Arrays



> the even entries appear first

```c++
void EvenOdd(vector<int>* A_ptr) {
  // TODO - you fill in here.
  // 将奇数仍到数组尾部即可
  vector<int>& A = *A_ptr;
  int next_even = 0, next_odd = A.size() - 1;
  while (next_even < next_odd) {
      if (A[next_even] % 2 == 0) {
          ++next_even;
      }
      else {
          std::swap(A[next_even], A[next_odd--]);
      }
  }
  return;
}
```

### The Dutch national flag problem

暴力解法需要O(n)的空间，使用数组自身将空间复杂度降低到O(1).

将数组中小于pivot的元素拍在最前面，等于pivot的排在中间，大于pivot的排在最后。

简单的想法是类似冒泡排序，通过两遍冒泡分别将小于和大于pivot的元素分配到两端。但是类似于上一题的思路，可以通过一遍直接扔的方式避免冒泡O(n^2)的复杂度。

```c++

void DutchFlagPartition(int pivot_index, vector<Color>* A_ptr) {
  // TODO - you fill in here.
  vector<Color> &A = *A_ptr; // 这个地方很蠢地忘记创建引用
  Color pivot = A[pivot_index];
  //小的扔到左边
  int smaller = 0;
  for (int i = 0; i < A.size(); ++i) {
      if (A[i] < pivot) {
          std::swap(A[i], A[smaller++]);
      }
  }
  //大的扔到右边
  int larger = A.size() - 1;
  for (int i = A.size() - 1; i >= 0 && A[i] >= pivot; --i) {
      if (A[i] > pivot) {
          std::swap(A[i], A[larger--]);
      }
  }
  return;
}
```



###　Increment an arbitrary-precision integer

> <1, 2, 9>   ==> <1, 3, 0>

需要处理的是第一位的进位问题。自己的实现调用了两遍reverse太过度了。EPI实现的代码就很简单。

```c++
vector<int> PlusOne(vector<int> A) {
  // TODO - you fill in here.
  std::reverse(A.begin(), A.end());
  int cnt = 0;
  ++A[0];
  for (int i = 0; i < A.size(); ++i) {
      A[i] += cnt;
      if (A[i] >= 10) {
          A[i] -= 10;
          cnt = 1;
      }
      else {
          cnt = 0;
      }
  }
  if (cnt != 0) {
      A.push_back(cnt);
  }
  std::reverse(A.begin(), A.end());
  return A;
}

//EPI代码
vector<int> PlusOne(vector<int> A) {
  // TODO - you fill in here.
  ++A.back();
  for (int i = A.size() - 1; i > 0 && A[i] >=10; --i) {
      A[i] = 0;
      ++A[i-1];
  }
  if (A[0] == 10) {
      A[0] = 0;
      A.insert(A.begin(),1);
  }
  return A;
}
```



### Multiply two arbitrary-precision integers

模拟乘法竖式

```c++
vector<int> Multiply(vector<int> num1, vector<int> num2) {
  // TODO - you fill in here.
  const int sign = num1.front() < 0 ^ num2.front() < 0 ? -1: 1;
  num1.front() = abs(num1.front());
  num2.front() = abs(num2.front());
  // 存放结果
  vector<int> result(num1.size() + num2.size(), 0);
  for (int i = num1.size()-1; i >= 0; --i) {
      for (int j = num2.size()-1; j >= 0; --j) {
          result[i+j+1] += num1[i] * num2[j];
          result[i+j] += result[i+j+1] / 10;
          result[i+j+1] %= 10;
      }
  }
  // 移除前导0  find_if_not
  result = {
          std::find_if_not(std::begin(result), std::end(result), [](int a){ return a==0;}),
          std::end(result)
  };
  if (result.empty()) {
      return {0};
  }
  result.front() *= sign;
  return result;
}
```

### Advancing through an array

数组中的每个元素给出最大移动步数，判断是否能移动到数组尾部。

~~题不刷，就会忘!~~  

看了解法之后也比较好理解，记录当前最大能到达的位置，不断地更新这个值就好。

```c++
// 时间复杂度O(n)，空间复杂度O(1)
bool CanReachEnd(const vector<int>& max_advance_steps) {
  // TODO - you fill in here.
  // 记录当前最远位置
  int furthest_so_far = 0, last_idx = max_advance_steps.size() - 1;
  for (int i = 0; i <= furthest_so_far && i <= last_idx; ++i) {
      furthest_so_far = std::max(furthest_so_far, max_advance_steps[i] + i);
  }
  return furthest_so_far >= last_idx;
}
```

### Delete duplicates from a sorted array

这个从左往右码就行了，数组为空的情况需要处理一下。

```c++
// 时间复杂度O(n)，空间复杂度O(1)
int DeleteDuplicates(vector<int>* A_ptr) {
  // TODO - you fill in here.
  vector<int> &A = *A_ptr;
  if (A.size() == 0) {
      return 0;
  }
  int valid_idx = 0, cur_idx = 1, length = A.size();
  while (cur_idx < length) {
      if (A[cur_idx] == A[valid_idx]) {
          ++cur_idx;
      }
      else{
          A[++valid_idx] = A[cur_idx++];
      }
  }
  return valid_idx+1;
}
```

### Buy and sell a stock once

买卖是按时间顺序的，计算今日卖出价格与历史最低价的差距，与最大收益比较即可。

```c++
double BuyAndSellStockOnce(const vector<double>& prices) {
  // TODO - you fill in here.
  double min_price = std::numeric_limits<double>::max(), max_profit = 0;
  for (auto& price: prices) {
      double profit_today = price - min_price;
      max_profit = std::max(max_profit, profit_today);
      min_price = std::min(min_price, price);
  }
  return max_profit;
}
```



### Buy and sell a stock twice

相比与上一题，这里需要买卖两次。

如何才能将一次的买入卖出变成两次，在上一题的基础上，一个暴力解法是将时间段划分成两部分，前一部分做第一个交易，后一部分做第二次交易。外层O(n)的遍历加上内层`BuyAndSellStockOnce`O(n)的复杂度，总的时间复杂度是O(n^2)。

暴力的解法中有很多的重复计算，如时间划分点变动一天，但是前一部分的计算都要重新做一遍。 既然在思路上是可以将时间拆分成两端，利用`BuyAndSellStockOnce`方法，可以 对第一次买卖的收益只做一遍计算，对第二次买卖的收益也只做一次计算。

由此，先正向计算一遍，在当前时间点前买卖一次的最大收益是多少，再反向计算一遍在当前时间点之后买卖一次的最大收益是多少。这两个值和的最大值即为最大收益。

```c++
double BuyAndSellStockTwice(const vector<double>& prices) {
  // TODO - you fill in here.
  // vector 开成int的了，卡了好一会没搞定
  vector<double> max_profit_first_buy(prices.size(), 0);
  double total_max_profit = 0;
	// 正向计算第一次买卖的收益变化
  double min_price_so_far = std::numeric_limits<double>::max();
  for (int i = 0; i < prices.size(); ++i) {
      min_price_so_far = std::min(min_price_so_far, prices[i]);
      total_max_profit = std::max(total_max_profit, prices[i] - min_price_so_far);
      max_profit_first_buy[i] = total_max_profit;
  }
	// 反向计算第二次买卖的收益变化
  double max_price_so_far = std::numeric_limits<double>::min();
  for (int i = prices.size() - 1; i > 0; --i) {
      max_price_so_far = std::max(max_price_so_far, prices[i]);
      total_max_profit = std::max(total_max_profit, max_price_so_far - prices[i] + max_profit_first_buy[i - 1]);
  }
  return total_max_profit;
}
```





###  Computing an alternation

void



### Enumerate all primes to n

 直接打表筛查。

这里使用bool数组打表，遇到了之前见过的一个问题， 由于C++98的设计原因，`vector<bool>`使用的是bit保存的信息，而不是正常的byte保存bool， 这导致了操作符`[]`并不能真正返回布尔值对应的地址。所以这里应该使用`deque<bool>`

[Why is vector not a STL container?](https://stackoverflow.com/questions/17794569/why-is-vectorbool-not-a-stl-container)


```c++
vector<int> GeneratePrimes(int n) {
  // TODO - you fill in here.
  std::deque<bool> sieve(n+1, true);
  sieve[0] = false;
  for (int i = 2; i < n/2+1; ++i) {
      for (int j = 2; i*j <= n; ++j) {
          sieve[i*j] = false;
      }
  }
  vector<int> ret;
  for (int i = 2; i <= n; ++i) {
      if (sieve[i]) {
          ret.push_back(i);
      }
  }
  return ret;
}
```



###　Permute the elements of an array

给定一个数组和一个排列，将该排列作用的数组上。

直接开辟新数组，可以直接根据排列映射得到结果。 在避免申请新数组的情况下，需要用到一个特性

> 每个排列可由一组独立的排列构成，组内的每个排列都是循环的。
>
> 白话就是每个排列可分成多个圈， 每个圈内shift一次，等价于原排列。



这里使用了C++的lambda表达式，`[]`内的为引用捕获。

使用非成员函数`begin`和`end`在这里有解释：[Why use non-member begin and end functions in C++11?](https://stackoverflow.com/questions/7593086/why-use-non-member-begin-and-end-functions-in-c11)

> Free functions: 非成员函数

非成员函数

```c++
void ApplyPermutation(vector<int> perm, vector<int>* A_ptr) {
  // TODO - you fill in here.
  vector<int> &A = *A_ptr;
  // 最多A.size个子排列
  for (int i = 0; i < A.size(); ++i) {
      int next = i;
      // 对当前组内顺序平移一次
      while (perm[next] >= 0) {
          std::swap(A[i], A[perm[next]]);
          int temp = perm[next];
        	// 使用负数表示已经被访问过， 避免申请新空间
          perm[next] -= perm.size();
          next = temp;
      }
  }
  std::for_each(std::begin(perm), std::end(perm), [&perm](int &x) {x += perm.size();});
  return;
}
```



### Compute the next permutation

要生成一个排列的下一个排列，需要分析其内在的规律。

如<6, 2, 1, 5, 4, 3, 0>来说，其后缀<5, 4, 3, 0>已经是降序的，意味着该后缀是最大字典序，没有下一个排列。需要将1与后面的元素交换，需要在后缀中找到一个比1大(比1小的字典序更小，符合下一个排列的要求)的最小数(下一个字典序的变动应该是最小的)。 得到<6, 2, 3, 5, 4, 1, 0>，这样前缀已经是最小的了，但后缀还不是。交换后的后缀仍然是降序排列， 将其反转可得到最小后缀，即下一个排列为<6, 2, 3, 0, 1, 4, 5>



```c++
vector<int> NextPermutation(vector<int> perm) {
  // TODO - you fill in here.
  int k = perm.size() - 2;
  // 找到最长递减后缀
  while (k >= 0 && perm[k] >= perm[k+1]) {
      --k;
  }
  if (k == -1) {
      return {};
  }
  //从后向前查找第一个大于perm k的元素
  //find_if返回Iterator，解引用后swap
  std::swap(
          *std::find_if(perm.rbegin(), perm.rend(), [&](int a) {return a > perm[k];}),
          perm[k]
          );
  // 将后缀重新由小到大排列
  std::reverse(perm.begin()+k+1, perm.end());
  return perm;
}
```





### Sample offline data

很久很久以前

大名鼎鼎的蓄水池算法，