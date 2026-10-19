# 基础课程13：模块、包与标准库

入口案例：`python-learn1/demo13.py`。

教学包：`python-learn1/lesson13_tools/`。

关联知识：[[ai-ta-基础课程10补充]]、[[ai-ta-基础课程11补充]]、[[ai-ta-基础课程12补充]]

> [!important] 当前必学
> 模块提供独立命名空间，包用于组织模块。模块不都对应普通 `.py` 文件。
> import 是加载模块并绑定名字，不是把另一个文件的文本复制过来。
> 导入可能执行模块顶层代码；演示或启动逻辑放在主入口保护中。
> 标准库不等于第三方库；内置模块只是标准库模块的一部分。

## 1. 四个概念先分清

| 概念 | 含义 | 例子 |
| --- | --- | --- |
| 模块 module | 可导入的组织单位，有自己的命名空间 | `scores.py`、`math`、`sys` |
| 包 package | 可以包含子模块、子包的组织单位，本身也是模块 | 本课 `lesson13_tools` |
| 标准库 | Python 发行版提供的常用功能集合 | `json`、`pathlib`、`datetime` |
| 第三方库 / 分发包 | 独立于标准库发布的依赖 | 后续后端、HTTP 等项目使用的外部依赖 |

`len()`、`print()` 是内置函数，通常不需要 import。`sys` 等内置模块仍需导入才能通过模块名字使用。`math` 等可能以扩展模块提供，不能简单理解成“所有库都是一份 Python 源码”。

模块名、导入包名与安装用的分发包名不一定一一对应；以后缺少依赖时，先查项目要求与官方安装说明，不直接根据 import 名字猜安装命令。

## 2. 三种常见导入形式

```python
import math
import math as maths
from math import sqrt

print(math.sqrt(9))   # 3.0
print(maths.sqrt(16)) # 4.0
print(sqrt(25))       # 5.0
```

- `import math` 绑定模块名，再用 `math.sqrt()` 访问属性。
- `import math as maths` 使用本地别名，不会修改模块本身的名称。
- `from math import sqrt` 将取出的对象绑定到当前名字，当前作用域不因此自动得到 `math` 这个名字。

多个模块都有同名函数时，保留模块限定名常更清楚。`from module import *` 容易污染命名空间和覆盖已有名字，学习与业务代码都优先明确导入。

### 导入绑定不等于实时变量链接

`from some_module import value` 把当时取出的对象绑定到当前名字。如果模块以后把 `value` 重新赋值，已导入的本地名字不会自动同步；如果大家引用的是同一个可变对象，修改对象内容则可能互相可见。这仍然是第十课的名字绑定与共享规则。

## 3. 本课包结构与依赖方向

```text
python-learn1/
├── demo13.py
└── lesson13_tools/
    ├── __init__.py
    ├── __main__.py
    ├── scores.py
    └── reports.py
```

| 文件 | 职责 |
| --- | --- |
| `scores.py` | 校验成绩与计算统计结果，不负责打印 |
| `reports.py` | 复用计算模块，将结果整理为文本 |
| `__init__.py` | 普通包初始化，选择性暴露常用接口 |
| `__main__.py` | `python -m lesson13_tools` 时的入口 |
| `demo13.py` | 组织演示，调用包与标准库 |

依赖方向为“入口 → 展示 → 计算”，计算模块不反过来导入入口。不是每个文件都需要导入其他所有文件。

```python
# 从 python-learn1 目录运行本段，或使用 demo13.py 入口。
import lesson13_tools
from lesson13_tools import scores as score_tools
from lesson13_tools.reports import format_report

print(lesson13_tools.summarize_scores([90, 55, 80]))
# {'count': 3, 'passed': [90, 80], 'average': 75.0}
print(format_report([]))  # 人数：0，及格：0，平均分：暂无
print(score_tools.__name__)  # lesson13_tools.scores
```

模块导入名通常使用合法标识符，不写 `.py`，不把文件路径分隔符当作模块名；嵌套模块使用点号。现有目录 `python-learn1` 带连字符，本课不把它当作常规包名，而是在其中组织命名规范的子包。

## 4. 普通包、相对导入与命名空间包

本课 `reports.py` 使用 `from .scores import summarize_scores`：点号表示当前包，两个点表示上一级包。相对导入基于包上下文，不是根据“当前文件夹看起来在哪里”随意猜测。

`__init__.py` 可以为空，也可以像本课那样从子模块导入常用接口。保持初始化轻量，避免一导入包就启动网络请求、读写文件或执行交互输入。

> [!tip] 修正旧课程中可能的绝对说法
> 普通包通常有 `__init__.py`；Python **3.3 起**支持无需该文件的隐式命名空间包。因此“任何没有 __init__.py 的目录都绝对不能成为包”并不准确。本课先使用普通包，复杂命名空间包后续按需学习。

本课 `__all__ = ['summarize_scores']` 主要控制星号导入暴露哪些名字，不是访问控制，也不阻止明确导入其他子模块。知道它的用途即可，不要求每个模块都添加。

## 5. __name__、主入口与 -m

```python
def main():
    print('开始执行本文件的演示')

if __name__ == '__main__':
    main()
```

直接运行文件时，其 `__name__` 通常为 `'__main__'`；正常导入时则是导入模块名，例如 `'demo13'`。保护块让函数定义可以被复用，而演示只在作为入口执行时启动。

> [!warning] 主入口保护不阻止所有导入行为
> 模块顶层的 import、赋值、函数 / 类定义，以及保护块之外的其他语句仍会执行。仅添加保护块，却把打印、请求、输入写在外面，不能避免那些副作用。

### 两种运行方式，注意各自工作目录

从项目根目录运行脚本：

```powershell
python python-learn1/demo13.py
```

在 `python-learn1` 目录运行包：

```powershell
python -m lesson13_tools
```

后者会执行包的 `__main__.py`，输出“人数：3，及格：2，平均分：75.0”。不要把 `-m` 参数写成文件路径或加 `.py`。

不要用 `python lesson13_tools/reports.py` 直接运行包含包内相对导入的文件；它可能缺少已知父包上下文。使用设计好的入口，或从包父目录通过 `-m` 运行对应模块。

## 6. 导入路径、缓存与模块来源

正常导入会检查模块缓存，并按导入机制查找加载。`sys.path` 是其中重要的模块搜索路径来源，但不能把整个过程简单等同于逐个目录搜索，内置模块等还有对应查找机制。

```python
import math
import math as another_math
import sys

print(another_math is math)      # True
print(sys.modules['math'] is math)  # True
print(math.__name__)            # math
```

同一解释器进程中，正常重复导入同一名字通常复用缓存，不会每次都从头执行模块。不同进程的缓存互不共享；重新加载、以不同名字加载等另有规则，不据此宣称“任何时候一个文件只执行一次”。

### 排查来源时看什么

- `sys.executable`：当前使用的解释器。
- `sys.path`：当前模块搜索路径配置的一部分。
- `module.__name__`：模块名。
- `module.__package__`：包上下文信息。
- `module.__file__`：文件型模块的来源路径；内置模块或某些特殊模块未必有这个属性。

> [!warning] 不用 sys.path.append 随意修补结构
> 从脚本文件启动与从 `-m` 启动时，默认搜索路径的起点可能不同，隔离运行等配置也会影响结果。遇到失败先核对启动位置和包结构，不到处追加绝对路径，也不依赖 IDE 私下添加的搜索路径。

本课从根目录运行 `python python-learn1/demo13.py`，脚本目录可用于找到同级的教学包，不需要修改全局环境。

## 7. 常见导入错误与循环依赖

| 现象 | 优先检查 |
| --- | --- |
| `ModuleNotFoundError` | 名字是否拼错、包父目录是否可搜索、依赖是否安装到当前解释器 |
| `ImportError: cannot import name ...` | 目标是否定义该名字、版本差异、循环导入 |
| `attempted relative import with no known parent package` | 是否直接运行了包内相对导入文件 |
| 看似标准库却缺少常用属性 | 是否有同名本地文件遮蔽了真正模块 |

不要随意给文件命名为 `json.py`、`random.py`、`copy.py`、`typing.py` 等，可能遮蔽原本想导入的模块。改名后还要检查实际模块来源，必要时重启旧的交互进程，避免缓存造成误判。

循环导入是 A 导入 B、B 又在 A 尚未初始化完时读取 A 中的名字。优先调整职责与依赖方向，将共同功能移到更底层的模块；不是一律“把所有 import 移进函数”就算解决。

异常也可能发生在模块初始化内部，例如它依赖的另一个模块不存在。看到 `ModuleNotFoundError` 时要读完整回溯，不能直接认定最外层包没安装。

## 8. 标准库入门：用到什么查什么

| 模块 | 常见用途 | 本课重点 |
| --- | --- | --- |
| `math` | 数学函数 | `sqrt`、`ceil`、`floor`、`factorial` |
| `collections` | 常用容器工具 | `Counter` 计数 |
| `json` | JSON 文本与 Python 对象转换 | `dumps` / `loads` |
| `pathlib` | 路径表示与文件操作入口 | 区分路径对象、工作目录和文件所在目录 |
| `datetime` | 日期、时间、时间间隔 | `date` / `timedelta` |
| `random` | 模拟、抽样等伪随机操作 | `choice` / `sample` |
| `sys` | 解释器相关信息 | 当前解释器、导入路径与缓存 |

### 数学与计数

```python
import math
from collections import Counter

print(math.ceil(2.1), math.floor(-2.1))  # 3 -3
print(math.factorial(5))                 # 120
print(dict(Counter(['Python', 'JS', 'Python'])))
# {'Python': 2, 'JS': 1}
```

标准库阶乘可以替代第十课的手写教学实现。先理解原理，再在适合的场景复用可靠工具，不需要每次重复造轮子。

### JSON 文本与 Python 字典不是同一种类型

```python
import json

record = {'name': '张三', 'passed': True, 'remark': None}
text = json.dumps(record, ensure_ascii=False)
print(text)  # {"name": "张三", "passed": true, "remark": null}
print(json.loads(text) == record)  # True
print(type(text))  # <class 'str'>
```

`dumps/loads` 处理字符串，`dump/load` 则与文件对象配合，文件课再展开。默认 JSON 序列化不支持任意类实例、集合等；`str(dictionary)` 也不是规范 JSON 文本。`ensure_ascii=False` 控制字符串转义展示，不是文件编码设置。

### 随机操作与日期

```python
import random
from datetime import date, timedelta

rng = random.Random(13)
result = rng.sample([1, 2, 3, 4], k=2)
print(len(result), len(set(result)))  # 2 2：不放回抽取，原样本各项唯一
print((date(2026, 1, 1) + timedelta(days=7)).isoformat())  # 2026-01-08
```

`sample` 按样本位置不放回抽取，如果原序列中值有重复，结果仍可能有相等的值。`random` 用于一般模拟，不用于密码、登录令牌；这类需求后续使用标准库 `secrets`。复杂时区与线上时间处理留到项目阶段。

## 9. 工作目录与 __file__ 所在目录

`Path.cwd()` 是进程当前工作目录，取决于如何启动；`Path(__file__).resolve().parent` 是当前文件所在目录。

`demo13.py` 使用文件所在目录拼接示例路径，因此不必把启动位置误当成脚本位置。普通交互环境不一定定义 `__file__`，复制这段逻辑到 REPL 前要意识到上下文差别。

拼接 `Path` 对象不会创建文件；调用读写方法时才发生相应操作。路径与编码、异常处理将在文件课程中结合实践。

## 10. 安装依赖、虚拟环境与字节码缓存

本课只使用标准库和自己编写的包，无需安装第三方依赖。

后续项目需要外部依赖时，先确认目标项目虚拟环境和解释器，再按其文档安装。`python -m pip ...` 有助于明确使用这个 python 对应的 pip，避免“装到了另一个解释器”的问题。

> [!tip] 与前端经验对应
> import 更接近 JS 的模块导入；pip 是 Python 的包安装工具，功能上可与 npm 的安装用途类比。
> 但 Python 包结构、模块初始化、虚拟环境与 Node 的解析机制不是同一套规则，不直接套用 node_modules 或 package.json 的经验。

导入文件型模块时，可能生成 `__pycache__` 中的 `.pyc` 字节码缓存，这是正常行为，不是源码或必需提交的学习成果。本次根目录 `.gitignore` 只增加 Python 字节码缓存规则；运行时 `python -B ...` 可关闭字节码缓存写入，本课验证使用它避免产生额外文件。

`.pyc` 不是可靠源码保护方案，也不是完整安装依赖的替代品。项目发布、依赖锁定、包分发与 `pyproject.toml` 等内容后续按实际项目学习。

## 11. 回顾练习

从 `python-learn1` 目录运行，先预测输出：

```python
import lesson13_tools
from lesson13_tools.scores import summarize_scores
from lesson13_tools.reports import format_report

print(lesson13_tools.summarize_scores is summarize_scores)
print(summarize_scores([0, 60, 100], pass_mark=60)['passed'])
print(format_report([]))
```

> [!question]- 展开查看答案
> - `True`：包初始化暴露的是 scores 模块中的同一个函数对象。
> - `[60, 100]`：0 是合法成绩，但未达到及格线。
> - `人数：0，及格：0，平均分：暂无`：空输入不发生除以零。
> - 正常导入教学包不会自动执行包入口报告；`python -m lesson13_tools` 才进入本课包入口。

可以尝试把第九课的标签清理函数独立成模块，再从入口调用。当前优先掌握可复用函数、明确导入、主入口和包内依赖；插件加载、导入钩子和复杂发布流程暂不展开。
