Title: EPI-Binary Trees
Date: 2020-04-05 19:20
Modified: 2020-04-05 20:20
Category: LeetCode
Tags: EPI, cpp
Slug: epi-Binary-Trees

很久很久以前，有人刷题不做记录，从Array刷到二叉树，刷了几年还是在刷二叉树。

<img src="{static}/images/what.jfif" style="max-width: 80%">

这里记录一下做**Elements of Programming Interviews**的题目，避免四年之后还是在刷二叉树。

[TOC]



## Binary Trees

### 结构定义

```c++
template <typename T>
struct BinaryTreeNode {
  T data;
  unique_ptr<BinaryTreeNode<T>> left, right;
}

```

EPI这部分的定义，跟我之前数据结构学得有点点区别...假书害人



- full binary tree，满二叉树，非叶结点都有两个子结点
- perfet binary tree，完美二叉树，深度为k且有2^(k+1)-1个结点(每一层都被完全填充)。
-  complete binary tree，完全二叉树，除了最后一层外的其他每一层都被完全填充，并且所有结点保持左对齐





### Test if a binary tree is height-balanced

测试二叉树的高度是否平衡， 在Leetcode也做过，不同的是我当时用height=-1表示子树不平衡。

EPI的做法蛮有意思，定义了一个结构体，通过返回结构体的形式返回多个参数值，是我之前没见过的。

```c++
struct BalancedSatusWithHeight {
    bool balanced;
    int height;
};
BalancedSatusWithHeight CheckBalanced(
        const unique_ptr<BinaryTreeNode<int>> & tree ) {
    if (tree == nullptr) {
        return {true, -1};
    }
    auto left_result = CheckBalanced(tree->left);
    if (!left_result.balanced) {
        return {false, 0};
    }
    auto right_result = CheckBalanced(tree->right);
    if (!right_result.balanced) {
        return {false, 0};
    }
    bool is_balanced = abs(left_result.height - right_result.height) <= 1;
    int height = std::max(left_result.height, right_result.height) + 1;
    return {is_balanced, height};
}
bool IsBalanced(const unique_ptr<BinaryTreeNode<int>>& tree) {
  // TODO - you fill in here.
  return CheckBalanced(tree).balanced;
}
```





### Test if a binary tree is symmetric

检测树是否对称，检测根结点的左右子树是否对称即可。

前序遍历， 左右子树分别用中左右、中右左的顺序。

```c++
bool CheckSymmetrice(const unique_ptr<BinaryTreeNode<int>> &left, const unique_ptr<BinaryTreeNode<int>> &right) {
    if (!left && !right) {
        return true;
    }
    if (!left || !right) {
        return false;
    }
    if (left->data != right->data) {
        return false;
    }
    return CheckSymmetrice(left->left, right->right) && CheckSymmetrice(left->right, right->left);
}
bool IsSymmetric(const unique_ptr<BinaryTreeNode<int>>& tree) {
  // TODO - you fill in here.
  if (!tree) {
      return true;
  }
  return CheckSymmetrice(tree->left, tree->right);
}
```





### Compute the lowest common ancestor in a binary tree

查找两个结点的最近公共祖先。

在看解析之前，我只能想到暴力的解法，遍历每个结点，leetcode好像也是可以过这个暴力解的。

关键点应该是在于想清楚问题的形式，对于两个结点的最近公共祖先来说，这两个结点肯定不是在同一个子树中，否则还可以向下深入一层。

那么在自底向上的查找过程中，记录当前已经找到的结点的个数，可以避免多次遍历。

```c++
struct Status {
    int num_target_nodes;
    BinaryTreeNode<int>* ancestor;
};
Status LCAHelper(const unique_ptr<BinaryTreeNode<int>>& tree,
                 const unique_ptr<BinaryTreeNode<int>>& node0,
                 const unique_ptr<BinaryTreeNode<int>>& node1) {
    if (tree == nullptr) {
        return {0, nullptr};
    }
    // 查找左子树
    auto left_result = LCAHelper(tree->left, node0, node1);
    if (left_result.num_target_nodes == 2){
        return left_result;
    }
    // 查找右子树
    auto right_result = LCAHelper(tree->right, node0, node1);
    if (right_result.num_target_nodes == 2) {
        return right_result;
    }
    // 如果当前结点或左右子树的目标和为2 则当前为目标结点
    int num_target_nodes = left_result.num_target_nodes +
            right_result.num_target_nodes +
            (tree == node0) + (tree == node1);
    return {num_target_nodes, num_target_nodes == 2 ? tree.get() : nullptr};
}
BinaryTreeNode<int>* Lca(const unique_ptr<BinaryTreeNode<int>>& tree,
                         const unique_ptr<BinaryTreeNode<int>>& node0,
                         const unique_ptr<BinaryTreeNode<int>>& node1) {
  // TODO - you fill in here.
  return LCAHelper(tree, node0, node1).ancestor;
}
```





### Compute the LCA when nodes have parent pointers

还是查找LCA，不同的是有了父结点指针。

分别从两个结点向上查找，记录路径。对齐根节点后，从后向前查找，最后一个相同的结点即为最近祖先。

这里使用了O(h)的空间，如果记录树的高度，同时只在树上操作的话，可以避免这一开销。

```c++
BinaryTreeNode<int>* Lca(const unique_ptr<BinaryTreeNode<int>>& node0,
                         const unique_ptr<BinaryTreeNode<int>>& node1) {
  // TODO - you fill in here.
  std::vector<BinaryTreeNode<int>*> path0, path1;
  BinaryTreeNode<int> *p0 = node0.get(), *p1 = node1.get();
  // 查找node0的路径
  while (p0) {
      path0.push_back(p0);
      p0 = p0->parent;
  }
  // 查找node1的路径
  while (p1) {
      path1.push_back(p1);
      p1 = p1->parent;
  }
  // 对齐根结点
  int idx0 = path0.size() - 1, idx1 = path1.size() - 1;
  while(idx0 >= 0 && idx1 >= 0) {
      if (path0[idx0] != path1[idx1]) {
          break;
      }
      --idx0, --idx1;
  }
  return path0[idx0+1];
}
```



### Sum the root-to-leaf paths in a binary tree

二叉树每个结点内包含二值(0， 1)， 从根结点到叶结点的序列可以组成一个二进制序列，计算树中所有序列的和。

这个递归的思路还是比较清晰， 向下调用的时候，相当于积攒路径上的值，到达叶结点后，返回每个叶结点序列的值并求和。

```c++
int SumRootToLeafHelper(const unique_ptr<BinaryTreeNode<int>>& tree, int partial_sum) {
    if (!tree) {
        return 0;
    }
    partial_sum = partial_sum * 2 + tree->data;
    // 叶结点
    if (!tree->left && !tree->right) {
        return partial_sum;
    }
    return SumRootToLeafHelper(tree->left, partial_sum) +
            SumRootToLeafHelper(tree->right, partial_sum);
}

int SumRootToLeaf(const unique_ptr<BinaryTreeNode<int>>& tree) {
  // TODO - you fill in here.
  return SumRootToLeafHelper(tree, 0);
}
```



### Find a root to leaf path with specified sum

判断二叉树中是否存在路径和为target num的路径



```c++
bool HasPathSumHelper(const unique_ptr<BinaryTreeNode<int>>& tree,
                        int current_sum, int target) {
    if (!tree) {
        return false;
    }
    current_sum += tree->data;
    if (!tree->left && !tree->right) {
        if (current_sum == target) {
            return true;
        } else {
            return false;
        }
    }
    return HasPathSumHelper(tree->left, current_sum, target) || HasPathSumHelper(tree->right, current_sum, target);
}
bool HasPathSum(const unique_ptr<BinaryTreeNode<int>>& tree,
                int remaining_weight) {
  // TODO - you fill in here.
  return HasPathSumHelper(tree, 0, remaining_weight);
}
```





### Implement an inorder traversal without recursion

不能用递归遍历的话，可以选择使用栈，需要注意压栈顺序。

~~我只能用单个栈实现前序遍历...~~

还是需要模拟中序遍历的情况，先尽可能向左，到达叶结点后访问值域，再向右向左访问。



```c++
vector<int> InorderTraversal(const unique_ptr<BinaryTreeNode<int>>& tree) {
  // TODO - you fill in here.
  std::stack<BinaryTreeNode<int>*> stk;
  auto curr = tree.get();
  vector<int> ret;
  while (!stk.empty() || curr) {
      if (curr) {
          stk.push(curr);
          curr = curr->left.get();
      } else {
          // curr 为空, 上一个结点为叶结点
          curr = stk.top();
          stk.pop();
          ret.push_back(curr->data); // 访问当前结点
          curr = curr->right.get(); // 向右访问一次
      }
  }
  return ret;
}
```





### Compute the kth node in an inorder traversal



```c++
const BinaryTreeNode<int>* FindKthNodeBinaryTree(
    const unique_ptr<BinaryTreeNode<int>>& tree, int k) {
  // TODO - you fill in here.
    std::stack<BinaryTreeNode<int>*> stk;
    auto curr = tree.get();
    int c_th = 0;
    while (!stk.empty() || curr) {
        if (curr) {
            stk.push(curr);
            curr = curr->left.get();
        } else {
            // curr 为空, 上一个结点为叶结点
            curr = stk.top();
            stk.pop();
            ++c_th;
            if (c_th == k) {
                return curr;
            }
            curr = curr->right.get(); // 向右访问一次
        }
    }

  return nullptr;
}
```





### Compute the successor

successor 是在中序遍历中出现在给定结点后的结点。假设每个结点都有父节点的信息。

最简单的方法是，通过父节点指针一直找到根节点，再中序遍历。虽然这样多了很多不必要的计算。



如果该结点有右子树的话，successor就是中序遍历右子树时的第一个结点。

~~如果该结点没有右子树，又可以分两种情况~~

- ~~该结点是左子树，successor就是父结点~~
- ~~该结点是右子树，successor是父结点的父结点~~

上面的情况考虑不够完备，如果父节点也是在右子树中的话，上述的情况是不满足的。 这里要找的是最近的且位于左子树中的祖先结点，这样它的父结点才是在中序遍历时会访问到的下一个结点。



```c++
BinaryTreeNode<int>* FindSuccessor(
    const unique_ptr<BinaryTreeNode<int>>& node) {
  // TODO - you fill in here.

  if (node->right.get() != nullptr) {
      auto curr = node->right.get();
      while (curr && curr->left.get()) {
          curr = curr->left.get();
      }
      return curr;
  }
  auto *curr = node.get();
  while (curr->parent != nullptr && curr->parent->left.get() != curr) {
      curr = curr->parent;
  }
  return curr->parent;
}
```





### Implement an inorder traversal with constant space

不使用额外空间实现中序遍历，结点含有父结点信息。

这里父结点信息是解决问题的关键，可是不会用啊...看解析吧



要求不开辟新空间存储，就需要手动使用指针在二叉树上移动。

那么就需要知道当前的指针是处于什么状态， 这里将指针的状态归类为

- 向下访问阶段
  - 有左子树，继续往下
  - 无左子树，访问数据域，向上访问
- 从子树返回阶段
  - 是从左子树返回的，访问数据域，访问右子树
  - 是从右子树返回的，则整个分支访问完成，返回上层

由上面的分类可以看出，需要明确指针的状态才能控制下一步的移动方向。 这里使用双指针prev和curr判断当前指针状态。

```c++
vector<int> InorderTraversal(const unique_ptr<BinaryTreeNode<int>>& tree) {
  // TODO - you fill in here.
  BinaryTreeNode<int> *prev = nullptr, *curr = tree.get();
  vector<int> ret;
  while (curr != nullptr) {
      BinaryTreeNode<int>* next;
      if (curr->parent == prev) {
          // 是从上往下访问
          if (curr->left != nullptr) {
              // 有左子树，继续往下
              next = curr->left.get();
          } else {
              // 到达叶结点， 访问数据
              ret.emplace_back(curr->data);
              // 如果有右子树， 继续向右，否则当前分支结束，向上
              next = (curr->right != nullptr) ? curr->right.get() : curr->parent;
          }
      } else if (curr->left.get() == prev) {
          // 是从左子树向上回溯
          ret.emplace_back(curr->data);
          next = (curr->right != nullptr) ? curr->right.get() : curr->parent;
      } else {
          next = curr->parent;
      }
      prev = curr;
      curr = next;
  }

  return ret;
}
```





### Reconstruct a binary tree from traversal data



...

...

...

忘了

这个在想法上还是很容易理解，前序遍历的第一个位置是根结点的值，在中序遍历中根结点的左右两边分别是左右子树。

拿着前序遍历的根结点值就能将中序的序列分开，并递归地往下处理。这样就能自底向上地创建每一个结点。

那么在处理时就需要将每个子树的前序区间跟中序区间指示出来。并且已知根结点的值，需要在中序遍历序列中查找其下标，通过构建hashtable的方式将查找的时间复杂度从O(n)降低到O(1)。总的时间复杂度为O(n)，空间复杂度为O(h+n)。

EPI的代码中用了`make_unique`让创建结点的这个过程直观了很多。



```c++
unique_ptr<BinaryTreeNode<int>> BinaryTreeFromPreorderInorderHelper(
        const vector<int>& preorder, size_t preorder_start, size_t preorder_end,
        size_t inorder_start, size_t inorder_end,
        const std::unordered_map<int ,size_t> &node_to_inorder_idx) {
    // 区间内无有效的值
    if (preorder_end <= preorder_start || inorder_end <= inorder_start) {
        return nullptr;
    }
    size_t root_inorder_idx = node_to_inorder_idx.at(preorder[preorder_start]);
    size_t  left_subtree_size = root_inorder_idx - inorder_start;
    return std::make_unique<BinaryTreeNode<int>> (BinaryTreeNode<int>{
        preorder[preorder_start],
        BinaryTreeFromPreorderInorderHelper(
                preorder, preorder_start+1, preorder_start + 1 + left_subtree_size,
                inorder_start, root_inorder_idx, node_to_inorder_idx),
        BinaryTreeFromPreorderInorderHelper(
                preorder, preorder_start+1+left_subtree_size, preorder_end,
                root_inorder_idx+1, inorder_end, node_to_inorder_idx)
    });
}

unique_ptr<BinaryTreeNode<int>> BinaryTreeFromPreorderInorder(
    const vector<int>& preorder, const vector<int>& inorder) {
  // TODO - you fill in here.
  std::unordered_map<int, size_t > node_to_inorder_idx;
  for (size_t i = 0; i < inorder.size(); ++i) {
      node_to_inorder_idx.emplace(inorder[i], i);
  }
  return BinaryTreeFromPreorderInorderHelper(preorder, 0, preorder.size(), 0, inorder.size(), node_to_inorder_idx);
}
```



### Reconstruct a binary tree from a preorder traversal with markers

用null表示先序遍历中空的子结点，从这样的先序遍历序列重建二叉树。

。。。

不会



着手点在于null。 于上一题相比， 这里只需要前序遍历就能重建树，因为null结点提供了额外的信息，指示了应该在什么时候停止向下创建子树。

另外应该利用的一点是，前序遍历序列中的第一个值是根结点的值。虽然不知道右子树什么时候开始，如果左子树创建正确的话，那么剩余的元素全部是属于右子树的。

为了知道当前在构建哪一个结点以及右子树从什么时候开始，使用subtree_pointer_idx记录当前的结点。

总体的时间复杂度为O(n)。

另外这里使用了`move`函数

> std::move 只是将参数转换为右值引用而已（相当于一个 static_cast）



```c++
unique_ptr<BinaryTreeNode<int>> ReconstructPreorderHelper(
        const vector<int*> &preorder,
        int *subtree_pointer) {
    int &subtree_pointer_idx = *subtree_pointer;
    int *p_node = preorder[subtree_pointer_idx];
    ++subtree_pointer_idx;
    // 当前为空结点，返回
    if (p_node == nullptr) {
        return nullptr;
    }
    // 分别构建左右子树
    auto left = ReconstructPreorderHelper(preorder, subtree_pointer);
    auto right = ReconstructPreorderHelper(preorder, subtree_pointer);
    return std::make_unique<BinaryTreeNode<int>>(BinaryTreeNode<int>{
            *p_node,
            move(left),
            move(right)
    });
}
unique_ptr<BinaryTreeNode<int>> ReconstructPreorder(
    const vector<int*>& preorder) {
  // TODO - you fill in here.
  int subtree_pointer_idx = 0;
  return ReconstructPreorderHelper(preorder, &subtree_pointer_idx);
}
```





### Compute the leaves of a binary tree

访问二叉树的所有叶子结点，从左到右的顺序排列

```c++
void CreateListOfLeavesHelper(const unique_ptr<BinaryTreeNode<int>>& tree,
                              vector<const unique_ptr<BinaryTreeNode<int>>*> &ret){
    if (!tree.get()) {
        return;
    }
    if (!tree->left.get() && !tree->right.get()) {
        ret.push_back(&tree);
        return;
    }
    CreateListOfLeavesHelper(tree->left, ret);
    CreateListOfLeavesHelper(tree->right, ret);
}

vector<const unique_ptr<BinaryTreeNode<int>>*> CreateListOfLeaves(
    const unique_ptr<BinaryTreeNode<int>>& tree) {
  // TODO - you fill in here.
    vector<const unique_ptr<BinaryTreeNode<int>>*> ret;
    CreateListOfLeavesHelper(tree, ret);
    return ret;
}
```





### Compute the exterior of a binary tree

exterior定义：从根结点到最左的叶结点，从左到右所有的叶结点，最右的叶结点再到根结点。



直接的想法就是，先从根结点访问到最左下，再依次访问叶结点，再从根结点访问到最右结点，最后将3条路径的结果拼接起来。

这样会存在边角结点多次访问的问题。



将这样一个问题分解成在左右子树上的遍历，再将结果拼在一起。

在左子树中，边访问数据域边向下前进。而在右子树中，需要先到达最底层的结点才能继续访问数据域。 这样才能保证题目中要求的访问顺序。







```c++
bool IsLeaf(const unique_ptr<BinaryTreeNode<int>>& tree) {
    if (tree->left == nullptr && tree->right == nullptr) {
        return true;
    }
    return false;
}

vector<const unique_ptr<BinaryTreeNode<int>>*> LeftBoundaryLeaf(
        const unique_ptr<BinaryTreeNode<int>>& tree, bool is_boundary) {
    vector<const unique_ptr<BinaryTreeNode<int>>*> ret;
    if (!tree) {
        return {};
    }
    if (is_boundary || IsLeaf(tree)) {
        ret.emplace_back(&tree);
    }
    // 向左一直是保持boundary
    auto left_part = LeftBoundaryLeaf(tree->left, is_boundary);
    ret.reserve(ret.size() + left_part.size());
    ret.insert(ret.end(), left_part.begin(), left_part.end());
    // 向右的情况下，如果一个结点没有左子树，该结点仍然是boundary 的一部分
    auto right_part = LeftBoundaryLeaf(tree->right, is_boundary && tree->left == nullptr);
    ret.insert(ret.end(), right_part.begin(), right_part.end());
    return ret;
}

vector<const unique_ptr<BinaryTreeNode<int>>*> RightBoundaryLeaf(
        const unique_ptr<BinaryTreeNode<int>>& tree, bool is_boundary) {
    if (!tree) {
        return {};
    }
    vector<const unique_ptr<BinaryTreeNode<int>>*> ret;
    // 向左的情况下，如果上一个结点是boundary 当前结点没有左子树，该结点仍然是boundary 的一部分
    auto left_part = RightBoundaryLeaf(tree->left, is_boundary && tree->right == nullptr);
    ret.reserve(ret.size() + left_part.size());
    ret.insert(ret.end(), left_part.begin(), left_part.end());

    // 向左一直是保持boundary
    auto right_part = RightBoundaryLeaf(tree->right, is_boundary);
    ret.insert(ret.end(), right_part.begin(), right_part.end());
    if (is_boundary || IsLeaf(tree)) {
        ret.emplace_back(&tree);
    }
    return ret;
}

vector<const unique_ptr<BinaryTreeNode<int>>*> ExteriorBinaryTree(
    const unique_ptr<BinaryTreeNode<int>>& tree) {
  // TODO - you fill in here.
  vector<const unique_ptr<BinaryTreeNode<int>>*> ret;
  if (!tree) {
      return {};
  }
  ret.emplace_back(&tree);
  auto left_part = LeftBoundaryLeaf(tree->left, true);
  auto right_part = RightBoundaryLeaf(tree->right, true);

  ret.insert(ret.end(), left_part.begin(), left_part.end());
  ret.insert(ret.end(), right_part.begin(), right_part.end());
  return ret;
}
```





### Compute the right sibling tree

假设结点中还包含一个额外的域，level-next，指向右兄弟结点。

给一个perfect binary tree，找出每个结点的右兄弟结点。

既然给出了完美二叉树，直接按层遍历就能得到每个结点的兄弟结点。

```c++
void ConstructRightSibling(BinaryTreeNode<int>* tree) {
  // TODO - you fill in here.
  if (!tree) {
      return;
  }
  std::vector<BinaryTreeNode<int>*> curr_level, next_level;
  curr_level.push_back(tree);
  while (!curr_level.empty()) {
      for (int i = 0; i < curr_level.size() - 1; ++i) {
          curr_level[i]->next = curr_level[i+1];
      }
      for (auto each: curr_level) {
          if (each->left.get() != nullptr) {
              next_level.push_back(each->left.get());
              next_level.push_back(each->right.get());
          }
      }
      curr_level = next_level;
      next_level.clear();
  }
  return;
}
```



下面是EPI给出的空间复杂度为O(1)的解法，emm，😅

对于完美二叉树中的结点，可以分为两种情况

- 若是左孩子，则next为父结点的右孩子
- 若是右孩子，则next为父结点next的左孩子

根据这个特性，只要按层去访问即可。(因为一起的二叉树并不会有next域，利用next域可以快速地按层访问)。



```c++
void SetRightSibling(BinaryTreeNode<int>* iter) {
    // 传入的是最左侧的结点
    while (iter) {
        iter->left->next = iter->right.get();
        if (iter->next) {
            iter->right->next = iter->next->left.get();
        }
        iter = iter->next;
    }
}

void ConstructRightSibling(BinaryTreeNode<int>* tree) {
    // TODO - you fill in here.
    auto left_start = tree; // 沿着左侧向下
    while (left_start && left_start->left.get()) {
        SetRightSibling(left_start);
        left_start = left_start->left.get();
    }
    return;
}
```