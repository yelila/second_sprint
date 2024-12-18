class InvalidPredicate(SyntaxError):
    """
    Raised when a predicate string is not valid. 无效谓词字符串
    """
    def __init__(self, predicate_str: str, index: int):
        self.predicate_str = predicate_str
        self.index = index

    def __str__(self):
        return f"谓词公式{self.predicate_str}的第{self.index}个字符'{self.predicate_str[self.index]}'不符合语法"


class IncompletePredicate(SyntaxError):
    """
    Raised when a predicate string is incomplete. 谓词字符串不完整
    """
    def __init__(self, predicate_str: str):
        self.predicate_str = predicate_str

    def __str__(self):
        return f"谓词公式{self.predicate_str}不完整"


class ConflictingQuantifier(SyntaxError):
    """
    Raised when a predicate string has conflicting quantifier domains. 量词辖域冲突
    """
    def __init__(self, predicate_str: str, index: int):
        self.predicate_str = predicate_str
        self.index = index

    def __str__(self):
        return f"谓词公式{self.predicate_str}的第{self.index}个字符'{self.predicate_str[self.index]}'出现量词辖域冲突"

