Title: Feature Engineering for Machine Learning in Python
Date: 2019-09-03 21:20
Modified: 2019-09-03 21:20
Tags: DNS, CNAME, namecheap, 
Slug: fe-in-python
Summary: 

嚯嚯嚯

<br>
### Chapter 1, 'Creating Features'.
<br>
### Selecting specific data types
```python
# Create subset of only the numeric columns
so_numeric_df = so_survey_df.select_dtypes(include=['int', 'float'])

# Print the column names contained in so_survey_df_num
print(so_numeric_df.columns)
```

<br>
### Dealing with categorical features

- One-hot encoding
    - n features for n categories
    - Explainable
- Dummy encoding
    - n-1 features for n categories
    - Necessary information

```Python
# One hot
pd.get_dummies(df, columns=['Country'], prefix='C')

# Dummy
pd.get_dummies(df, columns=['Country'], drop_first=True, prefix='C')
```

Limiting columns
```Python
# 将出现次数少于10次的国家归入Other
# Create a series out of the Country column
countries = so_survey_df['Country']

# Get the counts of each category
country_counts = countries.value_counts()

# Create a mask for only categories that occur less than 10 times
mask = countries.isin(country_counts[country_counts < 10].index)

# Label all other categories as Other
countries[mask] = 'Other'

# Print the updated category counts
print(countries.value_counts())
```

<br>

### Numeric variables

- Binarizing columns
- Bining numeric variables

```Python
# 等间距cut
so_survey_df['equal_binned'] = pd.cut(so_survey_df['ConvertedSalary'], 5)

# 指定边界cut
# Import numpy
import numpy as np

# Specify the boundaries of the bins
bins = [-np.inf, 10000, 50000, 100000, 150000, np.inf]

# Bin labels
labels = ['Very low', 'Low', 'Medium', 'High', 'Very high']

# Bin the continuous variable ConvertedSalary using these boundaries
so_survey_df['boundary_binned'] = pd.cut(so_survey_df['ConvertedSalary'], 
                                         bins=bins, labels=labels)

# Print the first 5 rows of the boundary_binned column
print(so_survey_df[['boundary_binned', 'ConvertedSalary']].head())
```

<br>
### Missing data

<br>
Listwise deletion
```python
# drop row at least one na
df.dropna(how='any')

# drop specific columns
df.dropna(subset=[])
```
<br>

Fillna

```python
df['cl'].fillna(
    value='xxx', inplace=True
)
```

<br>
Fill continuous missing values

- Mean
- Median

<br>
### Dealing with other data issues

Bad character
- Numeric column has nan or other characters
- convert data type
- use isna find stray characters

<br>
Data distributions
![image.png](http://ww1.sinaimg.cn/large/dd456925gy1g6nw890s5ej20jb0adgmd.jpg)

```python
# box plot
# Create a boxplot of two columns
so_numeric_df[['Age', 'Years Experience']].boxplot()
plt.show()


#
```


<br>
### Scaling and transformations

长尾数据使用log变换

<br>

### Removing outliers

Use quantile
```python
# Find the 95th quantile
quantile = so_numeric_df['ConvertedSalary'].quantile(0.95)

# Trim the outliers
trimmed_df = so_numeric_df[so_numeric_df['ConvertedSalary'] < quantile]

```


<br>
### Scaling and transforming new data

Don't use test data. Avoid data leakage.


<br>
### Encoding text


clean text
```python
# Replace all non letter characters with a whitespace
speech_df['text_clean'] = speech_df['text'].str.replace('[^a-zA-Z]', ' ')

# Change to lower case
speech_df['text_clean'] = speech_df['text_clean'].str.lower()

# Print the first 5 rows of the text_clean column
print(speech_df['text_clean'].head())
```
<br>
Heigh level feature
```python
# Find the length of each text
speech_df['char_cnt'] = speech_df['text_clean'].str.len()

# Count the number of words in each text
speech_df['word_cnt'] = speech_df['text_clean'].str.split().str.len()

# Find the average length of word
speech_df['avg_word_length'] = speech_df.char_cnt / speech_df.word_cnt

# Print the first 5 rows of these columns
print(speech_df[['text_clean', 'char_cnt', 'word_cnt', 'avg_word_length']])
```

<br>
Word count
```python
# Import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer

# Instantiate CountVectorizer
cv = CountVectorizer()

# Fit the vectorizer
cv.fit(speech_df['text_clean'])

# Print feature names
print(cv.get_feature_names())
```

<br>
### Term frequency-inverse document frequency
这部分都不太想看了... 用不到的时候就会忘记 