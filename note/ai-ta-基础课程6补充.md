# 基础课程6：字典 dict

对应案例：`python-learn1/demo6.py`。

关联知识：[[ai-ta-基础课程5补充]]、[[ai-ta-基础课程3补充]]

> [!important] 字典的核心
> 字典保存“键 → 值”的对应关系，通过键查找值，而不是通过位置索引访问。
> 字典可修改，键不重复，值可以重复；Python 3.7 起保证保留插入顺序。
> `in` 默认检查键，`for item in 字典` 默认遍历键。

## 1. 从前端经验理解字典

```python
student = {'name': '张三', 'age': 18}
scores = {'张三': 100, '李四': 90}

print(student['name'])  # 张三
print(scores['李四'])   # 90
print(type(student))   # <class 'dict'>
print(len(student))    # 2：键值对数量
```

`student` 类似前端常见的对象数据，但 Python 字典不是 JS 对象的完全对应物。

| 需求           | Python 字典                          | JS 对照                                             |
| -------------- | ------------------------------------ | --------------------------------------------------- |
| 按字符串键读取 | `student['name']`                    | `student['name']` 或 `student.name`                 |
| 属性式读取     | `student.name` 不用于读取这个字典键  | 普通对象常用点语法                                  |
| 缺失键         | `student['missing']` 抛出 `KeyError` | 普通缺失属性通常得到 `undefined`                    |
| 键的类型       | 支持可哈希对象                       | 普通对象键主要是字符串或 Symbol；Map 可使用更多类型 |
| 成员判断       | `'name' in student` 检查字典键       | 普通对象的 `in` 还可能检查到原型链属性              |

字典与列表选择：一组按顺序排列的成绩可用列表；需要根据姓名找成绩时，字典更自然。二者也常组合使用。

## 2. 创建：{} 与 dict()

```python
empty = {}
student = dict(name='张三', age=18)
scores = dict([('张三', 100), ('李四', 90)])

print(empty)    # {}
print(student)  # {'name': '张三', 'age': 18}
print(scores)   # {'张三': 100, '李四': 90}
```

`('张三', 100)` 是一个二元组，这里先理解为一组键和值，元组后续再学。

你的 `dict({'张三': 100, '李四': 200})` 也是合法写法，只是已经写了字典字面量，直接使用它更简洁。对已有字典调用 `dict(original)` 则可以创建浅拷贝。

### 键唯一：相同键后面的值覆盖前面的值

```python
scores = {'张三': 100, '张三': 80}
print(scores)       # {'张三': 80}
print(len(scores))  # 1
```

实际代码应避免重复书写字面量键，防止无意覆盖。

### 键需要可哈希

“可哈希”可以先理解为：对象能按稳定的哈希与相等规则用于字典查找。常见字符串、整数可以作为键，列表、字典不可以。

```python
data = {1: '整数键', '1': '字符串键'}
print(data[1])    # 整数键
print(data['1'])  # 字符串键：1 与 '1' 是不同的键

# invalid = {['name']: '张三'}  # TypeError：list 不可哈希
```

> [!warning] 不要用“类型不同”判断键一定不同
> `True == 1 == 1.0`，它们的哈希也相同，因此在字典中不能作为三个独立的键。初学时业务键优先统一使用含义清楚的字符串，不必现在深入哈希实现。

## 3. 读取：[] 与 get()

```python
scores = {'张三': 100, '李四': 90}
print(scores['张三'])           # 100
print(scores.get('张三'))       # 100
print(scores.get('王五'))       # None
print(scores.get('王五', 0))    # 0
print('王五' in scores)         # False：get 默认值不会写入字典
# print(scores['王五'])         # KeyError
```

| 写法                     | 键存在 | 键不存在        |
| ------------------------ | ------ | --------------- |
| `data[key]`              | 返回值 | 抛出 `KeyError` |
| `data.get(key)`          | 返回值 | 返回 `None`     |
| `data.get(key, default)` | 返回值 | 返回指定默认值  |

字段必须存在时，使用 `[]` 可以及时暴露数据问题；可选字段可以用 `get()` 提供缺省值，不要把所有错误都用默认值掩盖。

> [!warning] get 的默认值只针对“键不存在”
> 键已存在但值是 `None`、`0`、`False` 或空字符串时，`get()` 会原样返回该值。
> `data.get(key) or 默认值` 会把所有假值都替换掉，与 `data.get(key, 默认值)` 不等价。

```python
settings = {'timeout': 0, 'nickname': None}
print(settings.get('timeout', 30))   # 0
print(settings.get('timeout') or 30) # 30：这里合法值 0 也被替换了
print(settings.get('nickname', '匿名'))  # None
print('nickname' in settings)       # True：键存在，只是值为 None
```

## 4. 增加、修改与批量更新

```python
scores = {'张三': 100}
scores['李四'] = 90    # 不存在的键：新增
scores['张三'] = 95    # 已存在的键：修改
scores.update({'李四': 99, '王五': 80})
print(scores)         # {'张三': 95, '李四': 99, '王五': 80}
```

`update()` 修改原字典，已有键被新值覆盖，返回 `None`；不要写成 `scores = scores.update(...)`。

### setdefault：不存在时才写入默认值

```python
scores = {'张三': 100}
print(scores.setdefault('张三', 0))  # 100：不覆盖原值
print(scores.setdefault('王五', 0))  # 0：新增键并返回默认值
print(scores)                       # {'张三': 100, '王五': 0}
```

先掌握 `get()` 与普通赋值，再认识 `setdefault()`：`get()` 只读取，`setdefault()` 可能修改字典。

## 5. 删除与清空

| 操作                     | 用途                           | 返回值 / 注意                         |
| ------------------------ | ------------------------------ | ------------------------------------- |
| `del data[key]`          | 删除键值对                     | 键不存在抛出 `KeyError`；`del` 是语句 |
| `data.pop(key)`          | 删除并取回对应值               | 键不存在抛出 `KeyError`               |
| `data.pop(key, default)` | 删除并取回值，缺失时返回默认值 | 有默认值时不因键缺失报错              |
| `data.popitem()`         | 删除并返回最后插入的键值对     | 返回二元组；空字典抛出 `KeyError`     |
| `data.clear()`           | 清空原字典                     | 返回 `None`                           |

```python
scores = {'张三': 100, '李四': 90}
removed = scores.pop('李四')
print(removed)                   # 90
print(scores.pop('王五', '不存在')) # 不存在
scores.clear()
print(scores)                    # {}
```

`del scores` 是删除名字绑定，`scores.clear()` 是清空字典内容。若多个变量引用同一个字典，`clear()` 的影响会被它们共同看到。

## 6. in / not in：默认检查键

```python
scores = {'张三': 100, '李四': 90}
print('张三' in scores)          # True
print('王五' not in scores)      # True
print(100 in scores)             # False：100 不是键
print(100 in scores.values())    # True：在值中查找
print(('张三', 100) in scores.items())  # True：检查键值对
```

同一个值可以出现在多个键下，因此“根据值找键”不一定只有一个结果。

## 7. keys / values / items 与遍历

```python
scores = {'张三': 100, '李四': 90}
print(list(scores.keys()))    # ['张三', '李四']
print(list(scores.values()))  # [100, 90]
print(list(scores.items()))   # [('张三', 100), ('李四', 90)]

for name in scores:
    print(name, scores[name])

for name, score in scores.items():
    print(f'{name}：{score}')
```

`for name, score in scores.items()` 使用上一课之前学过的解包赋值，直接获取键和值。它在用途上类似 JS 的 `Object.entries()` 配合解构遍历。

### 视图不是固定快照

`keys()`、`values()`、`items()` 返回字典视图，不是列表。它们反映原字典当前的内容；用 `list(...)` 才会取得当时各元素的浅层快照。

```python
scores = {'张三': 100}
keys_view = scores.keys()
keys_snapshot = list(scores.keys())
scores['李四'] = 90

print(list(keys_view))  # ['张三', '李四']：视图随原字典变化
print(keys_snapshot)   # ['张三']：已有列表不会自动增加键
```

> [!warning] 遍历字典时不要增删其键
> 对原字典边遍历边增删键可能触发 `RuntimeError` 或导致遍历不完整。需要删除多项时，可以先收集待删除键，再删除；也可以筛选生成新字典。

## 8. 有序不等于自动排序

字典保留插入顺序，更新已有键通常不改变它的位置；删除后重新添加，会排在末尾。按键访问不等于列表的位置索引：`data[0]` 查的是整数键 `0`，不是第一个键值对。

```python
scores = {'李四': 90, '张三': 100}
scores['李四'] = 95
print(list(scores))   # ['李四', '张三']：更新不改变位置
print(sorted(scores)) # ['张三', '李四']：按字符串规则排序键，返回列表
print(scores)         # {'李四': 95, '张三': 100}：原字典顺序没变
```

> [!tip] “字典无序”的旧说法要结合版本看
> 当前学习 Python 3 时，应记住 Python 3.7 起字典插入顺序是语言保证。但字典相等比较不要求插入顺序一致，不能把它完全当列表理解。

## 9. 字典生成式与列表组合

```python
scores = {'张三': 100, '李四': 55, '王五': 80}
passed = {name: score for name, score in scores.items() if score >= 60}
print(passed)  # {'张三': 100, '王五': 80}

squares = {number: number ** 2 for number in range(1, 4)}
print(squares) # {1: 1, 2: 4, 3: 9}

items = ['张三', '李四', '王五']
prices = [100, 55, 80]
d = {item.upper():price for item, price in zip(items, prices)}
print(d)
```

基本形式为 `{键表达式: 值表达式 for ...}`，与列表生成式对应，但产生的是字典。如果生成重复键，后生成的值会覆盖前面的值。

列表常用来保存多条记录，每条记录用字典描述：

```python
students = [
    {'name': '张三', 'score': 100},
    {'name': '李四', 'score': 55},
]
passed_names = [student['name'] for student in students if student['score'] >= 60]
print(passed_names)  # ['张三']
```

这种“列表 + 字典”的数据形态常见于接口处理。不过 Python 字典不是 JSON 文本：Python 使用 `True`、`False`、`None`，JSON 使用 `true`、`false`、`null`。两者转换后续用 `json` 模块学习。

## 10. 赋值与浅拷贝

```python
student = {'name': '张三', 'skills': ['JS']}
alias = student
copied = student.copy()  # 也可以用 dict(student)

alias['name'] = '李四'
copied['skills'].append('Python')

print(student) # {'name': '李四', 'skills': ['JS', 'Python']}
print(copied)  # {'name': '张三', 'skills': ['JS', 'Python']}
```

和列表一样，赋值不复制对象，浅拷贝只新建外层容器，嵌套列表仍然共享。需要复制到什么层级，要根据数据结构决定，不用看到字典就一律深拷贝。

## 11. 小实践：统计单词次数

```python
words = ['python', 'js', 'python', 'vue', 'js']
counts = {}

for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)  # {'python': 2, 'js': 2, 'vue': 1}
```

第一次遇到单词时，`get()` 返回 0，再通过赋值写入 1；之后读取已有次数并加 1。真正写入字典的是左侧的 `counts[word] = ...`，不是 `get()`。

## 12. 回顾练习

```python
data = {'a': 0, 'b': None}
print(data.get('a', 9))
print(data.get('b', 9))
print(data.get('c', 9))
print('c' in data)

view = data.keys()
data['c'] = 3
removed = data.pop('a')
print(removed)
print(list(view))
print({key: value for key, value in data.items() if value is not None})
```

> [!question]- 展开查看答案
>
> - 前四行依次输出 `0`、`None`、`9`、`False`。默认值只在键缺失时使用，不会写入字典。
> - `removed` 是 `0`，是被移除的值。
> - 视图展开得到 `['b', 'c']`，反映添加和删除之后的键。
> - 最后得到 `{'c': 3}`，筛掉了值为 `None` 的项，原字典仍保留键 `'b'`。

> [!tip] 当前优先级
> 先熟练使用 `[]`、`get()`、赋值、`in`、删除和 `items()` 遍历。视图、浅拷贝及生成式通过例子理解即可；哈希底层实现可以以后再深入。
