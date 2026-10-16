# 第五课：列表。每节重新准备数据，方便单独选中运行。
# 从项目根目录运行：python python-learn1/demo5.py

print('\n--- 1. 创建列表：[] 与 list() ---')
languages = ['Python', 'JS', 'Python']
print(languages)                # ['Python', 'JS', 'Python']
print(type(languages))          # <class 'list'>
print(len(languages))           # 3
print([])                      # []
print(list('Python'))           # ['P', 'y', 't', 'h', 'o', 'n']
print(list(range(3)))           # [0, 1, 2]

print('\n--- 2. 索引、查找与成员判断 ---')
languages = ['Python', 'JS', 'Python']
print(languages[0])             # Python
print(languages[-1])            # Python：最后一个元素
print('JS' in languages)        # True
print('Java' not in languages)  # True：没有 out in 这种运算符
print(languages.index('Python'))  # 0：第一次出现的位置
print(languages.count('Python'))  # 2：出现次数
# languages[3]                 # IndexError：索引越界
# languages.index('Java')      # ValueError：没有这个值

print('\n--- 3. 遍历：元素与索引 ---')
languages = ['Python', 'JS']
for language in languages:
    print(language)
for index, language in enumerate(languages):
    print(index, language)      # 0 Python，然后 1 JS

print('\n--- 4. 增加：append / extend / insert ---')
numbers = [1, 2]
result = numbers.append(3)
print(numbers, result)         # [1, 2, 3] None
numbers.extend([4, 5])
print(numbers)                 # [1, 2, 3, 4, 5]
numbers.insert(1, 99)
print(numbers)                 # [1, 99, 2, 3, 4, 5]

items = [1]
items.append([2, 3])
print(items)                   # [1, [2, 3]]：整体作为一个元素
items = [1]
items.extend([2, 3])
print(items)                   # [1, 2, 3]：逐个加入

print('\n--- 5. 删除：remove / pop / del / clear ---')
numbers = [10, 20, 20, 30]
numbers.remove(20)
print(numbers)                 # [10, 20, 30]：只删除第一个匹配值
removed = numbers.pop()
print(removed, numbers)        # 30 [10, 20]
removed = numbers.pop(0)
print(removed, numbers)        # 10 [20]
numbers = [10, 20, 30, 40]
del numbers[1:3]
print(numbers)                 # [10, 40]
numbers.clear()
print(numbers)                 # []
# numbers.pop()                # IndexError：空列表无法弹出元素
# numbers.remove(999)          # ValueError：没有这个值

print('\n--- 6. 修改与切片赋值 ---')
numbers = [10, 20, 30, 40]
numbers[1] = 99
print(numbers)                 # [10, 99, 30, 40]
numbers[1:3] = [7, 8, 9]
print(numbers)                 # [10, 7, 8, 9, 40]：长度可以变化

print('\n--- 7. 读取切片：左闭右开 ---')
numbers = [0, 1, 2, 3, 4, 5]
print(numbers[1:4])            # [1, 2, 3]
print(numbers[:3])             # [0, 1, 2]
print(numbers[3:])             # [3, 4, 5]
print(numbers[::2])            # [0, 2, 4]
print(numbers[::-1])           # [5, 4, 3, 2, 1, 0]
print(numbers[99:])            # []：切片越界不会像单个索引那样报错
print(numbers)                 # [0, 1, 2, 3, 4, 5]：读取切片不改变原列表

print('\n--- 8. 排序与反转 ---')
numbers = [10, 2, 30]
ordered = sorted(numbers)
print(ordered, numbers)        # [2, 10, 30] [10, 2, 30]
result = numbers.sort(reverse=True)
print(numbers, result)         # [30, 10, 2] None
numbers.reverse()
print(numbers)                 # [2, 10, 30]：反转当前顺序
print(sorted(['10', '2', '30']))          # ['10', '2', '30']：按字符串规则
print(sorted(['10', '2', '30'], key=int)) # ['2', '10', '30']：按转换后的数值排序
# key=int 只决定排序依据，结果中的元素仍然是字符串。

print('\n--- 9. 列表生成式：映射与筛选 ---')
squares = [number ** 2 for number in range(1, 6)]
evens = [number for number in range(1, 11) if number % 2 == 0]
labels = ['偶数' if number % 2 == 0 else '奇数' for number in range(1, 5)]
print(squares)                 # [1, 4, 9, 16, 25]
print(evens)                   # [2, 4, 6, 8, 10]
print(labels)                  # ['奇数', '偶数', '奇数', '偶数']

print('\n--- 10. 赋值、浅拷贝与嵌套列表 ---')
original = [1, 2]
alias = original
copied = original.copy()       # 也可以用 original[:] 或 list(original)
alias.append(3)
print(original, copied)        # [1, 2, 3] [1, 2]
print(alias is original)       # True
print(copied is original)      # False

original = [[1], [2]]
copied = original.copy()
copied[0].append(99)
print(original)                # [[1, 99], [2]]：浅拷贝仍共享内部列表

rows = [[]] * 3
rows[0].append('共享')
print(rows)                    # [['共享'], ['共享'], ['共享']]
rows = [[] for _ in range(3)]
rows[0].append('独立')
print(rows)                    # [['独立'], [], []]

print('\n--- 11. 小实践：筛选及格分数，再降序排序 ---')
scores = [59, 88, 100, 45, 72]
passed = [score for score in scores if score >= 60]
ranked = sorted(passed, reverse=True)
print('原始成绩：', scores)       # [59, 88, 100, 45, 72]
print('及格排名：', ranked)       # [100, 88, 72]
