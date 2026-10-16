# 基础课程7：元组 tuple

运行案例：`python-learn1/drmo7.py`，沿用当前文件名。

关联知识：[[ai-ta-基础课程5补充]]、[[ai-ta-基础课程6补充]]

> [!important] 当前必学
> 元组是有序、不可变、允许重复元素的序列，可以保存不同类型的元素。
> 单元素元组必须有逗号：`(10,)`。`(10)` 只是整数表达式加括号。
> “不可变”限制元组直接保存的元素，不会递归冻结其中的列表、字典。

## 1. 列表、元组与字典的区别

| 类型 | 分类 | 常见用途 | 是否能原地增删改 |
| --- | --- | --- | --- |
| `list` | 可变序列 | 一批需要增删的记录 | 能 |
| `tuple` | 不可变序列 | 一组位置有含义、结构相对固定的数据 | 不能 |
| `dict` | 可变映射 | 根据字段名或键查值 | 能 |
| `str` | 不可变序列 | 文本 | 不能 |

字典即使保留插入顺序，也仍然是映射，不应称为序列。序列一般按位置索引访问，字典按键访问。

元组可用于坐标 `(x, y)`、姓名成绩对 `(name, score)` 等。不是所有“暂时不想修改的列表”都必须换成元组，选择应看数据含义。

## 2. 创建：逗号是关键

```python
record = ('Python', 'world', 98)
also_record = 'Python', 'world', 98
empty = ()
single = ('Python',)

print(type(record))    # <class 'tuple'>
print(type(single))    # <class 'tuple'>
print(type(('Python'))) # <class 'str'>
```

非空元组通常由逗号构成，括号用于分组和提高可读性；空元组使用 `()`。不要据此推导为“所有地方只加逗号都一样”，函数调用等语法仍需遵循各自规则。

```python
print(tuple())          # ()
print(tuple([1, 2]))    # (1, 2)
print(tuple('Python'))  # ('P', 'y', 't', 'h', 'o', 'n')
print(('Python',))      # ('Python',)：完整字符串作为一个元素
# tuple(10)             # TypeError：整数不能被逐项迭代
```

> [!tip] 你的创建案例
> `tuple(('Python', 'world', 98))` 合法，但内部已经是元组，直接写内部字面量即可。`tuple(existing_tuple)` 也不保证产生一个不同的新对象，不要把转换写法当作复制身份的保证。

## 3. 读取、切片、查询与遍历

```python
values = ('Python', 'JS', 'Python', 98)
print(values[0])              # Python
print(values[-1])             # 98
print(values[1:3])            # ('JS', 'Python')
print(len(values))            # 4
print('JS' in values)         # True
print('Java' not in values)   # True
print(values.count('Python')) # 2
print(values.index('Python')) # 0：第一次匹配的位置

for index, value in enumerate(values):
    print(index, value)
```

这些用法与列表相似：索引越界会抛出 `IndexError`，`index()` 找不到值会抛出 `ValueError`。切片仍遵循包含起点、不包含终点的规则。

元组没有 `append()`、`extend()`、`remove()`、`pop()`、`sort()` 等原地修改方法。

## 4. 不可变不等于变量不能重新赋值

```python
point = (10, 20)
original = point
point += (30,)

print(original)  # (10, 20)
print(point)     # (10, 20, 30)
```

这里相当于拼接元组，再让 `point` 绑定结果；原来的元组没有被追加元素。`point[0] = 99` 则会抛出 `TypeError`，因为它尝试修改元组本身。

> [!warning] 不用 id 变化概括“修改”
> 原地改变对象内容、让变量改指其他对象，是两种不同操作。不可变对象不能原地修改；重新赋值也不意味着每次都必须分配全新的对象。`id()` 反映身份，学习时重点看对象是否被修改、引用是否共享。

`del point` 删除名字绑定，不是删除元组中的某一项；`del point[0]` 则不允许。

## 5. 嵌套对象仍可能改变

```python
student = ('张三', ['JS'])
student[1].append('Python')
print(student)  # ('张三', ['JS', 'Python'])

# student[1] = []  # TypeError：不能把那个位置换成另一个列表
```

元组仍保存原来那个列表对象，变化的是列表内部内容，因此没有违反元组不可变的规则。

> [!warning] 转换不会递归复制
> `tuple(some_list)` 生成元组结构，但不会深拷贝其中的列表或字典。把容器转成元组，不等于获得完全独立、完全冻结的数据。

## 6. 打包、解包与星号收集

```python
record = '张三', 18  # 打包为一个元组
name, age = record  # 解包到两个名字
print(name, age)    # 张三 18

first, *middle, last = (10, 20, 30, 40)
print(first)       # 10
print(middle)      # [20, 30]：注意是 list
print(last)        # 40

a, b = 1, 2
a, b = b, a
print(a, b)        # 2 1
```

没有星号时，目标数量必须与元素数量匹配；一个解包目标列表中最多有一个星号收集目标。解包并不限于元组，也可以用于列表等可迭代对象。

上一课的 `for key, value in data.items()` 就是在解包每一组键值对。后续学习函数时，“返回多个值”也常用元组打包再解包，这里先认识联系。

## 7. 转换、拼接与排序

```python
numbers = (3, 1, 2)
editable = list(numbers)
editable[0] = 9
print(numbers)         # (3, 1, 2)
print(tuple(editable)) # (9, 1, 2)

print((1, 2) + (3,))  # (1, 2, 3)
print(('a',) * 3)     # ('a', 'a', 'a')
print(sorted(numbers))        # [1, 2, 3]：sorted 返回列表
print(tuple(sorted(numbers))) # (1, 2, 3)
```

拼接和重复不会原地修改元组。重复时元素引用也会重复；如果元素是可变列表，仍需注意共享引用，和第五课的列表重复问题类似。

## 8. 了解即可：括号生成的是元组吗？

```python
expression = (number ** 2 for number in range(1, 4))
print(type(expression))  # <class 'generator'>
print(tuple(expression)) # (1, 4, 9)
print(tuple(expression)) # ()：这个生成器已经被消费完
```

`(表达式 for ... in ...)` 是生成器表达式，不是“元组生成式”。它按迭代逐步产出值；需要元组时，使用 `tuple(...)` 收集，例如 `tuple(number ** 2 for number in range(1, 4))`。

生成器先知道区别即可，之后再学习迭代器、`yield` 与惰性计算。

## 9. 了解即可：元组作为字典键

```python
seats = {(1, 2): '张三', (1, 3): '李四'}
print(seats[(1, 2)])  # 张三：用排号和座号组合查找

# invalid = {('张三', []): 100}  # TypeError：其中的列表不可哈希
```

一个元组能否作为字典键，要看它的所有元素是否都可哈希。“元组不可变”不能直接推出“任何元组都能当键”。常见纯数字、字符串组成的元组可以；包含列表或字典的不行。

## 10. 与 JS / TS 的区别

| 内容 | Python 元组 | JS / TS 对照 |
| --- | --- | --- |
| 运行时类型 | 真正的 `tuple` 类型 | TS 元组在运行时仍是 JS 数组 |
| 元素位置替换 | 运行时不允许 | 普通 JS 数组可以修改 |
| TS 类型检查 | Python 不因写成元组就限定每个位置的静态类型 | TS 可用 `[string, number]` 描述位置类型 |
| 深层不可变 | 不保证 | TS `readonly` 主要约束类型检查，也不等于运行时深冻结 |

Python 元组的不可变机制不能用 JS 的 `const` 理解：`const` 约束变量重新赋值，而 Python 的普通变量仍能重新绑定，受限制的是元组对象的修改。

## 11. 小实践：用列表保存多条元组记录

```python
students = [('张三', 90), ('李四', 55), ('王五', 80)]
passed_names = []

for name, score in students:
    if score >= 60:
        passed_names.append(name)

print(passed_names)  # ['张三', '王五']
```

外层列表负责管理多条记录，内层元组表达固定的姓名、成绩位置关系。字段增多或顺序容易混淆时，字典常更清楚，例如 `{'name': '张三', 'score': 90}`。后续可再认识具名元组和数据类，不必现在展开。

## 12. 回顾练习

```python
one = (5)
two = (5,)
print(type(one), type(two))

original = ([1], 2)
alias = original
original[0].append(3)
original = original + (4,)
print(alias)
print(original)

first, *rest = (10, 20, 30)
print(rest, type(rest))
```

> [!question]- 展开查看答案
> - 第一行类型是 `<class 'int'>` 与 `<class 'tuple'>`，单元素元组关键在逗号。
> - `alias` 是 `([1, 3], 2)`：内部列表可以修改，别名仍引用原元组。
> - `original` 是 `([1, 3], 2, 4)`：拼接后重新绑定，原元组没有增加位置。
> - `rest` 是 `[20, 30]`，类型为 `list`。
