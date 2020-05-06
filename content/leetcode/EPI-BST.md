Title: EPI-BST
Date: 2020-04-20 19:20
Modified: 2020-04-20 20:20
Category: LeetCode
Tags: EPI, c++
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

