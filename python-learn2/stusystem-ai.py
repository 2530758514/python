"""学生系统录入功能对照版：保留原文件，只实现当前学到的录入与保存。"""

# 运行：python python-learn2/stusystem-ai.py
# 数据保存在本文件同目录的 student-ai.jsonl，每行一个 JSON 对象。
# 不读取或改写原程序的 student.txt。类型标注写法要求 Python 3.9+。
import json  # 字典与 JSON 文本互转，对应 JS 的 JSON.stringify / JSON.parse 用途。
from pathlib import Path  # 路径对象，提供路径拼接和 open 等方法。
from typing import TypedDict  # 向编辑器说明字典字段，不自动做运行时校验。


class Student(TypedDict):
    """描述学生字典的结构，不会自动进行运行时校验。"""

    id: str
    name: str
    english: int
    python: int
    java: int


# __file__ 是本文件路径；resolve().parent 取得绝对目录，/ 在此表示拼接路径。
DATA_FILE = Path(__file__).resolve().parent / 'student-ai.jsonl'


def read_score(subject: str) -> int:
    """只重试输错的这一科，不要求重新输入姓名与其他成绩。"""
    # subject: str / -> int 是可选类型说明，真正的转换由下面 int(raw) 完成。
    while True:
        # strip 去两端空白，返回新字符串；不删除中间空格。
        raw = input(f'{subject}成绩（0～100 的整数）：').strip()
        try:
            score = int(raw)
        except ValueError:
            print('请输入整数，例如 80；不能输入空内容或 80.5。')
            continue
        if 0 <= score <= 100:
            return score
        print('成绩必须在 0～100 之间，请重新输入。')


def read_existing_ids(path: Path = DATA_FILE) -> set[str]:
    """读取已有 ID。仅把文件不存在当作首次运行，不忽略损坏数据。"""
    # path 是参数，Path 是类型，DATA_FILE 是默认值；set[str] 表示字符串集合。
    # 冒号后是类型标注，右侧 set() 才是真正创建空集合。
    existing_ids: set[str] = set()
    try:
        with path.open('r', encoding='utf-8') as file:
            # enumerate 同时给出行号和文本，从 1 编号；不跳过第一行。
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    # 合法 JSON 也可能是列表或数字，因此先当普通 object 读取。
                    record: object = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f'数据文件第 {line_number} 行不是合法 JSON。') from error
                # isinstance 检查运行时类型；先确认字典，才能按本例调用 .get。
                if not isinstance(record, dict):
                    raise ValueError(f'数据文件第 {line_number} 行应当是学生字典。')
                student_id = record.get('id')
                # 字典类型正确不等于字段有效：还需确认 ID 是非空字符串。
                if not isinstance(student_id, str) or not student_id.strip():
                    raise ValueError(f'数据文件第 {line_number} 行缺少有效字符串 ID。')
                student_id = student_id.strip()
                if student_id in existing_ids:
                    raise ValueError(f'数据文件第 {line_number} 行存在重复 ID：{student_id}')
                existing_ids.add(student_id)
    except FileNotFoundError:
        return existing_ids
    return existing_ids


def save(students: list[Student], path: Path = DATA_FILE) -> None:
    """追加学生记录；错误由调用方处理，不切换成覆盖模式。"""
    if not students:
        return
    # 先序列化，再打开文件；writelines 不会自动换行，所以每项补上 \n。
    lines = [json.dumps(student, ensure_ascii=False) + '\n' for student in students]
    with path.open('a', encoding='utf-8', newline='\n') as file:
        file.writelines(lines)


def insert(path: Path = DATA_FILE) -> int:
    """录入一条完整记录就保存一条；返回本次成功保存的人数。"""
    existing_ids = read_existing_ids(path)
    saved_count = 0
    while True:
        student_id = input('输入 ID（直接回车结束录入）：').strip()
        if not student_id:
            break
        if student_id in existing_ids:
            print('这个 ID 已存在，请换一个 ID。')
            continue

        name = input('输入姓名：').strip()
        while not name:
            print('姓名不能为空。')
            name = input('输入姓名：').strip()

        student: Student = {
            'id': student_id,
            'name': name,
            'english': read_score('英语'),
            'python': read_score('Python'),
            'java': read_score('Java'),
        }
        # 只有 save 正常返回，才提示成功并更新本次录入状态。
        save([student], path)
        existing_ids.add(student_id)
        saved_count += 1
        print(f'已保存：{name}（ID：{student_id}）')

        answer = input('是否继续添加？y/n：').strip().lower()
        if answer != 'y':
            break

    print(f'本次成功保存 {saved_count} 名学生。')
    return saved_count


def menu() -> None:
    """当前只展示已实现功能，后续跟着课程扩展。"""
    print('\n======学生信息系统（AI 对照版）======')
    print('1. 录入信息')
    print('0. 退出')


def main() -> None:
    try:
        while True:
            menu()
            # 菜单按字符串判断即可，输入字母也不会因 int 转换而崩溃。
            choice = input('请选择：').strip()
            if choice == '0':
                if input('确定退出吗？y/n：').strip().lower() == 'y':
                    print('谢谢使用。')
                    return
            elif choice == '1':
                try:
                    insert()
                except (OSError, ValueError) as error:
                    # 这里是交互边界：给出原因，不宣称未完成的写入已经成功。
                    print(f'录入中止：{error}')
                    print('请检查数据文件或权限；已提示保存成功的记录无需重复录入。')
            else:
                print('当前仅支持 0 和 1，请重新选择。')
    except (KeyboardInterrupt, EOFError):
        print('\n已结束输入；尚未完整录入的这条记录不会保存。')


if __name__ == '__main__':
    main()
