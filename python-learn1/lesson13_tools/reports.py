"""展示模块：通过包内相对导入复用成绩计算。"""

from .scores import summarize_scores


def format_report(scores, *, pass_mark=60):
    """返回报告文本，由调用方决定打印或保存。"""
    summary = summarize_scores(scores, pass_mark=pass_mark)
    average = summary['average']
    average_text = '暂无' if average is None else f'{average:.1f}'
    return f"人数：{summary['count']}，及格：{len(summary['passed'])}，平均分：{average_text}"
