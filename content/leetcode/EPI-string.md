Title: EPI-String
Date: 2020-03-27 18:20
Modified: 2020-03-27 18:20
Category: LeetCode
Tags: EPI, c++
Slug: epi-code-string



很久很久以前，有人刷题不做记录，从Array刷到String，刷了几年还是在刷String。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还是在刷String。

## String



### String 的基本语法

```c++
//
.append("");
.push_back('');
.pop_back();
.insert(begin() + shift, "");
.substr(pos, len);
.compare("");

//
```





### Interconvert strings and integers

虽然这题的意思是要手动转换。。。但是有现成的封装📦为啥不用呢

```c++
string IntToString(int x) {
  // TODO - you fill in here.
  return std::to_string(x);
}
int StringToInt(const string& s) {
  // TODO - you fill in here.
  return std::stoi(s);
}
```





### Base conversion

进制间的相互转换，原理上倒是挺简单，写的时候犯浑了，将取余后的结果和字符进行比较。。。



```c++
string ConvertBase(const string& num_as_string, int b1, int b2) {
  // TODO - you fill in here.
  int start_idx = num_as_string[0] == '-' ? 1 : 0;
  bool neg = num_as_string[0] == '-';
  int num = 0, len = num_as_string.size() - 1;
  // 转为10进制
  for (; start_idx < num_as_string.size(); ++start_idx) {
      char ch = num_as_string[start_idx];
      int c_val;
      if (ch >= '0' && ch <= '9') {
          c_val = ch - '0';
      }
      else {
          c_val = ch - 'A' + 10;
      }
      num *= b1;
      num += c_val;
  }
  if (num == 0) {
      return "0";
  }
//  string ret = std::to_string(num) + ";";
  //转为b2进制
  string ret;
  while (num) {
      int mod = num % b2;
      if (0 <= mod && mod <= 9) {
          ret.push_back('0'+mod);
      }
      else {
          ret.push_back('A' + mod - 10);
      }
      num /= b2;
  }
  if (neg) {
      ret.push_back('-');
  }
  return {ret.rbegin(), ret.rend()};
}
```



### Compute the spreadsheet column encoding

将表格的列名‘AABEZ’转换为整型数值。等价于进制转换。



```c++
int SSDecodeColID(const string& col) {
  // TODO - you fill in here.
  int id = 0;
  for (auto &code : col) {
       id *= 26;
       id += code - 'A' + 1;
  }
  return id;
}
```





### Replace and remove

将字符串中的‘b’删除，将‘a'换成’dd‘。

题目保证给出s的大小满足要求，为了不开辟新空间，第一遍正向将’b‘删除，同时统计’a‘的个数，第二部反向将元素向后移动。



```c++
int ReplaceAndRemove(int size, char s[]) {
  // TODO - you fill in here.
  int a_cnt = 0;
  int write_idx = 0, last_idx = 0;
  while(last_idx < size) {
      if (s[last_idx] == 'b') {
          ++last_idx;
          continue;
      }
      if (s[last_idx] == 'a') {
          ++a_cnt;
      }
      s[write_idx++] = s[last_idx++];
  }

  int back_write_idx = write_idx + a_cnt-1, back_idx = write_idx - 1;
  int ret_cnt = back_write_idx+1;
  while (back_write_idx >= 0) {
      if (s[back_idx] == 'a') {
          s[back_write_idx--] = 'd';
          s[back_write_idx--] = 'd';
          --back_idx;
      }
      else {
          s[back_write_idx--] = s[back_idx--];
      }
  }
  return ret_cnt;
}
```



### Test palindromicity

>  palindromic string：移除非字母数字的字符，不考虑大小写，剩下的左右对称。



```c++
bool IsPalindrome(const string& s) {
  // TODO - you fill in here.
  int l_idx = 0, r_idx = s.size() - 1;
  while (l_idx < r_idx) {
      while(l_idx < r_idx && !std::isalnum(s[l_idx])) {
          ++l_idx;
      }
      while (r_idx > l_idx && !std::isalnum(s[r_idx])) {
          --r_idx;
      }
      if (std::tolower(s[l_idx++]) != std::tolower(s[r_idx--])) {
          return false;
      }
  }
  return true;
}
```



### Reverse all the words in a sentence

将句子中的单词逆序排列，这里是将每个单词提取出来，逆序后填回原字符串， 空间复杂度为O(n)。



EPI给出了一个空间复杂度O(1)的解法：先将字符串翻转，再对每个单词进行翻转。



```c++
//EPI solution
void ReverseWords(string* s) {
    std::reverse(s->begin(), s->end());
    size_t start = 0, end;
    while ((end = s->find(' ', start)) != string::npos) {
        std::reverse(s->begin()+start, s->begin()+end);
        start = end + 1;
    }
    std::reverse(s->begin() + start, s->end());
    return;
}

void ReverseWords(string* s) {
  // TODO - you fill in here.
  string &ss = *s;
  int s_len = (*s).size();
  std::vector<string> words;
  int word_st_idx = 0, word_end_idx = 0;
  while (word_end_idx < s_len) {
      // find next word
      while (word_end_idx < s_len && ss[word_end_idx] != ' ') {
          ++word_end_idx;
      }
      words.push_back(ss.substr(word_st_idx, word_end_idx-word_st_idx));
      // deal with space
      if (word_end_idx < s_len && ss[word_end_idx] == ' ') {
          words.push_back(" ");
      }
      // move idx to next word
      ++word_end_idx;
      word_st_idx = word_end_idx;
  }
  // fill words reversely
  int s_idx = 0;
  for (int w_idx = words.size() - 1; w_idx >= 0; --w_idx) {
      for (int idx_in_word = 0; idx_in_word < words[w_idx].size(); ++idx_in_word) {
          ss[s_idx++] = words[w_idx][idx_in_word];
      }
  }
  return;
}


```





### The look-and-say problem

>  look-and-say序列：<1, 11, 21, 1211,...> 

对前一个序列值，读出其有x个y值，写作xy。

模拟即可。

> std::to_string 的参数类型均为数值类型

```c++
string LookAndSay(int n) {
  // TODO - you fill in here.
  string start_str = "1";
  for (int i = 1; i < n; ++i) {
      int iter_idx = 0;
      string c_str;
      while (iter_idx < start_str.size()) {
          char c_val = start_str[iter_idx];
          int cnt = 1;
          while (iter_idx < start_str.size() - 1 && start_str[iter_idx] == start_str[iter_idx+1]) {
              ++iter_idx;
              ++cnt;
          }
          ++iter_idx;
          c_str += std::to_string(cnt) + std::to_string(c_val-'0');
      }
      start_str = c_str;
  }
  return start_str;
}
```





### Convert from Roman to decimal

将罗马数字转换为10进制，难度可能在理解规则上。

```c++
const std::map<char, int> mp = {
        {'I', 1},
        {'V', 5},
        {'X', 10},
        {'L', 50},
        {'C', 100},
        {'D', 500},
        {'M',1000}
};
int RomanToInteger(const string& s) {
  // TODO - you fill in here.
  int cnt = 0;
  for (int i = 0; i < s.size(); ++i) {
      char ch = s[i];
      if (i > 0) {
        	// 处理exception
          if ((ch == 'V' || ch == 'X') && s[i-1] == 'I') {
              cnt -= 1 * 2;
          }
          if ((ch == 'L' || ch == 'C') && s[i-1] == 'X') {
              cnt -= 10 * 2;
          }
          if ((ch == 'D' || ch == 'M') && s[i-1] == 'C') {
              cnt -= 100 * 2;
          }
      }
      cnt += mp.at(ch);
  }
  return cnt;
}
```





### Compute all valid IP addresses

计算一个无分隔符的ip字符串的所有可能形式。

遍历3个分隔符的位置，判断每个区间的字串是否合法。 需要处理边界情况，如整个串都是不合法的。



```c++
// 判断ip区间十分合规
inline bool isValid(const string& s){
    if (s.size() > 3){
        return false;
    }
    if (s.size() > 1 && s[0] == '0') {
        return false;
    }
    int val = std::stoi(s);
    return val <= 255;
}

vector<string> GetValidIpAddress(const string& s) {
  // TODO - you fill in here.
  if (s.size() < 4) {
      return {};
  }
  vector<string> ret;
  // 遍历3个点的位置
  for (int first_dot = 0; first_dot < s.size()-3; ++first_dot) {
      string f_part = s.substr(0, first_dot+1);
      if (!isValid(f_part)) continue;
      for (int sec_dot = first_dot+1; sec_dot < s.size() - 2; ++sec_dot) {
          string s_part = s.substr(first_dot+1, sec_dot-first_dot);
          if (!isValid(s_part)) continue;
          for (int th_dot = sec_dot + 1; th_dot < s.size() - 1; ++th_dot) {
              string t_part = s.substr(sec_dot+1, th_dot-sec_dot);
              if (!isValid(t_part)) continue;
              string fo_part = s.substr(th_dot+1, s.size() - th_dot);
              if (!isValid(fo_part)) continue;

              ret.emplace_back(f_part + "." + s_part + "." + t_part + "." + fo_part);
          }
      }
  }
  return ret;
}
```





### Write a string sinusoidally

输出字符串的蛇皮走位。 将字符串展示成sin函数状，然后按行输出。

模拟的做法是申请3个数组，依次往数组内填充元素。这样的做法太浪费空间，sin函数形状也是有规律的，直接按照下标拼接结果即可。



```c++
string SnakeString(const string& s) {
  // TODO - you fill in here.
  string ret;
  for (int i = 1; i < s.size(); i+=4) {
      ret.push_back(s[i]);
  }
  for (int i = 0; i < s.size(); i+=2) {
      ret.push_back(s[i]);
  }
  for (int i = 3; i < s.size(); i+=4) {
      ret.push_back(s[i]);
  }
  return ret;
}
```





### Implement run-length encoding

RLE编码在kaggle比赛中也见过，即将`bbbccd`表示为`3b2c1d`。类似与之前的lookup-and-say。

有个需要注意的地方就是计数会是大于1位数的，在编码和解码的时候都需要注意这个。

```c++
string Decoding(const string &s) {
  // TODO - you fill in here.
  string ret;
  for (size_t i = 0; i < s.size();) {
      size_t ed = i;
      // ed 为字符位置
      while (std::isdigit(s[ed])) {
          ++ed;
      }
      int cnt = std::stoi(s.substr(i, ed-i));
      char ch = s[ed];
      while(cnt--) {
          ret.push_back(ch);
      }
      i = ed+1;
  }
  return ret;
}
string Encoding(const string &s) {
  // TODO - you fill in here.
  string ret;
  size_t start = 0;
  while (start < s.size()) {
      int cnt = 1;
      char ch = s[start];
      while (start < s.size() - 1 && s[start] == s[start+1]) {
          ++cnt;
          ++start;
      }
      ret += std::to_string(cnt);
      ret.push_back(ch);
      ++start;
  }
  return ret;
}
```





### Find the first occurrence of a substring

子串查找，上KMP。可惜忘光了。。。



有3种线性时间的搜索算法：KMP、BM、RK。其中RK是最简单，最容易实现的。

RK算法基于滚动的hash，当s与t的子串hash值相同时，他们有可能是匹配的，进一步验证其是否真正匹配。滚动的hash匹配避免了匹配失败时的多次回溯。

```c++
int RabinKarp(const string &t, const string &s) {
  // TODO - you fill in here.
  if (t.size() < s.size()) {
      return -1;
  }
  const int kBase = 26;
  int t_hash = 0, s_hash = 0;
  int power_s = 1; // kBase ^|s|
  for (int i = 0; i < s.size(); ++i) {
      power_s = i ? power_s * kBase : 1;
      t_hash = t_hash * kBase + t[i] - '0';
      s_hash = s_hash * kBase + s[i] - '0';
  }

  for (int i = s.size(); i < t.size(); ++i) {
      // 匹配成功
      if (t_hash == s_hash && t.compare(i - s.size(), s.size(), s) == 0) {
          return i - s.size();
      }

      // 滚动更新hash
      t_hash -= (t[i-s.size()] - '0') * power_s;
      t_hash = t_hash * kBase + t[i] - '0';
  }
    if (t_hash == s_hash && t.compare(t.size() - s.size(), s.size(), s) == 0) {
        return t.size() - s.size();
    }
  return -1;
}
```