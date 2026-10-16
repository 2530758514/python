# 基础课程4：分支与循环

关联课程：[[基础课程4]]

前置知识：[[ai-ta-基础课程3补充]]

> [!important] 本课重点
> - `:` 和缩进组织代码块，通常每层使用 4 个空格，不混用 Tab 与空格。
> - 条件表达式写作 `结果1 if 条件 else 结果2`。
> - `range()` 包含起点、不包含终点；步长可以为负，但不能为 0。
> - `break` 退出最近一层循环；`continue` 跳过本轮剩余代码。
> - 循环的 `else` 在正常结束时执行；通过对应循环的 `break` 退出时不执行。

## 1. 代码块不等于块级作用域

你的笔记把 JS 的块作用域与 Python 缩进联系起来，这里需要分开理解：代码块表示一组语句，作用域决定名字在哪里可以访问。

```python
score = 80

if score >= 60:
    result = '及格'

print(result)  # 及格：if 不创建独立的块级作用域
```

JS 的 `let`、`const` 在 `{}` 中受块级作用域约束；Python 的 `if`、`for`、`while` 不创建这种作用域。如果条件没成立，上例的赋值就不会执行，之后读取未定义的名字会报错。

> [!warning] 缩进是语法的一部分
> 同一代码块需要一致缩进。推荐每层 4 个空格；编辑器按 Tab 键也可能插入空格，关键在于实际缩进字符。不要混用 Tab 与空格。

## 2. if / elif / else：一组分支只选一条

```python
score = 85

if score >= 90:
    print('优秀')
elif score >= 60:
    print('及格')
else:
    print('需要继续练习')
# 输出：及格
```

条件从上到下检查，命中一个分支后，就不再检查这组后面的 `elif`。如果写成多个独立的 `if`，则可能执行多处代码。

> [!tip] 条件顺序会影响结果
> 上例若先判断 `score >= 60`，95 分也会直接进入“及格”分支。区间判断注意边界，可以使用上一课的链式比较，例如 `0 <= score <= 100`。

### 条件表达式：先写结果，再写条件

原笔记的 `条件表达式1 if 结果1 else 结果2` 顺序需要调整为：

```python
age = 18
status = '成年' if age >= 18 else '未成年'
print(status)  # 成年
```

对应 JS：

```javascript
const status = age >= 18 ? '成年' : '未成年'
```

条件表达式会产生一个值，而且只计算被选择的结果表达式。复杂多分支优先写普通 `if`，避免嵌套表达式难读。

### pass：占位置，不改变执行流程

```python
ready = True

if ready:
    pass  # 此处计划以后补充逻辑

print('继续执行')  # 仍会输出
```

代码块不能只写注释而没有语句，此时可以用 `pass`。`pass` 不会退出或跳过循环，不等于 `break` 或 `continue`。

## 3. range：起点、终点与步长

入门时可以把 `range()` 看作生成整数序列的工具。更准确地说，它创建一个表示整数序列的 `range` 对象，不是直接创建包含所有整数的列表，也不是生成器。

| 写法 | `list(...)` 展开结果 |
| --- | --- |
| `range(5)` | `[0, 1, 2, 3, 4]` |
| `range(2, 5)` | `[2, 3, 4]` |
| `range(1, 8, 2)` | `[1, 3, 5, 7]` |
| `range(5, 0, -2)` | `[5, 3, 1]` |
| `range(5, 0)` | `[]` |
| `range(0)` | `[]` |

> [!warning] 不是“总在 stop - 1 结束”
> 统一规则是“不包含 stop”。正步长时取小于 stop 的值，负步长时取大于 stop 的值。
> 例如 `range(1, 8, 2)` 最后一项为 7，`range(1, 9, 2)` 最后一项也为 7。
> 步长方向与区间不匹配会得到空序列；步长为 0 则抛出 `ValueError`。

```python
numbers = range(1, 6)
print(numbers)        # range(1, 6)
print(list(numbers))  # [1, 2, 3, 4, 5]
print(3 in numbers)   # True
```

`range` 按规则表示序列，不必预先存储所有元素。循环时直接使用即可，不需要先转为列表；`list()` 适合小范围展示，巨大范围不要为了循环而展开。

## 4. while 与 for：选择合适的循环

| 场景 | 常见选择 |
| --- | --- |
| 按条件反复执行，例如还有重试次数 | `while` |
| 遍历字符串、列表等对象的元素 | `for item in 对象` |
| 固定执行 n 次 | `for _ in range(n)` |

### while：每轮开始前检查条件

```python
number = 1
even_total = 0
odd_total = 0

while number < 10:
    if number % 2 == 0:
        even_total += number
    else:
        odd_total += number
    number += 1

print(even_total, odd_total)  # 20 25：统计的是 1～9
```

你的 `not bool(number % 2)` 也可以判断偶数，但 `number % 2 == 0` 更直接。`not` 本身就会按真假值取反，不需要先手动 `bool()`。

### for-in：直接取得元素

原笔记标题 `fro-in` 应为 `for-in`。

```python
for letter in 'Python':
    print(letter)  # 每轮取一个字符

for _ in range(3):
    print('练习一次')  # 共输出三次
```

`_` 在这里是普通变量名，约定表示“不关心这个值”，不是特殊的丢弃语法。

> [!tip] JS 对照
> Python 的 `for item in values` 更接近 JS 的 `for (const item of values)`。
> JS 的 `for...in` 遍历属性键，不要因为都出现 `in` 就认为含义相同。

### 避免用 sum 当变量名

```python
even_total = 0
for number in range(2, 101, 2):
    even_total += number

print(even_total)  # 2550：2～100 的偶数和
print(sum(range(2, 101, 2)))  # 2550：内置 sum 函数的简洁写法
```

用 `sum = 0` 是合法的，但会遮蔽当前作用域中原本可用的内置 `sum` 函数，之后调用 `sum(...)` 可能报错。当前练习先掌握累加过程，再认识简洁写法。

## 5. break、continue 与 pass

原笔记中的 `brank` 应为 `break`。

| 语句 | 效果 |
| --- | --- |
| `break` | 立即结束最近一层循环 |
| `continue` | 跳过本轮剩余语句，开始下一轮 |
| `pass` | 什么也不做，继续执行后续语句 |

```python
for number in range(1, 6):
    if number == 2:
        continue
    if number == 4:
        break
    print(number)
# 依次输出 1、3
```

### while 中的 continue 与死循环

```python
number = 0
while number < 5:
    number += 1  # 放在可能 continue 之前，确保推进
    if number == 3:
        continue
    print(number)
# 依次输出 1、2、4、5
```

> [!warning] continue 可能跳过变量更新
> 如果计数更新写在循环末尾，而 `continue` 在前面，就可能一直重复同一个值。检查 `while` 时，要确认每条执行路径是否能让循环结束；`for` 会自动取得下一项，通常不需要手动更新迭代变量。

嵌套循环中的 `break` 只退出最近一层循环，不会一次退出全部循环。

## 6. 循环 else：没有通过 break 退出才执行

`else:` 与对应的 `for` 或 `while` 对齐，且不能漏掉冒号。它不表示“循环条件为假时每轮执行”，也不是附属于循环内部的 `if`。

```python
target = 3

for number in range(1, 6):
    if number == target:
        print('找到了')
        break
else:
    print('没有找到')
# target 为 3 时输出“找到了”；改为 9 时输出“没有找到”
```

| 结束方式 | 对应的循环 else 是否执行 |
| --- | --- |
| `for` 遍历完毕 | 是 |
| `while` 条件变为假 | 是 |
| 循环一次也没进入 | 是 |
| 执行对应循环的 `break` | 否 |
| 仅执行过 `continue`，之后正常结束 | 是 |
| 未处理异常导致执行离开循环，或函数中执行 `return` 离开 | 否 |

```python
remaining = 2
while remaining > 0:
    remaining -= 1
else:
    print('次数用完')  # 正常结束时执行
```

> [!tip] 实际用途
> 循环 `else` 常用于“寻找目标，找到就 break；遍历完仍没找到就执行兜底”。它不是必须使用的语法；复杂流程也可以明确记录是否找到，让代码更易读。

## 7. 回顾练习

先预测输出，再运行核对：

```python
print(list(range(6, 0, -2)))
print('偶数' if 7 % 2 == 0 else '奇数')

for number in range(3):
    if number == 1:
        continue
    print(number)
else:
    print('正常结束')

for number in range(3):
    if number == 1:
        break
else:
    print('这句会执行吗？')

for number in range(0):
    print('进入循环')
else:
    print('空序列也会执行 else')
```

> [!question]- 展开查看答案
> - 第一行输出 `[6, 4, 2]`，不包含终点 0。
> - 第二行输出“奇数”。
> - 第一个循环依次输出 `0`、`2`、“正常结束”；`continue` 不阻止循环正常结束后的 `else`。
> - 第二个循环在 `number == 1` 时退出，不执行 `else`，因此没有输出。
> - 第三个循环不进入循环体，但输出“空序列也会执行 else”。

## 8. 小实践：有限次数的密码校验

练习目标：最多输入三次，正确就结束；三次均错误再提示次数用完。这里只练控制流程，真实系统不能把明文密码直接写在代码中。

```python
for attempt in range(1, 4):
    password = input(f'第 {attempt} 次，请输入练习密码：')
    if password == 'python123':
        print('验证成功')
        break
    print('密码错误')
else:
    print('三次机会已用完')
```

可以尝试修改：输入 `q` 时退出。注意提前退出也会触发 `break`，因此“退出”和“验证成功”需要在各自分支中明确表达，不能只凭没有执行 `else` 判断成功。
