# 第十一课：异常处理。可整份运行，故意触发的异常均在示例边界处理。
# 从项目根目录运行：python python-learn1/demo11.py

print('\n--- 1. 捕获异常后，从哪里继续 ---')
try:
    number = int('abc')
    print('这行不会执行')
except ValueError as error:
    print(type(error).__name__)  # ValueError
print('继续执行后面的代码')

print('\n--- 2. 不同异常分别处理，子类放前面 ---')
for raw in ['2', '0', 'abc']:
    try:
        result = 10 / int(raw)
    except ValueError:
        print('请输入合法整数')
    except ZeroDivisionError:
        print('除数不能为零')
    else:
        print(result)
# 依次输出：5.0、除数不能为零、请输入合法整数

print('\n--- 3. 多个类型共用一段处理逻辑 ---')
for index in [0, 5, '0']:
    try:
        print([10, 20][index])
    except (IndexError, TypeError) as error:
        print(type(error).__name__)
# 依次输出：10、IndexError、TypeError

print('\n--- 4. try / except / else / finally 的顺序 ---')
def divide_text(raw):
    try:
        divisor = int(raw)
        result = 10 / divisor
    except ValueError:
        print('except：转换失败')
    except ZeroDivisionError:
        print('except：除数为零')
    else:
        print(f'else：成功，结果是 {result}')
    finally:
        print('finally：本次尝试结束')


divide_text('2')    # else，然后 finally
divide_text('0')    # except，然后 finally
divide_text('abc')  # except，然后 finally

print('\n--- 5. 异常传播：内层没处理，由调用方处理 ---')
def parse_count(raw):
    return int(raw)


try:
    parse_count('wrong')
except ValueError:
    print('调用方捕获到了 parse_count 中的转换异常')

print('\n--- 6. raise：类型不对与值不对 ---')
def validate_score(score):
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError('成绩必须是数值，不能是布尔值')
    if not 0 <= score <= 100:
        raise ValueError('成绩必须在 0～100 之间')
    return score


for score in [0, 88, 100, -1, 101, '90', True]:
    try:
        print(validate_score(score))
    except (TypeError, ValueError) as error:
        print(type(error).__name__, str(error))

print('\n--- 7. bare raise：处理后继续抛出 ---')
def parse_required_integer(raw):
    try:
        return int(raw)
    except ValueError:
        print('内层记录：转换失败，交给调用方决定')
        raise  # 重新抛出当前正在处理的异常


try:
    parse_required_integer('abc')
except ValueError:
    print('外层：异常没有被吞掉')

print('\n--- 8. 异常链：转换成更明确的业务说明 ---')
def parse_age(raw):
    try:
        return int(raw)
    except ValueError as error:
        raise ValueError('年龄需要填写整数文本') from error


try:
    parse_age('eighteen')
except ValueError as error:
    print(str(error))                 # 年龄需要填写整数文本
    print(type(error.__cause__).__name__)  # ValueError：原始原因保留

print('\n--- 9. finally 在 return 前完成清理 ---')
def read_status():
    try:
        return '已完成'
    finally:
        print('先执行 finally')


print(read_status())  # 先输出“先执行 finally”，再输出“已完成”
# 不在 finally 中 return，否则可能覆盖原返回值甚至压住异常。

print('\n--- 10. with 管理资源：内存文本示例，不写磁盘 ---')
from io import StringIO

with StringIO('Python\nJS') as stream:
    print(stream.readline().strip())  # Python
print(stream.closed)                  # True
# 实际文件通常写 with open(path, encoding='utf-8') as file:

print('\n--- 11. 了解即可：自定义异常 ---')
class InvalidScoreError(ValueError):
    """成绩格式合法，但不满足本例的业务范围。"""


def require_passing_score(score):
    validate_score(score)
    if score < 60:
        raise InvalidScoreError('当前操作要求成绩至少为 60')
    return score


try:
    require_passing_score(55)
except InvalidScoreError as error:
    print(str(error))  # 当前操作要求成绩至少为 60
# 类与继承后续再学，这里先认识“命名一种业务错误”的作用。

print('\n--- 12. 小实践：有限次数尝试解析输入 ---')
def first_valid_count(raw_values, *, max_attempts=3):
    """依次尝试候选文本，返回首个非负整数；次数用尽或候选耗尽则报错。"""
    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int):
        raise TypeError('max_attempts 必须是整数，不能是布尔值')
    if max_attempts < 1:
        raise ValueError('max_attempts 必须至少为 1')
    for attempt, raw in enumerate(raw_values, start=1):
        if attempt > max_attempts:
            break
        # 本例约定 raw_values 是字符串序列；不吞掉错误输入类型导致的 TypeError。
        try:
            value = int(raw)
        except ValueError:
            continue
        if value >= 0:
            return value
    raise ValueError('限定尝试范围内没有合法的非负整数')


print(first_valid_count(['abc', '-1', '0']))  # 0：零是合法结果，不按真假值判断
try:
    first_valid_count(['abc', '-1', 'bad', '9'])
except ValueError as error:
    print(str(error))
