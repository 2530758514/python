# 第九课：字符串。保留下方原始探索案例，再提供分节运行示例。
# 原注释中的 id 数字仅是当时运行的观察，不保证换一次运行仍相同。
# 从项目根目录运行：python python-learn1/demo9.py

# a = 'Python'
# b = "Python"
# c = '''Python'''
# d = 'python'
# print(id(a)) # 2323169409280
# print(id(b)) # 2323169409280
# print(id(c)) # 2323169409280
# print(id(d)) # 2323168082032

# a = 'abc%'
# b = 'abc%'
# print(id(a)) # 2389537693712
# print(id(b)) # 2389537693712

# a = 'abc'
# b = 'ab' + 'c'
# c = ''.join(['ab', 'c'])
# print(id(a)) # 2389537693712
# print(id(b)) # 2389537693712
# print(id(c)) # 2389537882048

# s = 'hello, hello'
# print(s.index('e'))
# print(s.rindex('e'))
# print(s.find('o'))
# print(s.rfind('o'))

# s = 'killian'
# s2 = 'KILLIAN'
# s3 = 'killian KILLIAN Yang yang YANG'
# print(s.upper())
# print(s2.lower())
# print(s3.swapcase())
# print(s.capitalize())
# print(s3.title())

print('\n--- 1. 内容比较与不可变 ---')
a = 'Python'
b = ''.join(['Py', 'thon'])
print(a == b)                   # True：比较内容，不依赖 is / id
text = 'python'
changed = text.replace('p', 'P')
print(text, changed)            # python Python：原字符串没有改变
# text[0] = 'P'                  # TypeError：不能替换字符串中的位置

print('\n--- 2. 索引、切片与成员判断 ---')
text = 'Python'
print(text[0], text[-1])         # P n
print(text[1:4])                 # yth
print(text[::-1])                # nohtyP
print(text[99:])                 # 空字符串
print('Py' in text, 'py' in text) # True False：区分大小写
print(len('你好'))               # 2：这里统计 Unicode 码点，不是 UTF-8 字节数

print('\n--- 3. 转义、原始字符串与多行 ---')
print(repr('第一行\n第二行\t结束'))  # repr 显示转义，便于观察
path = r'C:\study\python'
print(path)                      # C:\study\python
multiline = '''第一行
第二行'''
print(multiline)
# 原始字符串不是“任意内容免转义”，不能以奇数个反斜杠直接结尾。

print('\n--- 4. 查找、计数与前后缀 ---')
text = 'hello, hello'
print(text.index('e'), text.rindex('e'))  # 1 8
print(text.find('o'), text.rfind('o'))    # 4 11
print(text.find('x'))                    # -1
print(text.count('hello'))               # 2
print(text.startswith('hello'), text.endswith('hello'))  # True True
# text.index('x')                        # ValueError：找不到
# 不直接写 if text.find('hello')：索引 0 为假，-1 却为真。

print('\n--- 5. 大小写转换 ---')
text = 'hello PYTHON'
print(text.upper())            # HELLO PYTHON
print(text.lower())            # hello python
print(text.swapcase())         # HELLO python
print(text.capitalize())       # Hello python：其余字母小写
print(text.title())            # Hello Python：按其单词边界规则转换
print('Straße'.casefold() == 'STRASSE'.casefold())  # True：大小写无关比较

print('\n--- 6. 清理与替换 ---')
print(repr('  Python\n'.strip()))        # 'Python'
print('xyPythonxy'.strip('xy'))          # Python：去两端属于 x/y 的字符
print(repr('abc: cab'.lstrip('abc: ')))  # ''：不是删除完整前缀
print('abc: cab'.removeprefix('abc: '))  # cab：Python 3.9+
print('report.txt'.removesuffix('.txt')) # report：Python 3.9+
print('a-a-a'.replace('a', 'b', 2))      # b-b-a

print('\n--- 7. 拆分与拼接 ---')
print(' a  b\tc\n'.split())    # ['a', 'b', 'c']：合并连续空白
print('a,,b,'.split(','))       # ['a', '', 'b', '']：保留空项
print('a=b=c'.split('=', 1))    # ['a', 'b=c']
print('a=b=c'.rsplit('=', 1))   # ['a=b', 'c']
print('a\nb\r\nc'.splitlines()) # ['a', 'b', 'c']
print('-'.join(['Python', 'JS']))  # Python-JS
print(','.join(str(number) for number in [1, 2, 3]))  # 1,2,3
# ','.join([1, 2, 3])           # TypeError：join 的每一项必须是字符串

print('\n--- 8. 判断与比较 ---')
print('abc'.isalpha(), '123'.isdecimal())  # True True
print('²'.isdigit(), '²'.isdecimal())    # True False
print('abc123'.isalnum(), ' \t'.isspace()) # True True
print(''.isalpha(), ''.isdecimal())       # False False
print('10' < '2')                         # True：按字符串规则比较
# isdigit 不是通用数字校验器，例如它不能验证负号和小数。

print('\n--- 9. 格式化与对齐 ---')
name = '张三'
score = 88.125
print(f'{name}：{score:.2f}')        # 张三：88.12
print('{}：{:.2f}'.format(name, score))  # 张三：88.12
print('%s：%.2f' % (name, score))    # 张三：88.12，旧课程中可能出现
print(f'{7:03d}')                   # 007
print(f'{0.875:.1%}')               # 87.5%
print(f'{{姓名}}：{name}')            # {姓名}：张三
print(repr('Py'.center(6, '-')))     # '--Py--'
print(repr('Py'.ljust(5, '.')))      # 'Py...'
print(repr('Py'.rjust(5, '.')))      # '...Py'

print('\n--- 10. 文本与字节 ---')
text = '你好'
encoded = text.encode('utf-8')
print(type(encoded), len(encoded))  # <class 'bytes'> 6
print(encoded.decode('utf-8'))      # 你好
print(str(encoded) == text)         # False：str(bytes) 不是解码

print('\n--- 11. 小实践：清理课程标签并保序去重 ---')
raw = ' Python, JS,python, , Vue ,JS '
cleaned = []
for part in raw.split(','):
    tag = part.strip().lower()
    if tag and tag not in cleaned:
        cleaned.append(tag)
print(cleaned)                     # ['python', 'js', 'vue']
print(' / '.join(cleaned))          # python / js / vue
