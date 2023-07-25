Title: EPI-Stacks and Queues
Date: 2020-03-31 18:20
Modified: 2020-04-05 18:20
Category: LeetCode
Tags: EPI, cpp
Slug: epi-stacks-and-queues

[TOC]

很久很久以前，有人刷题不做记录，从Array刷到Stacks and Queues，刷了几年还是在刷Stacks and Queues。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还是在刷Stacks and Queues。



## Stacks

### 基本语法

```c++
.push(val);
.top();
.pop(); // does not return
.empty();

```




### Implement a stack with max API

第一时间觉得蛮简单的，记录个max就成了。问题是max元素pop出去之后就不存在了。

将标准库自带的`stack`再封装一层，同时保存当前栈中的最大元素。

```c++
class Stack {
 public:
  bool Empty() const {
    // TODO - you fill in here.
    return element_with_max_cached_.empty();
  }
  int Max() const {
    // TODO - you fill in here.
    if (Empty()) {
        throw length_error("MAX(): empty stack");
    }
    return element_with_max_cached_.top().c_max;
  }
  int Pop() {
    // TODO - you fill in here.
    if (Empty()) {
        throw length_error("Pop(): empty stack");
    }
    int pop_elem = element_with_max_cached_.top().element;
    element_with_max_cached_.pop();
    return pop_elem;
  }
  void Push(int x) {
    // TODO - you fill in here.
    int max_val;
    if (Empty()) {
        max_val = x;
    }
    else {
        max_val = std::max(element_with_max_cached_.top().c_max, x);
    }
    element_with_max_cached_.push(ElementWithMaxCached{x, max_val});
    return;
  }
private:
    struct ElementWithMaxCached {
      int element;
      int c_max;
  };
  std::stack<ElementWithMaxCached> element_with_max_cached_;
};
```



### Evaluate RPN expressions



逆波兰表达式，思路上还是比较简单的，就是太久不写手生。

> getline的一个函数形式是
>
> template< class CharT, class Traits, class Allocator >
> std::basic_istream<CharT,Traits>& getline( std::basic_istream<CharT,Traits>&& input,
>                                          								  std::basic_string<CharT,Traits,Allocator>& str,
>                                            								CharT delim );
>
> 其中第3个参数指定line中的delimiter，默认为 '\n'

```c++
int Evaluate(const string& expression) {
  // TODO - you fill in here.
  std::stack<int> intermediate_result;
  std::stringstream ss(expression);
  std::string token;
  const char kDelimiter = ',';
  while (getline(ss, token, kDelimiter)) {
      if (token == "+" || token == "-" || token == "*" || token == "/") {
        // 注意pop出x 和 y的顺序
          const int y = intermediate_result.top();
          intermediate_result.pop();
          const int x = intermediate_result.top();
          intermediate_result.pop();
          switch (token.front()) {
              case '+':
                  intermediate_result.emplace(x + y);
                  break;
              case '-':
                  intermediate_result.emplace(x - y);
                  break;
              case '*':
                  intermediate_result.emplace(x * y);
                  break;
              case '/':
                  intermediate_result.emplace(x / y);
                  break;
          }
      }
      else {
          const int val = std::stoi(token);
          intermediate_result.emplace(val);
      }
  }
  return intermediate_result.top();
}
```



### Is a string well-formed?

括号配对，栈的经典入门题了...

```c++
bool IsWellFormed(const string& s) {
  // TODO - you fill in here.
  std::stack<char> stk;
  for (auto ch: s) {
      if (ch == '{' || ch == '(' || ch == '['){
          stk.emplace(ch);
      } else {
          if (stk.empty()) {
              return false;
          }
          if ((ch == '}' && stk.top() != '{') ||
              (ch == ')' && stk.top() != '(') ||
              (ch == ']' && stk.top() != '[')) {
              return false;
          }
          stk.pop();
      }
  }
  if (!stk.empty()) {
      return false;
  }
  return true;
}
```





### Normalize pathnames

将文件的路径名缩短。

用vector模拟栈的操作，没有直接用stack是为了方便顺序地对结果做拼接。

```c++
string ShortestEquivalentPath(const string& path) {
  // TODO - you fill in here.
  std::vector<string> path_names;
  if (path.front() == '/') {
      path_names.push_back("/");
  }
  std::stringstream ss(path);
  string token;
  while (getline(ss, token, '/')) {
      if (token == "..") {
          // .. 进入上级目录 需要判断当前是pop back 还是插入..
          if (path_names.empty() || path_names.back() == "..") {
              path_names.push_back(token);
          } else {
              //
              path_names.pop_back();
          }
      } else if (token != "." && token != "") {
          path_names.push_back(token);
      }
  }
  string ret;
  if (!path_names.empty()) {
      ret = path_names.front(); // front 单独处理 防止开始既是 /
      for (int i = 1; i < path_names.size(); ++i) {
          if (i == 1 && ret == "/") {
              ret += path_names[i];
          } else {
              ret += "/" + path_names[i];
          }
      }
  }
  return ret;
}
```





### Compute buildings with a sunset view

一条街道上从东到西排列着一排建筑，西边的建筑如果太高了，东边的将看不到日落。

以从东到西的顺序给出建筑高度，返回能看见日落的建筑的下标。

想法上还是比较简单，将元素依次入栈，，如果下个元素大于当前栈顶，pop栈直到当前值小于栈顶或栈为空。



```c++
vector<int> ExamineBuildingsWithSunset(
    vector<int>::const_iterator sequence_begin,
    const vector<int>::const_iterator& sequence_end) {
    // TODO - you fill in here.
  if (sequence_begin == sequence_end) {
      return {};
  }
  vector<int> building_height(sequence_begin, sequence_begin+1);
  vector<int> building_idx(1,0);
  ++sequence_begin;
  int c_max = building_height[0], c_idx = 1;
  while (sequence_begin != sequence_end){
      int height = *sequence_begin;
      while (!building_height.empty() && building_height.back() <= height) {
          building_height.pop_back();
          building_idx.pop_back();
      }
      building_height.push_back(height);
      building_idx.push_back(c_idx);
      ++sequence_begin;
      ++c_idx;
  }
  std::reverse(begin(building_idx), end(building_idx));
  return building_idx;
}
```



## Queue

Duque: double-ended queue



### 基本语法

```c++
// queue
.front();
.back();
.push(val);
.pop();

//deque
//+
.push_back(val);
.emplace_back(val);
.push_front(val);
.pop_back();
.pop_front();
.front();
.back();
```





### Compute binary tree nodes in order of increasing depth

树的按层遍历, 这题在leetcode上写过，不过用的是递归的方式。

代码里的unique_ptr也给我看懵了，直接看注解。

```c++
// unique_ptr p
p.release(); // return a pointer th the managed oject and released the ownership
p.reset(); // replace the managed object
p.swap();

p.get(); // return pointer
p.get_deleter();
operator bool
```



非递归的写法是，用两个队列分别表示当前层和下一层的结点

```c++
vector<vector<int>> BinaryTreeDepthOrder(
    const unique_ptr<BinaryTreeNode<int>>& tree) {
  // TODO - you fill in here.
  // 定义当前层的结点，用根节点初始化
  std::queue<BinaryTreeNode<int>*> curr_depth_nodes({tree.get()});
  vector<vector<int>> ret;

  while (!curr_depth_nodes.empty()) {
      // 定义下一层
      std::queue<BinaryTreeNode<int>*> next_depth_nodes;
      vector<int> this_level;
      // 遍历当前层
      while (!curr_depth_nodes.empty()) {
          auto curr = curr_depth_nodes.front();
          curr_depth_nodes.pop();
          if (curr) {
              this_level.emplace_back(curr->data);
              // 先左后右 保证按层顺序
              next_depth_nodes.emplace(curr->left.get());
              next_depth_nodes.emplace(curr->right.get());
          }
      }
      if (!this_level.empty()) {
          ret.emplace_back(this_level);
      }
      curr_depth_nodes = next_depth_nodes;
  }
  return ret;
}
```





### Implement a circular queue

用循环数组模拟队列...也是数据结构课本上的题目了...

这题多了个要求，要能够自适应resize。 记录好head和tail的位置，剩下的就是填代码进去了。

```c++
class Queue {
 public:
  Queue(size_t capacity) {
      data = new std::vector<int>(capacity);
      head = 0, tail = 0;
      cap = capacity;
  }
  void _Resize() {
      int new_cap = data->size() * 2 + 1;
      auto new_field = new std::vector<int>(new_cap);
      int n_idx = 0;
      while(head != tail) {
          (*new_field)[n_idx++] = (*data)[head];
          head = (head + 1) % cap;
      }
      head = 0;
      tail = n_idx;
      delete data;
      data = new_field;
      cap = new_cap;
  }
  void Enqueue(int x) {
    // TODO - you fill in here.
    if ((tail + 1) % cap == head) {
        _Resize();
    }
    (*data)[tail] = x;
    tail = (tail + 1) % cap;
    return;
  }
  int Dequeue() {
    // TODO - you fill in here.
    int c_val = (*data)[head];
    head = (head + 1) % cap;
    return c_val;
  }
  int Size() const {
    // TODO - you fill in here.
    return (tail + cap - head) % cap;
    return 0;
  }

private:
    std::vector<int>* data;
    int head, tail;
    int cap;
};
```





### Implement a queue using stacks

用栈模拟队列，队列跟栈的性质是完全相反的，不过一个栈倒腾两次也就成了队列。

所以用两个栈来回倒也能实现队列的功能。

```c++
class Queue {
 public:
  void Enqueue(int x) {
    // TODO - you fill in here.
    stk.emplace(x);
    return;
  }
  int Dequeue() {
      // TODO - you fill in here.
      if (stk.empty()) {
          throw length_error("Empty Dequeue");
      }
      int v;
      while (!stk.empty()) {
          v = stk.top();
          aux_stk.emplace(v);
          stk.pop();
      }
      // 取队首元素
      int ret_val = aux_stk.top();
      aux_stk.pop();
      while (!aux_stk.empty()) {
          v = aux_stk.top();
          aux_stk.pop();
          stk.emplace(v);
      }
      return ret_val;
  }

private:
    std::stack<int> stk, aux_stk;
};
```





### Implement a queue with max API

emm，跟之前的stack with max API感觉有些相似。

Python里Counter都是dict的形式，这里用map记录不同元素值的计数。

```c++
class QueueWithMax {
 public:
  void Enqueue(int x) {
    // TODO - you fill in here.
    data.emplace_back(x);
    cnt[x] += 1;
    return;
  }
  int Dequeue() {
    // TODO - you fill in here.
    int v = data.front();
    data.pop_front();
    --cnt[v];
    if (cnt[v] == 0) {
        cnt.erase(v);
    }
    return v;
  }
  int Max() const {
    // TODO - you fill in here.
    int max_val = data.front();
    for (auto iter = cnt.cbegin(); iter != cnt.cend(); ++iter) {
        if (max_val < iter->first) {
            max_val = iter->first;
        }
    }
    return max_val;
  }

private:
    std::deque<int> data;
    std::map<int, int> cnt;

};
```

