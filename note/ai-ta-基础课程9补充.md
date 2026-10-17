# 基础课程9：字符串 str

对应案例：`python-learn1/demo9.py`。保留了你的探索案例，后半部分是可直接运行的分节示例。

关联知识：[[ai-ta-基础课程补充]]、[[ai-ta-基础课程5补充]]、[[ai-ta-基础课程7补充]]

> [!important] 当前必学
> 字符串是不可变的 Unicode 文本序列，按索引读取的是长度为 1 的字符串，Python 没有单独的 char 类型。
> 转换、替换、清理等操作不会原地修改字符串，使用返回结果才会得到变化。
> 内容相等用 `==`，不依赖 `is` 或 `id()`。

## 1. 单引号、双引号、三引号与原始字符串

```python
a = 'Python'
b = "Python"
print(a == b)  # True：引号形式不改变内容类型

multiline = '''第一行
第二行'''
print(multiline)
print(repr('a\nb\tc'))  # 'a\nb\tc'：repr 便于查看换行和制表符
print(r'C:\study\python')  # C:\study\python
```

单、双引号可以互相配合，例如 `"I'm learning Python"`；也可用反斜杠转义引号。三引号允许换行，但不自动进行变量插值；需要格式化时加 `f` 前缀。

常见转义：`\n` 是换行，`\t` 是制表符，`\\` 表示一个反斜杠。`r'...'` 抑制大多数反斜杠转义处理，适合书写一些路径和正则表达式。

> [!warning] 原始字符串也有边界
> `r'...'` 不是任意文本都能直接放入：例如不能以奇数个反斜杠直接结尾。实际项目处理文件路径还可学习 `pathlib`，本课先掌握字符串表示。

## 2. 字符串驻留与 id：先纠正容易过度归纳的地方

你的原案例比较了不同写法的 `id()`。相同字面量可能被编译器合并，部分字符串也可能被驻留复用；运行时拼接的结果则不一定使用同一个对象。

```python
a = 'Python'
b = ''.join(['Py', 'thon'])
print(a == b)  # True：这是内容比较的可靠结论
```

> [!warning] 观察不等于语言保证
> 不能根据一次 id 输出总结“包含某字符就不会共享”“join 一定产生不同身份”或“内容相同必定同一对象”。实现、优化和执行方式都可能影响观察。
> 编写业务代码时，不用背这些复用条件，判断文本内容用 `==`。

## 3. 不可变、索引、切片与成员判断

```python
text = 'Python'
print(text[0], text[-1])  # P n
print(text[1:4])          # yth
print(text[::-1])         # nohtyP
print(text[99:])          # 空字符串：切片允许边界越界
print('Py' in text)       # True
print('py' in text)       # False：区分大小写

changed = text.replace('P', 'p')
print(text, changed)      # Python python
# text[0] = 'p'           # TypeError
```

单个索引越界会抛出 `IndexError`，切片不包含终点。`+` 拼接字符串，`*` 搭配整数进行重复，相关解释见 [[ai-ta-基础课程补充]]。

### len 统计什么？

```python
print(len('你好'))          # 2：Unicode 码点数
print(len('你好'.encode('utf-8')))  # 6：UTF-8 字节数
print(len('e\u0301'))      # 2：e 与组合重音，视觉上可能像一个字符
```

`len()` 不等于屏幕上可见字符的数量，也不等于文件字节数。JS 字符串长度基于 UTF-16 代码单元，某些 emoji 的长度会与 Python 不同；本课先认识这个区别，复杂文本边界后续按需处理。

## 4. 查找、计数与前后缀

| 方法 | 找到时 | 找不到时 |
| --- | --- | --- |
| `s.find(sub)` | 第一次出现的索引 | `-1` |
| `s.rfind(sub)` | 最后一次出现的索引 | `-1` |
| `s.index(sub)` | 第一次出现的索引 | `ValueError` |
| `s.rindex(sub)` | 最后一次出现的索引 | `ValueError` |
| `s.count(sub)` | 非重叠出现次数 | `0` |

```python
text = 'hello, hello'
print(text.index('e'), text.rindex('e'))  # 1 8
print(text.find('o'), text.rfind('o'))    # 4 11
print(text.count('hello'))               # 2
print('aaa'.count('aa'))                 # 1：不计算重叠匹配
print(text.startswith('hello'))          # True
print(text.endswith('hello'))            # True
```

这些查找方法还可按需要传入 `start`、`end` 限定范围，不必切出子字符串再查找。

> [!warning] 不直接用 if s.find(sub)
> 找到索引 0 时为假，没找到返回 -1 却为真。只判断包含关系就写 `sub in s`；需要位置就保存结果并判断是否为 `-1`。

## 5. 大小写转换

| 方法 | 示例与含义 |
| --- | --- |
| `upper()` | `'hello'.upper()` → `'HELLO'` |
| `lower()` | `'HELLO'.lower()` → `'hello'` |
| `swapcase()` | `'Py'.swapcase()` → `'pY'` |
| `capitalize()` | `'hello PYTHON'.capitalize()` → `'Hello python'` |
| `title()` | `'hello PYTHON'.title()` → `'Hello Python'` |
| `casefold()` | 更适合 Unicode 文本的大小写无关比较 |

```python
print('Straße'.casefold() == 'STRASSE'.casefold())  # True
```

这些方法不修改原字符串。`title()` 按自身的单词边界规则处理，不是智能标题排版，也不保证适合所有姓名或自然语言。对路径、密码等数据不要未经需求确认就统一大小写。

## 6. strip 清理边缘，replace 替换内容

```python
text = '  Python\n'
print(repr(text.strip()))   # 'Python'：去两端空白
print(repr(text.lstrip()))  # 'Python\n'：只处理左侧
print(repr(text.rstrip()))  # '  Python'：只处理右侧
print('xyPythonxy'.strip('xy'))  # Python
print('a-a-a'.replace('a', 'b', 2))  # b-b-a：最多替换两次
```

> [!warning] strip 参数不是完整前后缀
> `strip('xy')` 表示反复移除两端属于字符集合 x/y 的字符，而不是只移除文本 `'xy'`；它也不清理中间内容。
> `lstrip('abc: ')` 不是“删除完整前缀 abc: ”，可能误删后面的字符。

Python **3.9 起**可用下面的方法精确移除一次前后缀，旧课程可能未覆盖：

```python
print(repr('abc: cab'.lstrip('abc: ')))    # ''：连后面的 cab 也被移除了
print('abc: cab'.removeprefix('abc: '))    # cab
print('report.txt'.removesuffix('.txt'))          # report
```

前后缀未匹配时内容保持不变。只做这些简单清理不需要提前引入正则表达式。

## 7. split 拆分，join 拼接

```python
print(' a  b\tc\n'.split())  # ['a', 'b', 'c']：连续空白合并，忽略边缘空白
print('a,,b,'.split(','))     # ['a', '', 'b', '']：明确分隔符时保留空项
print(''.split())            # []
print(''.split(','))         # ['']
print('a=b=c'.split('=', 1))  # ['a', 'b=c']：限制拆分次数
print('a=b=c'.rsplit('=', 1)) # ['a=b', 'c']：从右侧开始拆
print('a\nb\r\nc'.splitlines()) # ['a', 'b', 'c']

print('-'.join(['Python', 'JS']))  # Python-JS
print(','.join(str(n) for n in [1, 2, 3]))  # 1,2,3
# ','.join([1, 2, 3])  # TypeError：每个元素必须是字符串
```

> [!tip] JS 对照
> Python 的 `s.split(',')` 与 JS 的 `s.split(',')` 在简单例子中相似，但默认规则不同：Python 不传参数按连续空白拆分；JS 不传分隔符时通常把原字符串作为一项返回。
> Python 写 `分隔符.join(字符串序列)`；JS 写 `数组.join(分隔符)`，调用位置不同。

拼接多项字符串常用 `join()`，避免在大型循环中反复累积不可变字符串；少量字段的拼接则优先考虑可读性。

## 8. 判断内容与比较

| 方法 | 检查内容 | 注意 |
| --- | --- | --- |
| `isalpha()` | 字母字符 | 不限于英文字母 |
| `isdecimal()` | 十进制数字字符 | 不限于 ASCII 的 0～9 |
| `isdigit()` | 更广的数字字符 | 例如 `'²'` 也返回 True |
| `isalnum()` | 字母或数字字符 | 空格不算 |
| `isspace()` | 空白字符 | 空格、制表符等 |
| `islower()` / `isupper()` | 有大小写字符的大小写情况 | 数字不自动让判断失败，例如 `'abc123'.islower()` 为 True |

这些方法在空字符串上均返回 `False`。它们不能直接代替完整业务校验，例如 `'-12'.isdigit()`、`'1.5'.isdigit()` 为 `False`，而 `'²'.isdigit()` 为 `True` 但 `int('²')` 仍然报错。实际数字转换要处理转换失败，之后学习异常时展开。

字符串比较按 Unicode 码点的字典序进行，不自动转为数字，也不等于中文拼音排序：

```python
print('10' < '2')          # True：先比较首个字符
print(int('10') < int('2')) # False：数值比较
```

## 9. 格式化：优先掌握 f-string

f-string 自 Python **3.6** 起提供。把表达式放进 `{}`，用途类似 JS 模板字符串，但格式说明更丰富。

```python
name = '张三'
score = 88.125
print(f'{name}：{score:.2f}')       # 张三：88.12
print('{}：{:.2f}'.format(name, score)) # 张三：88.12
print('%s：%.2f' % (name, score))   # 张三：88.12：旧式格式化仍有效
print(f'{7:03d}')                  # 007：宽度 3，不足补 0
print(f'{0.875:.1%}')              # 87.5%
print(f'{{姓名}}：{name}')           # {姓名}：双花括号输出字面量花括号
```

`.2f` 控制显示为两位小数，不会修改原变量，也不能当作消除浮点误差的工具。不要把它理解为所有情况下简单“四舍五入”；需要十进制精度与明确舍入规则时，回看 [[ai-ta-基础课程补充#Decimal：从小数文本构造]]。

### 对齐与填充

```python
print(repr('Py'.center(6, '-')))  # '--Py--'
print(repr('Py'.ljust(5, '.')))   # 'Py...'
print(repr('Py'.rjust(5, '.')))   # '...Py'
```

宽度表示最小长度，不会因原字符串更长就截断。中文与复杂 Unicode 字符的视觉宽度也不一定等于 `len()`。

## 10. 了解即可：str 与 bytes 的边界

```python
text = '你好'
encoded = text.encode('utf-8')
print(type(encoded), len(encoded)) # <class 'bytes'> 6
print(encoded.decode('utf-8'))     # 你好
print(str(encoded) == text)        # False
```

`str` 是文本，`bytes` 是字节序列；`encode()` 将文本编码为字节，`decode()` 将字节解码为文本。`str(encoded)` 产生字节对象的字符串表示，不是按 UTF-8 解码。

爬虫、文件与网络接口会遇到编码问题。要先判断当前拿到的是文本还是字节，并使用正确编码；不用为了不报错一律忽略解码错误，以免悄悄丢失内容。

## 11. 小实践：清理标签并保留首次顺序

```python
raw = ' Python, JS,python, , Vue ,JS '
cleaned = []
for part in raw.split(','):
    tag = part.strip().lower()
    if tag and tag not in cleaned:
        cleaned.append(tag)

print(cleaned)             # ['python', 'js', 'vue']
print(' / '.join(cleaned)) # python / js / vue
```

这是分隔、清理、统一规则、过滤、去重与拼接的组合练习。这里标签较少，用列表便于理解；更大数据量可再结合集合判断是否出现过。

## 12. 回顾练习

```python
text = '  Python,JS,,Vue  '
parts = text.strip().split(',')
print(parts)
print('/'.join(part for part in parts if part))
print(text.find('Python'))
print('Python'.find('Python'))
print('Python'.find('Java'))
print('report.txt'.removesuffix('.txt'))
```

> [!question]- 展开查看答案
> - 列表为 `['Python', 'JS', '', 'Vue']`，指定逗号分隔符保留空项。
> - 拼接得到 `'Python/JS/Vue'`，通过 `if part` 过滤空字符串。
> - 原字符串中的索引是 `2`，因为前面有两个空格。
> - 后两次查找分别为 `0` 和 `-1`，不能直接把查找结果当布尔值判断是否找到。
> - 最后一项是 `'report'`。

当前优先掌握查找、清理、拆分拼接和 f-string；字符串复用实现、正则表达式与复杂 Unicode 处理后续按实际需求深入。
