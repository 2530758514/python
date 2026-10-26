# 基础实践：stusystem 学生信息系统补充

实践目录：`python-learn2/`。实践笔记统一使用 `ai-ta-基础实践<项目名>补充.md` 命名；助教对照代码使用 `-ai.py` 后缀，保留原始课程代码。

## 学生管理系统

### 添加功能：insert 与 save

原始文件：`python-learn2/stusystem.py`。

对照文件：`python-learn2/stusystem-ai.py`。

关联知识：[[ai-ta-基础课程10补充]]、[[ai-ta-基础课程11补充]]、[[ai-ta-基础课程14补充]]

> [!important] 这次学习的目标
> 不是把初学项目改成复杂框架，而是让每个函数职责清楚、失败路径明确、用户输入可重试、保存成功的提示可信。
> 插件警告有的指出真实风险，有的是可读性建议，不代表每一个黄色提示都会导致运行失败。

#### 一、我的问题记录

以下按“问题 + 解答”整理本轮问过的内容，与后面的优化说明分开。新问题先在对话中解释，等你说“记笔记”时再集中补充。

##### 问题 1：截图中的 save 函数错在哪里，所有警告都必须照改吗？

**解答：** 循环调用 write 可以正确写入，并不是语法错误；插件建议 writelines 主要是代码组织建议。更重要的两个问题是：

- 手动 close 在中途抛异常时可能执行不到，使用 with 管理文件关闭更稳妥。
- a 模式本就会在文件不存在时尝试创建，不需要失败后改成 w；w 成功打开已有文件会截断内容。

文件权限、路径等问题通常属于 OSError 体系，不是把 int 转换时的 ValueError 原样搬过来就能处理。

保留原存储格式的最小改法如下，文件错误交给调用方处理：

```python
def save(students, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        for student in students:
            file.write(str(student) + '\n')
```

这只是说明 with 和模式选择，不代表 str(字典) 就是 JSON。`writelines()` 也不会自动换行，仍需给每条文本补 `\n`。

##### 问题 2：json、Path 和 TypedDict 分别做什么？

**解答：** 它们来自标准库，无需另行安装，各有职责：

| 工具 | 本项目的作用 | JS / TS 对照 |
| --- | --- | --- |
| json | 字典转 JSON 文本，读取时再转回对象 | JSON.stringify / JSON.parse |
| Path | 构造文件路径，并提供 open 等方法 | 与 Node 路径工具的用途类似 |
| TypedDict | 向编辑器说明学生字典的键和字段类型 | 类似 TS 对象类型说明，不自动做运行时校验 |

```python
import json
from pathlib import Path

student = {'id': '001', 'name': '张三'}
text = json.dumps(student, ensure_ascii=False)
print(json.loads(text)['name'])  # 张三
path = Path('student-ai.jsonl')  # 创建路径对象，不创建文件
print(path.name)                # student-ai.jsonl
```

`Path(__file__).resolve().parent` 表示脚本文件所在目录，后面 `/ 'student-ai.jsonl'` 是拼接路径，不是除法。这样存储位置不随启动时的工作目录改变。

json 与 Path 优先掌握；TypedDict 先知道用途即可，它不是解决截图警告的必要前提。

##### 问题 3：def read_score(subject: str) -> int 和 TS 类型声明一样吗，必须写吗？

**解答：** 用途相似，是可选类型标注：`subject: str` 说明预期参数是字符串，`-> int` 说明预期返回整数。省略后函数仍然可以定义和运行。

```python
def add(a: int, b: int) -> int:
    return a + b

print(add(1, 2))      # 3
print(add('a', 'b'))  # ab：故意违反标注，运行时没有自动拦截
```

编辑器或类型检查器可能提示第二次调用，但标注本身不会执行校验、转换或拦截。`score = int(raw)` 才真正执行整数转换。Python int 特指整数，不能与 TS 同时表示普通整数和小数的 number 完全等同。

##### 问题 4：input(...).strip() 是什么，还有哪些常用方法？

**解答：** input 返回字符串，strip 去掉其两端空白，不删除中间空格，类似 JS trim。

```python
text = '  90  '
cleaned = text.strip()
print(repr(cleaned))  # '90'
print(repr(text))     # '  90  '：原字符串不变
print(bool('   '))          # True
print(bool('   '.strip()))  # False
print('  Y  '.strip().lower())  # y：先去边缘空白，再转小写
```

| 方法 | 作用 | 示例结果 |
| --- | --- | --- |
| strip / lstrip / rstrip | 两端 / 左端 / 右端去空白 | `'  Py  '.lstrip()` → `'Py  '` |
| lower / upper | 转小写 / 大写 | `'YES'.lower()` → `'yes'` |
| replace | 替换内容 | `'a-b'.replace('-', '/')` → `'a/b'` |
| split | 拆成列表 | `'Python,JS'.split(',')` → `['Python', 'JS']` |
| startswith / endswith | 检查前缀 / 后缀 | `'data.txt'.endswith('.txt')` → True |

int 本身可以接受 `' 90 '`，所以转换前 strip 不是必须的；它在 ID、姓名和菜单的空白处理上更明显。`strip('ab')` 表示去掉两端属于 a 或 b 的字符，不是删除完整前后缀。

##### 问题 5：path: Path = DATA_FILE 与 -> set[str] 怎么读？

**解答：** 把整行拆开，而不是把 Path = DATA_FILE 看成一组赋值：

```text
def read_existing_ids(path: Path = DATA_FILE) -> set[str]:
                      ↑     ↑        ↑            ↑
                    参数名  类型    默认值      返回类型
```

- path 是参数名，Path 是预期参数类型。
- DATA_FILE 是默认值，调用时不传 path 就使用它。默认值在函数定义时求值，并非每次调用重新读取同名常量。
- set[str] 表示“元素预期是字符串的集合”，用途类似 TS 的 Set<string>，例如 `{'001', '002'}`。

```python
existing_ids: set[str] = set()
#             类型说明   真正创建空集合
existing_ids.add('001')
print(existing_ids)  # {'001'}
```

调用本项目函数时，`read_existing_ids()` 使用默认路径，`read_existing_ids(Path('other.jsonl'))` 使用自定义路径。标注不会把普通字符串自动转换成 Path；当前实现需要使用 path.open，传字符串会在执行该调用时失败。

##### 问题 6：enumerate(file, start=1) 是什么？

**解答：** enumerate 在遍历时同时提供编号和元素，start=1 让编号从 1 开始；遍历文件时每个元素就是一行文本。

```python
from io import StringIO

with StringIO('张三\n\n李四\n') as file:
    for line_number, line in enumerate(file, start=1):
        if not line.strip():
            continue
        print(line_number, line.strip())
# 1 张三
# 3 李四
```

`line_number, line` 是解包赋值。默认编号从 0 开始，start=1 只改变编号，不跳过第一行。空白行也已参与编号，因此后续报错行号能对应真实文件位置。

它与 JS 数组 entries 配合解构的用途相似，但这里直接逐行遍历文件，不必先把整个文件转成列表。

##### 问题 7：isinstance(record, dict) 是什么，JSON 解析成功为什么还检查？

**解答：** isinstance(对象, 类型) 判断对象是否为指定类型或其子类的实例，返回布尔值。合法 JSON 可以解析成字典，也可能是列表、数字或 None。

```python
import json

for text in ['{"id": "001"}', '[1, 2]', '123', 'null']:
    record = json.loads(text)
    print(isinstance(record, dict))
# True、False、False、False
```

本项目接下来要执行 `record.get('id')`，所以先检查字典类型；`if not isinstance(record, dict)` 就是“不是字典则报告错误”。

```python
print(isinstance('001', str))        # True
print(isinstance(90, (int, float)))  # True：符合任意一个类型即可
```

> [!important] 容器类型与字段有效性分开检查
> 是字典不代表一定有 id，也不代表 id 是非空字符串。因此后面还需要读取字段、检查 str 类型和空白内容，再检查是否重复。

#### 二、优化代码说明与写法

以下保留原来的讲解，说明为什么这样改；不要求一次性掌握，阅读时可以围绕具体语句继续提问。

##### 1. 怎么运行、从哪里开始对照

从项目根目录运行：

```powershell
python python-learn2/stusystem-ai.py
```

先读 `read_score()`，再读 `save()`，最后看 `insert()` 如何组合它们，之后再看重复 ID 检查与菜单。

添加功能部分聚焦录入与保存。当前对照版还提供后续学到的删除功能，见本文件的“删除功能”分类；其他功能随课程继续扩展。

数据位置固定为脚本同目录的 `student-ai.jsonl`。原程序的相对路径 `student.txt` 按启动时工作目录解释，两者不共用文件，也没有自动迁移旧数据。

##### 2. 为什么不能随便使用裸 except

原代码中真正预期的错误是：文本无法转换成整数。

```python
try:
    score = int('80.5')
except ValueError:
    print('请输入整数')
```

裸 `except:` 还会拦截其他错误甚至 `KeyboardInterrupt`，用户按 Ctrl+C 也可能被当作“成绩无效”。把捕获类型写清楚，才能让真正的代码问题暴露出来。

> [!tip] 不是任何 except 都越具体越好
> 接近输入转换的地方捕获 ValueError；菜单层可以集中处理文件操作产生的 OSError。关键是“这一层是否有能力解释并处理这个失败”，不是给每行都加 try。

##### 3. 为什么把单科输入拆成函数

原版将三科转换放在同一个 try 中，失败后 continue 回到外层循环，需要重新填 ID 和姓名，已输入的其他成绩也丢失。

对照版用 `read_score(subject)` 管理自己的循环：

```python
def read_score(subject):
    while True:
        raw = input(f'{subject}成绩：').strip()
        try:
            score = int(raw)
        except ValueError:
            print('请输入整数')
            continue
        if 0 <= score <= 100:
            return score
        print('成绩必须在 0～100 之间')
```

这里区分了两个问题：`abc` / `80.5` 无法转成整数；`-1` / `101` 可以转成整数，但不符合本项目的成绩范围。

return 结束的是这个辅助函数，把合法成绩交给 insert；continue 只重试这一科。函数拆分的价值不只是“代码短一点”，还包括把重试范围缩小到真正失败的步骤。

##### 4. with 管理文件，不靠手动 close 收尾

```python
from io import StringIO

with StringIO() as file:
    file.writelines(['第一条\n', '第二条\n'])
    print(repr(file.getvalue()))  # '第一条\n第二条\n'
print(file.closed)  # True
```

真实文件也采用 `with path.open(...) as file:`。中途出现写入异常时，with 仍负责关闭资源，避免手写 close 因异常被跳过。

截图中“循环 write 可改成 writelines”是代码组织建议，逐次 write 并非错误。对照版先把小批量记录序列化，再用 writelines 写入；它不自动加换行，所以每一项都显式附加 `\n`，也不承诺所有内容要么全部写入、要么全部回滚。

##### 5. 为什么删掉 a 失败后改 w 的逻辑

`a` 模式本来就在目标文件不存在时创建文件，不需要失败后再用 w 创建。

如果 a 因权限、父目录不存在等问题失败，改 w 通常不能解决根因；若后续成功打开已有文件，w 又会截断旧内容。因此文件失败应该向调用方报告原因，不用另一种模式掩盖它。

对照版由 save 负责追加，把异常留给 main 的交互边界处理。只有 save 正常返回，才更新已存在 ID、成功人数，并显示“已保存”。

> [!warning] 保存失败不等于完全没写入
> 写入或关闭时发生 I/O 错误，可能已经留下部分内容。本例不是数据库事务，不自动回滚或保证断电可靠性。遇到异常应先检查文件，不能盲目重试同一条记录。

##### 6. 为什么换为 JSON Lines

原版的 `str(student)` 是 Python 对象表示，不是规范 JSON。对照版用 `json.dumps()` 生成每条 JSON 文本，用 `json.loads()` 解析，不需要 eval。

```python
import json

student = {'id': '001', 'name': '张三', 'english': 90, 'python': 80, 'java': 70}
line = json.dumps(student, ensure_ascii=False)
print(json.loads(line) == student)  # True
```

JSON Lines 是每行一个完整 JSON 值，不是一个外层 JSON 数组，因此不能直接用一次 json.load 读取整个多行记录文件。本例选择一行一条字典，方便追加和逐行读取。

这改变了存储格式，所以使用单独的 `student-ai.jsonl`，不把 JSON 混进原版已有的 student.txt。

##### 7. ID、空白与保存时机

| 项目 | 原版 / 易忽略处 | 对照版 |
| --- | --- | --- |
| ID 命名 | `id` 遮蔽内置函数 | 使用 `student_id` |
| 文本空白 | 只输入空格也会通过非空判断 | ID、姓名用 strip 后检查 |
| 成绩重试 | 任一转换失败就重新填整条 | 只重试当前科目 |
| 重复 ID | 没有检查 | 检查独立数据文件中已保存 ID 和本次新 ID |
| 保存时机 | 全部录完后才统一保存 | 每条完整记录立即保存 |
| 菜单输入 | 非数字导致 int 报错 | 对 '0' / '1' 进行字符串判断 |
| 中断 | 裸 except 可能拦截用户中断 | 主入口统一处理 Ctrl+C / 输入结束 |

ID 保留字符串形式，所以 `'001'` 不会变成数字 1；本例区分大小写，`A1` 与 `a1` 是不同 ID。是否统一大小写要依据实际业务规定，不能自作主张处理。

已经保存的记录在下一条输入中断时仍会保留；当前没填完的记录不会写入。这是本次相对原版的明确行为变化。

##### 8. 已有文件为什么不直接忽略读取错误

`read_existing_ids()` 只在 FileNotFoundError 时认为是首次运行。发现非法 JSON、非字典行、缺少有效 ID 或重复 ID，就报告行号并中止本次录入，而不是假装文件为空。

它目前只校验读取 ID 所必需的结构，不代表已完成整条历史成绩数据的全面校验。后续增加查询、修改等操作时，再把完整记录校验抽成公共函数。

这份实现适合单进程学习项目，多进程同时录入时“先查重、后追加”并不是并发安全保证；不用现在引入文件锁或数据库，但应知道边界。

##### 9. 类型标注与 TypedDict：辅助理解，不替代校验

对照版中的 `Student(TypedDict)` 描述学生字典有哪些键，各自值是什么类型，帮助编辑器推断字段，而不是创建带自动验证的学生对象。

- `list[Student]` 表示学生字典列表；这种内置容器泛型写法从 Python **3.9** 起支持。
- `-> int` 表示函数预期返回整数，不保证运行时自动转换。
- TypedDict 在 typing 中从 Python **3.8** 起提供，当前项目解释器可以使用。

类型标注不是为了“消灭所有黄色提示”。本例真正的数据保证来自 strip、int 转换、范围检查和已有文件检查。若插件还有提示，需要结合具体检查器配置判断，不能仅凭运行成功宣称静态诊断全部通过。

##### 10. 你可以亲自验证的场景

- 输入非整数成绩、越界成绩，观察是否只要求重新填写该科。
- ID 输入 `001`、姓名输入两端有空格的文本，检查保存结果。
- 保存一条后再次输入相同 ID，观察重复提醒。
- 不输入 ID 直接回车，确认返回菜单而不新增记录。
- 保存一条后在下一条中断输入，确认已保存的记录仍在。

> [!question]- 一个小问题：为什么不写 if not score 判断成绩有效？
> 因为 0 分也是合法成绩，但 bool(0) 为 False。应当直接用范围判断 `0 <= score <= 100`，不能拿真假值代替业务有效性。

本节只对照“录入与保存”。输入、持久化和展示的职责已经初步分开，后续功能分别归类，不需要现在搭建多层框架。

### 删除功能：delete 与 delete_student

原始文件：`python-learn2/stusystem.py`，保留你参考课程编写的版本。

对照文件：`python-learn2/stusystem-ai.py`，通过菜单“3. 删除信息”使用。

关联知识：[[ai-ta-基础课程8补充]]、[[ai-ta-基础课程11补充]]、[[ai-ta-基础课程14补充]]

#### 一、删除功能的问题记录

##### 问题 1：tempfile 是什么，NamedTemporaryFile 用来干什么？

**解答：** tempfile 是标准库，帮助创建临时文件和临时目录。NamedTemporaryFile 会真正创建一个有文件名的临时文件，并返回打开的文件对象，不只是生成路径。

本项目先把“保留的学生记录”写入临时文件，写完并关闭后再替换原文件，避免先以 w 模式清空原文件，再处理中途报错。

| 参数 | 本项目中的含义 |
| --- | --- |
| `mode='w'` | 向新创建的临时文件写文本，不是提前清空原学生文件 |
| `encoding='utf-8'` | 文本编码 |
| `newline='\n'` | 写入时不将换行转换为系统的其他形式 |
| `dir=path.parent` | 临时文件放在原数据文件所在目录，便于同文件系统替换 |
| `prefix=...` / `suffix='.tmp'` | 设定文件名前后缀，中间由库生成 |
| `delete=False` | 关闭后保留这个临时文件，供后续替换或清理 |

`file.name` 是临时文件路径，因此代码使用 `Path(file.name)` 保存路径对象。

> [!important] 关闭和删除不是同一件事
> 离开 with 后文件句柄关闭；本例显式设置 delete=False，所以此时临时文件仍存在。
> 随后 `temporary_path.replace(path)` 用已写好的临时文件替换原数据文件。Windows 下尤其需要先关闭句柄，再进行替换。

##### 问题 2：unlink 是什么？missing_ok=True 有什么用？

**解答：** `Path.unlink()` 删除路径指向的文件，也可删除符号链接本身，不用于递归删除普通目录。

本项目的 `temporary_path.unlink(missing_ok=True)` 位于 finally，负责清理这一次创建的临时文件：

- 替换成功：临时路径已经不存在，missing_ok=True 让这一情况不报 FileNotFoundError。
- 写入或替换失败：临时文件可能仍在，清理它，避免遗留无用文件。
- 权限不足等其他错误不会因为 missing_ok=True 就全部被忽略。

不要混淆下面两种操作：

| 写法 | 改变什么 |
| --- | --- |
| `del temporary_path` | 删除这个变量名的绑定，不负责删除磁盘文件 |
| `temporary_path.unlink()` | 删除磁盘上的对应文件 |

这里被 unlink 删除的是临时文件，不是直接把整个学生数据文件删掉。missing_ok 参数自 Python **3.8** 起支持。

##### 问题 3：remaining_lines 这句列表生成式怎么读？

**解答：** 原句是：

```python
# 行文本只作结构演示；实际项目中保存的是 JSON 文本行。
rows = [
    ('001', '张三的记录\n'),
    ('002', '李四的记录\n'),
    ('003', '王五的记录\n'),
]
student_id = '002'
remaining_lines = [line for current_id, line in rows if current_id != student_id]
print(remaining_lines)  # ['张三的记录\n', '王五的记录\n']
```

按下面顺序理解：

1. `for ... in rows`：逐个取出 `(ID, 文本行)`。
2. `current_id, line`：解包，分别取得当前 ID 和文本行。
3. `if current_id != student_id`：只保留不是待删除 ID 的记录。
4. 最前面的 `line`：将文本行放进新列表，而不是放入整组元组。

同样的逻辑用普通循环展开：

```python
rows = [('001', '张三的记录\n'), ('002', '李四的记录\n')]
student_id = '002'
remaining_lines = []

for current_id, line in rows:
    if current_id != student_id:
        remaining_lines.append(line)

print(remaining_lines)  # ['张三的记录\n']
```

这句只创建“准备保留的文本列表”，没有修改原 rows，也没有直接写磁盘。

##### 问题 4：删除版的 read_existing_ids 做了什么？

**解答：** 它复用 `read_student_lines(path)` 读取和检查数据，再提取已有 ID，返回字符串集合：

```python
# 这是项目中的函数形式，调用前需要先定义 read_student_lines。
def read_existing_ids(path):
    return {student_id for student_id, _line in read_student_lines(path)}
```

`read_student_lines()` 返回 `[(ID, 原文本行), ...]`；包装函数只关心 ID，不再重复编写读取文件、JSON 解析和 ID 检查。

用固定数据演示等价的普通循环：

```python
rows = [('001', '张三的记录\n'), ('002', '李四的记录\n')]
existing_ids = set()
for student_id, _line in rows:
    existing_ids.add(student_id)
print(sorted(existing_ids))  # ['001', '002']：排序只为了方便展示
```

`_line` 是普通变量名，前面的下划线表示“本处不打算使用这个值”，不是特殊丢弃语法。

添加功能用它检查重复 ID，删除功能用它判断是否有记录、目标是否存在。读取函数已经发现重复 ID 时会报告错误，并不是依靠 set 去重来掩盖原文件中的重复数据。

##### 问题 5：student_id for 是什么意思？

**解答：** `student_id for` 不是一个独立语法，要放回集合生成式中拆开看：

```text
{student_id  for student_id, _line in rows}
 ↑结果表达式     ↑遍历、解包
```

基本结构是 `{结果表达式 for 变量 in 数据}`。书写时结果放前面，理解时先看后面的 for：先拿到变量，再计算结果表达式，将结果放进集合。

```python
rows = [('001', '张三的记录'), ('002', '李四的记录')]
ids = {student_id for student_id, _line in rows}
labels = {f'学生-{student_id}' for student_id, _line in rows}
print(sorted(ids))     # ['001', '002']
print(sorted(labels))  # ['学生-001', '学生-002']
```

前面写什么，决定集合里收集什么。`[... for ...]` 产生列表，`{... for ...}` 产生集合；`{键: 值 for ...}` 才是字典生成式，不能只看花括号判断类型。

#### 二、删除功能的优化代码说明

##### 1. 先理解整体流程

```text
delete：负责与使用者交互
  → 读取已有 ID，检查是否有学生
  → 输入 ID，查找目标，确认删除
  → delete_student：读取完整记录，筛选保留行
      → replace_student_lines：写临时文件、关闭、替换原文件
  → 只有成功返回后才显示“已删除”并增加成功人数
```

`read_student_lines()` 是添加和删除的公共读取函数，本次为了复用而从旧的 ID 读取逻辑中提取出来，不代表添加功能必须重新实现。

##### 2. 为什么不用 eval，为什么先读完再写？

原版用 eval 解析文件中的 Python 表达式，它可能执行内容，不适合把学生文件当作纯数据来处理。对照版继续读取独立的 student-ai.jsonl，使用 json.loads，不读取或自动迁移原版 student.txt。

原版先以 w 打开数据文件，再逐行解析和写入；如果解析到一半报错，旧内容早已被截断。对照版先读取并验证整个文件的 JSON、字典类型和有效 ID，再决定是否写入。它仍只验证当前功能需要的 ID 结构，不代表完整成绩数据都经过业务校验。

##### 3. 为什么保留原文本行？

读取结果保存 `(规范化后的 ID, 原文本行)`。筛选时根据 ID 判断，写回时直接使用保留的文本行，避免为了删除一条记录而重建其他学生字典、遗漏尚未使用的字段。

“保留文本行”不代表逐字节完全一致：文本读取可能转换换行，空白行被跳过，重写时采用本项目的换行规则。目标不存在或使用者取消时不会重写，因此那两种情况原文件内容保持不变。

##### 4. 成功、失败和取消如何区分？

| 情况 | 行为 |
| --- | --- |
| 文件不存在或没有有效记录 | 提示暂无学生信息，不创建空数据文件 |
| 输入空 ID | 返回菜单，不修改文件 |
| 没有对应 ID | 提示未找到，不重写文件 |
| 未确认删除 | 提示取消，不重写文件 |
| 删除最后一名学生 | 将数据文件替换为空文件，不删除数据文件本身 |
| 数据损坏、ID 无效或重复 | 报告问题，中止本次删除，不提前清空原文件 |
| 临时写入或替换失败 | 不提示删除成功，向交互层报告错误，尝试清理临时文件 |

`delete_student()` 的 True / False 表示是否完成删除；I/O 或数据错误通过异常报告。`delete()` 返回本次成功删除人数，这两个返回值含义不同。

##### 5. 这不是完整的数据库事务

临时写入后替换，主要避免本例“原文件提前清空”的问题，不提供并发更新、断电持久化或所有异常都能恢复的保证。另一个进程同时改文件时仍可能丢失更新，权限或清理失败也需要处理。

学习阶段先理解读取、筛选、写回的边界；文件锁、备份与数据库事务后续按项目需求再学。

##### 6. 自己可以验证什么？

- 使用 AI 对照版先添加两名学生，再删除其中一名，检查另一名的字段仍然保留。
- 输入不存在的 ID，确认没有显示成功，也没有改写文件。
- 找到目标后取消，确认记录仍在。
- 删除最后一名学生，再次进入删除功能，观察“暂无学生信息”。
- 在复制的练习文件中制造非法 JSON，观察程序是否在写回前报告问题；不要用真实资料练习损坏数据。

> [!question]- 回顾：把 remaining_lines 最前面的 line 改成 current_id，会得到什么？
> 得到“保留学生 ID 的列表”，而不是原记录文本列表。若直接写回文件就会丢失姓名和成绩，因此要先想清楚结果表达式应当收集什么。
