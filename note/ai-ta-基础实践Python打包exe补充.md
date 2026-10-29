# 基础实践：Python 打包为 Windows exe

关联项目：[[ai-ta-基础实践stusystem补充]]。

资料核对日期：2026-10-29。本次实测项目解释器为 Python 3.15.0，已安装 PyInstaller 6.22.3。版本会变化，其他环境需要重新核对。

> [!important] 本次笔记的范围
> 整理打包流程和项目适配要点，没有安装新依赖、修改现有程序或重新生成 exe。
> 命令和选项已核对，不等于完成了实际 exe 的运行验收。
> 学生系统使用 input / print，必须保留控制台；可修改数据应保存在可写的持久目录，不放进单文件临时解包目录。

## 一、问题记录

本节是课程收尾补充，目前没有专项提问。后续打包时遇到的具体问题，先在对话中解答，收到“记笔记”指令后再按“问题 + 解答”汇总到这里，不把助教补充内容伪装成你已提过的问题。

## 二、操作说明与项目适配

### 1. 打包 exe 到底做了什么？

以 PyInstaller 为例，它会分析入口脚本与依赖，把运行需要的 Python 解释器、模块等一起收集，形成目录包或单文件可执行程序。因此目标机器通常不需要另外安装 Python。

这不是改后缀名，也不是保证把 Python 逻辑全部编译成高性能机器码。exe 体积可能明显大于源文件，打包本身不代表程序变快或源码被可靠加密。

Windows exe 应在 Windows 环境构建；PyInstaller 不是通用跨平台编译器。目标机器的操作系统、架构与依赖仍需匹配，不能认为“生成了 exe 就能在所有电脑运行”。[官方项目说明](https://pypi.org/project/pyinstaller/)

### 2. 先确认解释器，再确认打包工具

下面命令用于查看环境，不会打包：

```powershell
python --version
python -c "import sys; print(sys.executable)"
python -m PyInstaller --version
```

如果 python 指向 Windows Store 别名、错误版本或其他虚拟环境，先选择正确解释器。本次实际检查的是：

```powershell
& 'C:\Users\ASUS\AppData\Local\Programs\Python\Python315\python.exe' -m PyInstaller --version
```

这是当前电脑的已验证路径，不是所有人的通用安装位置。`python -m PyInstaller` 有助于明确使用这个解释器对应的打包工具，PyInstaller 模块名注意大小写。

核对时，官方发布信息列出的支持范围包括 Python 3.15；但工具支持解释器，不等于你的所有第三方依赖都已兼容。[版本与支持范围](https://pypi.org/project/pyinstaller/)

后续可选：为打包创建独立环境，避免把无关依赖带入构建。以下是操作参考，本次没有执行：

```powershell
# 从项目根目录执行，并先确认 python 是要使用的解释器。
python -m venv .venv-pack
.\.venv-pack\Scripts\python.exe -m pip install pyinstaller
.\.venv-pack\Scripts\python.exe -m PyInstaller --version
```

后续打包命令也使用同一个环境中的 python。构建环境还需安装项目实际使用的第三方依赖；本学生系统主要依赖标准库，不需要额外猜装一堆包。能在现有环境使用，不代表必须先升级或重新安装。

### 3. 先解决学生数据路径，再打包

当前 AI 版的代码是：

```python
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / 'student-ai.jsonl'
```

源码运行时，它定位到脚本目录；PyInstaller 单文件模式下，入口脚本的 __file__ 位于运行时临时解包目录。将新增学生写到那里，程序退出清理后可能无法保留数据。目录模式中的内部资源位置也不应直接当作用户数据目录。[官方运行时路径说明](https://pyinstaller.org/en/stable/runtime-information.html)

如果目标是便携学习程序，可以把用户数据放在 exe 所在的可写目录。下面是未来需要应用到 AI 文件顶部的适配示例，本次未修改实际程序：

```python
import sys
from pathlib import Path

def get_data_file():
    if getattr(sys, 'frozen', False):
        # 打包运行时，sys.executable 是 exe 本身，不是 Python 解释器。
        base_dir = Path(sys.executable).resolve().parent
    else:
        base_dir = Path(__file__).resolve().parent
    return base_dir / 'student-ai.jsonl'

# 应在 read_existing_ids 等函数定义之前设置，供默认参数绑定。
DATA_FILE = get_data_file()
```

不要打包后才在 main 中修改 DATA_FILE，并以为 `path=DATA_FILE` 的默认参数会自动更新；它们已在函数定义时绑定了默认值。

> [!warning] 数据文件不是打包资源
> 字体、图标、模板属于随程序携带的资源；学生记录属于运行中会修改的数据。
> 不把真实学生数据通过 --add-data 嵌入 exe，也不把临时解包内容当作持久存储。
> exe 目录若没有写权限，例如某些安装目录，应改用明确的用户数据目录；便携方案应放在自己有权限的文件夹。

旧程序的 student.txt 和 AI 版 student-ai.jsonl 格式不同，不通过改扩展名自动迁移。你当前已有的 stusystem.spec 指向原版 stusystem.py，不是 AI 版。

### 4. 先目录模式：容易检查依赖

完成所需路径适配、确认脚本可运行后，再从项目根目录执行：

```powershell
python -m PyInstaller --onedir --console --name stusystem-ai python-learn2/stusystem-ai.py
```

默认输出位置对应当前构建工作目录，此例从项目根目录执行：

```text
项目根目录/
├── build/                     构建中间文件
├── dist/
│   └── stusystem-ai/
│       ├── stusystem-ai.exe
│       └── _internal/         当前默认布局下的依赖资源
└── stusystem-ai.spec          本次生成的构建配置
```

运行：

```powershell
.\dist\stusystem-ai\stusystem-ai.exe
```

分发时复制整个 stusystem-ai 文件夹，不能只拎走其中一个 exe。先用目录模式确认功能和依赖，再考虑单文件，定位问题通常更直接。[官方运行模式](https://pyinstaller.org/en/stable/operating-mode.html)

### 5. 再单文件模式：方便携带，但仍有外部数据

```powershell
python -m PyInstaller --onefile --console --name stusystem-ai python-learn2/stusystem-ai.py
.\dist\stusystem-ai.exe
```

`--onefile` 的短写是 `-F`。它将程序打进单个可执行文件，运行时仍可能解包资源到临时目录，启动开销与目录模式不同。

单文件不等于学生记录也永远存在 exe 内。按前面的便携路径方案录入后，会在 exe 同目录生成独立的 student-ai.jsonl；移动程序时，要按需要一起备份和迁移这个数据文件。

两条构建命令使用相同的 --name，会更新同名 spec；需要长期保留不同构建方案时，应分别命名或维护各自的配置，不把上一次 spec 当作永远不变。

### 6. 常见参数与控制台陷阱

| 参数 | 作用 | 本项目是否需要 |
| --- | --- | --- |
| `--onedir` / `-D` | 目录分发，默认模式 | 适合先验证 |
| `--onefile` / `-F` | 单文件分发 | 验证后按需求选择 |
| `--console` / `-c` | 保留控制台，默认行为 | 需要，学生系统依赖 input / print |
| `--windowed` / `--noconsole` / `-w` | 不提供控制台 | 当前命令行系统不要使用 |
| `--name` / `-n` | 指定程序与 spec 名称 | 区分原版与 AI 版 |
| `--icon` / `-i` | 指定程序图标 | 可选，需提供实际存在且支持的图标文件 |
| `--add-data` | 添加非代码资源 | 有真实资源需求时再用，不用于可修改学生数据 |
| `--hidden-import` | 补充无法静态发现的导入 | 仅在诊断确认缺失后使用 |

`-w` 不是“界面更漂亮”，不会把命令行程序变成 GUI。当前程序隐藏控制台后，input 所需的输入环境可能不可用，报错也更难观察。[官方选项说明](https://pyinstaller.org/en/stable/usage.html)

### 7. spec、build 与 dist 怎么处理？

- build：分析日志、缓存和中间产物，不是给普通用户运行的目录。
- dist：最终分发产物，需要测试后才交付。
- .spec：构建配置脚本，可以描述入口、依赖、资源和控制台等选项。不是 exe，也不是学生数据。

使用经过维护的 spec 构建时，可以执行 `python -m PyInstaller 路径/配置.spec`；很多参数已由 spec 控制，不要假定重新加 --onefile 等选项就一定能覆盖配置。

本次发现你已有 `python-learn2/build/`、`python-learn2/dist/` 和 `python-learn2/stusystem.spec`，它们来自你自己的练习。本次保留、不删除、不覆盖，也不自动提交。

生成的构建产物通常不进入源码提交；spec 如果成为人工维护、可复现构建的一部分，可以单独审阅后纳入 Git。虚拟环境也不作为源码提交。本次没有为此额外修改 .gitignore。

### 8. 最容易遇到的几个问题

| 现象 | 优先排查 |
| --- | --- |
| 命令不存在 | 当前解释器是否安装 PyInstaller，优先 python -m PyInstaller |
| exe 一闪而过 | 从终端运行，保留错误输出；检查是否正常执行结束 |
| No module named ... | 环境缺少依赖，或动态导入未被发现；结合完整日志判断 |
| 打包后找不到图片、模板 | 资源是否实际包含，运行时路径是否正确 |
| 录入成功，重开后数据没了 | 是否写进临时解包目录，是否换了运行 / 数据位置 |
| 无法保存 | 数据目录是否可写，文件是否被占用，读取与写入格式是否一致 |
| 拿到另一台机器不能启动 | 是否漏带目录依赖，平台、架构、系统环境是否匹配 |

不要一出错就添加大量 hidden-import，也不要通过反复换解释器掩盖具体日志。先让源码正常运行，再检查构建日志、运行错误和路径。[官方排错指南](https://pyinstaller.org/en/stable/when-things-go-wrong.html)

### 9. 如何确认真的完成了打包？

构建成功只是第一步，至少手动验证：

1. 在终端启动 exe，菜单与输入正常。
2. 录入一名虚构学生，退出后重新启动，记录仍可查询。
3. 编辑与删除虚构记录，再次启动确认保存结果。
4. 检查实际数据文件位置，确认不在 _MEI 等临时解包目录。
5. 在不同工作目录启动，仍读到约定的数据文件。
6. 目录模式完整复制分发目录；在合适的目标环境验证，而不只测试开发机。

本次只做文档与命令选项核对，没有运行你已有的 exe，也没有验证它的持久化行为。不要把本笔记的存在当作当前程序已经适配打包的证明。

### 10. 回顾

> [!question]- 学生系统能不能直接用 -F -w，让它变成没有黑窗口的桌面软件？
> 不能。-F 改变分发形式，-w 隐藏控制台，二者都不会自动生成图形界面。当前系统依赖 input / print，应保留控制台。

> [!question]- 把 student-ai.jsonl 作为打包资源带进去，就能直接保存真实学生信息吗？
> 不应这样设计。只读资源与可修改的用户数据应区分；单文件资源在临时目录，修改不会自动写回原 exe。先明确持久数据位置，再做保存。
