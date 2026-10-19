"""包入口：在 python-learn1 目录运行 python -m lesson13_tools。"""

from .reports import format_report


def main():
    print(format_report([90, 55, 80]))


if __name__ == '__main__':
    main()
