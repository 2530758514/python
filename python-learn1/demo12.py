# 第十二课：类、对象与深浅拷贝。
# 从项目根目录运行：python python-learn1/demo12.py
# 建议整份运行；选中片段时需先执行其依赖的类定义和 import。
import copy


print('\n--- 1. 面向过程：用函数处理记录 ---')
def describe_student(student):
    return f"{student['name']}：{student['score']} 分"


record = {'name': '张三', 'score': 90}
print(describe_student(record))  # 张三：90 分

print('\n--- 2. 类与实例：组织状态和行为 ---')
class Student:
    """保存学习者姓名、成绩与技能的教学模型。"""

    school = 'Python 学习班'  # 类属性

    def __init__(self, name, score=0, skills=None):
        self.name = name
        self.score = self.validate_score(score)
        # 明确选择：复制传入列表的外层，不接管调用方原列表。
        self.skills = list(skills) if skills is not None else []

    def describe(self):
        return f'{self.name}：{self.score} 分'

    def add_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)

    @staticmethod
    def validate_score(score):
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError('成绩必须是数值，不能是布尔值')
        if not 0 <= score <= 100:
            raise ValueError('成绩必须在 0～100 之间')
        return score

    @classmethod
    def from_record(cls, record):
        return cls(record['name'], record.get('score', 0), record.get('skills'))

    def __str__(self):
        return self.describe()

    def __repr__(self):
        return f'Student(name={self.name!r}, score={self.score!r})'


first = Student('张三', 90, ['JS'])
second = Student('李四', 80)
print(first.describe())          # 张三：90 分
print(Student.describe(first))   # 张三：90 分：绑定实例的直观对照
print(first is second)           # False：两个不同实例
print(Student.validate_score(88)) # 88
print(Student.from_record({'name': '王五', 'score': 75}))  # 王五：75 分

print('\n--- 3. 类属性与实例属性 ---')
print(first.school, second.school)  # Python 学习班 Python 学习班
first.school = '张三的自学小组'      # 建立同名实例属性，遮蔽类属性
Student.school = '新学习班'
print(first.school)                # 张三的自学小组
print(second.school)               # 新学习班
print(Student.school)              # 新学习班
del first.school
print(first.school)                # 新学习班：删除实例遮蔽后重新读到类属性

print('\n--- 4. 可变类属性的共享陷阱 ---')
class SharedSkills:
    skills = []  # 故意示范：所有未遮蔽此属性的实例共享同一列表


shared_a = SharedSkills()
shared_b = SharedSkills()
shared_a.skills.append('Python')
print(shared_b.skills)             # ['Python']
first.add_skill('Python')
print(first.skills, second.skills) # ['JS', 'Python'] []：Student 在初始化时分开创建

print('\n--- 5. 特殊属性与对象观察 ---')
print(first.__class__ is Student)  # True
print(type(first) is Student)      # True
print(isinstance(first, Student))  # True
print(Student.__name__)           # Student
print(Student.__doc__)            # 类的说明文本
print(vars(first))                # 本例的实例属性字典，不包含未遮蔽的 school
print(first.__dict__ is vars(first)) # True：当前类的普通实例上成立
print(str(first))                 # 张三：90 分
print(repr(first))                # Student(name='张三', score=90)
# __module__ 反映定义所在模块，直接运行与导入时可能不同，不写死预期值。

print('\n--- 6. 了解即可：继承、覆盖与 super ---')
class Graduate(Student):
    def __init__(self, name, score=0, skills=None, *, topic='AI 应用'):
        super().__init__(name, score, skills)
        self.topic = topic

    def describe(self):
        return f'{super().describe()}，方向：{self.topic}'


graduate = Graduate.from_record({'name': '赵六', 'score': 95})
print(graduate.describe())         # 赵六：95 分，方向：AI 应用
print(isinstance(graduate, Student), type(graduate) is Student)  # True False
print(issubclass(Graduate, Student)) # True
print(Graduate.__bases__ == (Student,))  # True

print('\n--- 7. 赋值、浅拷贝、深拷贝 ---')
original = Student('张三', 90, ['JS'])
alias = original
shallow = copy.copy(original)
deep = copy.deepcopy(original)

print(alias is original, shallow is original, deep is original)  # True False False
print(shallow.skills is original.skills) # True：属性中的列表仍共享
print(deep.skills is original.skills)    # False：本例嵌套列表也被复制
shallow.name = '李四'
shallow.add_skill('Python')
print(original.name, original.skills)   # 张三 ['JS', 'Python']
print(shallow.name, shallow.skills)     # 李四 ['JS', 'Python']
print(deep.name, deep.skills)           # 张三 ['JS']

print('\n--- 8. 深拷贝保留被复制结构内部的共享关系 ---')
common = ['JS']
graph = [common, common]
cloned = copy.deepcopy(graph)
print(cloned is graph)                  # False
print(cloned[0] is common)              # False
print(cloned[0] is cloned[1])           # True：同一原对象没有被拆成两个独立对象
cloned[0].append('Python')
print(graph)                           # [['JS'], ['JS']]
print(cloned)                          # [['JS', 'Python'], ['JS', 'Python']]

print('\n--- 9. 小实践：先复制，再修改学习档案 ---')
source = Student.from_record({'name': '张三', 'score': 90, 'skills': ['JS']})
draft = copy.deepcopy(source)
draft.name = '张三的练习副本'
draft.add_skill('Python')
print(source.name, source.skills)       # 张三 ['JS']
print(draft.name, draft.skills)         # 张三的练习副本 ['JS', 'Python']
# 本课只在构造时校验 score，直接赋值 source.score 不会再次触发校验。
# 后续学习 property 时再集中实现“赋值也需要校验”的约束。
