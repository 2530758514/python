# # 标识符和保留字
# import keyword
# print(keyword.kwlist)

# # 变量
# name='张三'
# print(name)
# print('标识', id(name))
# print('类型', type(name))
# print('值', name)

# # 变量重复赋值后，会指向新的空间
# name='李四'
# print('标识', id(name))
# print('类型', type(name))
# print('值', name)

# # 数据类型
# # 整数，整数可以表示为二进制、十进制（默认）、八进制、十六进制
# n1=1
# n2=-10
# n3=0
# print(n1, type(n1))
# print(n2, type(n2))
# print(n3, type(n3))

# # 浮点
# f1=1.1
# f2=2.2
# f3=2.1
# print(f1 + f2) # 3.3000000000000003
# print(f1 + f3) # 3.2

# # 解决方案，引入模块 Decimal
# # decimal 通常表示“十进制的、小数的”；
# # 关键在于：Decimal 要解决精度问题，必须用字符串构造，而不是用 float 构造。
# from decimal import Decimal
# # ① 纯 float —— 不精确
# print(1.1 + 2.2)
# # 3.3000000000000003

# # ② float 构造 Decimal —— 照样不精确（只是把误差精确展开了）
# print(Decimal(1.1) + Decimal(2.2))
# # 3.300000000000000266453525910

# # ③ 字符串构造 Decimal —— 精确！
# print(Decimal("1.1") + Decimal("2.2"))
# # 3.3

# # 布尔类型
# b1=True
# b2=False
# print(b1, type(b1))
# print(b2, type(b2))
# print(b1+1)
# print(b2+1)

# # 字符串类型
# s1='人生得意须尽欢'
# s2="莫使金樽空对月"
# s3="""窗前,
# 明月光"""
# print(s1)
# print(s2)
# print(s3)

# # 类型转换
# name='张三'
# age=20
# # TypeError: can only concatenate str (not "int") to str
# # print('名字：'+name+'年龄'+age+'。')
# print('名字：'+name+'年龄'+str(age)+'。')
# print(f'年龄：{age}')
# print('3' * 2)
# print(3 + True)

# 注释
name='张三'
'''
name=abgcd
'''

"""
name='李四'
"""

print(name)