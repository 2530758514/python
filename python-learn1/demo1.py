print(520)
print('502')
print('502', '521', '522')
print('你好，\n今天是一个不错的日子~\t你有想好今天去吃什么吗？')

fp = open('E:/Project2/study/python/store/demo1.txt', 'a+')
print('hellow world', file=fp)
fp.close()