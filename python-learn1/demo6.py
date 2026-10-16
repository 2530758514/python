# 字典创建
# scores = { '张三': 100, '李四': 200 }
# print(scores)
# print(type(scores))

# student = dict({ '张三': 100, '李四': 200 })
# print(student)
# print(type(student))

# 获取字典的元素
# scores = { '张三': 100, '李四': 200 }
# print(scores['张三'])
# # print(scores['王五']) # 没有会报错
# print(scores.get('张三'))
# print(scores.get('王五')) # 没有返回 None
# print(scores.get('王五', '赵六')) # 赵六是在没有时返回的内容

# 字典操作
# scores = { '张三': 100, '李四': 200 }
# print('张三' in scores)
# print('王五' not in scores)

# del scores['张三']
# print(scores)
# scores.clear()
# print(scores)
# scores['赵六'] = 99
# print(scores)
# scores['赵六'] = 110
# print(scores)

# keys\values\items
# scores = { '张三': 100, '李四': 200 }
# keys = scores.keys()
# print(keys)
# print(type(keys))
# print(list(keys))

# values = scores.values()
# print(values)
# print(type(values))
# print(list(values))

# items = scores.items()
# print(items)
# print(type(items))
# print(list(items))

# 字典操作
# scores = { '张三': 100, '李四': 200 }
# for item in scores:
#     print(item, scores[item], scores.get(item))

settings = {'timeout': 0, 'nickname': None}
print(settings.get('timeout', 30))
print(settings.get('timeout') or 30)
print(settings.get('timeout2', 40))
