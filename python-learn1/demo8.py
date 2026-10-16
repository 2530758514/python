# 第八课：集合 set。每节独立准备数据，可以单独选中运行。
# 从项目根目录运行：python python-learn1/demo8.py
# 为方便核对，示例多用 sorted() 展示同类型元素；排序结果是列表。

print('\n--- 1. 创建与去重 ---')
numbers = {3, 1, 2, 2}
print(type(numbers), len(numbers))  # <class 'set'> 3
print(sorted(numbers))             # [1, 2, 3]
print(type({}), type(set()))        # <class 'dict'> <class 'set'>
print(sorted(set([3, 1, 3, 2])))    # [1, 2, 3]
print(sorted(set('banana')))        # ['a', 'b', 'n']
print(set('abc') == {'abc'})        # False：字符集合与完整字符串元素不同

print('\n--- 2. 成员判断与遍历 ---')
skills = {'Python', 'JS'}
print('Python' in skills)           # True
print('Java' not in skills)         # True
for skill in sorted(skills):
    print(skill)                   # JS，然后 Python：这里遍历排序后的列表
# skills[0]                        # TypeError：集合没有位置索引

print('\n--- 3. 增加：add 与 update ---')
numbers = {1, 2}
result = numbers.add(2)
print(sorted(numbers), result)     # [1, 2] None：重复添加不增加数量
numbers.add(3)
numbers.update([3, 4, 5])
print(sorted(numbers))             # [1, 2, 3, 4, 5]
words = set()
words.add('abc')
print(sorted(words))               # ['abc']：整体添加
words = set()
words.update('abc')
print(sorted(words))               # ['a', 'b', 'c']：逐个字符添加

print('\n--- 4. 删除：remove / discard / pop / clear ---')
numbers = {1, 2, 3}
numbers.remove(2)
numbers.discard(99)                # 不存在也不报错
print(sorted(numbers))             # [1, 3]
# numbers.remove(99)               # KeyError：要删除的元素不存在
before = numbers.copy()
removed = numbers.pop()            # 移出任意一个元素，不保证是哪一个
print(removed in before)           # True
print(removed not in numbers)      # True
print(len(numbers))                # 1
numbers.clear()
print(numbers)                     # set()
# numbers.pop()                    # KeyError：集合为空

print('\n--- 5. 交集、并集、差集与对称差集 ---')
a = {1, 2, 3}
b = {3, 4}
print(sorted(a & b))               # [3]：共同元素
print(sorted(a | b))               # [1, 2, 3, 4]：全部元素，去重
print(sorted(a - b))               # [1, 2]：只在 a 中
print(sorted(b - a))               # [4]：只在 b 中
print(sorted(a ^ b))               # [1, 2, 4]：只在其中一个集合中
print(sorted(a.intersection([2, 3, 9])))  # [2, 3]：方法可接收列表等可迭代对象
print(sorted(a), sorted(b))        # [1, 2, 3] [3, 4]：原集合未修改

print('\n--- 6. 子集、真子集与不相交 ---')
a = {1, 2}
b = {1, 2, 3}
print(a <= b, a < b)               # True True
print(a <= a, a < a)               # True False
print(b >= a, b > a)               # True True
print(a.isdisjoint({3, 4}))        # True：没有共同元素
print({1, 2} == {2, 1})            # True：不比较顺序

print('\n--- 7. 原地更新与重新绑定 ---')
a = {1, 2}
alias = a
a |= {3}
print(sorted(alias))              # [1, 2, 3]：原地更新，共享引用可见
a = {1, 2}
alias = a
a = a | {3}
print(sorted(alias), sorted(a))    # [1, 2] [1, 2, 3]：重新绑定

print('\n--- 8. 集合生成式与元素限制 ---')
squares = {number ** 2 for number in [-2, -1, 0, 1, 2]}
print(sorted(squares))             # [0, 1, 4]：生成结果去重
evens = {number for number in range(6) if number % 2 == 0}
print(sorted(evens))               # [0, 2, 4]
points = {(1, 2), (2, 3)}           # 所有元素都可哈希的元组可以作集合元素
print((1, 2) in points)             # True
# invalid = {[1, 2]}               # TypeError：列表不可哈希
print(len({1, True, 1.0}))          # 1：相等且哈希相同，不是三个独立元素
frozen = frozenset([1, 2, 2])
print(type(frozen), sorted(frozen)) # <class 'frozenset'> [1, 2]
# frozen.add(3)                    # AttributeError：frozenset 不支持原地增加

print('\n--- 9. 小实践：比较名单 ---')
registered = {'张三', '李四', '王五'}
arrived = {'李四', '王五', '赵六'}
print('未到：', sorted(registered - arrived))  # ['张三']
print('临时到场：', sorted(arrived - registered))  # ['赵六']
print('已报名且到场：', sorted(registered & arrived))  # ['李四', '王五']

print('\n--- 10. 去重且保留首次出现顺序 ---')
languages = ['Python', 'JS', 'Python', 'Vue', 'JS']
unique = list(dict.fromkeys(languages))
print(unique)  # ['Python', 'JS', 'Vue']：借助字典的插入顺序；元素需可哈希
