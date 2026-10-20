"""第十四课：文件、with 与路径操作。演示仅修改独立临时目录。"""

# 从项目根目录运行：python python-learn1/demo14.py
# 导入本模块不运行演示；临时目录结束后自动清理，不改动 store 中的资料。
import json
import os
import shutil
import tempfile
from pathlib import Path


def save_students(path, students):
    """将可 JSON 序列化的学习记录写入文本文件；覆盖原内容，不自动创建父目录。"""
    # 先序列化，格式不支持时不会因为提前以 w 打开而截断原文件。
    text = json.dumps(students, ensure_ascii=False, indent=2)
    with open(path, 'w', encoding='utf-8', newline='\n') as file:
        file.write(text)


def load_students(path):
    """读取 JSON 数据；文件不存在、编码或内容错误时向调用方报告。"""
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def run_examples(root):
    """内部演示：root 由 main 创建的独立临时目录提供。"""
    print('\n--- 1. 路径对象与当前工作目录 ---')
    lesson_dir = Path(__file__).resolve().parent
    print(lesson_dir.name)                   # python-learn1
    print(Path.cwd().is_absolute())          # True：不等于必须是脚本目录
    notes_dir = root / 'notes'
    notes_dir.mkdir()
    text_path = notes_dir / 'lesson.txt'
    print(text_path.name, text_path.suffix)  # lesson.txt .txt
    print(text_path.exists())               # False：构造 Path 不创建文件

    print('\n--- 2. w 写入、a 追加与 r 读取 ---')
    with open(text_path, 'w', encoding='utf-8', newline='\n') as file:
        written = file.write('第一行\n')
        file.writelines(['第二行\n', '第三行\n'])
        print(written)                      # 4：字符数，不是 UTF-8 字节数
    print(file.closed)                      # True
    with open(text_path, 'a', encoding='utf-8', newline='\n') as file:
        file.write('追加内容\n')
    with open(text_path, 'r', encoding='utf-8') as file:
        print(repr(file.read()))            # '第一行\n第二行\n第三行\n追加内容\n'
        print(repr(file.read()))            # ''：位置已到末尾

    print('\n--- 3. 按行读取与回到开头 ---')
    with open(text_path, encoding='utf-8') as file:
        print(repr(file.readline()))        # '第一行\n'
        file.seek(0)
        for number, line in enumerate(file, start=1):
            print(number, line.rstrip('\n')) # 不用 strip 误删正文两端的空格
    with open(text_path, encoding='utf-8') as file:
        print(len(file.readlines()))        # 4：一次读取所有剩余行到列表

    print('\n--- 4. x 创建与 w 截断 ---')
    unique_path = root / 'unique.txt'
    with open(unique_path, 'x', encoding='utf-8') as file:
        file.write('已有内容')
    try:
        with open(unique_path, 'x', encoding='utf-8'):
            pass
    except FileExistsError:
        print('x 不覆盖已有文件')
    with open(unique_path, 'w', encoding='utf-8') as file:
        file.write('新')
    print(unique_path.read_text(encoding='utf-8'))  # 新：原内容被截断

    print('\n--- 5. 二进制、tell 与 seek ---')
    binary_path = root / 'data.bin'
    with open(binary_path, 'wb') as file:
        file.write(b'ABCDE')
    with open(binary_path, 'rb') as file:
        print(file.read(2), file.tell())     # b'AB' 2
        file.seek(-2, os.SEEK_END)
        print(file.read())                   # b'DE'

    print('\n--- 6. 异常离开 with 也会关闭文件 ---')
    handle = None
    try:
        with open(text_path, encoding='utf-8') as handle:
            raise ValueError('故意中断本节读取')
    except ValueError:
        print(handle.closed)                # True
    try:
        with open(root / 'missing.txt', encoding='utf-8'):
            pass
    except FileNotFoundError:
        print('不存在的文件不会被 r 自动创建')

    print('\n--- 7. os 与 pathlib 的目录操作 ---')
    nested_dir = root / 'archive' / 'drafts'
    os.makedirs(nested_dir)
    print(os.path.basename(os.fspath(text_path))) # lesson.txt
    print(os.path.isfile(text_path), notes_dir.is_dir())  # True True
    print(sorted(os.listdir(notes_dir)))     # ['lesson.txt']：名称，不是完整路径
    print(sorted(path.name for path in notes_dir.iterdir()))  # ['lesson.txt']
    with os.scandir(notes_dir) as entries:
        print(sorted(entry.name for entry in entries if entry.is_file()))
    found = []
    for current, dirs, files in os.walk(notes_dir):
        for name in files:
            found.append((Path(current) / name).relative_to(root).as_posix())
    print(sorted(found))                    # ['notes/lesson.txt']

    print('\n--- 8. 复制、改名和删除：只操作本临时目录 ---')
    copied_path = nested_dir / 'copy.txt'
    shutil.copyfile(text_path, copied_path)
    print(copied_path.read_bytes() == text_path.read_bytes())  # True
    renamed_path = nested_dir / 'renamed.txt'
    copied_path.rename(renamed_path)          # 目标为本例新路径，无覆盖歧义
    print(copied_path.exists(), renamed_path.exists())  # False True
    os.remove(renamed_path)
    os.rmdir(nested_dir)                     # 只能删除空目录
    print(renamed_path.exists(), nested_dir.exists())  # False False

    print('\n--- 9. 小实践：JSON 文件持久化 ---')
    students = [{'name': '张三', 'score': 90}, {'name': '李四', 'score': 55}]
    json_path = root / 'students.json'
    save_students(json_path, students)
    restored = load_students(json_path)
    print(restored == students)              # True
    passed = [item['name'] for item in restored if item['score'] >= 60]
    print(passed)                           # ['张三']


def main():
    # 明确验证将自动清理的目录确实位于系统临时目录下，且是本课专用新目录。
    with tempfile.TemporaryDirectory(prefix='python-lesson14-') as directory:
        root = Path(directory).resolve()
        temp_parent = Path(tempfile.gettempdir()).resolve()
        if root.parent != temp_parent or not root.name.startswith('python-lesson14-'):
            raise RuntimeError('临时目录位置不符合本课约定')
        run_examples(root)
    print('\n临时目录已清理：', not root.exists())  # True


if __name__ == '__main__':
    main()
