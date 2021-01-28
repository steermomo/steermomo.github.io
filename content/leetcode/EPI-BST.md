Title: EPI-BST
Date: 2020-04-20 19:20
Modified: 2020-04-20 20:20
Category: LeetCode
Tags: EPI, cpp
Slug: epi-BST

很久很久以前，有人刷题不做记录。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还没刷过BST。

[TOC]

## BST



### 库函数

C++中的`set`和`map`是BST-based.



```c++
// 与unordered_set 和unordered_map有些不同的api

// set
.begin(); //返回的迭代器按key递增的顺序
*begin(); / *rbegin(); //返回BST中的最大最小元素
 
lower_bound(12);/upper_bound(3); //返回第一个大于等于/大于参数的元素

.equal_range(val);//
```

> ### equal_range 
>
> The range is defined by two iterators, one pointing to the first element that is *not less* than `key` and another pointing to the first element *greater* than `key`. Alternatively, the first iterator may be obtained with [lower_bound()](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/container/set/lower_bound.html), and the second with [upper_bound()](dfile:///Users/steer/Library/Application Support/Dash/DocSets/C++/C++.docset/Contents/Resources/Documents/en.cppreference.com/w/cpp/container/set/upper_bound.html).



### TEST IF A BINARY TREE SATISFIES THE BST PROPERTY

Write a program that takes as input a binary tree and checks if the tree satisfies the BST property .

Hint: Is it correct to check for each node that its key is greater than or equal to the key at its left child and less than or equal to the key at its right child ?

要检查二叉树的特性：左子树的所有结点值小于当前节点、右子树所有结点值大于当前节点。



```c++
bool IsBinaryTreeBSTHelper(const unique_ptr<BinaryTreeNode<int>>& p, int max_val, int min_val) {
    if (p == nullptr) {
        return true;
    }
    if (p->data > max_val || p->data < min_val) {
        return false;
    }
    return IsBinaryTreeBSTHelper(p->left, p->data, min_val) && IsBinaryTreeBSTHelper(p->right, max_val, p->data);
}
```



### FIND THE FIRST KEY GREATER THAN A GIVEN VALUE IN A BST

Write a program that takes as input a BST and a value , and returns the first key that would appear in an inorder traversal which is greater than the input value. For example , when applied to the BST in Figure 15.1 on Page 251 you should return 29 for input 23.



看完解析觉得自己就是个傻子，写了一大坨分情况讨论。

要找到比k值大的第一个元素，从BST的根结点向下搜索：如果当前结点值大于k，可能是候选点，向左搜索；如果当前节点小于k，则向右子树搜索更大的值。直到抵达树的叶结点。

该方法的时间复杂度为$O(h)$, 空间复杂度为$O(1)$

```c++
// search_first_greater_value_in_bst.cc
BstNode<int>* FindFirstGreaterThanK(const unique_ptr<BstNode<int>>& tree,
                                    int k) {
  // TODO - you fill in here.

    BstNode<int> *sub_tree = tree.get(), *ret_so_far = nullptr;
    while (sub_tree) {
        if (sub_tree->data > k) {
            ret_so_far = sub_tree;
            sub_tree = sub_tree->left.get();
        } else {
            sub_tree = sub_tree->right.get();
        }
    }
    return ret_so_far;
}
```





### FIND THE k LARGEST ELEMENTS IN A BST

A BST is a sorted data structure , which suggests that it should be possible to find the k largest keys easily .

Write a program that takes as input a BST and an integer k , and returns the k largest elements in the BST in decreasing order. 

Hint What does an inorder traversal yield ?



brute-force的方法就是中序遍历，返回最后k个元素。这样前面的元素都算白遍历了，相应地，可以从后面逆中序遍历。



```c++
bool FindKLargestInBSTHelper(BstNode<int>* sub_tree, int k, vector<int>& ret) {
    if (ret.size() == k) {
        return true;
    }
    if (sub_tree == nullptr) {
        return false;
    }
    bool found = FindKLargestInBSTHelper(sub_tree->right.get(), k, ret);
    // 找到元素后直接返回，不再遍历左子树
    if (found) {
        return true;
    }
    ret.emplace_back(sub_tree->data);
    return FindKLargestInBSTHelper(sub_tree->left.get(), k, ret);
}
vector<int> FindKLargestInBST(const unique_ptr<BstNode<int>>& tree, int k) {
  // TODO - you fill in here.
  vector<int> ret;
  FindKLargestInBSTHelper(tree.get(), k, ret);
  return ret;
}
```





### COMPUTE THE LCA IN A BST

Since a BST is a specialized binary tree , the notion of lowest common ancestor , as expressed in Problem 10.4 on Page 155 , holds for BSTs too.

In general , computing the LCA of two nodes in a BST is no easier than computing the LCA in a binary tree , since structurally a binary tree can be viewed as a BST where all the keys are equal . However , when the keys are distinct , it is possible to improve on the LCA algorithms for binary trees.

Design an algorithm that takes as input a BST and two nodes , and returns the LCA of the two nodes. For example , for the BST in Figure 15.1 on Page 251 , and nodes C and G , your algorithm should return B . Assume all keys are distinct. Nodes do not have references to their parents .

Hint Take advantage of the BST property .



比之前在二叉树中查找LCA要简单一些。 虽然结点没有parent的信息， 对于BST，在知道结点值的情况下，就可以从上向下搜索到对应的结点。

从根结点开始搜索，直到抵达LCA，他们的搜索路径都是一致的，在LCA结点开始出现分歧。

```c++
//lowest_common_ancestor_in_bst.cc

// Input nodes are nonempty and the key at s is less than or equal to that at
// b.
BstNode<int>* FindLca(const unique_ptr<BstNode<int>>& tree,
                      const unique_ptr<BstNode<int>>& s,
                      const unique_ptr<BstNode<int>>& b) {
  // TODO - you fill in here.
  
  BstNode<int> *p = tree.get();
  int s_val = s->data, b_val = b->data;
  while(p != nullptr) {
      int c_val = p->data;
      if (s_val < c_val && b_val < c_val) {
          // go left
          p = p->left.get();
      } else if (s_val > c_val && b_val > c_val) {
          // go right
          p = p->right.get();
      } else {
          return p;
      }
  }
  return nullptr;
}
```





### RECONSTRUCT A BST FROM TRAVERSAL DATA

As discussed in Problem 10.12 on Page 163 there are many different binary trees that yield the same sequence of visited nodes in an inorder traversal. This is also true for preorder and postorder traversals. Given the sequence of nodes that an inorder traversal sequence visits and either of the other two traversal sequences , there exists a unique binary tree that yields those sequences . Here we study if it is possible to reconstruct the tree with less traversal information when the tree is known to be a BST.

It is critical that the elements stored in the tree be unique . If the root contains key v and the tree contains more occurrences of v , we cannot always identify from the sequence whether the subsequent vs are in the left subtree or the right subtree. For example , for the tree rooted at G in Figure 15.2 on Page 256 the preorder traversal sequence is 285 , 243 , 285 , 401. The same preorder traversal sequence is seen if 285 appears in the left subtree as the right child of the node with key 243 and 401 is at the root ' s right child .

Suppose you are given the sequence in which keys are visited in an inorder traversal of a BST , and all keys are distinct. Can you reconstruct the BST from the sequence ? If so , write a program to do so. Solve the same problem for preorder and postorder traversal sequences .

前序遍历的话，序列的第一个结点就是根结点，剩下的子序列就是左子树和右子树。而在剩余序列中，第一个结点又是左子树的根结点。

~~因此直接根据前序遍历，向一颗空的BST中插入结点就可以。~~  我本来以为这个想法是错的, 仔细想了一下没啥问题，测试样例也全过了。 在最坏情况下(全是左子树)这种方法的时间复杂度应该为$O(n^2 )$

```c++
void BstInsert(unique_ptr<BstNode<int>> &root, int val) {
    // 将指定位置插入结点
    if (root == nullptr) {
        root = std::make_unique<BstNode<int>>(
                BstNode<int>{val, nullptr, nullptr}
        );
        return;
    }
    if (root->data > val) {
        BstInsert(root->left, val);
    } else {
        BstInsert(root->right, val);
    }
}

unique_ptr<BstNode<int>> RebuildBSTFromPreorder(
    const vector<int>& preorder_sequence) {
  // TODO - you fill in here.
  if (preorder_sequence.empty()) {
      return nullptr;
  }
  unique_ptr<BstNode<int>> root = std::make_unique<BstNode<int>>(
          BstNode<int>{preorder_sequence[0], nullptr, nullptr}
          );
  // 顺序插入
  for (int i = 1; i < preorder_sequence.size(); ++i) {
      BstInsert(root, preorder_sequence[i]);
  }
  return root;
}
```



有了根结点的值，根据BST的性质，可以将剩下的子序列划分为左子树和右子树，递归地构建出BST。

```c++
//bst_from_preorder.cc

unique_ptr<BstNode<int>> RebuildBSTFromPreorderHelper(const vector<int>& preorder_sequence,
        int start, int end) {
    if (start >= end) {
        return nullptr;
    }
    // 查找左右子树的划分点
    int transition_point = start + 1;
    while (transition_point < end && preorder_sequence[transition_point] < preorder_sequence[start]) {
        ++transition_point;
    }
    // 递归构建子树
    return std::make_unique<BstNode<int>>(BstNode<int> {
       preorder_sequence[start],
       RebuildBSTFromPreorderHelper(preorder_sequence, start+1, transition_point),
       RebuildBSTFromPreorderHelper(preorder_sequence, transition_point, end)
    });
}

unique_ptr<BstNode<int>> RebuildBSTFromPreorder(
    const vector<int>& preorder_sequence) {
  // TODO - you fill in here.
  return RebuildBSTFromPreorderHelper(preorder_sequence, 0, preorder_sequence.size());
}
```



上述的做法在求分界点的片段中，对vector进行了多次遍历，如果BST只要左子树，将进行大量的遍历，时间复杂度为$O(n^2)$。



在最开始不太正确的思路还是提供了一些信息，子序列的第一个就是左子树的根结点。这样就没有必要每次都从根结点开始查找并插入，依次构建左子树就可以了嘛。

下面的方法，每次将`root_idx`向前推进一次, 根据`root_idx`创建当前的根结点. 时间复杂度为$O(n)$

```c++
unique_ptr<BstNode<int>> RebuildBSTFromPreorderHelper(const vector<int>& preorder_sequence,
        int &root_idx,
        int low_bound,
        int upper_bound) {
    if (root_idx >= preorder_sequence.size()) {
        return nullptr;
    }

    int root_val = preorder_sequence[root_idx];
    if (root_val < low_bound || root_val > upper_bound) {
        return nullptr;
    }
    ++root_idx;
    auto left_subtree = RebuildBSTFromPreorderHelper(preorder_sequence, root_idx, low_bound, root_val);
    auto right_subtree = RebuildBSTFromPreorderHelper(preorder_sequence, root_idx, root_val, upper_bound);
    return std::make_unique<BstNode<int>>(BstNode<int>{
        root_val,
        std::move(left_subtree),
        std::move(right_subtree)
    });
}

unique_ptr<BstNode<int>> RebuildBSTFromPreorder(
    const vector<int>& preorder_sequence) {
  // TODO - you fill in here.
  int root_idx = 0;
  return RebuildBSTFromPreorderHelper(preorder_sequence, root_idx, std::numeric_limits<int>::min(), std::numeric_limits<int>::max());
}
```





### Find the closest entries in three sorted arrays



Design an algorithm that takes three sorted arrays and returns one entry from each such that the minimum interval containing these three entries is as small as possible . For example , if the three arrays are ( 5 , 10 , 15 ) , ( 3 , 6 , 9 , 12 , 15 ) , and ( 8, 16 , 24 ) , then 15 , 15 , 16 lie in the smallest possible interval.

Hint How would you proceed if you needed to pick three entries in a single sorted array ?



我连题目都没看懂... 没理解错的话，是要在3个排序数组中分别找到3个元素，使得这3个元素之间的间距最小。



从这3个数组的头部开始，初始时读入3个元素，计算最大最小值之间的差异。然后将最小的元素替换为其下一个元素，再次计算最大最小的差异。

这里需要不停地插入、删除、找到最大最小元素，所以比较适合使用BST。（而我第一时间居然是想到造一个BST的轮子！！！！

在多个排序数组中，会出现相同的元素，这里用`multimap`保持迭代器信息.

```c++
//minimum_distance_3_sorted_arrays.cc

int FindClosestElementsInSortedArrays(
    const vector<vector<int>>& sorted_arrays) {
  // TODO - you fill in here.
  int min_distance_so_far = std::numeric_limits<int>::max();
  struct IterTail {
      vector<int>::const_iterator iter, tail;
  };
  // 存在多个相同值的情况，使用multimap
  std::multimap<int, IterTail> iter_and_tail;
    for (const vector<int>& sorted_array : sorted_arrays) {
        iter_and_tail.emplace(sorted_array.front(),
                              IterTail{cbegin(sorted_array), cend(sorted_array)});
    }
  while (true) {
      // 更新间距
      int min_val = iter_and_tail.cbegin()->first;
      int max_val = iter_and_tail.crbegin()->first;
      min_distance_so_far = std::min(max_val - min_val, min_distance_so_far);
      // 推进迭代器
      const auto next_min_iter = std::next(cbegin(iter_and_tail)->second.iter),
                 next_min_end = cbegin(iter_and_tail)->second.tail;
      if (next_min_iter == next_min_end) {
          return min_distance_so_far;
      }
      // 插入新迭代器位置
      iter_and_tail.emplace(
              *next_min_iter,
              IterTail{next_min_iter, next_min_end}
              );
      // 删除最小元素
      iter_and_tail.erase(iter_and_tail.cbegin());

  }
  return 0;
}
```





### ENUMERATE NUMBERS OF THE FORM a + b $\sqrt{2}$

Numbers of the form a + b$\sqrt q$ , where a and b are nonnegative integers , and q is an integer which is not the square of another integer , have special properties , e. g . , they are closed under addition and multiplication . Some of the first few numbers of this form are given in Figure 15.4.



Design an algorithm for efficiently computing the k smallest numbers a + b$\sqrt{2}$  for nonnegative integers a and b.



要计算前k个符合a + b $\sqrt{2}$的数值。

暴力的解法就是分别计算前k个a和b对应的值，然后对$k^2$个结果排序. 



时间复杂度更低的方法有些类似之前用堆排序查找最小的$n$个值做法.   这里用到两个特性:

1. C++中的set的底层是BST
2. BST的`begin()`方法返回最小元素的迭代器.

这样在最开始时向BST中插入$a$, $b$均为0的结点, 然后每次从BST中取出最小元素, 将其$a$, $b$值分别+1后再插入到BST中.

```c++
struct ABSqrt2{
    ABSqrt2(int a, int b) : a(a), b(b), val(a + b * sqrt(2)){}
    bool operator <(const ABSqrt2& rhs) const { return val < rhs.val;}
    int a, b;
    double val;
};
vector<double> GenerateFirstKABSqrt2(int k) {
  // TODO - you fill in here.
  std::set<ABSqrt2> candidates;
  candidates.emplace(0, 0);

  vector<double> ret;
  while (ret.size() < k) {
      auto next_smallest = candidates.cbegin();
      ret.emplace_back(next_smallest->val);

      candidates.emplace(next_smallest->a + 1, next_smallest->b);
      candidates.emplace(next_smallest->a, next_smallest->b+1);

      candidates.erase(next_smallest);
  }

  return ret;
}
```





### THE MOST VISITED PAGES PROBLEM

You are given a server log file containing billions of lines. Each line contains a number of fields. For this problem, the relevant field is an id denoting the page that was accessed.
Write a function to read the next line from a log file, and a function to find the k most visited pages, where k is an input to the function. Optimize performance for the situation where calls to the two functions are interleaved. You can assume the set of distinct pages is small enough to fit in RAM.







### BUILDA MINIMUM HEIGHT BST FROM A SORTED ARRAY
Given a sorted array, the number of BSTs that can be built on the entries in the array grows enormously with its size. Some of these trees are skewed, and are closer to lists; others are more balanced. See Figure 15.3 on Page 259 for an example.
How would you build a BST of minimum possible height from a sorted array?
Hint: Which element should be the root?

要构建最矮的BST，BST的左右子树需要平衡， 这样才能降低树的高度。

而且数组也已经是排序过的，则排在中间位置的结点用于构建根结点。

递归地向下构建树



```c++
unique_ptr<BstNode<int>> BuildMinHeightBSTFromSortedArrayHelper(const vector<int>& A, int left, int right){
    if (left >= right) {
        return nullptr;
    }
    int middle_idx = left + (right - left) / 2;
    // 递归构建结点
    return std::make_unique<BstNode<int>>(BstNode<int>{A[middle_idx],
                                                       BuildMinHeightBSTFromSortedArrayHelper(A, left, middle_idx),
                                                       BuildMinHeightBSTFromSortedArrayHelper(A, middle_idx+1, right)});
}
```





### INSERTIONANDDELETIONINABST

A BST is a dynamic data structure—in particular, if implemented carefully, key inser-tion and deletion can be made very fast.
Design efficient functions for inserting and removing keys in a BST. Assume that all elements in the BST are unique, and that your insertion method must preserve this property.





### TEST IF THREE BST NODES ARE TOTALLY ORDERED
Write a program which takes two nodes in a BST and a third node, the "middle" node, and determines if one of the two nodes is a proper ancestor and the other a proper descendant of the middle. (A proper ancestor of a node is an ancestor that is not equal to the node; a proper descendant is defined similarly.) For example, in Figure 15.1 on Page 251, if the middle is Node /, your function should return true if the two nodes are {A,K\ or It should return false if the two nodes are {I,P\ or {/, K\. You can assume that all keys are unique. Nodes do not have pointers to their parents

给出BST中的两个结点和第三个结点，判断第三个结点是否是刚好在前两个结点中间（在同一条向上遍历的路径内）， 结点不包含父结点信息。



因为是BST，结点不包含父结点信息也可以实现路径遍历。

从第一个结点查找至第二个结点，如果中间有经过第3个结点，则第3个结点是在它们之间的。

这里因为前两个结点并没有保证顺序，需要逆转再查找一次。

```c++
bool IsAncAndDes(std::vector<BstNode<int>*> &lookup) {
    // 从head 到 tail遍历一次
    auto head = lookup.front(), tail = lookup.back();
    int c_idx = 0;
    while (head != nullptr && head->data != tail->data) {
        if (head->data == lookup[c_idx]->data) {
            ++c_idx;
        }
        if (head->data > tail->data) {
            head = head->left.get();
        } else {
            head = head->right.get();
        }
    }
    if (head == nullptr || c_idx < 2) {
        return false;
    }
    return true;
}
bool PairIncludesAncestorAndDescendantOfM(
    const unique_ptr<BstNode<int>>& possible_anc_or_desc_0,
    const unique_ptr<BstNode<int>>& possible_anc_or_desc_1,
    const unique_ptr<BstNode<int>>& middle) {
  // TODO - you fill in here.
  std::vector<BstNode<int>*> lookup = {possible_anc_or_desc_0.get(), middle.get(), possible_anc_or_desc_1.get()};
  bool s_order_ret = IsAncAndDes(lookup);
  if (s_order_ret) {
      return true;
  }
  std::reverse(std::begin(lookup), std::end(lookup));
  bool reverse_order_ret = IsAncAndDes(lookup);
  if (reverse_order_ret) {
      return true;
  }
  return false;
}
```



### THE RANGE LOOKUP PROBLEM

Consider the problem of developing a web-service that takes a geographical loca- tion, and returns the nearest restaurant. The service starts with a set of restaurant locations—each location includes X and Y-coordinates. A query consists of a location, and should return the nearest restaurant (ties can be broken arbitrarily).



One approach is to build two BSTs on the restaurant locations: Tx sorted on the X coordinates, and Ty sorted on the Y coordinates. A query on location ( p,q) can be performed by finding all the restaurants whose X coordinate is in the interval [ p- D, p+ D], and all the restaurants whose Ycoordinate is in the interval [q- D, q+ D], taking the intersection of these two sets, and finding the restaurant in the intersection which is closest to ( p,q). Heuristically, if D is chosen correctly, the subsets are small and a brute-force search for the closest point is fast. One approach is to start with a small value for D and keep doubling it until the final intersection is nonempty.
There are other data structures which are more robust, e.g., Quadtrees and k-d trees, but the approach outlined above works well in practice.
Write a program that takes as input a BST and an interval and returns the BST keys that lie in the interval. For example, for the tree in Figure 15.1 on Page 251, and interval [16, 31], you should return 17, 19, 23, 29, 31.



对BST中序遍历可以得到顺序序列，在中序遍历的过程中，设置条件进行剪枝，降低搜索的空间，直接针对区间进行搜索， 区间内的值都找完后立刻退出搜索。

```c++
void RangeLookupInBSTHelper(BstNode<int>* node, vector<int>& ret, const Interval& interval) {
    if (node == nullptr) {
        return;
    }
    int c_data = node->data;
    if (c_data >= interval.left) {
        RangeLookupInBSTHelper(node->left.get(), ret, interval);
    }
    if (c_data >= interval.left && c_data <= interval.right) {
        ret.emplace_back(c_data);
    }
    if (c_data <= interval.right) {
        RangeLookupInBSTHelper(node->right.get(), ret, interval);
    }

}
vector<int> RangeLookupInBST(const unique_ptr<BstNode<int>>& tree,
                             const Interval& interval) {
  // TODO - you fill in here.
  vector<int> ret;
  RangeLookupInBSTHelper(tree.get(), ret, interval);
  return ret;
}
```



## Augmented BSTs



### ADD CREDITS

Consider a server that a large number of clients connect to. Each client is identified by a string. Each client has a "credit", which is a nonnegative integer value. The server needs to maintain a data structure to which clients can be added, removed, queried, or updated. In addition, the server needs to be able to add a specified number of credits to all clients simultaneously.

Design a data structure that implements the following methods:

+ Insert
+ Remove
+ Lookup
+ Add-to-all
+ Max