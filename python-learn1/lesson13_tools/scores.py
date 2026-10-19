"""成绩计算模块：不依赖打印、交互输入或文件操作。"""


def validate_score(score):
    """只接受 0～100 的 int/float 数值，排除布尔值。"""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError('成绩必须是数值，不能是布尔值')
    if not 0 <= score <= 100:
        raise ValueError('成绩必须在 0～100 之间')
    return score


def summarize_scores(scores, *, pass_mark=60):
    """统计数值成绩序列；不修改输入，空序列平均分为 None。"""
    validate_score(pass_mark)
    values = [validate_score(score) for score in scores]
    passed = [score for score in values if score >= pass_mark]
    average = sum(values) / len(values) if values else None
    return {'count': len(values), 'passed': passed, 'average': average}
