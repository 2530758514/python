# 第十课：函数。建议整份运行；单独选中时需包含所依赖的前面函数定义。
# 从项目根目录运行：python python-learn1/demo10.py

print('\n--- 1. 定义、调用与返回值：保留原案例 ---')
def calc(a, b):
    c = a + b
    return c


result = calc(1, 2)
print(result)  # 3

print('\n--- 2. print 不等于 return ---')
def show_total(a, b):
    print(a + b)


result = show_total(1, 2)  # 函数内部输出 3
print(result)             # None：没有显式返回结果
print(calc(1, 2) * 10)    # 30：返回值可以继续计算

print('\n--- 3. 位置参数、关键字参数与默认值 ---')
def greet(name, greeting='你好'):
    return f'{greeting}，{name}'


print(greet('张三'))                        # 你好，张三
print(greet('张三', '早上好'))               # 早上好，张三
print(greet(greeting='晚上好', name='李四')) # 晚上好，李四
# greet('张三', name='李四')                # TypeError：name 重复赋值
# greet()                                  # TypeError：缺少必需参数

print('\n--- 4. 多个结果与提前返回 ---')
def min_max(numbers):
    if not numbers:
        return None
    return min(numbers), max(numbers)  # 返回一个二元组


low, high = min_max([3, 1, 8])
print(low, high)                # 1 8
print(min_max([]))              # None：调用方不能直接把它解包成两项

print('\n--- 5. 参数绑定：修改对象与重新赋值 ---')
def append_skill(skills):
    skills.append('Python')


def replace_skills(skills):
    skills = ['Vue']  # 只改变局部名字的绑定
    return skills


skills = ['JS']
append_skill(skills)
print(skills)                   # ['JS', 'Python']：原列表被修改
print(replace_skills(skills))    # ['Vue']
print(skills)                   # ['JS', 'Python']：外部名字未重新绑定

print('\n--- 6. 默认参数只在定义时求值 ---')
def bad_collect(value, bucket=[]):  # 故意示范错误写法，不用于实际项目
    bucket.append(value)
    return bucket


print(bad_collect('a'))          # ['a']
print(bad_collect('b'))          # ['a', 'b']：复用了同一默认列表


def collect(value, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(value)
    return bucket


print(collect('a'))              # ['a']
print(collect('b'))              # ['b']
provided = []
collect('c', provided)
print(provided)                  # ['c']：传入的空列表仍会被使用

print('\n--- 7. *args、**kwargs 与调用解包 ---')
def total(*numbers):
    return sum(numbers)


def describe(name, **details):
    return name, details


print(total(), total(1, 2, 3))    # 0 6：numbers 是元组
print(total(*[4, 5, 6]))         # 15：调用时展开列表
print(describe('张三', age=18))   # ('张三', {'age': 18})：details 是字典
options = {'name': '李四', 'greeting': '欢迎'}
print(greet(**options))          # 欢迎，李四：展开关键字参数

print('\n--- 8. 了解即可：限定参数传递方式 ---')
def format_score(name, /, score, *, digits=1):  # / 语法要求 Python 3.8+
    return f'{name}：{score:.{digits}f}'


print(format_score('张三', score=88.125, digits=2))  # 张三：88.12
# format_score(name='张三', score=88)  # TypeError：name 只能按位置传入
# format_score('张三', 88, 2)         # TypeError：digits 只能按关键字传入

print('\n--- 9. 局部、外层与全局作用域 ---')
label = '模块变量'


def read_label():
    label = '局部变量'
    return label


print(read_label(), label)       # 局部变量 模块变量

counter = 0


def increment_global():
    global counter
    counter += 1


increment_global()
print(counter)                  # 1：global 是刻意示范，业务中优先参数和返回值


def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


next_count = make_counter()
print(next_count(), next_count())  # 1 2：外层局部状态保留在闭包中

print('\n--- 10. 函数对象、lambda 与类型标注 ---')
operation = calc
print(operation(2, 3))            # 5：赋值函数对象，不是立即调用
students = [{'name': '张三', 'score': 90}, {'name': '李四', 'score': 75}]
print(sorted(students, key=lambda student: student['score']))
# [{'name': '李四', 'score': 75}, {'name': '张三', 'score': 90}]


def add(a: int, b: int) -> int:
    """返回两个整数的和；类型标注不会自行执行运行时校验。"""
    return a + b


print(add(1, 2))                  # 3
print(add('a', 'b'))              # ab：故意违反标注，演示运行时没有自动拦截
print(add.__doc__)

print('\n--- 11. 递归：终止条件、递推与输入边界 ---')
def factorial(n):
    """计算非负整数的阶乘；排除 bool，仅用于小规模递归教学。"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError('n 必须是整数，不能是布尔值')
    if n < 0:
        raise ValueError('n 不能为负数')
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def factorial_loop(n):
    """循环版，参数约定与递归版相同。"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError('n 必须是整数，不能是布尔值')
    if n < 0:
        raise ValueError('n 不能为负数')
    result = 1
    for number in range(2, n + 1):
        result *= number
    return result


print(factorial(0), factorial(1), factorial(5))  # 1 1 120
print(factorial_loop(5))                        # 120
# factorial(-1)   # ValueError
# factorial(1.5)  # TypeError
# 递归层数受解释器限制；不要用巨大 n 试跑或盲目提高递归上限。

print('\n--- 12. 小实践：将成绩统计封装为函数 ---')
def summarize_scores(scores, *, pass_mark=60):
    """统计数值成绩列表；空列表平均分为 None，且不修改输入列表。"""
    passed = [score for score in scores if score >= pass_mark]
    average = sum(scores) / len(scores) if scores else None
    return {'count': len(scores), 'passed': passed, 'average': average}


scores = [90, 55, 80]
print(summarize_scores(scores))
# {'count': 3, 'passed': [90, 80], 'average': 75.0}
print(summarize_scores([], pass_mark=70))
# {'count': 0, 'passed': [], 'average': None}
print(scores)  # [90, 55, 80]：函数没有修改原列表
