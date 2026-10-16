# 基础课程5：列表 list

运行案例：`python-learn1/demo5.py`，各节独立准备数据，可整份运行或选中一节运行。

关联知识：[[ai-ta-基础课程3补充]]、[[ai-ta-基础课程4补充]]

> [!important] 先建立列表的概念
> 列表是有序、可变、允许重复元素的容器。可以存放不同类型，但实际业务中通常让同一列表中的数据含义保持一致。
> `list` 是类型，`[]` 是常用的列表字面量，`list()` 可以创建空列表或将可迭代对象转换为列表。
> 成员判断使用 `in` / `not in`，没有 `out in`。

## 1. 创建与访问

```python
languages = ['Python', 'JS', 'Python']
print(len(languages))     # 3：长度
print(languages[0])       # Python：索引从 0 开始
print(languages[-1])      # Python：负索引从末尾数
print(list('abc'))        # ['a', 'b', 'c']
print(list(range(3)))     # [0, 1, 2]
```

`list('abc')` 会拆分字符，若希望字符串整体作为一个元素，应写 `['abc']`。

> [!warning] 与 JS 数组的差异
> JS 数组越界读取通常得到 `undefined`，Python 列表越界读取会抛出 `IndexError`。
> Python 不能用 `items[len(items)] = value` 自动扩展列表，增加元素应使用 `append()` 等方法。

## 2. 查询、成员判断与遍历

| 操作 | 用途 | 注意 |
| --- | --- | --- |
| `value in items` | 是否存在该元素 | 按相等比较进行成员判断 |
| `value not in items` | 是否不存在 | 不是 `out in` |
| `items.index(value)` | 第一个匹配元素的索引 | 找不到抛出 `ValueError`，不是 JS 的 `-1` |
| `items.count(value)` | 出现次数 | 找不到返回 `0` |

```python
items = ['Python', 'JS', 'Python']
print('JS' in items)         # True
print('Java' not in items)   # True
print(items.index('Python')) # 0
print(items.count('Python')) # 2

for index, value in enumerate(items):
    print(index, value)      # enumerate 同时提供索引和值，默认从 0 开始
```

Python 的列表 `in` 类似 JS 的 `includes()` 这一用途，但比较规则不完全相同。JS 的 `in` 检查属性，不是数组是否包含某个值。

## 3. 增：append、extend、insert

| 操作 | 效果 | 返回值 |
| --- | --- | --- |
| `items.append(value)` | 末尾添加一个元素 | `None` |
| `items.extend(values)` | 逐个追加可迭代对象中的元素 | `None` |
| `items.insert(index, value)` | 指定位置插入一个元素 | `None` |
| `items + other` | 拼接两个列表，产生新列表 | 新列表 |

```python
items = [1]
items.append([2, 3])
print(items)  # [1, [2, 3]]：添加了一个列表元素

items = [1]
items.extend([2, 3])
print(items)  # [1, 2, 3]：添加了两个元素
```

`extend('ab')` 会追加 `'a'`、`'b'` 两个字符；如果需要追加整个字符串，应使用 `append('ab')`。

> [!warning] 不要写 items = items.append(value)
> `append()` 修改原列表，返回 `None`。这样赋值会让 `items` 变成 `None`。
> `sort()`、`reverse()`、`clear()` 等方法也返回 `None`，但 `pop()` 会返回移出的元素，不要一概而论。

## 4. 删：按值、按位置或按范围

| 操作 | 效果 | 返回值 / 易错点 |
| --- | --- | --- |
| `items.remove(value)` | 删除第一个相等的元素 | 返回 `None`；不存在抛出 `ValueError` |
| `items.pop()` | 删除最后一项 | 返回被删除的元素；空列表报错 |
| `items.pop(index)` | 删除指定索引项 | 返回被删除的元素；索引越界报错 |
| `del items[index]` | 删除指定索引项 | `del` 是语句；索引越界报错 |
| `del items[start:stop]` | 删除切片范围 | 可一次删除多项 |
| `items.clear()` | 清空原列表 | 返回 `None`，列表仍存在 |

`del items` 删除的是名字绑定，不等于清空列表。若别的名字还引用这个列表，它们仍可访问它。

> [!tip] 遍历时别直接删除同一个列表的元素
> 删除会让后续元素移动，容易漏处理。需要筛选数据时，优先使用生成新列表的列表生成式，原列表先保留。

## 5. 改与切：区分读取切片、切片赋值

```python
items = [0, 1, 2, 3, 4, 5]
print(items[1:4])   # [1, 2, 3]
print(items[:3])    # [0, 1, 2]
print(items[3:])    # [3, 4, 5]
print(items[::2])   # [0, 2, 4]
print(items[::-1])  # [5, 4, 3, 2, 1, 0]
print(items[99:])   # []：切片会容许边界超出列表范围
```

切片语法为 `items[start:stop:step]`：包含起点、不包含终点，步长不能为 0。负步长用于反向取值，省略边界时会根据方向选择合适的默认值。

```python
items = [10, 20, 30, 40]
items[1] = 99
print(items)  # [10, 99, 30, 40]

items[1:3] = [7, 8, 9]
print(items)  # [10, 7, 8, 9, 40]
```

> [!important] 左右两侧含义不同
> `part = items[1:3]` 读取切片，会产生新的外层列表。
> `items[1:3] = [...]` 则修改原列表。默认步长为 1 时，替换元素数量可以不同，列表长度也可以变化。
> 如果用 `items[::2] = [...]` 这类非 1 步长切片赋值，右侧元素数量必须与选中的位置数量匹配。

## 6. 排序与反转

| 操作 | 修改原列表 | 返回值 |
| --- | --- | --- |
| `items.sort()` | 是 | `None` |
| `sorted(items)` | 否 | 排好序的新列表 |
| `items.reverse()` | 是 | `None` |
| `items[::-1]` | 否 | 反向读取的新列表 |

```python
numbers = [10, 2, 30]
print(sorted(numbers))                 # [2, 10, 30]
print(sorted(numbers, reverse=True))   # [30, 10, 2]
print(numbers)                        # [10, 2, 30]

print(sorted(['10', '2', '30']))           # ['10', '2', '30']
print(sorted(['10', '2', '30'], key=int))  # ['2', '10', '30']
```

`reverse=True` 表示反向排序；`reverse()` 只是反转当前顺序，不保证降序。`key=int` 用转换后的数值作为排序依据，不会把结果元素变成整数。传入函数时写 `int`，不是提前调用 `int()`。

> [!warning] JS 排序经验不能直接照搬
> Python 对纯数字列表默认按数值排序；JS 的普通数组 `sort()` 默认按字符串规则排序。
> Python 的 `sorted([1, '2'])` 会因整数和字符串无法直接比较大小而报 `TypeError`，需要先统一数据或指定合理的排序依据。

## 7. 列表生成式：用表达式创建新列表

基本形式：`[结果表达式 for 变量 in 可迭代对象]`。

```python
# 普通循环
squares = []
for number in range(1, 6):
    squares.append(number ** 2)

# 同样的生成逻辑
squares = [number ** 2 for number in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# 末尾 if：筛选，只保留满足条件的项
evens = [number for number in range(1, 11) if number % 2 == 0]
print(evens)    # [2, 4, 6, 8, 10]

# 前面的 if/else：决定每项的结果，不会筛掉元素
labels = ['偶数' if number % 2 == 0 else '奇数' for number in range(1, 5)]
print(labels)   # ['奇数', '偶数', '奇数', '偶数']
```

对应 JS 的思路：转换类似 `map()`，筛选类似 `filter()`。不要为了简短堆叠复杂逻辑；多步骤、带日志的处理通常用普通 `for` 更清楚。

列表生成式会实际创建结果列表，不是按需逐项产出的生成器；结果很大时也会占用相应内存。

## 8. 复制与共享：给已有知识补上实际案例

```python
original = [1, 2]
alias = original
copied = original.copy()  # 也可用 original[:] 或 list(original)
alias.append(3)
print(original)           # [1, 2, 3]
print(copied)             # [1, 2]
```

这三种复制方式都是浅拷贝：外层列表是新的，元素仍引用原来的对象。

```python
original = [[1], [2]]
copied = original.copy()
copied[0].append(99)
print(original)  # [[1, 99], [2]]：内部列表仍然共享
```

> [!warning] 重复列表不会自动复制内部对象
> `[[]] * 3` 重复引用同一个内部列表，修改其中一项会影响三处。
> 需要三个独立空列表时，用 `[[] for _ in range(3)]`，每轮都会新建一个列表。
> 先理解浅拷贝，不必现在展开深拷贝的所有规则。

## 9. 练习：先预测，再运行

```python
items = [3, 1, 3, 2]
part = items[1:3]
items.remove(3)
part.append(9)
print(items)
print(part)
print(sorted(items, reverse=True))
print([number * 10 for number in items if number > 1])
```

> [!question]- 展开查看答案
> - `items` 是 `[1, 3, 2]`：`remove()` 只删除第一个 3。
> - `part` 是 `[1, 3, 9]`：读取切片得到新列表，追加不影响原列表。
> - 排序结果是 `[3, 2, 1]`，不改变 `items`。
> - 生成式结果是 `[30, 20]`：先筛出大于 1 的元素，再乘以 10，保持遍历顺序。

案例文件最后还有“筛选及格分数，再降序排序”的小实践。可以尝试增加不及格名单与平均分，注意空列表不能直接用总和除以长度。
