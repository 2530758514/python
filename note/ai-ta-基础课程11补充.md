# 基础课程11：异常与 try 处理流程

运行案例：`python-learn1/demo11.py`。所有故意触发的异常都在示例边界处理，可整份运行，不需要交互输入，也不会写入磁盘文件。

关联知识：[[ai-ta-基础课程10补充]]、[[ai-ta-基础课程6补充]]、[[ai-ta-基础课程9补充]]

> [!important] 当前必学
> 异常表示程序执行遇到了无法按当前路径继续处理的情况。处理异常不是让失败操作自动成功，而是决定如何恢复、提示、清理或继续向外报告。
> 优先捕获能合理处理的具体类型，缩小 `try` 的范围，不把所有错误都当作同一种输入问题。
> 捕获之后从处理块之后继续，不回到出错语句，也不自动执行被跳过的语句。

## 1. 异常与语法错误、逻辑错误

| 情况 | 例子 | 处理方向 |
| --- | --- | --- |
| 语法错误 | 漏写冒号、缩进错误 | 先修正代码，使文件可以解析 |
| 运行时异常 | `int('abc')`、除以零 | 修正原因，或在合适边界处理可预期的失败 |
| 逻辑错误 | 用错公式，结果不符合业务要求 | 不一定抛异常，需要检查需求、结果与边界 |

同一个文件如果无法解析，里面的 `try` 还没有机会执行，因此不能靠它捕获这个文件自身的语法错误。不过动态解析的代码仍可产生可捕获的 `SyntaxError`：

```python
try:
    compile('if True print(1)', '<学习示例>', 'exec')
except SyntaxError:
    print('动态解析的代码有语法错误')
```

`compile()` 本课只用于说明这个边界，不要求现在掌握动态执行。

## 2. 从报错信息中读什么

```text
Traceback (most recent call last):
  File "demo.py", line 2, in <module>
    number = int('abc')
ValueError: invalid literal for int() with base 10: 'abc'
```

先看最后的异常类型与说明，再向上找自己的代码位置与调用链。实际文件路径、行号、措辞可能随代码和解释器版本变化，不必背完整英文消息。

不要只截最后一句就忽略前面的调用位置；也不要因为“程序没退出”就认为数据已经正确处理。

## 3. 常见异常类型速查

| 类型 | 常见原因 | 例子 |
| --- | --- | --- |
| `ValueError` | 参数类型可接受，但值不符合要求 | `int('abc')`、`items.index(不存在的值)` |
| `TypeError` | 操作、参数类型或调用方式不合要求 | `'年龄' + 18`、函数缺少必需参数 |
| `ZeroDivisionError` | 除数为零 | `10 / 0` |
| `IndexError` | 序列索引越界 | `[1][3]` |
| `KeyError` | 字典等按键查找或删除失败 | `{}['name']`、`set().remove(1)` |
| `NameError` | 找不到名字 | 使用未定义变量 |
| `UnboundLocalError` | 局部名字尚未绑定就读取 | 第十课中未声明 global 的局部自增案例 |
| `AttributeError` | 对象不存在该属性或方法 | `(1, 2).append(3)` |
| `FileNotFoundError` | 文件或路径不存在 | 读取不存在的文件 |
| `PermissionError` | 文件或资源访问权限不足 | 无权读取或写入的路径 |
| `UnicodeDecodeError` | 字节不符合所选解码规则 | 不正确的编码或损坏数据 |
| `RecursionError` | 递归过深等递归限制问题 | 缺少终止条件的递归 |
| `AssertionError` | `assert` 检查失败 | `assert 1 == 2` |

这是识别方向，不是必须背完的清单。同一个表达式在不同输入下可能出现不同异常，调试时以实际报错为准。

## 4. try / except / else / finally

```python
raw = '2'

try:
    divisor = int(raw)
    result = 10 / divisor
except ValueError as error:
    print('转换失败：', type(error).__name__)
except ZeroDivisionError:
    print('除数不能为零')
else:
    print(result)  # 5.0
finally:
    print('本次尝试结束')
```

| 部分 | 什么时候执行 | 用途 |
| --- | --- | --- |
| `try` | 进入时执行，遇到异常跳出剩余部分 | 放可能失败的操作 |
| `except` | 出现匹配的异常时，执行第一个匹配分支 | 恢复或转换错误 |
| `else` | `try` 正常执行到末尾时 | 放成功后的操作 |
| `finally` | 正常控制流离开结构前执行，包括异常传播或函数返回 | 清理资源等 |

`else` 和 `finally` 都可按需省略；`try` 不能孤立存在，至少需要 `except` 或 `finally`。如果 `try` 中通过 `return`、`break` 或 `continue` 提前离开，也不会执行它的 `else`。

> [!warning] finally 不是“任何情况下绝对会执行”
> 正常解释器控制流中，它会在返回或异常向外传播前运行；进程被强制终止、断电等不属于这种保证。不要把 finally 当作持久化数据必定成功的保证。

### 捕获后不会接着执行失败点后面的代码

```python
try:
    number = int('abc')
    print('不会执行到这里')
except ValueError:
    print('输入无效')

print('从结构之后继续')
```

`number` 也没有因这次失败赋值而获得新值。后续不要直接使用只在成功路径中才会创建的变量，优先把使用逻辑放在 `else`，或在设计上明确失败分支。

### else / except / finally 中的新异常不由同级 except 接住

```python
try:
    try:
        number = int('2')
    except ValueError:
        print('内部：转换错误')
    else:
        result = number / 0  # 内部 except 不负责这里的新异常
except ZeroDivisionError:
    print('由外层捕获 else 中的异常')
```

这是缩小 `try` 的价值：避免把后续业务代码里的错误也误当作输入转换错误。

## 5. 捕获范围、多个类型与继承关系

```python
for index in [0, 5, '0']:
    try:
        print([10, 20][index])
    except (IndexError, TypeError) as error:
        print(type(error).__name__)
# 10、IndexError、TypeError
```

多个类型共用处理逻辑时用元组形式，`except (A, B)` 也适用于旧 Python 3 课程。不写 `except A or B`，那不是捕获两个类型。

异常存在继承关系，例如 `KeyError`、`IndexError` 属于 `LookupError`；`FileNotFoundError`、`PermissionError` 属于 `OSError`。捕获父类会同时捕获它的子类，因此具体分支应放在通用分支前面。

```python
try:
    {}['name']
except KeyError:
    print('缺少这个键')
except LookupError:
    print('其他查找错误')
```

### 为什么不统一写 except Exception？

`Exception` 覆盖大多数普通运行时异常，用得太宽可能把拼错变量名、代码缺陷或不可恢复的错误一起掩盖。只有边界明确、确实要统一记录并处理时才使用，不把它当作每个函数的必备包装。

`KeyboardInterrupt`、`SystemExit` 不属于 `Exception`，而属于更上层的 `BaseException` 体系。裸 `except:` 或捕获 `BaseException` 可能拦住用户中断与退出信号，普通业务代码应避免随意使用。

> [!warning] 不用 except: pass 掩盖问题
> `pass` 只是忽略当前分支，没有修复失败操作，后续可能继续使用缺失或过期数据。若明确允许失败，应解释原因，并给出清楚的回退行为或保留诊断信息。

## 6. 异常传播：在哪一层处理？

```python
def parse_count(raw):
    return int(raw)

try:
    count = parse_count('abc')
except ValueError:
    print('请提供整数文本')
```

内层不处理时，异常沿调用链向外传播，直到匹配处理器；没有处理器时通常终止当前执行并报告 traceback。不是每个函数都必须捕获自己可能抛出的所有异常。

适合的分工：底层负责计算与报告问题，上层负责向使用者提示、决定回退或退出。调用链上反复捕获、打印再返回假结果，会让问题更难定位。

## 7. raise：主动报告不符合约定的输入

```python
def validate_score(score):
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError('成绩必须是数值，不能是布尔值')
    if not 0 <= score <= 100:
        raise ValueError('成绩必须在 0～100 之间')
    return score

print(validate_score(88))  # 88
try:
    validate_score(101)
except ValueError as error:
    print(str(error))      # 成绩必须在 0～100 之间
```

`raise` 抛出异常，后续当前路径立即中断；仅创建 `ValueError('说明')` 或打印“错误”都不会自动抛出异常。本例明确接受内置 `int` / `float` 体系中的数值并排除布尔值，不代表所有项目都只能使用这两类数值。

不把合法业务结果随意当异常，例如“搜索没有结果”通常可返回空列表；异常适合表达当前操作无法按约定完成。

### 裸 raise：重新抛出正在处理的异常

```python
def parse_required_integer(raw):
    try:
        return int(raw)
    except ValueError:
        print('转换失败，继续向调用方报告')
        raise

try:
    parse_required_integer('abc')
except ValueError:
    print('调用方收到了异常')
```

在处理器中用 `raise` 重新抛出原异常，保留原来的回溯；通常不必改为 `raise error` 来重新附加当前抛出位置。没有正在处理的异常时执行裸 `raise` 会报 `RuntimeError`。

### 了解即可：raise ... from ... 保留因果关系

```python
def parse_age(raw):
    try:
        return int(raw)
    except ValueError as error:
        raise ValueError('年龄需要填写整数文本') from error

try:
    parse_age('eighteen')
except ValueError as error:
    print(str(error))                      # 年龄需要填写整数文本
    print(type(error.__cause__).__name__)  # ValueError
```

转换成面向当前业务的说明，同时明确保留原始原因。这里示范的是格式转换，不包含年龄正负或范围校验。复杂日志或后台诊断应保留 traceback，而不只留一句“失败了”。

## 8. finally 与 return：不要吞掉错误

```python
def read_status():
    try:
        return '已完成'
    finally:
        print('先清理')

print(read_status())  # 先输出“先清理”，再输出“已完成”
```

> [!warning] 不在 finally 中 return
> finally 中的 return 可能覆盖原返回值，甚至压住正在传播的异常；里面的 break、continue 也可能带来控制流问题。清理逻辑应尽量简单，也要避免让清理时的新异常掩盖原始原因。

## 9. 了解即可：with 管理资源

```python
from io import StringIO

with StringIO('Python\nJS') as stream:
    print(stream.readline().strip())  # Python

print(stream.closed)  # True：离开 with 后已关闭
```

这里使用内存文本对象，便于直接运行且不依赖文件。真实文件通常用 `with open(path, encoding='utf-8') as file:` 管理关闭，文件操作课再展开。

对于正常的文件上下文管理，离开代码块时会关闭资源，包括因异常离开；这不代表 `with` 自动把异常变成成功，也不代表所有上下文管理器都采用相同的异常处理策略。

## 10. 了解即可：自定义异常与 assert

```python
class InvalidScoreError(ValueError):
    """一种有明确名称的业务校验错误。"""

try:
    raise InvalidScoreError('当前操作要求成绩至少为 60')
except InvalidScoreError as error:
    print(str(error))
```

类和继承后续再学，现在先认识自定义异常可以命名一种错误，让调用方有针对性地处理。一般基于 `Exception` 或合适的普通异常子类，而不是直接继承 `BaseException`。

`assert 条件, '说明'` 可检查开发者预期的内部不变量，失败时抛出 `AssertionError`；优化运行可能移除断言，不应靠它验证用户输入、业务权限或关键外部数据。业务校验使用明确条件和 `raise`。

## 11. 与 JS 的对照

| 需求 | Python | JS 对照 |
| --- | --- | --- |
| 捕获 | `except ValueError as error` | `catch (error)` 后自己判断类型 |
| 多种错误分类 | 多个 except，按顺序匹配 | 通常在 catch 内分支判断 |
| 成功路径 | 可使用 `else` | 没有同样的 try-else 语法 |
| 清理 | `finally` | 也有 finally |
| 主动抛出 | `raise ValueError('说明')` | `throw new Error('说明')` 等 |

Python 必须抛出异常类或实例，不像 JS 可以随意 `throw` 一个字符串。异步任务中的错误边界后续结合 `async` / `await` 再学，不把同步 try 规则直接套到未等待的后台任务上。

## 12. 小实践与回顾练习

`demo11.py` 的 `first_valid_count()` 依次尝试候选文本，最多转换指定次数，返回第一个合法非负整数。它允许结果为 `0`，没有结果时明确抛错；只捕获可预期的格式错误，不把错误输入类型统一吞掉。

先预测下面的输出顺序：

```python
for raw in ['0', 'bad', '2']:
    try:
        value = 8 / int(raw)
    except ValueError:
        print('格式错误')
    except ZeroDivisionError:
        print('不能除以零')
    else:
        print(f'结果：{value}')
    finally:
        print('本轮结束')
```

> [!question]- 展开查看答案
> - 第一轮：`不能除以零` → `本轮结束`。
> - 第二轮：`格式错误` → `本轮结束`。
> - 第三轮：`结果：4.0` → `本轮结束`。
> - 失败轮次不会执行 else，finally 也不表示本轮操作成功。

当前优先掌握具体异常、成功和失败路径、raise 与捕获边界。异常组与 `except*`、异步取消、框架全局异常处理属于后续并发或后端项目内容，本课不提前展开。
