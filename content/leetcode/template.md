Title: LeetCode-Tree
Date: 2020-02-29 18:20
Modified: 2020-03-01 18:20
Category: LeetCode
Tags: leetcode, c++
Slug: leetcode-tree




### 572. Subtree of Another Tree (Easy)

Given two non-empty binary trees s and t, check whether tree t has exactly the same structure and node values with a subtree of s. A subtree of s is a tree consists of a node in s and all of this node's descendants. The tree s could also be considered as a subtree of itself.

#### Solution
直接两个套两个递归函数就成, 再加上边界检查就过了.
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