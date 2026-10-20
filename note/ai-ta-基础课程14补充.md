# 基础课程14：文件操作、with、os 与路径

运行案例：`python-learn1/demo14.py`。

关联知识：[[ai-ta-基础课程9补充]]、[[ai-ta-基础课程11补充]]、[[ai-ta-基础课程13补充]]

> [!important] 当前必学
> 路径表示位置，文件对象负责实际读写；创建 Path 不会创建文件。
> 文本模式读写 str，二进制模式读写 bytes。明确文本编码，优先使用 with 管理关闭。
> `w` 会在成功打开时截断已有文件，不是等 write 时才覆盖。
> with 管理资源退出，不提供事务回滚；发生异常前已经写入的内容不会自动撤销。

本课案例只在 `TemporaryDirectory` 新建的独立临时目录内写入、复制、改名和删除，不读取或改动你的 `store` 资料。运行结束后自动清理；如果要保留文件，需要另行选择明确的练习目录。

## 1. 文件操作的基本流程

准备路径 → 以合适模式打开 → 读取或写入 → 关闭资源。

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory(prefix='lesson14-note-') as directory:
    path = Path(directory) / 'hello.txt'
    with open(path, 'w', encoding='utf-8') as file:
        file.write('你好，Python')

    print(file.closed)  # True：离开内层 with 后文件关闭
    with open(path, 'r', encoding='utf-8') as file:
        print(file.read())  # 你好，Python
```

`open()` 返回文件对象，不是直接返回文件全部内容。即使路径正确，也可能因权限、磁盘或编码等原因失败，所以要结合上一课的异常处理理解。

## 2. 打开模式：决定是否创建、截断和追加

| 模式 | 用途 | 不存在时 | 已存在时 |
| --- | --- | --- | --- |
| `r` | 读取，默认模式 | 抛出 FileNotFoundError | 从开头读取 |
| `w` | 写入 | 创建文件 | 成功打开即截断为零长度 |
| `a` | 追加写入 | 创建文件 | 保留原内容，写入追加到末尾 |
| `x` | 排他创建 | 创建文件 | 抛出 FileExistsError |

`b` 表示二进制模式，如 `rb`、`wb`；默认 `t` 为文本模式。`+` 表示读写更新，如 `r+`、`w+`、`a+`，但不会抵消基本模式的行为。

- `r+`：允许读写，不自动截断，文件必须存在。
- `w+`：允许读写，但打开时依然会截断原内容。
- `a+`：允许读取和追加，读取前常需要 `seek(0)`，写入仍追加。

> [!warning] w / w+ 不是“只改写相同数量的字符”
> 原文件有 100 个字符，以 w 打开后只写一个字符，结果不会保留后面 99 个字符。r、w 等模式也不会自动创建缺失的父目录。

本课先熟练使用单向读写，理解文件位置后再用 `+`，避免同时读写时把位置弄错。

## 3. 编码：文本与字节之间的转换规则

```python
text = '你好'
data = text.encode('utf-8')
print(len(text), len(data))  # 2 6
print(data.decode('utf-8'))  # 你好
```

文本文件在磁盘上仍然存储字节。`open(..., encoding='utf-8')` 在文本与字节之间执行编码和解码，文本模式下 `read()` 返回 str，`write()` 接收 str。

默认编码受 Python 版本、运行配置与环境影响。项目中明确写出文本编码，有助于跨环境运行，但读取已有文件时仍需匹配它实际使用的编码；写 `encoding='utf-8'` 不会把任意旧文件自动转为 UTF-8。

二进制模式不传 `encoding`，读写 bytes；图片、音频、压缩包通常应按二进制处理，不先强行解码为字符串。

> [!warning] 忽略解码错误可能丢数据
> `errors='ignore'` 可能跳过无法解码的字节，不能因为“不报错”就认为内容正确。遇到 UnicodeDecodeError，先检查来源编码、数据完整性及是否把二进制误当文本。

## 4. with 做了什么，没做什么

`with` 是上下文管理语法，不只用于文件。对普通文件对象，它在离开代码块时执行关闭，包括因异常或函数返回离开。

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory(prefix='lesson14-note-') as directory:
    path = Path(directory) / 'partial.txt'
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write('已经写入')
            raise ValueError('故意中断')
    except ValueError:
        print(file.closed)  # True
    print(path.read_text(encoding='utf-8'))  # 已经写入：并没有回滚
```

如果 `open()` 本身失败，还没有成功得到文件对象，就不能假定后面的变量已经赋值。捕获合适的异常，别在失败路径里对未创建的句柄调用 `close()`。

> [!tip] 和前端经验的联系
> with 可类比“把获取和释放资源的生命周期组织在一起”，不是 JS 的 with 语句，也不是自动重试或自动撤销操作。它与 try/finally 有联系，但上下文管理协议允许资源管理器定义更具体的退出行为。

## 5. 读取方式与文件当前位置

| 方法 | 返回值 | 注意 |
| --- | --- | --- |
| `file.read()` | 所有剩余内容 | 大文件会占用较多内存 |
| `file.read(size)` | 最多指定数量的内容 | 文本按字符，二进制按字节理解 |
| `file.readline()` | 一行内容 | 通常保留行尾换行；末尾返回空字符串或空 bytes |
| `file.readlines()` | 剩余各行组成的列表 | 不是逐行流式处理的替代品 |
| `for line in file` | 逐行迭代 | 适合常见逐行处理任务 |

```python
from io import StringIO

with StringIO('Python\nJS\n') as file:
    print(repr(file.readline()))  # 'Python\n'
    print(repr(file.read()))      # 'JS\n'：从当前位置继续
    print(repr(file.read()))      # ''：已经到末尾
    file.seek(0)
    print(file.readlines())       # ['Python\n', 'JS\n']
```

重复 read 不会自动从头再读，需要 `seek(0)` 回到开头。对真实大文件，优先循环逐行处理或按块读取，而不是读入全部内容后再遍历。

### 保留正文与换行的区别

`print(line)` 自己还会加一个换行，若 line 已含换行，容易出现额外空行。可用 `print(line, end='')` 保持原样，或按需要处理行尾。

`strip()` 会删两端空白，不适合所有正文；如果只想去掉一个行尾换行，可以按规则使用 `rstrip('\n')` 等。先确定是否允许改变缩进与尾随空格，再选择清理方式。

## 6. 写入、换行与缓冲

```python
from io import StringIO

with StringIO() as file:
    count = file.write('第一行\n')
    file.writelines(['第二行\n', '第三行'])
    print(count)                 # 4：字符数
    print(repr(file.getvalue())) # '第一行\n第二行\n第三行'
```

`write()` 返回写入的字符数或字节数，不是写入后的完整内容。`writelines()` 不会自动给每项补换行，想分行要自己提供 `\n`。

文本模式默认可将读取到的常见行结束符规范化为 `\n`；写入时默认换行转换可能随系统而异。需要明确生成 LF 换行时，可在 `open()` 中指定 `newline='\n'`。`newline=''` 等设置另有含义，不要把所有配置都当作“去掉换行”。

普通文件写入通常有缓冲，`flush()` 将 Python 缓冲内容交给下层，关闭文件也会处理缓冲；这不等于已经保证断电后数据仍在。操作系统同步、原子替换与可靠持久化在实际项目中再深入。

## 7. 二进制与 seek / tell

```python
from io import BytesIO
import os

with BytesIO(b'ABCDE') as file:
    print(file.read(2))          # b'AB'
    print(file.tell())          # 2
    file.seek(-2, os.SEEK_END)
    print(file.read())           # b'DE'
```

二进制文件可按字节位置理解 seek 的偏移；`os.SEEK_SET`、`os.SEEK_CUR`、`os.SEEK_END` 分别表示相对开头、当前位置和末尾。

> [!warning] 文本模式的位置不是任意字符索引
> 文本流 tell 返回的位置值可能包含恢复解码状态所需的信息，不应直接当作 Unicode 字符序号做算术。常见安全用法是 `seek(0)`，或使用先前 tell 返回的位置恢复读取。需要任意字节偏移时使用合适的二进制方式。

## 8. os 与 pathlib：两套常用接口

| 需求 | os / os.path | pathlib |
| --- | --- | --- |
| 当前工作目录 | `os.getcwd()` | `Path.cwd()` |
| 拼接路径 | `os.path.join(...)` | `base / 'name.txt'` |
| 是否文件 / 目录 | `os.path.isfile` / `isdir` | `path.is_file()` / `is_dir()` |
| 创建目录 | `os.mkdir` / `os.makedirs` | `path.mkdir(parents=True, exist_ok=True)` |
| 列出子项 | `os.listdir` / `os.scandir` | `path.iterdir()` |
| 递归遍历 | `os.walk` | 按需用 glob / rglob 等接口 |
| 改名 / 替换 | `os.rename` / `os.replace` | `path.rename()` / `replace()` |
| 删除文件 | `os.remove` / `os.unlink` | `path.unlink()` |
| 删除空目录 | `os.rmdir` | `path.rmdir()` |

`pathlib` 自 Python **3.4** 起进入标准库；旧课程偏重 os 时，可以两者对照学习，没必要把旧接口都判为错误。普通文件路径操作可优先用 Path 表达，os 也提供环境变量等其他系统接口。

### 相对路径以什么为基准？

`open('store/demo.txt')` 通常相对进程工作目录，不自动相对源码文件。`Path(__file__).resolve().parent` 可取得文件所在目录，交互环境未必有 `__file__`。

避免为了让一个相对路径成功就在工具函数里 `os.chdir()`，它会改变整个进程的工作目录，影响其他读写。明确传入目录或构造路径通常更容易维护。

```python
from pathlib import Path

example = Path('notes') / 'lesson.txt'
print(example.name)    # lesson.txt
print(example.stem)    # lesson
print(example.suffix)  # .txt
print(example.parent.as_posix())  # notes
```

`os.listdir()` 返回名称，`Path.iterdir()` 返回子路径对象；不要默认它们按名字排序。`os.walk()` 提供当前目录、子目录名和文件名，名字仍要与当前目录拼接后才能表示对应路径。

## 9. 复制、删除与路径边界

`shutil.copyfile(source, target)` 复制文件内容；`copy2()` 还尝试保留更多元数据，不等于复制所有平台特性。改名的覆盖规则可能因接口与操作系统而不同，不能假定 rename 在每个环境都拒绝覆盖目标。

删除普通文件用 unlink/remove，rmdir 只删空目录。递归删除会影响整棵目录树，真实资料不要拿来随手试验。本课只对明确创建的临时目录执行这些操作，代码没有递归删除任意输入路径的入口。

`exists()` 的检查与后续操作之间仍可能发生变化，权限也可能改变；检查通过不保证打开、复制或删除一定成功。能合理恢复时捕获具体的 OSError 子类，不靠 `except: pass` 忽略失败。

文件名如果来自外部输入，后续项目还需验证路径范围；路径拼接不是访问范围隔离工具。本课使用固定文件名和独立目录，先练基本机制。

## 10. JSON 文件：把前面学过的数据保存下来

`demo14.py` 提供 `save_students(path, students)` 与 `load_students(path)`：

- 保存前先调用 `json.dumps()`，格式不支持时还没有以 w 打开原文件，避免这类失败提前截断原内容。
- 写入时明确 UTF-8，读取时使用相同编码。
- 缺少父目录、权限不足、磁盘写入失败仍然可能报错，不提供完整的事务或原子更新保证。
- 读取失败不自动返回空列表，以免把损坏文件误当作“没有学生”。

```python
# 从 python-learn1 目录运行，复用本课工具函数。
from pathlib import Path
from tempfile import TemporaryDirectory
from demo14 import save_students, load_students

with TemporaryDirectory(prefix='lesson14-note-') as directory:
    path = Path(directory) / 'students.json'
    students = [{'name': '张三', 'score': 90}]
    save_students(path, students)
    restored = load_students(path)
    print(restored == students)  # True
```

JSON 语法错误通常抛出 `json.JSONDecodeError`，它是 ValueError 的子类。语法正确也不代表结构符合业务要求，例如读到数字而不是记录列表，还需要单独校验。不能用 `eval()` 代替 JSON 解析外部数据。

## 11. 和 Node.js 文件操作的对照

| 内容 | Python 本课 | Node.js 对照 |
| --- | --- | --- |
| 文本读取 | `open(..., encoding='utf-8')` 或 Path 方法 | fs 接口指定编码后得到字符串 |
| 二进制内容 | bytes | 常见为 Buffer |
| 路径组织 | pathlib / os.path | path 模块 |
| 本课执行方式 | 普通文件接口是同步操作 | fs 有同步接口与异步 / Promise 接口 |

不要因 Python 代码写在函数里就认为文件 I/O 自动异步。CLI 脚本先把同步读写写清楚，异步后端中如何避免阻塞工作线程或事件循环，留到相应项目再学。

## 12. 回顾练习

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory(prefix='lesson14-note-') as directory:
    path = Path(directory) / 'count.txt'
    with open(path, 'w', encoding='utf-8') as file:
        file.write('12')
    with open(path, 'a', encoding='utf-8') as file:
        file.write('3')
    with open(path, encoding='utf-8') as file:
        first = file.read(1)
        rest = file.read()
        end = file.read()
    print(first, rest, repr(end))
    with open(path, 'w', encoding='utf-8') as file:
        file.write('9')
    print(path.read_text(encoding='utf-8'))
```

> [!question]- 展开查看答案
> - 追加后文件内容是字符串 `'123'`，不是数学运算。
> - 输出 `1 23 ''`，read 从当前位置继续，末尾返回空字符串。
> - 最后输出 `9`，不是 `923`，因为 w 打开时已截断原文件。

当前优先掌握模式、编码、with、按行处理和路径；CSV、原子替换、并发写入、文件锁与持久化保障后续按项目需要学习。
