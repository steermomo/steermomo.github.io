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

### 872. Leaf-Similar Trees (Easy)
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