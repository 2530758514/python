# 生成整数序列 range()
# r=range(10)
# print(r) # range(0, 10)
# print(list(r)) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# r=range(1, 10)
# print(list(r)) # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# r=range(1, 10, 2)
# print(list(r)) # [1, 3, 5, 7, 9]

# 循环结构

# while 循环
# a=1
# sum1=sum2=0
# while a < 10:
#     print('a:', a)
#     # 偶数求和
#     # if a % 2 == 0:
#     if not bool(a%2):
#         sum1 += a
#         print('偶数+', a)
#     else:
#         sum2 += a
#         print('奇数+', a)
#     a += 1

# print(f'偶数和: {sum1} 奇数和: {sum2}')

# for-in 循环
# for item in 'Python':
#     print(item)

# for i in range(10):
#     print(i)

# for _ in range(3):
#     print('我入三省吾身')

# sum = 0
# for item in range(1, 101):
#     if item %2 == 0:
#         sum += item

# print('总和:', sum)

i = 10
print('大' if i > 10 else '小')