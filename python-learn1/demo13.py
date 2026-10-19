"""第十三课：模块、包与标准库。导入本文件不会自动执行 main。"""

# 从项目根目录运行：python python-learn1/demo13.py
# 包入口演示：先 cd python-learn1，再 python -m lesson13_tools
import json
import math
import random
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import lesson13_tools
from lesson13_tools import scores as score_tools
from lesson13_tools.reports import format_report


def main():
    print('\n--- 1. 模块导入与别名 ---')
    import math as maths
    from math import sqrt

    print(math.sqrt(9), maths.sqrt(16), sqrt(25))  # 3.0 4.0 5.0
    print(maths is math)                          # True：正常重复导入复用缓存
    print(math.__name__)                          # math

    print('\n--- 2. 使用自定义包 ---')
    print(lesson13_tools.summarize_scores([90, 55, 80]))
    # {'count': 3, 'passed': [90, 80], 'average': 75.0}
    print(score_tools.summarize_scores([], pass_mark=70))
    # {'count': 0, 'passed': [], 'average': None}
    print(format_report([90, 55, 80]))  # 人数：3，及格：2，平均分：75.0
    print(format_report([]))           # 人数：0，及格：0，平均分：暂无
    print(score_tools.__name__)        # lesson13_tools.scores
    print(score_tools.__package__)     # lesson13_tools

    print('\n--- 3. 内置函数、模块与导入缓存 ---')
    print(len([1, 2, 3]))              # 3：内置函数不必 import
    print('sys' in sys.builtin_module_names)  # True：当前 CPython 的内置模块之一
    print(sys.modules['math'] is math)       # True：当前进程中的模块缓存
    print(lesson13_tools.summarize_scores is score_tools.summarize_scores)  # True

    print('\n--- 4. 标准库 math 与 collections ---')
    print(math.ceil(2.1), math.floor(-2.1))   # 3 -3
    print(math.factorial(5))                  # 120
    counts = Counter(['Python', 'JS', 'Python'])
    print(dict(counts))                       # {'Python': 2, 'JS': 1}

    print('\n--- 5. 标准库 json：文本与 Python 对象 ---')
    record = {'name': '张三', 'passed': True, 'remark': None}
    text = json.dumps(record, ensure_ascii=False)
    print(text)  # {"name": "张三", "passed": true, "remark": null}
    restored = json.loads(text)
    print(restored == record, type(text) is str)  # True True

    print('\n--- 6. 标准库 pathlib：路径不等于文件 ---')
    lesson_dir = Path(__file__).resolve().parent
    print(lesson_dir.name)                 # python-learn1
    example_path = lesson_dir / 'report.json'
    print(example_path.name, example_path.suffix)  # report.json .json
    print(Path.cwd().is_absolute())        # True：工作目录由启动位置决定
    # 拼接路径对象不会创建文件，也没有在这里写入 report.json。

    print('\n--- 7. 标准库 datetime 与 random ---')
    start = date(2026, 1, 1)
    print((start + timedelta(days=7)).isoformat())  # 2026-01-08
    rng = random.Random(13)  # 独立的伪随机生成器，不修改模块级随机状态
    chosen = rng.choice(['Python', 'JS', 'Vue'])
    print(chosen in ['Python', 'JS', 'Vue'])         # True：不依赖具体抽到哪个
    sampled = rng.sample([1, 2, 3, 4], k=2)
    print(len(sampled), len(set(sampled)))          # 2 2

    print('\n--- 8. 查看模块来源与解释器 ---')
    print(Path(score_tools.__file__).name)         # scores.py：本例文件型模块有 __file__
    print(Path(sys.executable).name)               # 当前解释器文件名，依环境而定
    print(__name__)                               # 直接运行时是 __main__
    # 内置模块不一定有 __file__；不要对所有模块盲目读取这个属性。


if __name__ == '__main__':
    main()
