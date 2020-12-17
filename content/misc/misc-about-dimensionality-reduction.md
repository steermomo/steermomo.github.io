Title: Dimensionality Reduction in Python - 这不是迷信
Date: 2019-08-26 18:18
Modified: 2019-08-26 18:18
Category: Python
Tags: PCA,Python, Machine Learning 
Slug: dimensionality-reduction-in-python
Summary: 

这次不是迷信...

因为有门课需要做笔记, 西瓜书第十章,降维与度量学习, 看到DataCamp上有Dimensionality Reduction in Python, 刚好拿来交差. 

Update: 看完感觉, 真水啊, 我学了个seaborn的pairplot跟heatmap.

<img src="{static}/images/sticker_writecode.webp" style="max-width: 30%">



看了DataCamp的[Dimensionality Reduction in Python ](https://www.datacamp.com/courses/dimensionality-reduction-in-python)


### Feature selection vs feature extraction

- Feature selection
    - 只选择部分特征
- Feature extraction
    - 计算, 提取, 生成新特征


```Python
# Create a pairplot and color the points using the 'Gender' feature
sns.pairplot(ansur_df_1, hue='Gender', diag_kind='hist')

# Show the plot
plt.show()
```
<img src="http://ww1.sinaimg.cn/large/dd456925ly1g6gymoje4qj20np0nptcl.jpg" style="max-width: 60%">
<!-- ![](http://ww1.sinaimg.cn/large/dd456925ly1g6gymoje4qj20np0nptcl.jpg) -->

```Python
# Remove one of the redundant features
reduced_df = ansur_df_1.drop('body_height', axis=1)

# Create a pairplot and color the points using the 'Gender' feature
sns.pairplot(reduced_df, hue='Gender')

# Show the plot
plt.show()
```
<img src="http://ww1.sinaimg.cn/large/dd456925ly1g6gypupvl9j20np0npgox.jpg" style="max-width: 60%">
<!-- ![](http://ww1.sinaimg.cn/large/dd456925ly1g6gypupvl9j20np0npgox.jpg) -->

<br>

### t-SNE visualization of high-dimensional data

Fitting t-SNE to the ANSUR data

这个数据集记录了一些人体的指标

```Python
# Non-numerical columns in the dataset
non_numeric = ['Branch', 'Gender', 'Component']

# Drop the non-numerical columns from df
df_numeric = df.drop(non_numeric, axis=1)

# Create a t-SNE model with learning rate 50
m = TSNE(50)

# Fit and transform the t-SNE model on the numeric dataset
tsne_features = m.fit_transform(df_numeric)
print(tsne_features.shape)

# Color the points according to Army Component
sns.scatterplot(x="x", y="y", hue='Component', data=df)

# Show the plot
plt.show()
```

![](http://ww1.sinaimg.cn/large/dd456925ly1g6gz2a3qqej20np0nptik.jpg)


<br>
### The curse of dimensionality


<br>
### Features with missing values or little variance

```Python
from sklearn.feature_selection import VarianceThreshold

# Create a VarianceThreshold feature selector
sel = VarianceThreshold(threshold=0.001)

# Fit the selector to normalized head_df
sel.fit(head_df / head_df.mean())

# Create a boolean mask
mask = sel.get_support()

# Apply the mask to create a reduced dataframe
reduced_df = head_df.loc[:, mask]

print("Dimensionality reduced from {} to {}.".format(head_df.shape[1], reduced_df.shape[1]))
```

<br>

### Pairwise correlation

Seaborn pairplot

```Python
# Create the correlation matrix
corr = ansur_df.corr()

# Generate a mask for the upper triangle 
mask = np.triu(np.ones_like(corr, dtype=bool))

# Add the mask to the heatmap
sns.heatmap(corr, mask=mask, cmap=cmap, center=0, linewidths=1, annot=True, fmt=".2f")
plt.show()
```
<img src="http://ws1.sinaimg.cn/mw690/dd456925ly1g6hpd7tf6uj20np0npwfg.jpg" style="max-width: 60%">
<!-- ![image](http://ws1.sinaimg.cn/mw690/dd456925ly1g6hpd7tf6uj20np0npwfg.jpg) -->



<br>
### Removing highly correlated features

<br>
### Selecting features for model performance

Pima Indians diabetes dataset

Automatic Recursive Feature Elimination

```Python
# Create the RFE with a LogisticRegression estimator and 3 features to select
rfe = RFE(estimator=LogisticRegression(), n_features_to_select=3, verbose=1)

# Fits the eliminator to the data
rfe.fit(X_train, y_train)

# Print the features and their ranking (high = dropped early on)
print(dict(zip(X.columns, rfe.ranking_)))

# Print the features that are not eliminated
print(X.columns[rfe.support_])

# Calculates the test set accuracy
acc = accuracy_score(y_test, rfe.predict(X_test))
print("{0:.1%} accuracy on test set.".format(acc)) 
```

<br>
### Tree-based feature selection

Recursive Feature Elimination with random forests
```Python
# Set the feature eliminator to remove 2 features on each step
rfe = RFE(estimator=RandomForestClassifier(), n_features_to_select=2, step=2, verbose=1)

# Fit the model to the training data
rfe.fit(X_train, y_train)

# Create a mask
mask = rfe.support_

# Apply the mask to the feature dataset X and print the result
reduced_X = X.loc[:, mask]
print(reduced_X.columns)
```

<br>
### Regularized linear regression
```Python
# Find the highest alpha value with R-squared above 98%
la = Lasso(0.1, random_state=0)

# Fits the model and calculates performance stats
la.fit(X_train_std, y_train)
r_squared = la.score(X_test_std, y_test)
n_ignored_features = sum(la.coef_ == 0)

# Print peformance stats 
print("The model can predict {0:.1%} of the variance in the test set.".format(r_squared))
print("{} out of {} features were ignored.".format(n_ignored_features, len(la.coef_)))
```

<br>
### Combining feature selectors

LassoCV
使用3个模型, 分别去做feature select, 投票后的结果, 作为单个模型特征选择的
```Python
from sklearn.linear_model import LassoCV

# Create and fit the LassoCV model on the training set
lcv = LassoCV()
lcv.fit(X_train, y_train)
print('Optimal alpha = {0:.3f}'.format(lcv.alpha_))

# Calculate R squared on the test set
r_squared = lcv.score(X_test, y_test)
print('The model explains {0:.1%} of the test set variance'.format(r_squared))

# Create a mask for coefficients not equal to zero
lcv_mask = lcv.coef_ != 0
print('{} features out of {} selected'.format(sum(lcv_mask), len(lcv_mask)))

from sklearn.feature_selection import RFE
from sklearn.ensemble import GradientBoostingRegressor

# Select 10 features with RFE on a GradientBoostingRegressor, drop 3 features on each step
rfe_gb = RFE(estimator=GradientBoostingRegressor(), 
             n_features_to_select=10, step=3, verbose=1)
rfe_gb.fit(X_train, y_train)

# Calculate the R squared on the test set
r_squared = rfe_gb.score(X_test, y_test)
print('The model can explain {0:.1%} of the variance in the test set'.format(r_squared))

# Assign the support array to gb_mask
gb_mask = rfe_gb.support_

from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor

# Select 10 features with RFE on a RandomForestRegressor, drop 3 features on each step
rfe_rf = RFE(estimator=RandomForestRegressor(), 
             n_features_to_select=10, step=3, verbose=1)
rfe_rf.fit(X_train, y_train)

# Calculate the R squared on the test set
r_squared = rfe_rf.score(X_test, y_test)
print('The model can explain {0:.1%} of the variance in the test set'.format(r_squared))

# Assign the support array to gb_mask
rf_mask = rfe_rf.support_


# Sum the votes of the three models
votes = np.sum([lcv_mask, rf_mask, gb_mask], axis=0)

# Sum the votes of the three models
votes = np.sum([lcv_mask, rf_mask, gb_mask], axis=0)

# Create a mask for features selected by all 3 models
meta_mask = votes >= 3

# Apply the dimensionality reduction on X
X_reduced = X.loc[:, meta_mask]

# Plug the reduced dataset into a linear regression pipeline
X_train, X_test, y_train, y_test = train_test_split(X_reduced, y, test_size=0.3, random_state=0)
lm.fit(scaler.fit_transform(X_train), y_train)
r_squared = lm.score(scaler.transform(X_test), y_test)
print('The model can explain {0:.1%} of the variance in the test set using {1:} features.'.format(r_squared, len(lm.coef_)))


```



<br>
### Feature extraction


<br>
### Principal component analysis

4 feature sample of the ANSUR dataset
```Python
# Create a pairplot to inspect ansur_df
sns.pairplot(ansur_df)

plt.show()
```
<img src="http://ws2.sinaimg.cn/mw690/dd456925ly1g6hraamp2ij20np0npdly.jpg" style="max-width: 60%">
<!-- ![image](http://ws2.sinaimg.cn/mw690/dd456925ly1g6hraamp2ij20np0npdly.jpg) -->



```Python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Create the scaler
scaler = StandardScaler()
ansur_std = scaler.fit_transform(ansur_df)

# Create the PCA instance and fit and transform the data with pca
pca = PCA()
pc = pca.fit_transform(ansur_std)
pc_df = pd.DataFrame(pc, columns=['PC 1', 'PC 2', 'PC 3', 'PC 4'])

# Create a pairplot of the principal component dataframe
sns.pairplot(pc_df)
plt.show()
```

<img src="http://wx4.sinaimg.cn/mw690/dd456925ly1g6hrdxcyjjj20np0npn40.jpg" style="max-width: 60%">
<!-- ![image](http://wx4.sinaimg.cn/mw690/dd456925ly1g6hrdxcyjjj20np0npn40.jpg) -->


PCA on larger dataset.
13 dimensions
```Python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Scale the data
scaler = StandardScaler()
ansur_std = scaler.fit_transform(ansur_df)

# Apply PCA
pca = PCA()
pca.fit(ansur_std)

# Inspect the explained variance ratio per component
print(pca.explained_variance_ratio_)
# [0.61449404 0.19893965 0.06803095 0.03770499 0.03031502 0.0171759
#  0.01072762 0.00656681 0.00634743 0.00436015 0.0026586  0.00202617
#  0.00065268]

# Print the cumulative sum of the explained variance ratio
print(pca.explained_variance_ratio_.cumsum())

# [0.61449404 0.81343368 0.88146463 0.91916962 0.94948464 0.96666054
#  0.97738816 0.98395496 0.99030239 0.99466254 0.99732115 0.99934732
#  1.        ]
```


<br>
### PCA applications

> class sklearn.decomposition.PCA(n_components=None, copy=True, whiten=False, svd_solver=’auto’, tol=0.0, iterated_power=’auto’, random_state=None)[source]¶

> Attributes:components_, explained_variance_ratio_

Understanding the components
```Python
# Build the pipeline
pipe = Pipeline([('scaler', StandardScaler()),
        		 ('reducer', PCA(n_components=2))])

# Fit it to the dataset and extract the component vectors
pipe.fit(poke_df)
vectors = pipe.steps[1][1].components_.round(2)

# Print feature effects
print('PC 1 effects = ' + str(dict(zip(poke_df.columns, vectors[0]))))
print('PC 2 effects = ' + str(dict(zip(poke_df.columns, vectors[1]))))

    #PC 1 effects = {'Sp. Atk': 0.46, 'Speed': 0.34, 'HP': 0.39, #'Defense': 0.36, 'Attack': 0.44, 'Sp. Def': 0.45}
    #PC 2 effects = {'Sp. Atk': -0.31, 'Speed': -0.67, 'HP': 0.08, #'Defense': 0.63, 'Attack': -0.01, 'Sp. Def': 0.24}
```


PCA for feature exploration
```Python
pipe = Pipeline([('scaler', StandardScaler()),
                 ('reducer', PCA(n_components=2))])

# Fit the pipeline to poke_df and transform the data
pc = pipe.fit_transform(poke_df)

# Add the 2 components to poke_cat_df
poke_cat_df['PC 1'] = pc[:, 0]
poke_cat_df['PC 2'] = pc[:, 1]

# Use the Type feature to color the PC 1 vs PC 2 scatterplot
sns.scatterplot(data=poke_cat_df, 
                x='PC 1', y='PC 2', hue='Type')
plt.show()
```
![image](http://ws2.sinaimg.cn/mw690/dd456925ly1g6hrtrt89ij20np0np0wj.jpg)

使用2个主成分
```Python
# Build the pipeline
pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('reducer', PCA(n_components=2)),
        ('classifier', RandomForestClassifier(random_state=0))])

# Fit the pipeline to the training data
pipe.fit(X_train, y_train)

# Score the accuracy on the test set
accuracy = pipe.score(X_test, y_test)

# Prints the model accuracy
print('{0:.1%} test set accuracy'.format(accuracy))

# 95.8%
```

使用3个主成分
```Python
# 95.0%
```


<br>
### Principal Component selection


Selecting the proportion of variance to keep
```Python
# Pipe a scaler to PCA selecting 80% of the variance
pipe = Pipeline([('scaler', StandardScaler()),
        		 ('reducer', PCA(n_components=0.8))])

# Fit the pipe to the data
pipe.fit(ansur_df)

print('{} components selected'.format(len(pipe.steps[1][1].components_)))

#> 11 components selected

pipe = Pipeline([('scaler', StandardScaler()),
        		 ('reducer', PCA(n_components=0.9))])

# Fit the pipe to the data
pipe.fit(ansur_df)

print('{} components selected'.format(len(pipe.steps[1][1].components_)))

#> 23 components selected
```

Choosing the number of components
Plot the explained variance ratio.
```Python
# Pipeline a scaler and pca selecting 10 components
pipe = Pipeline([('scaler', StandardScaler()),
        		 ('reducer', PCA(n_components=10))])

# Fit the pipe to the data
pipe.fit(ansur_df)

# Plot the explained variance ratio
plt.plot(pipe.steps[1][1].explained_variance_ratio_)

plt.xlabel('Principal component index')
plt.ylabel('Explained variance ratio')
plt.show()
```

<img src="http://ws3.sinaimg.cn/mw690/dd456925gy1g6hs52a6juj20np0npwfc.jpg" style="max-width: 50%">
<!-- ![image](http://ws3.sinaimg.cn/mw690/dd456925gy1g6hs52a6juj20np0npwfc.jpg) -->


PCA for image compression
```Python
plot_digits(X_test)
```

```Python
# Transform the input data to principal components
pc = pipe.transform(X_test)

# Prints the number of features per dataset
print("X_test has {} features".format(X_test.shape[1]))
print("pc has {} features".format(pc.shape[1]))

# X_test has 784 features
# pc has 78 features

X_rebuilt = pipe.inverse_transform(pc)

# Prints the number of features
print("X_rebuilt has {} features".format(X_rebuilt.shape[1]))
#> X_rebuilt has 784 features
```


|                             原图                             |                            重建后                            |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![image](http://wx4.sinaimg.cn/mw690/dd456925ly1g6hs6m92tej20np0npabd.jpg) | ![image](http://ws4.sinaimg.cn/mw690/dd456925ly1g6hs92p1daj20np0npac0.jpg) |

