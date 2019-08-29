Title: Winning a kaggle Competition 教你如何噶韭菜
Date: 2019-08-26 18:16
Modified: 2019-08-26 18:16
Category: Python, Machine Learning,
Tags: kaggle, 
Slug: misc-about-kaggle
Summary: 

我又迷信了呀....

<img src="{static}/images/sticker_newthing.webp" style="max-width: 50%">



看了DataCamp的[Winning a Kaggle Competition in Python ](https://www.datacamp.com/courses/winning-a-kaggle-competition-in-python/continue), 觉得有点用的就是介绍Target encoding的那部分. 丫的压根就没教我怎么Winning.  我肯定也是被收智商税的一类人, 幸好课程是白嫖的. Visual Studio Dev Essentials 送了俩月的DataCamp订阅.



唯一让我觉得新鲜的, 就是target encoding, 因为之前没看过. 其他的都是泛泛而谈.



<br>

#### Target encoding

Mean target encoding

- smoothing
- 

1. 在训练集上计算均值, 应用到测试集上
2. oof, 在某个kfold上计算, 应用到(k-1)fold上


```Python
# 在训练集上计算均值, 在测试集上应用mean target encoding
def test_mean_target_encoding(train, test, target, categorical, alpha=5):
    # Calculate global mean on the train data
    global_mean = train[target].mean()
    
    # Group by the categorical feature and calculate its properties
    train_groups = train.groupby(categorical)
    category_sum = train_groups[target].sum()
    category_size = train_groups.size()
    
    # Calculate smoothed mean target statistics
    train_statistics = (category_sum + global_mean * alpha) / (category_size + alpha)
    
    # Apply statistics to the test data and fill new categories
    test_feature = test[categorical].map(train_statistics).fillna(global_mean)
    return test_feature.values


# 在训练集上oof, 应用mean target encoding
def train_mean_target_encoding(train, target, categorical, alpha=5):
    # Create 5-fold cross-validation
    kf = KFold(n_splits=5, random_state=123, shuffle=True)
    train_feature = pd.Series(index=train.index)
    
    # For each folds split
    for train_index, test_index in kf.split(train):
        cv_train, cv_test = train.iloc[train_index], train.iloc[test_index]
      
        # Calculate out-of-fold statistics and apply to cv_test
        cv_test_feature = test_mean_target_encoding(cv_train, cv_test, target, categorical, alpha)
        
        # Save new feature for this particular fold
        train_feature.iloc[test_index] = cv_test_feature       
    return train_feature.values


#调用上述两个函数, 分别对训练集和测试集做target encoding
def mean_target_encoding(train, test, target, categorical, alpha=5):
  
    # Get test feature
    test_feature = test_mean_target_encoding(train, test, target, categorical, alpha)
    
    # Get train feature
    train_feature = train_mean_target_encoding(train, target, categorical, alpha)
    
    # Return new features to add to the model
    return train_feature, test_feature
```

在K-fold CV中使用 target encoding
```Python
# Create 5-fold cross-validation
kf = KFold(n_splits=5, random_state=123, shuffle=True)

# For each folds split
for train_index, test_index in kf.split(bryant_shots):
    cv_train, cv_test = bryant_shots.iloc[train_index], bryant_shots.iloc[test_index]

    # Create mean target encoded feature
    cv_train['game_id_enc'], cv_test['game_id_enc'] = mean_target_encoding(train=cv_train,
                                                                           test=cv_test,
                                                                           target='shot_made_flag',
                                                                           categorical='game_id',
                                                                           alpha=5)
    # Look at the encoding
    print(cv_train[['game_id', 'shot_made_flag', 'game_id_enc']].sample(n=1))
```

<br>
### Missing Data


Numerical data
- Mean/Median imputation
- Constant value imputation (-999)


Categorical data
- 高频项
- 新值 (MISS)


sklearn.impute SimpleImputer
```Python
# Import SimpleImputer
from sklearn.impute import SimpleImputer

# Create mean imputer
mean_imputer = SimpleImputer(strategy='mean')

# Price imputation
rental_listings[['price']] = mean_imputer.fit_transform(rental_listings[['price']])

# Import SimpleImputer
from sklearn.impute import SimpleImputer

# Create constant imputer
constant_imputer = SimpleImputer(strategy='constant', fill_value='MISSING')

# building_id imputation
rental_listings[['building_id']] = constant_imputer.fit_transform(rental_listings[['building_id']])
```

<br>
### Baseline Model



<br>
### Hyperparameter tuning

|     Competition type     | Feature engineering | Hyperparameter  optimization |
| :----------------------: | :-----------------: | :--------------------------: |
| Classic Machine Learning |         +++         |              +               |
|      Deep Learning       |          -          |             +++              |



- Grid search
- Random search
- Bayesian optimization



<br>

### Model ensemble



- blending
  - 多个模型， 取平均
- stacking
  - 多层预测
  - 第一层模型的预测结果， 作为第二层模型的输入特征



简单的blending

```Python
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

# Train a Gradient Boosting model
gb = GradientBoostingRegressor().fit(train[features], train['fare_amount'])

# Train a Random Forest model
rf = RandomForestRegressor().fit(train[features], train['fare_amount'])

# Make predictions on the test data
test['gb_pred'] = gb.predict(test[features])
test['rf_pred'] = rf.predict(test[features])

# Find mean of model predictions
test['blend'] = (test['gb_pred'] + test['rf_pred']) / 2
print(test[['gb_pred', 'rf_pred', 'blend']].head(3))
```



简单的stacking

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

# Split train data into two parts
part_1, part_2 = train_test_split(train, test_size=0.5, random_state=123)

# Train a Gradient Boosting model on Part 1
gb = GradientBoostingRegressor().fit(part_1[features], part_1.fare_amount)

# Train a Random Forest model on Part 1
rf = RandomForestRegressor().fit(part_1[features], part_1.fare_amount)


# Make predictions on the Part 2 data
part_2['gb_pred'] = gb.predict(part_2[features])
part_2['rf_pred'] = rf.predict(part_2[features])

# Make predictions on the test data
test['gb_pred'] = gb.predict(test[features])
test['rf_pred'] = rf.predict(test[features])


from sklearn.linear_model import LinearRegression

# Create linear regression model without the intercept
lr = LinearRegression(fit_intercept=False)

# Train 2nd level model in the part_2 data
lr.fit(part_2[['gb_pred', 'rf_pred']], part_2.fare_amount)

# Make stacking predictions on the test data
test['stacking'] = lr.predict(test[['gb_pred', 'rf_pred']])

# Look at the model coefficients
print(lr.coef_)
```





<br>

### Tips

1. Save folds
2. Save model runs
3. Save model predictions
4. Save performance results