# 第七课：元组。保留当前文件名 drmo7.py。
# 从项目根目录运行：python python-learn1/drmo7.py

# list 是可变序列，dict 是可变映射；str 和 tuple 是不可变序列。
# 原地修改对象与给变量重新赋值是两件事，不依靠 id 变化判断能否修改。

print('\n--- 1. 三种创建方式 ---')
t = ('Python', 'world', 98)
print(t)        # ('Python', 'world', 98)
print(type(t))  # <class 'tuple'>

# 这种写法合法，但右侧已经是元组，直接使用它即可。
t1 = tuple(('Python', 'world', 98))
print(t1)
print(type(t1))

# 逗号构成打包；为了清楚，实际代码通常保留括号。
t2 = 'Python', 'world', 98
print(t2)
print(type(t2))

print('\n--- 2. 空容器与单元素元组 ---')
t3 = []        # 空列表
d = ()         # 空元组
t4 = list()
d2 = dict()    # 空字典；{} 也是空字典
d3 = tuple()   # 空元组，使用不同变量名避免覆盖 d2
print(type(t3), type(d), type(t4), type(d2), type(d3))
print(type(('Python')))   # <class 'str'>：只是给字符串加括号
print(type(('Python',)))  # <class 'tuple'>：单元素元组必须有逗号
print(tuple('abc'))       # ('a', 'b', 'c')：逐字符转换
print(('abc',))           # ('abc',)：一个完整字符串元素

print('\n--- 3. 读取、切片、查询与遍历 ---')
values = ('Python', 'JS', 'Python', 98)
print(len(values))             # 4
print(values[0], values[-1])   # Python 98
print(values[1:3])             # ('JS', 'Python')
print(values[::-1])            # (98, 'Python', 'JS', 'Python')
print('JS' in values)          # True
print('Java' not in values)    # True
print(values.count('Python'))  # 2
print(values.index('Python'))  # 0
for index, value in enumerate(values):
    print(index, value)
# values[99]                   # IndexError：索引越界
# values.index('Java')         # ValueError：找不到值

print('\n--- 4. 不可变与重新绑定 ---')
point = (10, 20)
original = point
# point[0] = 99                # TypeError：不能替换元组中的元素
# point.append(30)             # AttributeError：没有 append 方法
point += (30,)                # 元组拼接后将 point 重新绑定，不修改原元组
print(original)               # (10, 20)
print(point)                  # (10, 20, 30)

print('\n--- 5. 元组内的可变对象 ---')
record = ('张三', ['JS'])
record[1].append('Python')
print(record)                 # ('张三', ['JS', 'Python'])
# record[1] = []               # TypeError：不能替换元组保存的列表引用

print('\n--- 6. 解包、星号收集与交换 ---')
name, age = ('张三', 18)
print(name, age)               # 张三 18
first, *middle, last = (10, 20, 30, 40)
print(first, middle, last)     # 10 [20, 30] 40：星号收集结果是列表
a, b = 1, 2
a, b = b, a
print(a, b)                   # 2 1

print('\n--- 7. 转换、排序与生成 ---')
numbers = (3, 1, 2)
editable = list(numbers)
editable[0] = 9
print(numbers, tuple(editable))  # (3, 1, 2) (9, 1, 2)
ordered = sorted(numbers)
print(ordered, type(ordered))    # [1, 2, 3] <class 'list'>
print(tuple(ordered))            # (1, 2, 3)
squares = tuple(number ** 2 for number in range(1, 4))
print(squares)                   # (1, 4, 9)

print('\n--- 8. 元组作为字典键 ---')
seats = {(1, 2): '张三', (1, 3): '李四'}
print(seats[(1, 2)])             # 张三：排号和座号共同定位
# invalid = {('张三', []): 100}   # TypeError：包含列表的元组不可哈希

print('\n--- 9. 小实践：姓名与成绩记录 ---')
students = [('张三', 90), ('李四', 55), ('王五', 80)]
for name, score in students:
    status = '及格' if score >= 60 else '继续练习'
    print(f'{name}：{score}，{status}')
