Title: EPI-Hash Tables
Date: 2020-04-17 19:20
Modified: 2020-04-17 20:20
Category: LeetCode
Tags: EPI, cpp
Slug: epi-Hash-Tables

很久很久以前，有人刷题不做记录，没刷过Hash Tables。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还没刷过Hash Tables。

[TOC]

## Hash Tables





### Boot camp

两个例子：哈希表的应用，哈希表class的设计



#### An application of hash tables

判断Anagrams



#### Design of a hashable class

假设有表示联络人的`class`，被存储在序列中。为了简单起见，每个联络人的信息只包含一系列string，包含相同的string set的联络人被视为同一个项目。

设计一个hash function 合并重复的联络人信息。

下面用到了两个未了解过的知识：

> ### std::hash
>
> ```c++
> template< class Key >
> struct hash
> ```
>
> The *enabled* specializations of the (since C++17) hash template defines a function object that implements a [hash function](https://en.wikipedia.org/wiki/Hash_function). Instances of this function object satisfy [*Hash*](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/named_req/Hash.html). In particular, they define an operator() const that:
>
> 1. Accepts a single parameter of type `Key`.
>
> 2. Returns a value of type [std::size_t](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/types/size_t.html) that represents the hash value of the parameter.
>
> 3. Does not throw exceptions when called.
>
> 4. For two parameters `k1` and `k2` that are equal, std::hash<Key>()(k1) == std::hash<Key>()(k2).
>
> 5. For two different parameters `k1` and `k2` that are not equal, the probability that std::hash<Key>()(k1) == std::hash<Key>()(k2) should be very small, approaching 1.0/[std::numeric_limits](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/types/numeric_limits.html)<[std::size_t](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/types/size_t.html)>::max().



unordered_set 第二个key_word指定所用的hash函数。

> ### std::unordered_set
>
> ```c++
> template<
>     class Key,
>     class Hash = std::hash<Key>,
>     class KeyEqual = std::equal_to<Key>,
>     class Allocator = std::allocator<Key>
> > class unordered_set;
> ```





```c++
struct ContactList {
  bool operator==(const ContactList& that) const {
    return unordered_set<string>(names.begin(), names.end()) == unordered_set<string>(that.names.begin(), that.names.end());
  }
  vector<string> name;
};

struct HashContactList {
  size_t operator()(const ContactList& contacts) const {
    size_t hash_code = 0;
    for (const string& name: unordered_set<string>(contracts.names.begin(), contracts.names.end())) {
      hash_code ^= hash<string>()(name);
    }
  }
}

vector<ContactList> MergeContractLists(cont vector<ContactList>& contracts) {
  unordered_set<ContactList, HashContractList> unique_contracts(contracts.begin(), contracts.end());
  
  return {unique_contracts.begin(), unique_contracts.end()};
}
```



### 库函数

hash table

```c++
// 都不允许键重复
// unordered_set 存储k
.insert(val);  //return a pair of iterator and boolean denoting whether the insertion took place.
.erase(val); // 
.find(val); // return iterator or end()
.size();
.count(val);
.contains(val); //c++20

// unordered_map 存储k-v

.insert({k, v});
.emplace({k, v});
.earse(k);
.find(k);
.size();


// functional header
hash<typename>()(val);
//int, bool, string, unique_ptr, shared_ptr, etc.
```





### FindAnagrams

```c++
vector<vector<string>> FindAnagrams(const vector<string>& dictionary) {
  // TODO - you fill in here.
  std::unordered_map<string, vector<string>> sorted_string_to_anagrams;
  for (const string& s: dictionary) {
      string sorted_s(s);
      std::sort(sorted_s.begin(), sorted_s.end());
      sorted_string_to_anagrams[sorted_s].emplace_back(s);
  }

  vector<vector<string>> ret;
  for (const auto& p: sorted_string_to_anagrams) {
      if (p.second.size() >= 2) {
          ret.emplace_back(p.second);
      }
  }
  return ret;
}
```





### Test for palindromic permutations

测试一个字符串能否permute成回文字符串。

A palindrome is a string that reads the same forwards and backwards, e.g., "level", "rotator", and "foobaraboof".

Write a program to test whether the letters forming a string can be permuted to form a palindrome. For example, "edified" can be permuted to form "deified".



直接对字母计数就可以( 难以想象之前不太会用C++的counter)

```c++
bool CanFormPalindrome(const string& s) {
  // TODO - you fill in here.
  std::unordered_map<char, int> cnt;
  for (const char& ch: s) {
      ++cnt[ch];
  }
  int odd_cnt = 0;
  for (const auto& p: cnt) {
      if (p.second % 2 != 0) {
          ++odd_cnt;
      }
      if (odd_cnt > 1) {
          return false;
      }
  }
  return true;
}
```





### Is an anonymous letter constructible?

Write a program which takes text for an anonymous letter and text for a magazine and determines if it is possible to write the anonymous letter using the magazine. The anonymous letter can be written using the magazine if for each character in the anonymous letter, the number of times it appears in the anonymous letter is no more than the number of times it appears in the magazine.

也是计数后相减。

```c++
bool IsLetterConstructibleFromMagazine(const string& letter_text,
                                       const string& magazine_text) {
  // TODO - you fill in here.
  std::unordered_map<char, int> cnt;
  for (const char& ch: magazine_text) {
      ++cnt[ch];
  }
  for (const char& ch: letter_text) {
      if (cnt.find(ch) == cnt.end()) {
          return false;
      }
      --cnt[ch];
      if (cnt[ch] < 0) {
          return false;
      }
  }
  return true;
}
```



...太天真，上面的做法虽然是对的，但是时间复杂度会高一些。如果magazine_text的内容很长，第一次遍历会消耗很多时间。改为先扫描letter_text， 这样就不用将magazine_text的内容也全部过一遍。

```c++
bool IsLetterConstructibleFromMagazine(const string& letter_text,
                                       const string& magazine_text) {
  // TODO - you fill in here.
  std::unordered_map<char, int> cnt;
  for (const char& ch: letter_text) {
      ++cnt[ch];
  }
  for (const char& ch: magazine_text) {
      auto iter = cnt.find(ch);
      if (iter != cnt.end()) {
          --iter->second;
          if (iter->second == 0) {
              cnt.erase(iter);
              if (cnt.empty()) {
                  break;
              }
          }

      }
  }
  return cnt.empty();
}
```



### Implement an ISBN cache

The International Standard Book Number (ISBN) is a unique commercial book iden- tifier. It is a string of length 10. The first 9 characters are digits; the last character is a check character. The check character is the sum of the first 9 digits, modulo 11, with 10 represented by 'X'. (Modern ISBNs use 13 digits, and the check digit is taken modulo 10; this problem is concerned with 10-digit ISBNs.)

Create a cache for looking up prices of books identified by their ISBN. You implement lookup, insert, and remove methods. Use the Least Recently Used (LRU) policy for cache eviction. If an ISBN is already present, insert should not change the price, but it should update that entry to be the most recently used entry. Lookup should also update that entry to be the most recently used entry.

Hint: Amortize the cost of deletion. Alternatively, use an auxiliary data structure.



这个没看懂Lookup跟LRU什么关系。

看了解析之后才明白这个是要干什么：缓存的大小是固定的，当插入的数量大于缓存的大小时，根据缓存策略剔除一个元素。



使用list维护LRU队列，list存储isbn信息。list能够满足快速地删除，头尾插入。同时使用hashtable记录isbn在队列中的位置及price，避免对list的顺序查找。





```c++
#include <vector>
#include <unordered_map>
#include <list>

class LruCache {
 public:
  LruCache(size_t capacity) {
      this->capacity = capacity;
  }
  int Lookup(int isbn) {
    // TODO - you fill in here.
    auto iter = isbn_price_table_.find(isbn);
    if (iter == isbn_price_table_.end()) {
        return -1;
    }
    int ret_val = iter->second.second;
    MoveFront(isbn, iter);
    return ret_val;
  }
  void Insert(int isbn, int price) {
    // TODO - you fill in here.
    auto iter = isbn_price_table_.find(isbn);
    if (iter == isbn_price_table_.end()) {
        // 未找到
        if (isbn_price_table_.size() == capacity) {
            // 需要替换一个出去
            int subs_isbn = lru_queue_.back();
            isbn_price_table_.erase(subs_isbn);
            lru_queue_.pop_back();

        }
        lru_queue_.emplace_front(isbn);
        isbn_price_table_.insert({isbn, {lru_queue_.begin(), price}});
    } else {
        MoveFront(isbn, iter); //找到项目，更新lru
    }
  }
  bool Erase(int isbn) {
    // TODO - you fill in here.
    auto iter = isbn_price_table_.find(isbn);
    if (iter == isbn_price_table_.end()) {
        return false;
    }
    lru_queue_.erase(iter->second.first);
    isbn_price_table_.erase(iter);
    return true;
  }

private:
    typedef std::unordered_map<int, std::pair<std::list<int>::iterator, int>> Table;
    Table isbn_price_table_;
    std::list<int> lru_queue_;
    size_t capacity;

    void MoveFront(int isbn, const Table::iterator& it) {
        lru_queue_.erase(it->second.first);
        lru_queue_.emplace_front(isbn);
        it->second.first = lru_queue_.begin();
    }
};
```





### Compute the LCA, optimizing for close ancestors



Problem 10.4 on Page 155 is concerned with computing the LCA in a binary tree with parent pointers in time proportional to the height of the tree. The algorithm presented in Solution 10.4 on Page 155 entails traversing all the way to the root even if the nodes whose LCA is being computed are very close to their LCA.

Design an algorithm for computing the LCA of two nodes in a binary tree. The algorithm's time complexity should depend only on the distance from the nodes to the LCA.

Hint: Focus on the extreme case described in the problem introduction.



之前有个计算LCA的题目，即使两个结点的LCA相聚很近，仍然需要回溯到根结点计算结点的高度。 

设计一个算法，其时间复杂度仅取决于目标结点与LCA的距离。



之前的题目因为没法快速地查找已访问的结点，所以需要记录结点的高度。有了hashtable后，可以在$O(1)$的时间内查找已访问元素.  因此在向上访问的同时记录历史信息, 用set做查找.

```c++
BinaryTreeNode<int>* Lca(const unique_ptr<BinaryTreeNode<int>>& node0,
                         const unique_ptr<BinaryTreeNode<int>>& node1) {
  // TODO - you fill in here.
  std::unordered_set<BinaryTreeNode<int>*> node_set;
  BinaryTreeNode<int> *p0 = node0.get(), *p1 = node1.get();
  while (p0 && p1) {
      auto iter = node_set.find(p0);
      if (iter != node_set.end()) {
          return *iter;
      }
      node_set.insert(p0);
      p0 = p0->parent;

      iter = node_set.find(p1);
      if (iter != node_set.end()) {
          return *iter;
      }
      node_set.insert(p1);
      p1 = p1->parent;
  }
  auto *residual = p0 == nullptr ? p1 : p0;
  while (residual != nullptr) {
      auto iter = node_set.find(residual);
      if (iter != node_set.end()) {
          return *iter;
      }
      residual = residual->parent;
  }
  return nullptr;
}
```



### Find the nearest repeated entries in an array

无题



### Find the smallest subarray covering all values

When you type keywords in a search engine , the search engine will return results , and each result contains a digest of the web page , i .e. , a highlighting within that page of the keywords that you searched for. For example , a search for the keywords " Union " and " save " on a page with the text of the Emancipation Proclamation should return the result shown in Figure 13.1.

Write a program which takes an array of strings and a set of strings , and return the indices of the starting and ending index of a shortest subarray of the given array that " covers " the set , i .e. , contains all strings in the set.



朴素的想法就是找到所有的subarray, 去比对是否满足要求, 时间复杂度应该是$O(n^3)$.

通过使用hashtable能够降低比对时的时间复杂度,将其降为$O(n^2)$.

实际上, 考虑到这个问题的特性, 时间复杂度可以更进一步降低为$O(n)$. subarray内有效的长度就是keyword的数量, 查找的过程可以视为在paragraph上的一个变长滑窗查找.

假设当前已经找到一个subarray, 那么接下来的查找只会向右进行, 而不必再考虑前面的组合. 比如将left idx调整到下一个关键词的位置, 将滑窗向右滑动.



```c++
struct Subarray {
  int start, end;
};

Subarray FindSmallestSubarrayCoveringSet(
    const vector<string> &paragraph, const unordered_set<string> &keywords) {
  // TODO - you fill in here.
  // 记录当前cover的关键字
  std::unordered_map<string, int> keywords_to_cover;
  for (auto &k: keywords) {
      ++keywords_to_cover[k];
  }
  int remain_to_cover = keywords_to_cover.size();

  Subarray result = {-1, -1};
  for (int left = 0, right = 0; right < paragraph.size(); ++right) {
      auto r_word = paragraph[right];
      //keywords 中的同一个单词可能会在paragraph中出现多次
      if (keywords.count(r_word) && --keywords_to_cover[r_word]>=0) {
          --remain_to_cover;
      }
      // remain_to_cover == 0 意味着当前已经找到一个满足条件的区间，将left右移至下一个关键词位置。
      while (remain_to_cover == 0) {
          if (result.start == -1 || right - left < result.end - result.start) {
              result = {left, right};
          }
          if (keywords.count(paragraph[left]) && ++keywords_to_cover[paragraph[left]] > 0){
              ++remain_to_cover;
          }
          ++left;
      }
  }
  return result;
}
```



### Find smallest subarray sequentially covering all values

In Problem 13.7 on Page 216 we did not differentiate between the order in which

keywords appeared . If the digest has to include the keywords in the order in which they appear in the search textbox , we may get a different digest . For example , for the search keywords " Union " and " save " , in that order , the digest would be " Union , and is not either to save " .

Write a program that takes two arrays of strings , and return the indices of the start ing and ending index of a shortest subarray of the first array ( the " paragraph " array ) that " sequentially covers " , i .e. , contains all the strings in the second array ( the " keywords " array ) , in the order in which they appear in the keywords array . You can assume all keywords are distinct. For example , let the paragraph array be ( apple , banana , cat , apple ) , and the keywords array be ( banana , apple ) . The para graph subarray starting at index 0 and ending at index 1 does not fulfill the specification , even though it contains all the keywords , since they do not appear in the specified order. On the other hand , the subarray starting at index 1 and ending at index 3 does fulfill the specification .

Hint: For each index in the paragraph array , compute the shortest subarray ending at that index which fulfills the specification .



感觉这个做法有点像DP，但是目前又不太能确定...



跟前一题有些相似，这里多了顺序的要求。需要一个table记录keyword的坐标，用于表示其出现的顺序。还需要设计一个table用于记录某个keyword上次出现的位置及以该关键字为结尾的subarray的长度。



```c++
struct Subarray {
  // Represent subarray by starting and ending indices, inclusive.
  int start, end;
};

Subarray FindSmallestSequentiallyCoveringSubset(
    const vector<string>& paragraph, const vector<string>& keywords) {
  // TODO - you fill in here.
  // 记录keyword的位置
  std::unordered_map<string, int> keyword_to_idx;
  for (int i = 0; i < keywords.size(); ++i) {
//      keyword_to_idx[keywords[i]] = i;
      keyword_to_idx.emplace(keywords[i] , i);
  }

  // 少打一个,  调了半天...
  vector<int> key_latest_occurrence(keywords.size(), -1);

  vector<int> shortest_subarray(keywords.size(), std::numeric_limits<int>::max());
  Subarray ret = {-1, -1};
  int shortest_array_len = std::numeric_limits<int>::max();
  for (int i = 0; i < paragraph.size(); ++i) {
      if (keyword_to_idx.count(paragraph[i])) {
          int key_idx = keyword_to_idx[paragraph[i]];
          if (key_idx == 0) {
              // 第一个keyword
              shortest_subarray[key_idx] = 1;
          } else if (shortest_subarray[key_idx-1] != std::numeric_limits<int>::max()) {

              shortest_subarray[key_idx] = shortest_subarray[key_idx-1] + i - key_latest_occurrence[key_idx-1];
          }
          key_latest_occurrence[key_idx] = i;

          if (key_idx == keywords.size() - 1 && shortest_array_len > shortest_subarray.back()) {
              shortest_array_len = shortest_subarray.back();
              ret = {i - shortest_subarray.back() + 1, i};
          }
      }
  }
  return ret;
}
```





### Find the longest subarray with distinct entries

Write a program that takes an array and returns the length of a longest subarray with the property that all its elements are distinct. For example , if the array is <f,s,f,e,t,w,e,n,w,e>then a longest subarray all of whose elements are distinct is <s, f, e, t, w>

Hint: What should you do if the subarray from indices i to j satisfies the property , but the subarray from i to j + 1 does not?



这题很像之前的Find the smallest subarray covering all values，要使用变长滑动窗口（或者说是双指针）。

假设当前滑动窗口中无重复的元素，当要处理下一个元素a时，如果该元素在窗口中不存在，直接将其加入窗口。如果这个元素存在过，那么需要收缩窗口的左侧。 左侧需要向右滑动到已经出现的a的右侧，这样窗口中又不会包含重复的元素了。

在这个过程中需要记录元素曾经出现过的位置。





```c++
int LongestSubarrayWithDistinctEntries(const vector<int>& A) {
  // TODO - you fill in here.
  std::unordered_map<int, int> last_appearance; //记录元素上次出现的位置
  int longest_array_start_idx = 0, result = 0;
  for (int i = 0; i < A.size(); ++i) {
      auto insert_ret = last_appearance.insert({A[i], i});
      if (!insert_ret.second) {  // 插入不成功, 说明A[i]之前出现过
          int prev_idx = insert_ret.first->second;
          if (prev_idx >= longest_array_start_idx) { // A[i] 在滑窗内
              longest_array_start_idx = prev_idx + 1;
          }
          insert_ret.first->second = i; // 更新位置
      }
      result = std::max(result, i - longest_array_start_idx + 1);
  }
  return result;
}
```



### Find the length of a longest contained interval

Write a program which takes as input a set of integers represented by an array , and returns the size of a largest subset of integers in the array having the property that if two integers are in the subset , then so are all integers between them. For example , if the input is ( 3 , - 2 , 7 , 9, 8, 1 , 2 , 0 , - 1 , 5 , 8 ) , the largest such subset is { - 2 ,- 1 , 0 , 1 , 2 , 3 ) , so you should return 6.

Hint Do you really need a total ordering on the input ?



要找到一个包含连续区间内所有整数值的集合。之前的滑窗法没法直接套用到这里， 因为元素处在不同的位置并不影响最终的结果。

对元素直接进行排序也是可以的，只是没太必要，这里并不需要元素的顺序信息。

为了对元素进行快速查找，将元素全部保持到set中。然后每次选择一个元素，向上向下扩张，将访问过的元素从set中剔除(如果是连续区间，在扩张的过程中一定会被访问到)。

这样算法的时间复杂度为$O(n)$。

```c++
int LongestContainedRange(const vector<int>& A) {
  // TODO - you fill in here.
  std::unordered_set<int> filter(A.begin(), A.end());
  int ret = 0;
  while (!filter.empty()) {
      int c_val = *filter.begin();
      filter.erase(c_val);
      int c_length = 1, bias = 1;
      while(filter.count(c_val+bias)) {
          filter.erase(c_val + bias); // 剔除已经访问过的元素
          ++bias;
          ++c_length;
      }
      bias = -1;
      while (filter.count(c_val + bias)) {
          filter.erase(c_val + bias);
          --bias;
          ++c_length;
      }
      ret = std::max(ret, c_length);
  }
  return ret;
}
```





### Compute all string decompositions

This concerned taking a string ( the " sentence " string ) and a set of strings ( the " words " ) , and finding the substrings of the sentence which are the concatenation of all the words ( in any order ) . For example , if the sentence string is " amanaplanacanal " and the set of words is { " can " , " apl " , " ana " }, " aplanacan " is a substring of the sentence that is the concatenation of all words.

Write as a program which takes input a string ( the " sentence " ) and an array of strings ( the " words " ) , and returns the starting indices of substrings of the sentence string which are the concatenation of all the strings in the words array . Each string must appear exactly once , and their ordering is immaterial. Assume all strings in the words array have equal length . It is possible for the words array to contain duplicates .

Hint: Exploit the fact that the words have the same length .



要在string中找到由words任意顺序组成的substring， 返回substring的起始位置。

题目中给出了words具有相同的长度，就避免了在string中试探合理的word。



方法的时间复杂度为$O(Nmn)$. N是string的长度, m是单词的数量,n是单词的长度.

```c++
bool FindAllSubstringsHelper(const string& s, std::unordered_map<string, int> word_cnt, int st_idx, int word_len, int num_words) {
    int nb = 0;
    for (int i = st_idx; nb < num_words;) {
        string c_sub = s.substr(i, word_len);
        auto iter = word_cnt.find(c_sub);
        if (iter == word_cnt.end()) {
            return false; //不匹配
        }
        if (--(iter->second) < 0) {
            return false; // 出现过多次
        }
        ++nb;
        i = st_idx + nb * word_len;
    }
    return true;
}
vector<int> FindAllSubstrings(const string& s, const vector<string>& words) {
  // TODO - you fill in here.
  std::unordered_map<string, int> word_cnt;
  for (auto &each: words) {
      ++word_cnt[each];
  }
  int word_len = words[0].size();
  vector<int> ret;
  // 下面的条件是 <=
  for (int i = 0; i + word_len * words.size() <= s.size(); ++i) {
      if (FindAllSubstringsHelper(s, word_cnt, i, word_len, words.size())) {
          ret.emplace_back(i);
      }
  }

  return ret;
}
```





### Test the Collatz conjecture

The Collatz conjecture is the following : Take any natural number. If it is odd , triple it and add one ; if it is even , halve it . Repeat the process indefinitely . No matter what number you begin with , you will eventually arrive at 1 .

As an example , if we start with 11 we get the sequence 11 , 34 , 17 , 52 , 26 , 13 , 40 , 20 , 10 , 5 , 16 , 8, 4 , 2 , 1 . Despite intense efforts , the Collatz conjecture has not been proved or disproved .

Suppose you were given the task of checking the Collatz conjecture for the first billion integers . A direct approach would be to compute the convergence sequence for each number in this set.

Test the Collatz conjecture for the first n positive integers

Hint How would you efficiently check the conjecture for n assuming it holds for all m < n?



之前在leetcode上见过有类似的题目，直接利用数学定理的真伪返回结果。对于这题也是类似的，既然这个定理没有被证伪，那么对于目前已知的数肯定都是对的，直接返回true就好了。

```c++
bool TestCollatzConjecture(int n) {
  // TODO - you fill in here.
  return true;
}
```



对于不那么抖机灵的做法，用一个set去测试生成的序列是否进入循环，同时数值类型需要改为long以避免上溢。

时间复杂度自然是没法分析了💇

```c++
bool TestCollatzConjecture(int n) {
  // TODO - you fill in here.
  std::unordered_set<long> table;
  for (int i = 1; i <= n; ++i) {
      long c_val = i;
      std::unordered_set<long> search_path;
      while (c_val != 1) {
          if (table.find(c_val) != table.end()) {
              // 当前序列已经存在过
              break;
          }
          if (search_path.find(c_val) != search_path.end()) {
              return false; // 序列进入循环， 证伪
          }
          search_path.insert(c_val);
          if (c_val % 2 == 0) {
              c_val /= 2;
          } else {
              c_val = c_val * 3 + 1;
          }
      }
      table.insert(search_path.begin(), search_path.end()); //更新搜索序列
  }
  return true;
}
```