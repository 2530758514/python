# 基础课程10：函数、参数、返回值、作用域与递归

对应案例：`python-learn1/demo10.py`。建议整份运行；选中片段运行时，要先执行它依赖的函数定义。

关联知识：[[ai-ta-基础课程5补充]]、[[ai-ta-基础课程6补充]]、[[ai-ta-基础课程7补充]]、[[ai-ta-基础课程9补充]]

> [!important] 当前必学
> 函数封装一个可复用的操作：参数输入，函数体处理，返回值输出。
> `print()` 显示内容，`return` 把结果交回调用者，两者不同。
> 形参是局部名字，绑定到实参对象；区分修改对象与重新绑定名字。
> 默认参数在函数定义时求值，不会在每次调用时重新创建。
> 递归必须有终止条件，并且每次调用都朝终止条件推进。

## 1. 定义不等于调用

```python
def calc(a, b):
    """返回两个参数相加的结果。"""
    c = a + b
    return c

result = calc(1, 2)
print(result)  # 3
```

- `def` 定义函数，`calc` 是函数名，括号中的 `a`、`b` 是形参。
- 调用 `calc(1, 2)` 时，`1`、`2` 是实参。
- 执行 `def` 会创建函数对象并绑定名字，但此时不执行函数体。调用时才执行函数体。
- 普通 `def` 函数需要先执行到定义，才能调用；不要直接照搬 JS 函数声明提升的行为。

### 函数对象与调用结果

```python
def double(number):
    return number * 2

operation = double     # 保存函数对象
result = double(3)     # 立即调用，保存结果
print(operation(4))    # 8
print(result)          # 6
```

这与你在 JS 中传递回调函数时区分 `handler` 与 `handler()` 的思路相似。

## 2. 参数：位置、关键字与默认值

```python
def greet(name, greeting='你好'):
    return f'{greeting}，{name}'

print(greet('张三'))                         # 你好，张三
print(greet('张三', '早上好'))                # 早上好，张三
print(greet(greeting='晚上好', name='李四'))  # 晚上好，李四
```

| 方式 | 含义 | 常见错误 |
| --- | --- | --- |
| 位置传参 | 按位置绑定形参 | 顺序不对可能结果错误 |
| 关键字传参 | 用形参名明确绑定 | 名字拼错、同一参数传两次会报错 |
| 默认值 | 调用未提供该参数时使用 | 不代表传入 None 也改用默认值 |

```python
def show(value='默认值'):
    return value

print(show())      # 默认值
print(show(None))  # None：明确传入的值不会被默认值替换
```

普通调用中位置参数写在关键字参数前，例如 `greet('张三', greeting='欢迎')`。不要写 `greet(name='张三', '欢迎')`，这是语法错误；解包调用的进阶组合以后再深入。

`greet()` 缺少必需参数、`greet('张三', name='李四')` 重复绑定，都抛出 `TypeError`。这和 JS 允许缺失参数得到 `undefined` 的惯常行为不同。

## 3. 返回值：None、提前结束与多个结果

```python
def display_total(a, b):
    print(a + b)

def calculate_total(a, b):
    return a + b

shown = display_total(1, 2)  # 输出 3
print(shown)                # None
print(calculate_total(1, 2) * 10)  # 30
```

函数自然执行到末尾，或执行不带表达式的 `return`，都返回 `None`。普通函数中 `return` 立即结束当前调用，其后的语句不再执行。

```python
def bounds(numbers):
    if not numbers:
        return None
    return min(numbers), max(numbers)

low, high = bounds([3, 1, 8])
print(low, high)    # 1 8
print(bounds([]))   # None
```

`return a, b` 实际返回一个元组，不是多个互相独立的返回通道。调用方再进行解包；如果可能返回 `None`，应先检查结果，不能直接把它解包成两项。

> [!tip] 函数设计建议
> 通用计算函数优先返回结果，由调用方决定是否打印、存文件或返回接口。返回值形态尽量明确，空数据和失败情况也应有约定。

## 4. 参数如何传递：对象共享，而不是自动复制

```python
def add_skill(skills):
    skills.append('Python')

def replace_skills(skills):
    skills = ['Vue']
    return skills

values = ['JS']
add_skill(values)
print(values)                  # ['JS', 'Python']
print(replace_skills(values))   # ['Vue']
print(values)                  # ['JS', 'Python']
```

进入函数时，形参这个局部名字绑定到实参对象：`append()` 改变共享列表，调用方可见；`skills = ...` 只改变局部名字的绑定，不会重新绑定调用方的 `values`。

不要简单记成“基本类型传值、列表传引用”，Python 采用一致的对象绑定机制。对象能否修改，决定了哪些操作会改变调用方可见的内容。

如果希望独立处理，可以在函数内部先复制容器，但浅拷贝仍可能共享嵌套对象，回看第五、六课。

## 5. 默认参数陷阱：不要直接用可变容器作默认值

```python
def bad_collect(value, bucket=[]):  # 故意示范问题
    bucket.append(value)
    return bucket

print(bad_collect('a'))  # ['a']
print(bad_collect('b'))  # ['a', 'b']
```

默认列表只在执行这次函数定义时创建一次。未显式提供 `bucket` 的调用会共享它，因此结果累积。字典、集合也有类似问题，JS 参数默认表达式按调用求值的经验不能直接迁移过来。

```python
def collect(value, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(value)
    return bucket

print(collect('a'))  # ['a']
print(collect('b'))  # ['b']
provided = []
collect('c', provided)
print(provided)     # ['c']
```

> [!warning] 不用 if not bucket 代替 is None
> 调用方传入的空列表也是假值，`if not bucket` 会把它换成另一个列表。这里用 `None` 明确表达“未提供容器”，保留调用方传入的空容器。

默认表达式不只限于容器：时间、随机数或其他函数调用如果写在默认参数位置，也是在定义时求值，不是每次调用刷新。

## 6. 可变数量参数与调用解包

```python
def total(*numbers):
    return sum(numbers)

def describe(name, **details):
    return name, details

print(total())                   # 0：numbers 是空元组
print(total(1, 2, 3))            # 6
print(total(*[4, 5, 6]))         # 15
print(describe('张三', age=18))  # ('张三', {'age': 18})
print(describe(**{'name': '李四', 'age': 20}))
# ('李四', {'age': 20})
```

| 位置 | `*` | `**` |
| --- | --- | --- |
| 定义形参时 | 收集剩余位置实参为元组 | 收集剩余关键字实参为字典 |
| 调用函数时 | 展开可迭代对象作为位置实参 | 展开映射作为关键字实参，键必须是字符串 |

`args`、`kwargs` 是习惯命名，真正决定语法的是星号。普通参数已接收的关键字不再被收集到 `kwargs`；展开字典也不能让参数重复绑定，或给不接受额外关键字的函数随意传参。

## 7. 作用域：局部、外层、全局、内置

常见函数代码可按 LEGB 理解名字查找：Local 当前函数局部 → Enclosing 外层函数 → Global 当前模块 → Built-in 内置名字。复杂的类与特殊作用域以后再学。

```python
label = '模块变量'

def read_label():
    label = '局部变量'
    return label

print(read_label())  # 局部变量
print(label)         # 模块变量
```

普通函数内对名字赋值，默认将它视作局部名字，参数也属于局部。Python 的 `if`、`for` 不创建 JS `let` 那样的块级作用域，但函数会创建局部作用域。

### 为什么读取后再赋值也可能报错？

```python
count = 10

def broken_increment():
    count += 1  # UnboundLocalError：局部 count 还没有值
    return count

# broken_increment()  # 故意不执行，让其他案例继续运行
```

不是“先向外读，再自动变成本地变量”。函数中有这类赋值时，名字通常已被判定为局部；`+=` 又需要先读取它，因此出错。

### global：重新绑定模块级名字

```python
count = 0

def increment_global():
    global count
    count += 1

increment_global()
print(count)  # 1
```

`global` 指当前模块级名字，不是让变量自动变成所有模块共享。仅读取模块变量通常不必声明；对已有全局列表调用 `append()` 也不等于重新绑定名字。业务函数通常优先通过参数和返回值传递状态，避免隐式修改全局数据。

### 了解即可：nonlocal 与闭包

```python
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

next_count = make_counter()
print(next_count(), next_count())  # 1 2
```

`nonlocal` 用于重新绑定外层函数中已有的名字，不是模块全局变量。外层函数结束后，返回的内部函数仍可访问相关外层绑定，这就是闭包的一种用法，和 JS 闭包思路相通。

不要用 `list`、`sum`、`str` 作变量名或函数名，以免遮蔽内置名字。

## 8. 递归：把问题化为更小的同类问题

阶乘：`0! = 1`，`n! = n × (n - 1)!`。下面明确只接受非负整数，并排除布尔值；`raise` 表示主动报告不符合约定的输入，异常处理后续再学。

```python
def factorial(n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError('n 必须是整数，不能是布尔值')
    if n < 0:
        raise ValueError('n 不能为负数')
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(0))  # 1
print(factorial(5))  # 120
```

`factorial(3)` 的过程：

```text
factorial(3) 等待 3 × factorial(2)
factorial(2) 等待 2 × factorial(1)
factorial(1) 返回 1
factorial(2) 返回 2 × 1 = 2
factorial(3) 返回 3 × 2 = 6
```

每次调用都有自己的参数和局部状态，返回时再逐层完成等待中的计算。

> [!warning] 递归不是循环的必然升级
> 必须有终止条件，输入还要逐步接近终止条件；漏写递归调用前的 `return`，结果也可能变成 `None`。
> Python 递归深度有限，深调用可能抛出 `RecursionError`；不要盲目提高上限。阶乘这种简单线性过程通常用循环或标准库更合适。
> 重复计算的递归，例如朴素斐波那契，会带来性能问题，之后再学习缓存与算法分析。

```python
def factorial_loop(n):
    # 教学简版：此处约定调用方传入非负整数，完整校验见 demo10.py。
    result = 1
    for number in range(2, n + 1):
        result *= number
    return result

print(factorial_loop(0), factorial_loop(5))  # 1 120
```

## 9. 了解即可：参数传递方式限制、lambda、类型标注

### / 与单独的 *

```python
def format_score(name, /, score, *, digits=1):
    return f'{name}：{score:.{digits}f}'

print(format_score('张三', score=88.125, digits=2))  # 张三：88.12
```

`/` 前的参数只能按位置传入；`*` 后的参数只能按关键字传入。这里的单独 `*` 不收集参数。`/` 用于 Python 函数定义的语法自 **Python 3.8** 起支持；只接受关键字的参数和 `nonlocal` 在 Python 3.0 已有。

阅读库文档时能识别它们即可，日常函数不必刻意加入所有参数形式。

### lambda：一个表达式的匿名函数

```python
students = [{'name': '张三', 'score': 90}, {'name': '李四', 'score': 75}]
ordered = sorted(students, key=lambda student: student['score'])
print([student['name'] for student in ordered])  # ['李四', '张三']
```

这里传递一个函数，排序时取每条记录的成绩作为依据。`lambda` 的表达式结果自动返回，不写 `return`；不适合多语句复杂逻辑，也不是 JS 箭头函数的所有语义对应物。

### 文档字符串与类型标注

```python
def add(a: int, b: int) -> int:
    """返回两个整数的和。"""
    return a + b

print(add(1, 2))    # 3
print(add.__doc__)  # 返回两个整数的和。
print(add('a', 'b')) # ab：故意违反标注，Python 运行时不会自动拦截
```

标注帮助 IDE、静态检查工具和读代码的人理解意图，本身不保证运行时校验。类似 TS 类型主要服务检查，但具体运行时系统不同；某些后端框架可以利用标注做校验，那是框架提供的能力。

## 10. 小实践：成绩统计函数

```python
def summarize_scores(scores, *, pass_mark=60):
    """输入数值成绩列表，返回统计字典；空列表平均分为 None。"""
    passed = [score for score in scores if score >= pass_mark]
    average = sum(scores) / len(scores) if scores else None
    return {'count': len(scores), 'passed': passed, 'average': average}

original = [90, 55, 80]
print(summarize_scores(original))
# {'count': 3, 'passed': [90, 80], 'average': 75.0}
print(summarize_scores([], pass_mark=70))
# {'count': 0, 'passed': [], 'average': None}
print(original)  # [90, 55, 80]：没有修改输入
```

这个练习连接了列表筛选、字典、参数和返回值。当前约定成绩都是数值，未校验分数范围；后续学习异常时可以再增加非法类型与范围检查，不把简化案例误当作完整接口校验。

## 11. 回顾练习

```python
def update(values, step=1):
    values.append(step)
    values = [99]
    return values

original = [0]
result = update(original, step=2)
print(original)
print(result)

def greet_only(name):
    print(f'你好，{name}')

returned = greet_only('张三')
print(returned)
```

> [!question]- 展开查看答案
> - `original` 为 `[0, 2]`：先修改了传入的列表。
> - `result` 为 `[99]`：局部名字重新绑定后，将新列表返回给调用方。
> - `greet_only` 先输出“你好，张三”，随后 `print(returned)` 输出 `None`，因为函数没有显式返回其他值。

下一步可尝试将第九课的标签清理封装成 `clean_tags(text)`，要求返回列表而不是只打印，并处理空字符串。装饰器、生成器函数、异步函数和复杂递归结构留到后续实际需求再学。
