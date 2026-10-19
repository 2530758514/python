# 基础课程12：面向对象、类与深浅拷贝

对应案例：`python-learn1/demo12.py`。建议整份运行，单独运行时需包含依赖的类定义和导入语句。

关联知识：[[ai-ta-基础课程10补充]]、[[ai-ta-基础课程11补充]]、[[ai-ta-基础课程5补充]]、[[ai-ta-基础课程6补充]]

> [!important] 当前必学
> 类描述一类对象的状态和行为；实例是按类创建的具体对象。类本身在 Python 中也是对象。
> `self` 表示当前实例；`__init__` 初始化已经创建的实例，不应返回业务结果。
> 实例属性通常保存在各自实例上；类属性可被多个实例访问，可变类属性要特别注意共享。
> 赋值不复制对象；浅拷贝只复制外层，深拷贝按对象结构递归复制，但不等于“所有东西都完全独立”。

## 1. 面向过程与面向对象：两种组织方式

面向过程通常围绕步骤和函数组织数据处理；面向对象将有关联的数据与行为组织到对象中。二者可以在同一个项目中配合，不是先后淘汰的关系。

```python
# 面向过程：记录作为参数传给函数
def describe_student(student):
    return f"{student['name']}：{student['score']} 分"

print(describe_student({'name': '张三', 'score': 90}))

# 面向对象：实例保存状态，由方法访问
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def describe(self):
        return f'{self.name}：{self.score} 分'

student = Student('张三', 90)
print(student.describe())
# 两种方式都输出：张三：90 分
```

一次性的文本清理函数不一定需要封装为类。需要维护有意义的状态、统一行为时，再考虑对象。不要为了“面向对象”给每个函数套一个类。

## 2. class、实例与初始化

```python
class Student:
    """学习者的简化模型。"""

    def __init__(self, name, score=0):
        self.name = name
        self.score = score

    def describe(self):
        return f'{self.name}：{self.score} 分'

first = Student('张三', 90)
second = Student('李四', 80)
print(first is second)          # False
print(first.name)               # 张三
print(first.describe())         # 张三：90 分
print(Student.describe(first))  # 张三：90 分
```

- `class Student:` 执行后创建类对象并绑定名字，类名通常使用大驼峰。
- `Student(...)` 创建实例，Python 不写 JS 的 `new`。
- 普通实例方法的第一个参数按约定叫 `self`；`first.describe()` 会自动绑定这个实例。
- `self.name` 是实例属性，单写 `name` 不会自动变成属性读取。
- `__init__` 接收调用类时提供的初始化参数，不能返回非 `None` 的值。

> [!tip] 了解即可：__new__ 与 __init__
> 对普通类的创建流程，可以先理解为 `__new__` 负责创建对象，随后 `__init__` 初始化它。初学时实现 `__init__` 即可，不必为了示范而重写 `__new__`，也不要直接调用 `obj.__init__()` 来假装重新创建对象。

`self` 不是 JavaScript 中可因调用方式改变的隐式 `this`，而是显式形参；理解方法绑定比死记“self 等于 this”更准确。

## 3. 实例属性、类属性与遮蔽

```python
class Student:
    school = 'Python 学习班'

    def __init__(self, name):
        self.name = name

first = Student('张三')
second = Student('李四')
first.school = '自学小组'
Student.school = '新学习班'

print(first.school)   # 自学小组：实例自己的同名属性
print(second.school)  # 新学习班：从类读取
print(Student.school) # 新学习班
del first.school
print(first.school)   # 新学习班：移除实例遮蔽后读到类属性
```

对当前普通属性，可先理解为实例有同名属性就读实例，没有就向类及父类查找。`property` 等描述符存在更精确的查找规则，后续再展开，不把这个简化模型当成所有情况的完整规则。

### 可变类属性容易被多个实例共享

```python
class BadStudent:
    skills = []

a = BadStudent()
b = BadStudent()
a.skills.append('Python')
print(b.skills)  # ['Python']：修改的是同一个类属性列表

class Student:
    def __init__(self, skills=None):
        self.skills = list(skills) if skills is not None else []

a = Student()
b = Student()
a.skills.append('Python')
print(b.skills)  # []：每个实例有独立的列表
```

这里没有给 `skills` 使用默认 `[]`，也没有把列表放在类体中共享。`list(skills)` 明确复制传入容器的外层，但内部嵌套对象仍可能共享，这是函数参数与浅拷贝知识的结合。

## 4. 三类常见方法

| 方法 | 首个自动绑定参数 | 用途 |
| --- | --- | --- |
| 实例方法 | 当前实例 `self` | 使用或修改实例状态 |
| `@classmethod` | 调用时对应的类 `cls` | 使用类信息，提供替代构造入口 |
| `@staticmethod` | 不自动绑定实例或类 | 与类有关、但不依赖实例或类状态的工具操作 |

```python
class Student:
    def __init__(self, name, score=0):
        self.name = name
        self.score = score

    @classmethod
    def from_record(cls, record):
        return cls(record['name'], record.get('score', 0))

    @staticmethod
    def is_passing(score):
        return score >= 60

student = Student.from_record({'name': '张三', 'score': 90})
print(student.name)             # 张三
print(Student.is_passing(90))   # True
```

`@classmethod`、`@staticmethod` 是这里会用到的内置装饰器，先掌握效果，自定义装饰器留到后续。`cls` 与 `self` 都是约定命名；类方法用 `cls(...)` 而非写死类名，有利于子类复用。

## 5. 特殊属性：先用来观察，不随意修改

```python
class Student:
    """学习者模型。"""

    def __init__(self, name):
        self.name = name

student = Student('张三')
print(student.__class__ is Student)  # True
print(Student.__name__)             # Student
print(Student.__doc__)              # 学习者模型。
print(student.__dict__)             # {'name': '张三'}
print(vars(student))                # {'name': '张三'}
```

| 属性 / 工具 | 含义与边界 |
| --- | --- |
| `obj.__class__` / `type(obj)` | 对象的直接类型；通常优先使用 type |
| `Class.__name__` | 类名，不是实例的业务姓名 |
| `Class.__module__` | 定义所在模块；直接运行时经常是 `__main__` |
| `Class.__doc__` | 文档字符串；没有时可能是 None |
| `obj.__dict__` / `vars(obj)` | 普通实例的属性存储，不自动包含全部类属性 |
| `Class.__dict__` | 类命名空间的只读代理视图，不是实例属性字典 |
| `Class.__bases__` | 直接基类组成的元组 |
| `Class.__mro__` | 方法解析顺序中的类组成的元组 |

> [!warning] 不是所有对象都有 __dict__
> 内置对象、使用 `__slots__` 的某些实例等可能没有实例属性字典。不要把 `obj.__dict__` 当作任何对象都能用的“转 JSON”方法，里面还可能有不可序列化或不应暴露的数据。

普通调试也可以使用 `getattr(obj, 'name', 默认值)`，但缺少必需字段时不应一律用默认值掩盖结构错误。不要把不可信输入直接当属性名任意修改对象。

## 6. 特殊方法：__str__ 与 __repr__

```python
class Student:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'学习者：{self.name}'

    def __repr__(self):
        return f'Student(name={self.name!r})'

student = Student('张三')
print(student)          # 学习者：张三
print(str(student))     # 学习者：张三
print(repr(student))    # Student(name='张三')
print([student])        # [Student(name='张三')]：容器展示元素通常使用 repr
```

`__str__` 面向易读展示，`__repr__` 面向调试且应尽量明确；二者都应返回字符串。f-string 中的 `!r` 表示对该值使用 `repr()`，便于观察引号和转义。

这些方法通过 `str()`、`repr()` 等约定协议被调用，平时优先使用普通接口，不必到处手动写双下划线方法调用。

### 属性命名与封装：了解即可

- `name`：公开属性。
- `_name`：表示内部使用的约定，不是强制访问限制。
- `__name`：在类定义上下文中触发名字改写，主要用于减少子类名字冲突，不是绝对私有或安全机制。
- `__name__`：系统约定的特殊名字，不等于“私有属性”。不要随意发明双下划线协议名字。

`__del__` 不应被当作可靠的文件关闭或业务清理时机，资源管理优先使用上一课的 `with`；`del obj` 是删除名字绑定，不等于必定立刻执行清理方法。

## 7. 了解即可：继承、覆盖与 super

```python
class Student:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return self.name

class Graduate(Student):
    def __init__(self, name, topic):
        super().__init__(name)
        self.topic = topic

    def describe(self):
        return f'{super().describe()}，方向：{self.topic}'

student = Graduate('张三', 'AI 应用')
print(student.describe())           # 张三，方向：AI 应用
print(isinstance(student, Student))  # True
print(type(student) is Student)      # False
print(issubclass(Graduate, Student)) # True
```

子类可以复用与覆盖行为。`isinstance()` 包含继承关系判断；`type(obj) is SomeClass` 则要求直接类型匹配。`super()` 按方法解析顺序继续查找，不应在多继承时简单理解为“固定找某个父类”。当前先练单继承，复杂 MRO 留到后续。

相同的方法调用可以由不同对象提供不同实现，这是理解多态的入口；Python 也常依据“对象提供了什么行为”使用对象，不要求所有协作对象必须继承同一个类。

## 8. 赋值、浅拷贝、深拷贝：核心对照

```python
import copy

class Student:
    def __init__(self, name, skills):
        self.name = name
        self.skills = list(skills)

original = Student('张三', ['JS'])
alias = original
shallow = copy.copy(original)
deep = copy.deepcopy(original)

print(alias is original)                  # True
print(shallow is original)                # False
print(shallow.skills is original.skills)  # True
print(deep.skills is original.skills)     # False

shallow.name = '李四'
shallow.skills.append('Python')
print(original.name, original.skills)  # 张三 ['JS', 'Python']
print(shallow.name, shallow.skills)    # 李四 ['JS', 'Python']
print(deep.name, deep.skills)          # 张三 ['JS']
```

| 方式 | 外层普通实例 | 本例的技能列表 | 适合如何理解 |
| --- | --- | --- | --- |
| `alias = original` | 同一个对象 | 同一个对象 | 只是多了一个名字 |
| `copy.copy(original)` | 新实例 | 共享 | 外层独立，属性仍引用原对象 |
| `copy.deepcopy(original)` | 新实例 | 新列表 | 根据结构递归复制，可变嵌套数据在本例中分离 |

修改浅拷贝的 `name` 是改新实例的属性绑定；对 `skills.append()` 则是改仍共享的列表。理解操作作用于哪一层，比背“深拷贝会变 id”更可靠。

### 深拷贝会保留结构内部的共享关系

```python
import copy

shared = ['JS']
original = [shared, shared]
cloned = copy.deepcopy(original)

print(cloned[0] is shared)     # False：与原结构分离
print(cloned[0] is cloned[1])  # True：副本内部仍共享同一个被复制列表
```

深拷贝会记录已处理对象，以处理重复引用和循环结构，并不是遇到每个位置都重新复制一份。它也不承诺任何对象都变成全新对象：函数、类等通常仍被共享；文件、网络连接等资源不能简单当作普通数据复制。自定义类还可能定制复制行为。

> [!warning] 不用深拷贝解决所有问题
> 深拷贝可能成本更高，也可能复制了本来就应共享的数据。先明确副本需要独立到哪一层，再选择赋值、浅拷贝或深拷贝。序列化后再解析也不是通用的对象深拷贝替代方案。

## 9. 与 JS / TS 的对照

| 内容 | Python | JS / TS 对照 |
| --- | --- | --- |
| 创建实例 | `Student(...)` | 通常 `new Student(...)` |
| 当前实例 | 方法首参 `self`，调用时绑定 | `this` 受调用方式与绑定规则影响 |
| 初始化 | `__init__`，不返回非 None 值 | `constructor` 有自己的创建规则，不能直接等同 |
| 每实例数据 | `self.skills = []` | 实例字段通常为每实例初始化 |
| 类上的数据 | 类体中的普通属性 | 可与 static 属性作初步用途对照，查找机制不同 |
| 浅拷贝 | `copy.copy(obj)` 对普通教学类可复制实例 | `{...instance}` 通常只复制可枚举自有属性到普通对象，不等于保留类实例 |

不要把 Python 类属性、原型链、TS 类型标注看成一套完全相同的机制；类比服务于理解，实际行为仍以当前语言规则为准。

## 10. 小实践与后续方向

`demo12.py` 用 `Student.from_record()` 接收字典，构造学习档案，再用深拷贝创建独立练习副本并增加技能。

案例明确约定姓名、技能列表的结构，只在初始化时检查分数；直接执行 `student.score = -1` 不会自动触发构造时校验。需要维持长期有效的属性约束时，后续学习 `property` 与更新方法，不能把一次校验误认为对象永远合法。

面向后端时，普通 Python 对象、数据库模型、接口数据结构各有职责，不是“写了 class 就能自动校验和保存数据”。`dataclasses` 自 Python **3.7** 起可以减少数据类样板代码，适合在基础类机制掌握后再学，不替代本课的对象与引用理解。

## 11. 回顾练习

```python
import copy

class Bag:
    category = '学习用品'

    def __init__(self):
        self.items = ['笔']

a = Bag()
b = copy.copy(a)
c = copy.deepcopy(a)
b.items.append('书')
b.category = '练习副本'

print(a.items)
print(c.items)
print(a.category, b.category)
print(a is b, a.items is b.items)
```

> [!question]- 展开查看答案
> - `a.items` 是 `['笔', '书']`，浅拷贝仍共享内部列表。
> - `c.items` 是 `['笔']`，深拷贝时创建了独立列表。
> - 输出 `学习用品 练习副本`，b 的赋值遮蔽了类属性，没有修改 a 或类。
> - 最后一行是 `False True`：不同实例仍可以引用同一个内部对象。

当前优先掌握实例创建、self、属性与方法、共享陷阱和复制层级；复杂继承、描述符、元类与自定义复制协议留到后续实际需求。
