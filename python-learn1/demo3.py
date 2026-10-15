# 输入函数
'''
a = input('number 1')
b = input('number 2')
print(type(a), type(b)) # <class 'str'>
print(a + b) # 12
print(int(a) + int(b)) # 3
'''

# 赋值运算符

# 链式赋值
# a=b=c=10
# print(a, id(a)) # 10 140720426542640
# print(b, id(b)) # 10 140720426542640
# print(c, id(c)) # 10 140720426542640

# a+=10
# print(a) # 20
# a*=3
# print(a) # 60
# a+=7
# print(a)
# a/=2 # 32.5
# # a//=2 # 32 会舍弃小数点后面的内容
# print(a)

# 系列解包赋值
a,b,c=10,20,30
print(a, b, c)

# 比较运算符

# 运算符优先级