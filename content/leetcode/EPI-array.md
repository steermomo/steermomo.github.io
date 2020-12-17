Title: EPI-Array
Date: 2020-03-26 18:20
Modified: 2020-03-26 18:20
Category: LeetCode
Tags: EPI,c++
Slug: epi-code-array



很久很久以前，有人刷题不做记录，从Array刷到Array，刷了几年还是在刷Array。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还是在刷Array。

[TOC]

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

从数组中随机抽取k个元素。 每次从剩余数组中抽取一个元素，直至抽到k个。



这个代码很“C++11”... 直接random取余数并不能生成真正的均匀分布。

C++11把随机数分为引擎和分布两个部分，需要先指定一个随机数引擎，再根据分布生成随机数。

> [std::random_device](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/numeric/random/random_device.html) is a non-deterministic uniform random bit generator, although implementations are allowed to implement [std::random_device](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/numeric/random/random_device.html) using a pseudo-random number engine if there is no support for non-deterministic random number generation.

random_device() 生成一个对象，其操作符`()`将推进引擎的状态，返回一个随机数，这里用于随机数引擎的种子。

这里的写法，我也没太看懂，为什么分布后面可以是花括号，将其换成圆括号是我能理解的写法。待更

```c++
void RandomSampling(int k, vector<int>* A_ptr) {
  // TODO - you fill in here.
  vector<int> &A = *A_ptr;
  // default_random_engine 生成随机数引擎
  // random_device()
  std::default_random_engine seed((std::random_device())());
  for (int i = 0; i < k; ++i) {
      std::swap(
              A[i],
              A[std::uniform_int_distribution<int>{i, static_cast<int>(A.size()-1)}(seed)]
              );
  }
  return;
}
```



### Sample online data

很久很久以前，有个蓄水池算法，要从流中随机抽取k个元素。

假设目前已经接受了n个包并抽取了k个元素，当第n+1个包到达时，其属于抽样集的概率应为k/(n+1)，这时随机一个概率值，若当前包可被保留，则从原k个元素中随机剔除一个。

数学证明可见：[水塘抽樣](https://zh.wikipedia.org/wiki/水塘抽樣)



```c++
// Assumption: there are at least k elements in the stream.
vector<int> OnlineRandomSample(vector<int>::const_iterator stream_begin,
                               const vector<int>::const_iterator stream_end,
                               int k) {
  // TODO - you fill in here.
  vector<int> ret;
  // 先填充k个元素
  for (int i = 0; i < k; ++i, ++stream_begin) {
      ret.push_back(*stream_begin);
  }
  // 初始化随机数引擎
  std::default_random_engine seed((std::random_device())());
  int element_so_far = k;
  while (stream_begin != stream_end) {
      ++element_so_far;
    	// 以 k/n+1的概率保留元素
      int rand_val = std::uniform_int_distribution<int>(0, element_so_far-1)(seed);
      if (rand_val < k) {
          ret[rand_val] = *stream_begin;
      }
      ++stream_begin;
  }
  return ret;
}
```





###　Compute a random permutation

生成一个随机的排列，每次从剩余集合中随机选择一个元素放置到当前位置。可使用之前的从离线采样函数，即从n个元素中随机抽取n个元素。



> std::iota
>
> Fills the range `[first, last)` with sequentially increasing values, starting with `value` and repetitively evaluating ++value.
>
> Equivalent operation:
>
> ```c++
> *(d_first)   = value;
> *(d_first+1) = ++value;
> *(d_first+2) = ++value;
> *(d_first+3) = ++value;
> ...
> ```



```c++
void RandomSampling(int k, vector<int> *A_ptr) {
  	// 离线采样
    vector<int> &A = *A_ptr;
    std::default_random_engine seed((std::random_device())());
    for (int i = 0; i < k; ++i) {
        std::swap(
                A[i],
                A[std::uniform_int_distribution<int>(i, static_cast<int>(A.size() - 1))(seed)]
                );
    }
    return;
}
vector<int> ComputeRandomPermutation(int n) {
  // TODO - you fill in here.
  vector<int> perm(n);
  // 生成序列
  std::iota(perm.begin(), perm.end(), 0);
  // 从n个采样n个，即随机打乱
  RandomSampling(perm.size(), &perm);
  return perm;
}
```







### Compute a random subset

这个有些类似与离线采样的那题，但是当k<<n时，大多数的元素都是未用到的，申请O(n)的空间有些浪费。这里使用hash table记录。

在离线采样方法中，数组中存放0~n-1的结果，每次交换两个元素。通过hash table，可以保存每次交换元素的下标。这样对交换的两个元素，共有四种情况(都在table内，只有一个在，都不在)



```c++
//申请O(n)空间
//Average running time:    1  s
//Median running time:   969 ms
vector<int> RandomSubset(int n, int k) {
  // TODO - you fill in here.
    vector<int> A(n);
    std::iota(A.begin(), A.end(), 0);
    std::default_random_engine seed((std::random_device())());

    for (int i = 0; i < k; ++i) {
        std::swap(
                A[i],
                A[std::uniform_int_distribution<int>(i, static_cast<int>(A.size() - 1))(seed)]
        );
    }
    return {A.begin(), A.begin() + k};
}

// Hash table

// Returns a random k-sized subset of {0, 1, ..., n - 1}.
vector<int> RandomSubset(int n, int k) {
  // TODO - you fill in here.
    std::default_random_engine seed((std::random_device())());
    std::unordered_map<int, int> changed_elements;
    for (int i = 0; i < k; ++i) {
        int rand_idx = std::uniform_int_distribution<int>(i, n - 1)(seed);
        auto ptr1 = changed_elements.find(i), ptr2 = changed_elements.find(rand_idx);

        if (ptr1 == changed_elements.end() && ptr2 == changed_elements.end()) {
            changed_elements[i] = rand_idx;
            changed_elements[rand_idx] = i;
        }
        else if (ptr1 == changed_elements.end() && ptr2 != changed_elements.end()) {
            changed_elements[i] = ptr2->second;
            ptr2->second = i;
        }
        else if (ptr1 != changed_elements.end() && ptr2 == changed_elements.end()) {
            changed_elements[rand_idx] = ptr1->second;
            ptr1->second = rand_idx;
        }
        else {
            std::swap(ptr1->second, ptr2->second);
        }
    }
    vector<int> ret;
    for (int i = 0; i < k; ++i) {
        ret.push_back(changed_elements[i]);
    }
    return ret;
}
```





### Generate nonuniform random numbers

按概率生成随机数。记得在做遗传算法的时候处理过这种问题，用饼图去累计概率。



```c++
int NonuniformRandomNumberGeneration(const vector<int>& values,
                                     const vector<double>& probabilities) {
  // TODO - you fill in here.
  std::default_random_engine seed((std::random_device())());
  double p = std::uniform_real_distribution<double> (0., 1.0)(seed);
  double con_sum = 0.;
  for (int i = 0; i < values.size(); ++i) {
      con_sum += probabilities[i];
      if (con_sum > p) {
          return values[i];
      }
  }
  return 0;
}
```





## Multidimensional arrays





### The Sudoku checker problem

判断一个未完成的数独盘是否是合法的。 我的做法比较粗暴，用3个集合分别检查3个约束是否满足。



```c++
// Check if a partially filled matrix has any conflicts.
bool IsValidSudoku(const vector<vector<int>>& partial_assignment) {
  // TODO - you fill in here.
  vector<std::unordered_set<int>> rows(9); //检测行冲突
  vector<std::unordered_set<int>> cols(9); //检测列冲突
  vector<std::unordered_set<int>> inner(9); //检测小9宫格冲突
  for (int r_idx = 0; r_idx < 9; ++r_idx) {
      for (int c_idx = 0; c_idx < 9; ++c_idx) {
          int c_val = partial_assignment[r_idx][c_idx];
          if (c_val == 0) {
              continue;
          }

          auto &c_row = rows[r_idx];
          if (c_row.find(c_val) != c_row.end()) {
              return false;
          }
          else {
              c_row.insert(c_val);
          }

          auto &c_col = cols[c_idx];
          if (c_col.find(c_val) != c_col.end()) {
              return false;
          }
          else {
              c_col.insert(c_val);
          }

          int inner_idx = (r_idx / 3) * 3 + c_idx / 3;
          auto &c_inner = inner[inner_idx];
          if (c_inner.find(c_val) != c_inner.end()) {
              return false;
          }
          else {
              c_inner.insert(c_val);
          }
      }
  }
  return true;
}
```





### Compute the spiral ordering of a 2D array

返回数组的螺旋序列。思路上是一层一层地对数组进行访问，最外圈访问完成后，该问题变成了相同形式，但规模更小的子问题。



这里刚开始时判断nextX和nextY时并没有考虑小于0的情况，但是也能通过测试样例，是因为在与`size()`相比较时，有符号的负值被转换为无符号，会满足第二个条件。当然在逻辑上是有漏洞的。

```c++
vector<int> MatrixInSpiralOrder(const vector<vector<int>>& square_matrix) {
  // TODO - you fill in here.
  // kShift 控制前进方向
  const vector<vector<int>> kShift = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
  int dir = 0, x = 0, y = 0;
  int nextX = 0, nextY = 0;
  vector<vector<int>> visited(square_matrix);
  vector<int> ret;
  for (int i = 0; i < square_matrix.size() * square_matrix.size(); ++i) {
      ret.push_back(square_matrix[x][y]);
      visited[x][y] = 0;
      nextX = x + kShift[dir][0];
      nextY = y + kShift[dir][1];
      if (nextX < 0 || nextX >= square_matrix.size() || nextY < 0 || nextY >= square_matrix.size() || visited[nextX][nextY] == 0) {
          dir = (dir + 1) % 4;
          nextX = x + kShift[dir][0];
          nextY = y + kShift[dir][1];
      }
      x = nextX;
      y = nextY;
  }
  return ret;
}
```





### Rotate a 2D array

将2D矩阵顺时针旋转90°。

按层处理，每层每次处理四个元素。即将每条边上对应位置的元素交换位置

```c++
void RotateMatrix(vector<vector<int>>* square_matrix_ptr) {
  // TODO - you fill in here.
  vector<vector<int>> &square_matrix = *square_matrix_ptr;
  const int mat_size = square_matrix.size() - 1;
  for (int i = 0; i < square_matrix.size() / 2; ++i) {
      for (int j = i; j < mat_size - i; ++j) {
          int temp1 = square_matrix[i][j]; // top element
          int temp2 = square_matrix[j][mat_size-i]; // right element
          int temp3 = square_matrix[mat_size-i][mat_size-j]; // bottom element
          int temp4 = square_matrix[mat_size-j][i]; // left element

          square_matrix[i][j] = temp4; // left2top
          square_matrix[j][mat_size-i] = temp1; //top2right
          square_matrix[mat_size-i][mat_size-j] = temp2; // right2bottom
          square_matrix[mat_size-j][i] = temp3; //bottom2left
      }
  }
  return;
}
```





### Compute rows in Pascal's Triangle

输出帕斯卡三角的前n行，直接模拟即可



```c++
vector<vector<int>> GeneratePascalTriangle(int num_rows) {
  // TODO - you fill in here.

  vector<vector<int>> ret = {{1}};
  if (num_rows == 0) {
      return {};
  }
  else if (num_rows == 1) {
      return ret;
  }
  for (int i = 1; i < num_rows; ++i) {
      vector<int> c_row;
      c_row.emplace_back(1);
      auto &last_row = ret[i-1];
      for (int j = 0; j < last_row.size() - 1; ++j) {
          c_row.push_back(last_row[j] + last_row[j+1]);
      }
      c_row.emplace_back(1);
      ret.emplace_back(c_row);
  }
  return ret;
}
```

