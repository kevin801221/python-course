## Python容器型別使用小技巧

Python中提供了非常豐富的容器型資料型別，大家最為熟悉的有`list`、`tuple`、`set`、`dict`等。下面為大家分享一些使用這些型別的小技巧，希望幫助大家寫出更加Pythonic的程式碼。

#### 1. 從字典中取最大

假設字典物件對應的變數名為`my_dict`。

- 取出最大值

    ```Python
    max(my_dict.values())
    ```

- 取值最大值的鍵

    ```Python
    max(my_dict, key=my_dict.get)
    ```

- 取出最大值的鍵和值

    ```python
     max(my_dict.items(), key=lambda x: x[1])
    ```

    或

    ```Python
    import operator
    
    max(my_dict.items(), key=operator.itemgetter(1))
    ```
    
    > **說明**：上面用到了`operator`模組的`itemgetter`函式，這個函式的的作用如下所示。在上面的程式碼中，`itemgetter`幫我們獲取到了二元組中的第2個元素。
    >
    > ```Python
    > def itemgetter(*items):
    >     if len(items) == 1:
    >         item = items[0]
    >         def g(obj):
    >             return obj[item]
    >     else:
    >         def g(obj):
    >             return tuple(obj[item] for item in items)
    >     return g
    > ```

#### 2. 統計列表元素出現次數

假設列表物件對應的變數名為`my_list`。

```Python
{x: my_list.count(x) for x in set(my_list)}
```

或

```Python
from itertools import groupby

{key: len(list(group)) for key, group in groupby(sorted(my_list))}
```

> **說明**：`groupby`函式會將相鄰相同元素分到一個組中，所以先用`sorted`函式排序就是為了將相同的元素放到一起。

或

```Python
from collections import Counter

dict(Counter(my_list))
```

#### 3. 截斷列表元素

假設列表物件對應的變數名為`my_list`，通常大家會想到用下面的方式來截斷列表。
```Python
my_list = my_list[:i]
my_list = my_list[j:]
```

然而，更好的方式使用下面的操作，大家可以認真想想為什麼。

```Python
del my_list[i:]
del my_list[:j]
```

#### 4. 按最長列表實現zip操作

Python的內建函式`zip`可以產生一個生成器物件，該生成器物件將兩個或多個可迭代物件的元素組裝到一起，如下所示。

```Python
list(zip('abc', [1, 2, 3, 4]))
```

執行上面的程式碼會得到一個如下所示的列表，相信大家也注意到了，列表中元素的個數是由`zip`函式中長度最小的可迭代物件決定的，所以下面的列表中只有3個元素。

```Python
[('a', 1), ('b', 2), ('c', 3)]
```

如果希望由`zip`函式中長度最大的可迭代物件來決定最終迭代出的元素個數，可以試一試`itertools`模組的`zip_longest`函式，其用法如下所示。

```Python
from itertools import zip_longest

list(zip_longest('abc', [1, 2, 3, 4]))
```

上面的程式碼建立出的列表物件如下所示。

```Python
[('a', 1), ('b', 2), ('c', 3), (None, 4)]
```

#### 5. 快速複製一個列表

如果希望快速複製一個列表物件，可以透過切片操作來實現，但是切片操作僅實現了淺複製，簡單的說就是切片建立了新的列表物件，但是新列表中的元素是和之前的列表共享的。如果希望實現深複製，可以使用`copy`模組的`deepcopy`函式。

- 淺複製

    ```Python
    thy_list = my_list[:]
    ```

    或

    ```Python
    import copy
    
    thy_list = copy.copy(my_list)
    ```

- 深複製

    ```Python
    import copy
    
    thy_list = copy.deepcopy(my_list)
    ```

#### 6. 對兩個或多個列表對應元素進行操作

Python內建函式中的`map`函式可以對一個可迭代物件中的元素進行“對映”操作，這個函式在批次處理資料時非常有用。但是很多人都不知道，這個函式還可以作用於多個可迭代物件，透過傳入的函式對多個可迭代物件中的對應元素進行處理，如下所示。

```Python
my_list = [11, 13, 15, 17]
thy_list = [2, 4, 6, 8, 10]
list(map(lambda x, y: x + y, my_list, thy_list))
```

上面的操作會得到如下所示的列表。

```Python
[13, 17, 21, 25]
```

當然，同樣的操作也可以用`zip`函式配合列表生成式來完成。

```Python
my_list = [11, 13, 15, 17]
thy_list = [2, 4, 6, 8, 10]
[x + y for x, y in zip(my_list, thy_list)]
```

#### 7. 處理列表中的空值和零值

假設列表物件對應的變數名為`my_list`，如果列表中有空值（`None`）和零值，我們可以用下面的方式去掉空值和零值。

```Python
list(filter(bool, my_list))
```

對應的列表生成式語法如下所示。

```Python
[x for x in my_list if x]
```

#### 8. 從巢狀列表中抽取指定列

假設`my_list`是一個如下所示的巢狀列表，該巢狀列表可以用來表示數學上的矩陣，如果要取出矩陣第一列的元素構成一個列表，我們可以這樣寫。

```Python
my_list = [
    [1, 1, 2, 2],
    [5, 6, 7, 8],
    [3, 3, 4, 4],
]
col1, *_ = zip(*my_list)
list(col1)
```

這裡我們會得到一個如下所示的列表，剛好是矩陣的第一列。

```Python
[1, 5, 3]
```

以此類推，如果想取出矩陣第二列的元素構成一個列表，可以用如下所示的方法。

```Python
_, col2, *_ = zip(*my_list)
list(col2)
```

至此，如果要實現矩陣的轉置操作，我們也可以按照上面的思路寫出下面的程式碼。

```Python
[list(x) for x in zip(*my_list)]
```

經過上面的操作，我們會得到如下所示的列表。

```Python
[[1, 5, 3], 
 [1, 6, 3], 
 [2, 7, 4], 
 [2, 8, 4]]
```