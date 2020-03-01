Title: LeetCode-Tree
Date: 2020-02-29 18:20
Modified: 2020-03-01 18:20
Category: LeetCode
Tags: leetcode, c++
Slug: leetcode-tree


![](https://docs.google.com/spreadsheets/d/1SbpY-04Cz8EWw3A_LBUmDEXKUMO31DBjfeMoA0dlfIA/edit#gid=126913158)

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