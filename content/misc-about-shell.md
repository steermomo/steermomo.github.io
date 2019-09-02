Title: Introduction to Shell for Data Science
Date: 2019-08-26 18:19
Modified: 2019-08-26 18:19
Category: Linux, Shell,
Tags: Shell, 
Slug: Introduction-to-Shell-for-Data-Science
Summary: 

emm, 这个有点太简单了
<img src="{static}/images/sticker_try.webp" style="max-width: 30%">

<br>

pwd (short for "print working directory")  
ls (which is short for "listing")  
cd (which stands for "change directory").  

cp&mv, 可以指定最后一个参数为文件夹  

<br>

## Chapter 2, 'Manipulating data'.

### less 
可同时打开多个文件
:n, :p, :q

### head

### ls
ls -F prints a / after the name of every directory, * after the name of every runnable program


### cut
```bash
cut -f 2-5, 8 -d , values.csv
# "select columns 2 through 5 and columns 8, using comma as the separator"
# 下标从1开始
```
<br>
### How can I repeat commands?
```bash
!head or !cut
!55
```
<br>
### How can I select lines containing specific values?
`head` and `tail` select rows, `cut` selects columns, and `grep` selects lines according to what they contain.

grep flags

- -c: print a count of matching lines rather than the lines themselves
- -h: do not print the names of files when searching multiple files
- -i: ignore case (e.g., treat "Regression" and "regression" as matches)
- -l: print the names of files that contain matches, not the matches
- -n: print line numbers for matching lines
- -v: invert the match, i.e., only show lines that don't match

<br>
### Why isn't it always safe to treat data as text?
paste 命令

<br>
## Chapter 3, 'Combining tools'.
<br>

wc (short for "word count") prints the number of characters, words, and lines 

```bash
grep "July 2017" seasonal/spring.csv | wc -l
```
<br>
### How can I sort lines of text?
`sort`, By default it does this in ascending alphabetical order.
but the flags -n and -r can be used to sort numerically and reverse the order of its output, while -b tells it to ignore leading blanks and -f tells it to fold case (i.e., be case-insensitive).
<br>
### How can I remove duplicate lines?
`unique`,  removes adjacent duplicated lines
```bash
cut -d , -f 2 seasonal/winter.csv | grep -v Tooth | sort | uniq -c
```
<br>
## Chapter 4, 'Batch processing'.
<br>
### How does the shell store information?
`set` 获取环境变量
<br>
### How can I repeat a command many times?
```bash
for ..vai.. in ..list..; do ..body.. ; done
```
<br>
### How can I record the names of a set of files?
> datasets=xx/*.csv  
> for filename in $datasets;...
<br>
### How can I do many things in a single loop?
separate them with semi-colons:

<br>
## Chapter 5, 'Creating new tools'.
<br>
### How can I record what I just did?
1. run history
2. tail -n 10
3. redirect to a file

### How can I pass filenames to scripts?
`$@`:  all of the command-line parameters given to the script
As well as `$@`, the shell lets you use `$1`, `$2`


### loops in a shell script
```bash
# Print the first and last data records of each file.
for filename in $@
do
    head -n 2 $filename | tail -n 1
    tail -n 1 $filename
done
```