Title: LeetCode-Tree
Date: 2020-02-29 18:20
Modified: 2020-03-01 18:20
Category: LeetCode
Tags: leetcode, cpp
Slug: leetcode-tree
[TOC]

![](https://docs.google.com/spreadsheets/d/1SbpY-04Cz8EWw3A_LBUmDEXKUMO31DBjfeMoA0dlfIA/edit#gid=126913158)
![](https://img.shields.io/badge/-Easy-green) ![](https://img.shields.io/badge/-Medium-orange)

通用数据结构定义
```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
```

## 遍历求解

### 572. Subtree of Another Tree (Easy)
![](https://img.shields.io/badge/-Easy-green)

Given two non-empty binary trees s and t, check whether tree t has exactly the same structure and node values with a subtree of s. A subtree of s is a tree consists of a node in s and all of this node's descendants. The tree s could also be considered as a subtree of itself.

#### Solution
直接两个套两个递归函数就成, 再加上边界检查就过了.
```c++
class Solution {
public:
    bool isSubtree(TreeNode* s, TreeNode* t) {
        if (nullptr == s && nullptr == t) {
            return true;
        }
        if (nullptr == s || nullptr == t) {
            return false;
        }
        return isIdentical(s, t) || isSubtree(s->left, t) || isSubtree(s->right, t);
    }
private:
    bool isIdentical(TreeNode* s, TreeNode* t) {
        if (nullptr == s && nullptr == t) {
            return true;
        }
        if (nullptr == s || nullptr == t) {
            return false;
        }
        if (s->val != t->val) {
            return false;
        }
        return isIdentical(s->left, t->left) && isIdentical(s->right, t->right);
    }
};
```

### 965. Univalued Binary Tree (Easy)
![](https://img.shields.io/badge/-Easy-green)

A binary tree is univalued if every node in the tree has the same value.

Return true if and only if the given tree is univalued.

Easy的题, 直接遍历就好了
```c++
class Solution {
public:
    bool isUnivalTree(TreeNode* root) {
        int rootVal = root->val;
        return isUnivalTree(root, rootVal);
    }
private:
    bool isUnivalTree(TreeNode* root, int rootVal) {
        if (nullptr == root) {
            return true;
        }
        if (root->val != rootVal) {
            return false;
        }
        return isUnivalTree(root->left, rootVal) && isUnivalTree(root->right, rootVal);
    }
};
```

## collecting nodes

### 107. Binary Tree Level Order Traversal II
Given a binary tree, return the bottom-up level order traversal of its nodes' values. (ie, from left to right, level by level from leaf to root).
本来打算按层遍历. 只要记录节点深度就可以
```c++
class Solution {
public:
    vector<vector<int>> levelOrderBottom(TreeNode* root) {
        vector<vector<int>> ret;
        levelTravel(root, ret, 0);
        reverse(ret.begin(), ret.end());
        return ret;
    }
private:
    void levelTravel(TreeNode* root, vector<vector<int>>& ans, int level) {
        if (nullptr == root) {
            return;
        }
        if (level >= ans.size()) {
            ans.push_back(vector<int>());
        }
        ans[level].push_back(root->val);
        levelTravel(root->left, ans, level+1);
        levelTravel(root->right, ans, level+1);
    }
};
```

### 429. N-ary Tree Level Order Traversal (Medium)
Given an n-ary tree, return the level order traversal of its nodes' values.

Nary-Tree input serialization is represented in their level order traversal, each group of children is separated by the null value (See examples).

跟107题其实一样
```c++
/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> children;

    Node() {}

    Node(int _val) {
        val = _val;
    }

    Node(int _val, vector<Node*> _children) {
        val = _val;
        children = _children;
    }
};
*/
class Solution {
public:
    vector<vector<int>> levelOrder(Node* root) {
        vector<vector<int>> ret;
        levelOrder(root, ret, 0);
        return ret;
    }
private:
    void levelOrder(Node* root, vector<vector<int>>& ret, int level) {
        if (nullptr == root) {
            return;
        }
        if (level >= ret.size()) {
            ret.push_back(vector<int>());
        }
        ret[level].push_back(root->val);
        for (auto p: root->children) {
            levelOrder(p, ret, level+1);
        }
    }
};
```

### 872. Leaf-Similar Trees (Easy)
![](https://img.shields.io/badge/-Easy-green)

Consider all the leaves of a binary tree.  From left to right order, the values of those leaves form a leaf value sequence.
Two binary trees are considered leaf-similar if their leaf value sequence is the same.

Return true if and only if the two given trees with head nodes root1 and root2 are leaf-similar.

```c++

class Solution {
public:
    bool leafSimilar(TreeNode* root1, TreeNode* root2) {
        vector<int> seq1, seq2;
        leafTravel(root1, seq1);
        leafTravel(root2, seq2);
        if (seq1.size() != seq2.size()) {
            return false;
        }
        for (int idx = 0; idx < seq1.size(); ++idx) {
            if (seq1[idx] != seq2[idx]) {
                return false;
            }
        }
        return true;
    }
private:
    void leafTravel(TreeNode* root, vector<int>& leafSeq) {
       if (nullptr == root) {
           return;
       }
        if (isLeaf(root)) {
            leafSeq.push_back(root->val);
        }
        leafTravel(root->left, leafSeq);
        leafTravel(root->right, leafSeq);
   }
    bool isLeaf(TreeNode* p) {
        if (nullptr == p) {
            return false;
        }
        if (p->left == nullptr && p->right == nullptr) {
            return true;
        }
        return false;
    }
};
```

### 669. Trim a Binary Search Tree (Easy)
![](https://img.shields.io/badge/-Easy-green)

Given a binary search tree and the lowest and highest boundaries as L and R, trim the tree so that all its elements lies in [L, R] (R >= L). You might need to change the root of the tree, so the result should return the new root of the trimmed binary search tree.

这题我用了一个很蠢的方法, 先构建出BST中在合法范围的元素序列, 再重新创建BST, 提交过不了.

看了一下正确的做法, 是从底向上执行trim.
```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    TreeNode* trimBST(TreeNode* root, int L, int R, bool top=true) {
        if (!root) {
            return root;
        }
        root->left = trimBST(root->left, L, R, false);
        root->right = trimBST(root->right, L, R, false);
        // 左右子节点都是trim后的, 如果当前节点值在合法范围内, 直接直接返回即可
        if (root->val >= L && root->val <= R) {
            return root;
        }
        TreeNode* ret = nullptr;
        // 根据当前节点在给定范围的方向, 返回某一个已经trim的子树
        if (root->val < L) {
            ret = root->right;
        }
        else {
            ret = root->left;
        }
        if (!top) {
            delete root;
        }
        return ret;
        
    }

};
```

### 1325. Delete Leaves With a Given Value
Given a binary tree root and an integer target, delete all the leaf nodes with value target.

Note that once you delete a leaf node with value target, if it's parent node becomes a leaf node and has the value target, it should also be deleted (you need to continue doing that until you can't).

自底向上删除, 能够一直删除叶结点. 
但是不知道为什么delete结点会导致崩溃, 看到讨论区的回复才知道, 应该是在这段代码之后, leetcode有插入其他访问结点的代码, 所有不能调用delete.

>https://leetcode.com/problems/delete-leaves-with-a-given-value/discuss/484264/JavaC++Python-Recursion-Solution/431234  
1.Leetcode doesn't let you call delete on a node.  
2.Use nullptr instead of NULL  

```cpp
class Solution {
public:
    TreeNode* removeLeafNodes(TreeNode* &p, int target) {
        if (nullptr == p) {
            return p;
        }
        removeLeafNodes(p->left, target);
        removeLeafNodes(p->right, target);
        if (!p->left && !p->right && p->val == target) {
            // delete p;
            p = nullptr;
        }
        return p;
    }  
};
```

### 113. Path Sum II (Medium)
Given a binary tree and a sum, find all root-to-leaf paths where each path's sum equals the given sum.

Note: A leaf is a node with no children.

想法上比较简单, 回溯即可.  
扎心的是看到了提交记录, 上一次是四年前... 四年了我在干嘛...
![image.png](https://image-ca-1251921514.cos.ap-shanghai.myqcloud.com/img20200302170551.png)

```cpp
class Solution {
public:
    vector<vector<int>> pathSum(TreeNode* root, int sum) {
        vector<vector<int>> ret;
        vector<int> path;
        if (nullptr == root) {
            return ret;
        }
        dfs(root, ret, path, 0, sum);
        return ret;
        
    }
private:
    void dfs(TreeNode* p,vector<vector<int>> &ret, vector<int>& path,int c_sum, int sum) {
        if (nullptr == p) {
            return;
        }
        c_sum += p->val;
        path.push_back(p->val);
        if (!p->left && !p->right && c_sum == sum) {
            ret.push_back(path);
        }
        dfs(p->left, ret, path, c_sum, sum);
        dfs(p->right, ret, path, c_sum, sum);
        path.pop_back();
        
    }
};
```

### 437. Path Sum III (Easy)
![](https://img.shields.io/badge/-Easy-green)

You are given a binary tree in which each node contains an integer value.

Find the number of paths that sum to a given value.

The path does not need to start or end at the root or a leaf, but it must go downwards (traveling only from parent nodes to child nodes).

The tree has no more than 1,000 nodes and the values are in the range -1,000,000 to 1,000,000.

对每个结点都求一次Path sum
```cpp
class Solution {
public:
    int pathSum(TreeNode* root, int sum) {
        int cnt = 0;
        stack<TreeNode*> stk;
        stk.push(root);
        while (!stk.empty()) {
            TreeNode* p = stk.top();
            stk.pop();
            if (nullptr == p) {
                continue;
            }
            dfs(p, 0, sum, cnt);
            stk.push(p->left);
            stk.push(p->right);
        }
        
        return cnt;
    }
private:
    void dfs(TreeNode* p, int c_sum, int sum, int &cnt) {
        if (nullptr == p) {
            return;
        }
        c_sum += p->val;
        if (c_sum == sum) {
            ++cnt;
        }
        dfs(p->left, c_sum, sum, cnt);
        dfs(p->right, c_sum, sum, cnt);
        // dfs(p->left, 0, sum, cnt);
        // dfs(p->right, 0, sum, cnt);
    }
};
```

### 257. Binary Tree Paths (Easy)
![](https://img.shields.io/badge/-Easy-green)

Given a binary tree, return all root-to-leaf paths.

Note: A leaf is a node with no children.

比较简单, 回溯搞定. 在遍历到叶结点再将vector拼成string.

```cpp
class Solution {
public:
    vector<string> binaryTreePaths(TreeNode* root) {
        vector<string> ret;
        vector<int> path;
        dfs(root, path, ret);
        return ret;
    }
private:
    void dfs(TreeNode* p, vector<int> &path, vector<string> &ret, bool top=false) {
        if (nullptr == p) {
            return;
        }
        path.push_back(p->val);
        if (!p->left && !p->right) {
            
            string pathStr = to_string(path[0]);
            for (int i = 1; i < path.size(); ++i) {
                pathStr += "->" + to_string(path[i]);
            }
            ret.push_back(pathStr);
            // return;
        }
        dfs(p->left, path, ret);
        dfs(p->right, path, ret);
        path.pop_back();
    }
};
```
### 235. Lowest Common Ancestor of a Binary Search Tree
![](https://img.shields.io/badge/-Easy-green)

Given a binary search tree (BST), find the lowest common ancestor (LCA) of two given nodes in the BST.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”

题目限定了给出BST, 从BST的性质考虑, 要是两个结点的LCA, 其值肯定在指定的两个结点之间.  
根据BST的性质, 当前结点值不在区间内时, 递归向下查询. 遇到的一个满足条件的结点即为要找的LCA.

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (nullptr == root) {
            return nullptr;
        }
        int v1 = p->val, v2 = q->val;
        int minVal = min(v1, v2);
        int maxVal = max(v1, v2);
        return dfs(root, minVal, maxVal);
    }
private:
    TreeNode* dfs(TreeNode* p, int minVal, int maxVal) {
        if (p->val > maxVal) {
            return dfs(p->left, minVal, maxVal);
        }
        else if (p->val < minVal) {
            return dfs(p->right, minVal, maxVal);
        }
        return p;
    }
};
```

### 449. Serialize and Deserialize BST (Medium) 
![](https://img.shields.io/badge/-Medium-orange)

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary search tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary search tree can be serialized to a string and this string can be deserialized to the original tree structure.

The encoded string should be as compact as possible.

Note: Do not use class member/global/static variables to store states. Your serialize and deserialize algorithms should be stateless.

十分懵逼, 之前学过的重建二叉树全忘记了, 直接看讨论区.  
逛完讨论区回来, 注意到是BST, 序列化直接使用前序遍历, 反序列化时直接创建BST就行, 因为按照BST前序遍历的顺序, 建树仍然是原树结构从上至下的顺序.  
麻烦的地方就在C++处理字符串的方法, 如果是Python直接split转换数据类型就成.  
使用`stringsteam`也能比较方便地处理字符串序列.

```cpp
class Codec {
public:

    // Encodes a tree to a single string.
    string serialize(TreeNode* root) {
        ostringstream  ost;
        serialize(root, ost);
        return ost.str();
    }

    // Decodes your encoded data to tree.
    TreeNode* deserialize(string data) {
        if(data == "") return nullptr;
        istringstream ist(data);
        int val;
        ist >> val;
        TreeNode *root = new TreeNode(val);
        while (ist >> val) {
            insertBST(root, val);
        }
        return root;
    }
private:
    void serialize(TreeNode* p, ostringstream &ost) {
        if (nullptr == p) {
            return;
        }
        ost << p->val << " ";
        serialize(p->left, ost);
        serialize(p->right, ost);
    }
    void insertBST(TreeNode* p, int val) {
        if (p->val > val) {
            if (p->left == nullptr) {
                p->left = new TreeNode(val);
            }
            else {
                insertBST(p->left, val);
            }
        }
        else {
            if (p->right == nullptr) {
                p->right = new TreeNode(val);
            }
            else {
                insertBST(p->right, val);
            }
        }
    }
};

// Your Codec object will be instantiated and called as such:
// Codec codec;
// codec.deserialize(codec.serialize(root));
```

![](https://img.shields.io/badge/-Easy-green)