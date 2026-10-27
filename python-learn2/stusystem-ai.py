"""学生系统对照版：实现录入、查询、删除和编辑。"""

# 运行：python python-learn2/stusystem-ai.py
# 数据保存在本文件同目录的 student-ai.jsonl，每行一个 JSON 对象。
# 不读取或改写原程序的 student.txt。类型标注写法要求 Python 3.9+。
import json  # 字典与 JSON 文本互转，对应 JS 的 JSON.stringify / JSON.parse 用途。
import tempfile  # 创建临时文件；删除或编辑时先写副本，再替换原数据文件。
from pathlib import Path  # 路径对象，提供路径拼接和 open 等方法。
from typing import Optional, TypedDict  # Optional[int] 表示整数或 None。


class Student(TypedDict):
    """描述学生字典的结构，不会自动进行运行时校验。"""

    id: str
    name: str
    english: int
    python: int
    java: int


# __file__ 是本文件路径；resolve().parent 取得绝对目录，/ 在此表示拼接路径。
DATA_FILE = Path(__file__).resolve().parent / 'student-ai.jsonl'


def validate_score(score: object) -> int:
    """集中校验成绩，输入界面和编辑保存共用同一规则。"""
    # isinstance 只判断、不转换；True 也属于 int，因此先明确排除 bool。
    if isinstance(score, bool) or not isinstance(score, int):
        raise TypeError('成绩必须是整数，不能是布尔值或字符串。')
    if not 0 <= score <= 100:
        raise ValueError('成绩必须在 0～100 之间。')
    return score


def read_score(subject: str, *, default: Optional[int] = None) -> int:
    """只重试输错的这一科，不要求重新输入姓名与其他成绩。"""
    # 单独的 * 不是占位符：default 只能写成 default=80，不能作为第二个位置实参。
    # default 是普通参数名；Optional[int] 表示 int 或 None，= None 才提供默认值。
    # 编辑时传入旧成绩，允许回车保留；录入时不传 default，仍然必须填写。
    if default is not None:
        validate_score(default)
    # subject: str / -> int 是可选类型说明，真正的转换由下面 int(raw) 完成。
    while True:
        # strip 去两端空白，返回新字符串；不删除中间空格。
        prompt = f'{subject}成绩（0～100 的整数）：'
        if default is not None:
            prompt = f'{subject}成绩（当前 {default}，回车保留）：'
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default  # 0 分也可以保留，不能写 if default。
        try:
            score = int(raw)
        except ValueError:
            print('请输入整数，例如 80；不能输入空内容或 80.5。')
            continue
        try:
            return validate_score(score)
        except ValueError as error:
            print(f'{error}请重新输入。')


def read_student_lines(path: Path = DATA_FILE) -> list[tuple[str, str]]:
    """返回 (ID, 原文本行)，供各功能复用。只校验 JSON 和 ID。"""
    # 保留原文本行，删除时不重建其他学生的字典，避免遗漏尚未用到的字段。
    rows: list[tuple[str, str]] = []
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
                # 每项保存 (ID, 原文本行)，后续可解包为 current_id, line。
                rows.append((student_id, line))
    except FileNotFoundError:
        return rows
    return rows


def read_existing_ids(path: Path = DATA_FILE) -> set[str]:
    """读取已有 ID；与删除功能共用同一份数据读取和校验逻辑。"""
    # path 是参数，Path 是类型，DATA_FILE 是默认值；set[str] 表示字符串集合。
    # 后面的 for 负责逐项解包，最前面的 student_id 决定收集什么；_line 表示本处不用文本行。
    return {student_id for student_id, _line in read_student_lines(path)}


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


def replace_student_lines(lines: list[str], path: Path = DATA_FILE) -> None:
    """先写临时文件，再替换原文件；用于本单进程练习，不提供并发或断电保障。"""
    temporary_path = None
    try:
        # 与目标文件放在同一个目录，避免跨文件系统替换。
        # delete=False 让退出 with 后文件仍存在，以便关闭句柄后再替换（Windows 尤其需要）。
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='\n',
            dir=path.parent, prefix=f'.{path.name}.', suffix='.tmp', delete=False,
        ) as file:
            # file.name 是已创建的临时文件名；Path 包装后可以调用 replace / unlink。
            temporary_path = Path(file.name)
            file.writelines(lines)
        # 临时文件完整写入并关闭后，才替换原文件，不提前用 w 清空原数据。
        if temporary_path.resolve().parent != path.parent.resolve():
            raise ValueError('临时文件必须与数据文件处于同一目录。')
        temporary_path.replace(path)
    finally:
        # 替换成功后临时路径已不存在；写入或替换失败时则清理本次临时文件。
        if temporary_path is not None:
            # unlink 删除文件；missing_ok 只忽略“文件不存在”，不忽略权限等其他错误。
            temporary_path.unlink(missing_ok=True)


def delete_student(student_id: str, path: Path = DATA_FILE) -> bool:
    """删除一个 ID，成功返回 True；不存在返回 False，且不重写文件。"""
    student_id = student_id.strip()
    if not student_id:
        raise ValueError('待删除 ID 不能为空。')
    # 先读完并检查整个文件，再考虑写入；损坏数据不会被 eval 执行或被当作空数据。
    rows = read_student_lines(path)
    # 解包 ID 和行文本 → 排除待删除 ID → 只把 line 放进新列表；此处还未写磁盘。
    remaining_lines = [line for current_id, line in rows if current_id != student_id]
    if len(remaining_lines) == len(rows):
        return False
    replace_student_lines(remaining_lines, path)
    return True


def delete(path: Path = DATA_FILE) -> int:
    """交互删除入口，与实际读写分开，返回本次删除人数。"""
    deleted_count = 0
    while True:
        existing_ids = read_existing_ids(path)
        if not existing_ids:
            print('暂无学生信息。')
            break
        student_id = input('输入待删除 ID（直接回车返回菜单）：').strip()
        if not student_id:
            break
        # 未找到目标时，不提示成功、不改写文件。
        if student_id not in existing_ids:
            print(f'没有找到 ID 为 {student_id} 的学生。')
        else:
            answer = input(f'确定删除 ID 为 {student_id} 的学生吗？y/n：').strip().lower()
            if answer == 'y':
                if delete_student(student_id, path):
                    deleted_count += 1
                    print(f'已删除 ID 为 {student_id} 的学生。')
                else:
                    print('该学生已不存在，本次未删除。')
            else:
                print('已取消本次删除。')
        if input('是否继续删除？y/n：').strip().lower() != 'y':
            break
    print(f'本次成功删除 {deleted_count} 名学生。')
    return deleted_count


def validate_student(record: object) -> Student:
    """检查完整学生字段，供编辑与查询展示复用；类型标注不代替运行时检查。"""
    # 是字典仅代表容器类型正确，后面仍要逐项检查 ID、姓名和成绩。
    if not isinstance(record, dict):
        raise ValueError('学生记录必须是字典。')
    student_id = record.get('id')
    name = record.get('name')
    if not isinstance(student_id, str) or not student_id.strip():
        raise ValueError('学生 ID 必须是非空字符串。')
    if not isinstance(name, str) or not name.strip():
        raise ValueError('学生姓名必须是非空字符串。')
    return {
        'id': student_id.strip(),
        'name': name.strip(),
        'english': validate_score(record.get('english')),
        'python': validate_score(record.get('python')),
        'java': validate_score(record.get('java')),
    }


def modify_student(student_id: str, updated: Student, path: Path = DATA_FILE) -> bool:
    """更新一个已有 ID；不存在或内容相同返回 False，校验或写回失败则抛错。"""
    student_id = student_id.strip()
    if not student_id:
        raise ValueError('待修改 ID 不能为空。')
    candidate = validate_student(updated)
    if candidate['id'] != student_id:
        raise ValueError('编辑时不能修改学生 ID。')

    rows = read_student_lines(path)
    for index, (current_id, line) in enumerate(rows):
        if current_id != student_id:
            continue
        # 在原字典副本上更新已编辑字段，保留其他可能存在的额外字段。
        record = json.loads(line)
        replacement = record.copy()
        replacement.update(candidate)
        if replacement == record:
            return False
        replacement_line = json.dumps(replacement, ensure_ascii=False) + '\n'
        lines = [original_line for _current_id, original_line in rows]
        lines[index] = replacement_line
        # 只在所有输入和序列化完成后写回，复用删除时的临时文件替换逻辑。
        replace_student_lines(lines, path)
        return True
    return False


def modify(path: Path = DATA_FILE) -> int:
    """循环编辑入口；每次确认保存后才更新本次成功次数，不递归调用自己。"""
    modified_count = 0
    while True:
        rows = read_student_lines(path)
        if not rows:
            print('暂无学生信息。')
            break
        student_id = input('输入待修改 ID（直接回车返回菜单）：').strip()
        if not student_id:
            break

        current_line = None
        for current_id, line in rows:
            if current_id == student_id:
                current_line = line
                break
        if current_line is None:
            print(f'没有找到 ID 为 {student_id} 的学生。')
        else:
            current = validate_student(json.loads(current_line))
            print(f"当前：{current['name']}，英语 {current['english']}，"
                  f"Python {current['python']}，Java {current['java']}")
            name = input(f"姓名（当前 {current['name']}，回车保留）：").strip()
            updated: Student = {
                'id': student_id,  # 保留原 ID，避免编辑后与其他学生冲突。
                'name': name or current['name'],
                'english': read_score('英语', default=current['english']),
                'python': read_score('Python', default=current['python']),
                'java': read_score('Java', default=current['java']),
            }
            if updated == current:
                print('内容没有变化，未写入文件。')
            else:
                answer = input('确定保存以上修改吗？y/n：').strip().lower()
                if answer != 'y':
                    print('已取消本次修改。')
                elif modify_student(student_id, updated, path):
                    modified_count += 1
                    print(f'已修改 ID 为 {student_id} 的学生。')
                else:
                    print('目标已不存在或内容相同，本次未保存。')
        if input('是否继续修改？y/n：').strip().lower() != 'y':
            break
    print(f'本次成功保存 {modified_count} 次修改。')
    return modified_count


def search_students(
    path: Path = DATA_FILE, *, student_id: str = '', name: str = '',
) -> list[Student]:
    """精确查询并返回新列表；两种条件都传入时优先 ID，不写入文件。"""
    student_id = student_id.strip()
    name = name.strip()
    if not student_id and not name:
        raise ValueError('请提供学生 ID 或姓名，不能用空条件查询。')

    results: list[Student] = []
    for current_id, line in read_student_lines(path):
        try:
            student = validate_student(json.loads(line))
        except (TypeError, ValueError) as error:
            # 有坏记录时明确指出，不悄悄跳过后把不完整结果当作查询成功。
            raise ValueError(f'ID 为 {current_id} 的学生记录有误：{error}') from error
        # 保留课程的规则：ID 非空时只查 ID，不因 ID 不匹配再改查姓名。
        if student_id:
            matches = student['id'] == student_id
        else:
            matches = student['name'] == name
        if matches:
            results.append(student)
    # 每次调用新建结果列表，同名学生可以有多条，连续查询不会混入上次结果。
    return results


def show_student(students: list[Student]) -> None:
    """展示结果和总分，不修改记录；用列分隔而非依赖终端制表位。"""
    if not students:
        print('未找到匹配的学生。')
        return
    # 全部检查通过后再输出表格，避免打印到一半才发现成绩不能相加。
    validated = [validate_student(student) for student in students]
    print('ID | 姓名 | 英语 | Python | Java | 总分')
    for student in validated:
        total_score = student['english'] + student['python'] + student['java']
        values = (
            student['id'], student['name'], str(student['english']),
            str(student['python']), str(student['java']), str(total_score),
        )
        # join 拼接的每一项都须是字符串；分隔列不承诺中英文等宽对齐。
        print(' | '.join(values))
    print(f'共找到 {len(validated)} 名学生。')


def search(path: Path = DATA_FILE) -> None:
    """交互查询入口；读取、筛选和展示各自独立，输入错误用循环重试。"""
    while True:
        if not read_existing_ids(path):
            print('暂无学生信息。')
            return
        mode = input('按 ID 查询输入 1，按姓名查询输入 2，返回输入 0：').strip()
        if mode == '0':
            return
        if mode not in ('1', '2'):
            print('请输入 0、1 或 2。')
            continue  # 不递归调用 search，避免旧一轮流程在返回后继续执行。

        keyword = input('输入查询内容（精确匹配，直接回车返回菜单）：').strip()
        if not keyword:
            print('已取消本次查询。')
            return
        if mode == '1':
            results = search_students(path, student_id=keyword)
        else:
            results = search_students(path, name=keyword)
        show_student(results)
        if input('是否继续查询？y/n：').strip().lower() != 'y':
            return


def menu() -> None:
    """当前只展示已实现功能，后续跟着课程扩展。"""
    print('\n======学生信息系统（AI 对照版）======')
    print('1. 录入信息')
    print('2. 查询信息')
    print('3. 删除信息')
    print('4. 修改信息')
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
            elif choice == '2':
                try:
                    search()
                except (OSError, ValueError, TypeError) as error:
                    print(f'查询中止：{error}')
                    print('请检查数据文件或权限，查询不会修改文件。')
            elif choice == '3':
                try:
                    delete()
                except (OSError, ValueError) as error:
                    print(f'删除中止：{error}')
                    print('请检查数据文件或权限；未完成替换时不会提示删除成功。')
            elif choice == '4':
                try:
                    modify()
                except (OSError, ValueError, TypeError) as error:
                    print(f'修改中止：{error}')
                    print('请检查数据内容或权限；未完成替换时不会提示修改成功。')
            else:
                print('当前仅支持 0、1、2、3 和 4，请重新选择。')
    except (KeyboardInterrupt, EOFError):
        print('\n已结束输入；已完成的保存、删除或修改以此前的成功提示为准。')


if __name__ == '__main__':
    main()
