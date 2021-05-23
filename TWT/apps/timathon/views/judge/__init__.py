from .judge import JudgeView
from .judge_vote import JudgeVote

judge = JudgeView.as_view()
judge_vote = JudgeVote.as_view()
