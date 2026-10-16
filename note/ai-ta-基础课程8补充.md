# 基础课程8：集合 set

运行案例：`python-learn1/demo8.py`。

关联知识：[[ai-ta-基础课程5补充]]、[[ai-ta-基础课程6补充]]、[[ai-ta-基础课程7补充]]

> [!important] 当前必学
> 集合是没有重复元素的容器，`set` 可修改，但不提供位置索引或切片。
> 集合不保证插入顺序，也不自动排序，不要依赖打印或遍历顺序。
> 空集合写 `set()`；`{}` 是空字典。
> 集合元素必须可哈希，与字典键的要求相似。

## 1. 创建：花括号与 set()

```python
numbers = {3, 1, 2, 2}
print(type(numbers))       # <class 'set'>
print(len(numbers))        # 3
print(sorted(numbers))     # [1, 2, 3]：排序后的展示结果是 list
print(type({}))            # <class 'dict'>
print(type(set()))         # <class 'set'>
print(sorted(set('banana'))) # ['a', 'b', 'n']
```

`set('abc')` 逐字符创建集合，`{'abc'}` 则只有一个完整字符串元素。`set()` 接收可迭代对象，例如列表、字符串、`range`；整数不是可迭代对象，`set(10)` 会报 `TypeError`。

> [!warning] 无序不是“每次都随机打乱”
> 某次打印恰好有规律，不代表集合承诺那个顺序；也不能依赖 `list(set(values))` 保留原顺序。
> 本课用 `sorted()` 展示同类型元素，是为了输出可核对，不代表集合本身有序。混合不可比较的类型也可能无法直接排序。

## 2. 查询与遍历

```python
skills = {'Python', 'JS'}
print('Python' in skills)  # True
print('Java' not in skills) # True
print(bool(set()))         # False：空集合为假

for skill in sorted(skills):
    print(skill)           # JS，然后 Python：按排序后的列表遍历

# skills[0]                # TypeError：没有位置索引
```

需要经常判断“是否出现过”或“不关心顺序的去重”时，集合很自然。哈希查找通常比逐个扫描长列表更适合反复成员判断，但不代表任何数据规模、任何操作都更快，不必为少量数据过度优化。

## 3. 增加：add 与 update

| 操作 | 含义 | 返回值 |
| --- | --- | --- |
| `s.add(value)` | 添加一个可哈希元素，已存在则不重复添加 | `None` |
| `s.update(values)` | 逐个添加可迭代对象中的元素 | `None` |

```python
letters = set()
letters.add('abc')
print(sorted(letters))  # ['abc']

letters = set()
letters.update('abc')
print(sorted(letters))  # ['a', 'b', 'c']
```

与列表的 `append` / `extend` 可作用途对照，但集合有去重和可哈希要求。不能直接 `s.add([1, 2])`，可以 `s.update([1, 2])`，因为后者实际加入的是两个整数。

不要写 `s = s.add(value)`，否则变量会绑定返回值 `None`。

## 4. 删除：remove、discard、pop、clear

| 操作 | 行为 | 缺失或空集合时 |
| --- | --- | --- |
| `s.remove(value)` | 删除指定元素，返回 `None` | 不存在抛出 `KeyError` |
| `s.discard(value)` | 删除指定元素，返回 `None` | 不存在不报错 |
| `s.pop()` | 移出并返回任意一个元素 | 空集合抛出 `KeyError` |
| `s.clear()` | 清空原集合，返回 `None` | 空集合也可调用 |

```python
numbers = {1, 2, 3}
numbers.remove(2)
numbers.discard(99)
print(sorted(numbers))  # [1, 3]

removed = numbers.pop()
print(removed not in numbers)  # True，不指定 removed 必须是几
numbers.clear()
print(numbers)                # set()
```

> [!warning] pop 不是随机抽样
> “任意元素”表示 API 不承诺移出哪一项，不等于随机或均匀抽样。集合的 `pop()` 也不能像列表那样传入索引。

集合没有按索引修改元素的操作。需要替换一个值时，可以删除旧值再添加新值；注意集合不能保存重复值，替换后元素数量未必保持不变。

## 5. 集合运算：交、并、差、对称差

令 `a = {1, 2, 3}`、`b = {3, 4}`：

| 运算 | 写法 | 对应方法 | 结果（排序后展示） |
| --- | --- | --- | --- |
| 交集 | `a & b` | `a.intersection(b)` | `[3]` |
| 并集 | `a \| b` | `a.union(b)` | `[1, 2, 3, 4]` |
| 差集 | `a - b` | `a.difference(b)` | `[1, 2]` |
| 对称差集 | `a ^ b` | `a.symmetric_difference(b)` | `[1, 2, 4]` |

```python
a = {1, 2, 3}
b = {3, 4}
print(sorted(a - b))  # [1, 2]
print(sorted(b - a))  # [4]：差集有方向
print(sorted(a & b))  # [3]
print(sorted(a | b))  # [1, 2, 3, 4]
print(sorted(a ^ b))  # [1, 2, 4]
print(sorted(a))      # [1, 2, 3]：这些写法没有修改 a
```

这里 `&`、`|`、`^` 执行集合运算，不是对元素做数值位运算。运算含义要结合操作数类型判断，和之前的字符串重复是同一种学习思路。

方法形式可接收列表等可迭代对象：`a.intersection([2, 3])` 可以；运算符形式则要求集合类型，不能直接写 `a & [2, 3]`。

## 6. 子集、超集与不相交

```python
a = {1, 2}
b = {1, 2, 3}
print(a <= b)                 # True：a 是 b 的子集，允许相等
print(a < b)                  # True：真子集，必须不相等
print(a <= a, a < a)          # True False
print(b >= a, b > a)          # True True：超集、真超集
print(a.issubset(b))          # True
print(b.issuperset(a))        # True
print(a.isdisjoint({3, 4}))   # True：没有共同元素
print({1, 2} == {2, 1})       # True：相等不比较顺序
```

`<`、`>` 比的是包含关系，不是元素个数，也不是逐元素比较大小。例如 `{1} < {2, 3}` 是 `False`，即使左边元素更少。

## 7. 原地更新、赋值与复制

| 产生运算结果 | 对应原地更新 |
| --- | --- |
| `a \| b` | `a.update(b)` 或 `a \|= b` |
| `a & b` | `a.intersection_update(b)` 或 `a &= b` |
| `a - b` | `a.difference_update(b)` 或 `a -= b` |
| `a ^ b` | `a.symmetric_difference_update(b)` 或 `a ^= b` |

```python
a = {1, 2}
alias = a
copied = a.copy()
a |= {3}
print(sorted(alias))   # [1, 2, 3]：别名看到原地修改
print(sorted(copied))  # [1, 2]：独立的外层集合

a = {1, 2}
alias = a
a = a | {3}
print(sorted(alias))   # [1, 2]：这里重新绑定 a
```

这些更新方法返回 `None`。`copy()` 或 `set(existing_set)` 创建浅拷贝，不代表递归复制对象内部内容。遍历原集合时避免增加或删除其元素；需要筛选时优先生成新集合。

## 8. 集合元素：可哈希，而不只是“看起来不可变”

常见数字、字符串，以及所有元素都可哈希的元组可以作集合元素。列表、字典、普通 `set` 不可哈希，不能直接放进另一个集合。

```python
points = {(1, 2), (2, 3)}
print((1, 2) in points)  # True
print(len({1, True, 1.0}))  # 1：相等且哈希相同，被视为同一个元素
print(len({1, '1'}))       # 2：数字与字符串不同
# invalid = {([1], 2)}     # TypeError：这个元组包含不可哈希的列表
```

> [!tip] 了解即可：frozenset
> `frozenset()` 是不可变集合，不支持 `add`、`remove` 等原地修改。它本身可哈希，因此可以用作字典键或普通集合的元素；其内部元素也需要可哈希。

```python
group = frozenset([1, 2, 2])
groups = {group}
print(sorted(group))   # [1, 2]
print(group in groups) # True
```

## 9. 集合生成式与去重顺序

```python
squares = {number ** 2 for number in [-2, -1, 0, 1, 2]}
print(sorted(squares))  # [0, 1, 4]：计算后去重
evens = {number for number in range(6) if number % 2 == 0}
print(sorted(evens))    # [0, 2, 4]
```

`{表达式 for ...}` 是集合生成式；`{键: 值 for ...}` 是字典生成式，注意冒号的区别。

需要去重并保留首次出现顺序时，不直接使用 `list(set(values))`：

```python
languages = ['Python', 'JS', 'Python', 'Vue', 'JS']
unique = list(dict.fromkeys(languages))
print(unique)  # ['Python', 'JS', 'Vue']
```

这里利用字典的插入顺序，`dict.fromkeys()` 用给定元素作为键，默认值是 `None`，再由 `list()` 取得键。元素仍须可哈希；列表或字典组成的记录不能直接套用。

## 10. 与 JS Set 的对照

| 用途 / 行为 | Python | JS Set 对照 |
| --- | --- | --- |
| 创建空集合 | `set()` | `new Set()` |
| 添加 | `s.add(value)` 返回 `None` | `s.add(value)` 返回 Set 自身，可链式调用 |
| 成员判断 | `value in s` | `s.has(value)` |
| 删除不存在的元素 | `discard()` 不报错，返回 `None` | `delete()` 返回是否删除成功的布尔值 |
| 元素数量 | `len(s)` | `s.size` |
| 遍历顺序 | 不保证插入顺序 | 保留插入顺序 |
| 数组作为元素 | Python 列表不可哈希，不能直接加入 | JS 数组可作为元素，按对象身份区分 |

不要因 JS 的 `new Set(array)` 常被用于去重，就认为 Python `set()` 的顺序与比较规则也相同。

## 11. 小实践：比较名单

```python
registered = {'张三', '李四', '王五'}
arrived = {'李四', '王五', '赵六'}

print(sorted(registered - arrived))  # ['张三']：报名但未到
print(sorted(arrived - registered))  # ['赵六']：未报名但到场
print(sorted(registered & arrived))  # ['李四', '王五']：报名且到场
```

这类集合差异可用于理解已处理与待处理任务、抓取链接去重等后续场景。现在先掌握集合的含义，不需要提前引入爬虫框架。

## 12. 回顾练习

```python
a = {1, 2, 2, 3}
b = {3, 4}
print(len(a))
print(sorted(a ^ b))
print({1, 3} <= a)

alias = a
new_set = a - b
a.discard(99)
a.add(5)
print(sorted(alias))
print(sorted(new_set))
print(type({}), type(set()))
```

> [!question]- 展开查看答案
> - 长度是 `3`，重复元素 2 只保留一份。
> - 对称差集排序后为 `[1, 2, 4]`，排除了共同元素 3。
> - 子集判断为 `True`。
> - `alias` 排序后为 `[1, 2, 3, 5]`，与 a 引用同一个集合。
> - `new_set` 排序后为 `[1, 2]`，差集返回的结果没有随 a 变化。
> - 最后一行是 `<class 'dict'> <class 'set'>`。
