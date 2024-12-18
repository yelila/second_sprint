from __future__ import annotations

from torch.autograd import variable

from src.exception import *
from src.item import *


SYMBOL_NOT = '¬';
SYMBOL_CONJUNCTION = '∧';
SYMBOL_DISJUNCTION = '∨';
SYMBOL_IMPLY = '→';
SYMBOL_EQUIVALENT = '↔';
SYMBOL_LEFT_BRACKET = '(';
SYMBOL_RIGHT_BRACKET = ')';
SYMBOL_FULL = '∀';
SYMBOL_EXIST = '∃';
SYMBOL_SPACE = ' ';
SYMBOL_COMMA = ','; # 结束符

PRIORITY_NOT = 1;           # 优先级最高 非 SYMBOL_NOT = '¬';
PRIORITY_CONJUNCTION = 2;   # 优先级第二 链接  包括与 SYMBOL_CONJUNCTION = '∧';
PRIORITY_DISJUNCTION = 3;   # 优先级第三 链接  包括或 SYMBOL_DISJUNCTION = '∨';
PRIORITY_IMPLY = 4;         # 优先级第四 蕴含  包括前件后件 SYMBOL_IMPLY = '→';
PRIORITY_EQUIVALENT = 5;    # 优先级第四 等价  包括双等号 SYMBOL_EQUIVALENT = '↔';
# 这个怎么用？

class Formula:
    def __init__(self):
        self.quantifiers = []  # 量词列表 全称量词 和 存在量词
        self.item = []     # 子公式列表 
        self.statue = 0        # 状态 0
        self.left_bracket_num = 0 # 左括号计数器 用于判断是否匹配 右括号 公式 = （公式）现象
        self.name = None       # 原子公式名称


    @classmethod
    def parse(cls, predicate_str: str) -> Formula:
        # todo 2：predicate_str是包含原子谓词、逻辑运算符和括号的谓词公式
        # todo 3: predicate_str是包含原子谓词、逻辑运算符、括号和量词的谓词公式
        if not predicate_str:
            raise IncompletePredicate(predicate_str)
        cls = Formula()

        for i in range(len(predicate_str)):
            cls.forward(predicate_str, i)

        if cls.item:
            return cls.item[-1]
        else:
            raise InvalidPredicate(predicate_str,len(predicate_str))


    def forward(self, predicate_str, index):
        if self.statue == 0: # 初始状态
            self.statue_0(predicate_str, index)
        elif self.statue == 1: # 公式开始前
            self.statue_1(predicate_str, index)
        elif self.statue == 2: # 括号后
            self.statue_2(predicate_str, index)
        elif self.statue == 3: # 原子公式名称中
            self.statue_3(predicate_str, index)
        elif self.statue == 4: # 原子公式名称后
            self.statue_4(predicate_str, index)
        elif self.statue == 5: # 开始项列表
            self.statue_5(predicate_str, index)
        elif self.statue == 6: # 项前
            self.statue_6(predicate_str, index)
        elif self.statue == 7: # 项名称中
            self.statue_7(predicate_str, index)
        elif self.statue == 8: # 项名称后
            self.statue_8(predicate_str, index)
        elif self.statue == 9: # 结束项列表
            self.statue_9(predicate_str, index)
        elif self.statue == 10: # 公式后
            self.statue_10(predicate_str, index)
        elif self.statue == 11: # 量词前
            self.statue_11(predicate_str, index)
        elif self.statue == 12: # 量词中
            self.statue_12(predicate_str, index)
        elif self.statue == 13: # 量词后
            self.statue_13(predicate_str, index)
        elif self.statue == 14: # 结束公式，返回公式对象
            self.statue_14(predicate_str, index)


    def statue_0(self, predicate_str, index): # 初始状态
        if predicate_str[index] == SYMBOL_NOT:
            self.statue = 1
            self.item.append(NonFormula()) # 非公式 入栈 不考虑 非 量词 叠加的问题
            print("非公式 入栈")
        elif predicate_str[index] == SYMBOL_SPACE:
            self.statue = 1
        elif predicate_str[index] == SYMBOL_LEFT_BRACKET:
            """
            这里有可能跟公式 或者是 量词
            如果是 量词： 需要一个 Formula 对象 作为子公式 入栈
            如果是 公式： 直接入栈
            """
            self.statue = 2 # 左括号 转移到括号后
            self.item.append(Formula()) # 公式 入栈
            print("公式 入栈")
        elif predicate_str[index].isalpha():
            self.statue = 3 # 原子公式 转移到原子公式名称中
            self.item.append(AtomicFormula()) #原子公式 入栈
            print("原子公式 入栈")
            self.name = predicate_str[index] # 原子公式名称
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_1(self, predicate_str, index): # 公式开始前
        if predicate_str[index] == SYMBOL_NOT:
            self.statue = 1
            self.item.append(NonFormula()) # 非公式 入栈 不考虑 非 量词 叠加的问题
            print("非公式 入栈")
        elif predicate_str[index] == SYMBOL_SPACE:
            self.statue = 1 # 空格 忽略 状态不变
        elif predicate_str[index] == SYMBOL_LEFT_BRACKET:
            """
            这里有可能跟公式 或者是 量词
            如果是 量词： 需要一个 Formula 对象 作为子公式 入栈 如果到时候发现是 量词 则量词进入该公式量词列表 新建一个 Formula 对象 作为量词的子公式 入栈
            如果是 公式： 直接入栈
            """
            self.statue = 2
            self.item.append(Formula()) # 公式 入栈
            print("公式 入栈")
        elif predicate_str[index].isalpha():
            self.statue = 3
            self.item.append(AtomicFormula()) #原子公式 入栈
            print("原子公式 入栈")
            self.name = predicate_str[index] # 原子公式名称
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_2(self, predicate_str, index): # 括号后
        if predicate_str[index] == SYMBOL_LEFT_BRACKET:
            """
            进入子公式
            这里有可能跟公式 或者是 量词
            """
            self.statue = 2 # 左括号 转移到括号后
            self.item.append(Formula()) # 公式 入栈
            print("公式 入栈")
        elif predicate_str[index] == SYMBOL_SPACE:
            self.statue = 2 # 空格 忽略 状态不变
        elif predicate_str[index].isalpha():
            self.statue = 3
            self.item.append(AtomicFormula()) #原子公式 入栈
            print("原子公式 入栈")
            self.name = predicate_str[index]
        elif predicate_str[index] == SYMBOL_NOT:
            self.statue = 1
            self.item.append(NonFormula()) # 非公式 入栈 不考虑 非 量词 叠加的问题
            print("非公式 入栈")
        elif predicate_str[index] == SYMBOL_CONJUNCTION or predicate_str[index] == SYMBOL_DISJUNCTION:
            """
            待完善
            """
            self.statue = 11 # 量词 转移到量词前
            self.item[-1].quantifiers.append(predicate_str[index]) # 量词 入栈
            print("量词 入栈")
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_3(self, predicate_str, index): # 原子公式名称中
        if predicate_str[index].isalpha() or predicate_str[index].isdigit():
            self.name += predicate_str[index]
        elif predicate_str[index] == SYMBOL_SPACE:
            self.statue = 4 # 空格 转移到原子公式名称后
            self.item[-1].name = self.name
            self.name = ""  # 重置名称
        elif predicate_str[index] == SYMBOL_LEFT_BRACKET:
            self.statue = 5 # 左括号 转移到开始项列表
            self.item[-1].name = self.name
            self.name = ""  # 重置名称
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_4(self, predicate_str, index): # 原子公式名称后
        if predicate_str[index] == SYMBOL_SPACE:
            self.statue = 4 # 空格 忽略 状态不变
        elif predicate_str[index] == SYMBOL_LEFT_BRACKET:
            self.statue = 5 # 左括号 转移到开始项列表
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_5(self, predicate_str, index): # 开始项列表
        if predicate_str[index] == SYMBOL_SPACE:
            self.statue = 6 # 空格 转移到项前
        elif predicate_str[index].isalpha():
            self.statue = 7 # 项名称 转移到项名称中
            self.name = predicate_str[index]
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_6(self, predicate_str, index): # 项前
        if predicate_str[index] == SYMBOL_SPACE:
            self.statue = 6 # 空格 忽略 状态不变
        elif predicate_str[index].isalpha():
            self.statue = 7 # 项名称 转移到项名称中
            self.name = predicate_str[index]
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_7(self, predicate_str, index): # 项名称中
        if predicate_str[index].isalpha()  or predicate_str[index].isdigit():
            self.name += predicate_str[index]
        elif predicate_str[index] == SYMBOL_SPACE:
            self.statue = 8 # 空格 转移到项名称后
        elif predicate_str[index] == SYMBOL_COMMA:
            self.statue = 6 # 逗号 转移到项前
            self.item[-1].items.append(Variable(self.name)) # 变量 入栈
            print("变量 入栈")
            self.name = ""  # 重置名称
        elif predicate_str[index] == SYMBOL_RIGHT_BRACKET:
            """
            一个原子式结束 需要出栈
            """
            self.statue = 9 # 右括号 转移到公式后
            self.item[-1].items.append(Variable(self.name))
            print("变量 入栈")
            self.name = ""  # 重置名称
            if len(self.item) > 1: # 子公式结束
                atoformula = self.item.pop() # 出栈
                self.item[-1].item.append(atoformula)
                print("子公式 出栈 入item")
        elif predicate_str[index] == SYMBOL_LEFT_BRACKET:
            self.statue = 5 # 左括号 转移到开始项列表
            atom = AtomicFormula() # 原子公式 入栈
            atom.name = self.name
            self.name = ""  # 重置名称
            self.item.append(atom) # 原子公式 入栈
            print("原子公式 入栈")
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_8(self, predicate_str, index): # 项名称后
        if predicate_str[index] == SYMBOL_SPACE:
            self.statue = 8 # 空格 忽略 状态不变
        elif predicate_str[index] == SYMBOL_COMMA:
            self.statue = 6 # 逗号 转移到项前
            self.item[-1].items.append(Variable(self.name))
            print("变量 入栈")
            self.name = ""  # 重置名称
        elif predicate_str[index] == SYMBOL_RIGHT_BRACKET:
            """
            一个原子式结束 需要出栈
            """
            self.statue = 9  # 右括号 转移到公式后
            self.item[-1].items.append(Variable(self.name))
            print("变量 入栈")
            self.name = ""  # 重置名称
            if len(self.item) > 1:  # 子公式结束
                atoformula = self.item.pop()  # 出栈
                self.item[-1].item.append(atoformula)
                print("子公式 出栈 入item")
        elif predicate_str[index] == SYMBOL_LEFT_BRACKET:
            self.statue = 5 # 左括号 转移到开始项列表
            atom = AtomicFormula() # 原子公式 入栈
            print("原子公式 入栈")
            atom.name = self.name
            self.name = ""  # 重置名称
            self.item.append(atom) # 原子公式 入栈
            print("原子公式 入栈")
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_9(self, predicate_str, index): # 结束项列表
        if predicate_str[index] == SYMBOL_SPACE:
            if type(self.item[-1]) == 'AtomicFormula': # 原子式没有结束
                self.statue = 9
            else:
                self.statue = 10
        elif predicate_str[index] == SYMBOL_RIGHT_BRACKET:
            """
            一个原子式结束 不一定需要出栈 
            """
            if len(self.item) > 1: # 子公式结束
                atoformula = self.item.pop() # 出栈
                self.item[-1].item.append(atoformula)
                print("子公式 出栈 入item")
                if type(self.item[-1]) == 'AtomicFormula': # 原子式没有结束
                    self.statue = 9 # 右括号 转移到公式后
                else:
                    self.statue = 10  # 右括号 转移到公式后
            else:
                self.statue = 10 # 右括号 转移到公式后
        elif predicate_str[index] == SYMBOL_COMMA:
            self.statue = 6 # 逗号 转移到项前
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_10(self, predicate_str, index): # 公式后
        if predicate_str[index] == SYMBOL_SPACE:
            self.statue = 10 # 空格 忽略 状态不变
        elif predicate_str[index] == SYMBOL_RIGHT_BRACKET:
            """
            公式结束 
            """
            if len(self.item) > 1: # 子公式结束
                formula = self.item.pop() # 出栈
                if self.item: # 还有父公式
                    self.item[-1].item.append(formula)
                    print("子公式 出栈 入item")
                    self.statue = 1 # 右括号 转移到公式后
                else: # 根公式
                    self.statue = 14 # 右括号 转移到结束公式
                    self.formula = formula
        elif predicate_str[index] == SYMBOL_CONJUNCTION:
            conjunction = ConjunctionFormula() # 与公式 入栈
            print("与公式 入栈")
            if self.item: # 还有父公式
                formula = self.item.pop() # 出栈
                conjunction.set_left_child(formula)
                self.item.append(conjunction)
                print("出栈 创建与公式 入item")
                self.statue = 1 # 右括号 转移到公式后
            else: # 没有父公式 报错
                raise InvalidPredicate(predicate_str, index)
        elif predicate_str[index] == SYMBOL_DISJUNCTION:
            disjunction = DisjunctiveFormula() # 或公式 入栈
            print("或公式 入栈")
            if self.item: # 还有父公式
                formula = self.item.pop() # 出栈
                disjunction.set_left_child(formula)
                self.item.append(disjunction)
                print("出栈 创建或公式 入item")
                self.statue = 1 # 右括号 转移到公式后
            else: # 没有父公式 报错
                raise InvalidPredicate(predicate_str, index)
        elif predicate_str[index] == SYMBOL_IMPLY:
            implication = ImplicationFormula() # 蕴含公式 入栈
            print("蕴含公式 入栈")
            if self.item: # 还有父公式
                formula = self.item.pop() # 出栈
                implication.set_left_child(formula)
                self.item.append(implication)
                print("出栈 创建蕴含公式 入item")
                self.statue = 1  # 右括号 转移到公式后
            else: # 没有父公式 报错
                raise InvalidPredicate(predicate_str, index)
        elif predicate_str[index] == SYMBOL_EQUIVALENT:
            equivalent = EquivalentFormula() # 等价公式 入栈
            print("等价公式 入栈")
            if self.item: # 还有父公式
                formula = self.item.pop() # 出栈
                equivalent.set_left_child(formula)
                self.item.append(equivalent)
                print("出栈 创建等价公式 入item")
                self.statue = 1  # 右括号 转移到公式后
            else: # 没有父公式 报错
                raise InvalidPredicate(predicate_str, index)
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_11(self, predicate_str, index): # 量词前
        if predicate_str[index] == SYMBOL_SPACE:
            self.statue = 11 # 空格 忽略 状态不变
        elif predicate_str[index].isalpha():
            self.statue = 12 # 量词 转移到量词中
            self.name = predicate_str[index]
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_12(self, predicate_str, index): # 量词中
        if predicate_str[index].isalpha() or predicate_str[index].isdigit():
            self.name += predicate_str[index]
        elif predicate_str[index] == SYMBOL_SPACE:
            self.statue = 13 # 空格 转移到量词后
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_13(self, predicate_str, index): # 量词后
        if predicate_str[index] == SYMBOL_SPACE:
            self.statue = 13 # 空格 忽略 状态不变
        elif predicate_str[index] == SYMBOL_RIGHT_BRACKET:
            """
            量词结束 需要出栈
            """
            self.item[-1].quantifiers.append(self.name)
            print("量词 出栈")
            self.name = ""  # 重置名称
            self.statue = 1 # 右括号 转移到公式开始前
        else:
            raise InvalidPredicate(predicate_str, index)

    def statue_14(self, predicate_str, index): # 结束公式
        if predicate_str[index] == '\r':
            self.statue = 14 # 回车 忽略 状态不变
        elif predicate_str[index] == '\n':
            self.statue = 14 # 换行 忽略 状态不变
        else:
            raise InvalidPredicate(predicate_str, index)







class AtomicFormula(Formula):
    """
    AtomicFormula是逻辑公式的原子元素，包括：
    - 原子命题,常量、变量(p,q,r,...)
    - 原子函数(f(x),g(y,z),...)
    可以嵌套
    继承自Formula
    """
    def __init__(self):
        super().__init__()
        self.name = None
        self.items = []

    @classmethod
    def parse(cls, atomic_predicate_str: str) -> Formula:
        # todo 1：atomic_predicate_str是原子谓词
        pass

    def __str__(self):
        """
        返回原子谓词的字符串表示
        :return:
        """
        items_str = ",".join(self.items)
        return f"{self.name}({items_str})"


class NonFormula(Formula):
    """
    NonFormula是逻辑公式的非元素，包括：
    - 否定(¬)
    非公式 后面跟着一个公式 使用set_child方法设置子公式
    """
    def __init__(self):
        super().__init__()
        self.child = None

    def set_child(self, child: Formula):
        self.child = child

    def __str__(self):
        return f"{SYMBOL_NOT}({self.child})"


class BinaryFormula(Formula):
    """
    BinaryFormula是逻辑公式的二元运算符，包括：
    - 与(∧)
    - 或(∨)
    - 蕴含(→)
    - 等价(↔)
    二元公式 包含着两个公式 使用set_left_child和set_right_child方法设置左右子公式
    """
    def __init__(self):
        super().__init__()
        self.left_child = None
        self.right_child = None

    def set_left_child(self, left_child: Formula):
        self.left_child = left_child

    def set_right_child(self, right_child: Formula):
        self.right_child = right_child


class ConjunctionFormula(BinaryFormula):
    """
    ConjunctionFormula是逻辑公式的与运算符，包括：
    - 与(∧)
    与公式 包含着两个公式 使用set_left_child和set_right_child方法设置左右子公式
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"({self.left_child}) {SYMBOL_CONJUNCTION} ({self.right_child})"


class DisjunctiveFormula(BinaryFormula):
    """
    DisjunctiveFormula是逻辑公式的或运算符，包括：
    - 或(∨)
    或公式 包含着两个公式 使用set_left_child和set_right_child方法设置左右子公式
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"({self.left_child}) {SYMBOL_DISJUNCTION} ({self.right_child})"


class ImplicationFormula(BinaryFormula):
    """
    ImplicationFormula是逻辑公式的蕴含运算符，包括：
    - 蕴含(→)
    蕴含公式 包含着两个公式 使用set_left_child和set_right_child方法设置左右子公式
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"({self.left_child}) {SYMBOL_IMPLY} ({self.right_child})"


class EquivalentFormula(BinaryFormula):
    """
    EquivalentFormula是逻辑公式的等价运算符，包括：
    - 等价(↔)
    等价公式 包含着两个公式 使用set_left_child和set_right_child方法设置左右子公式
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"({self.left_child}) {SYMBOL_EQUIVALENT} ({self.right_child})"


if __name__ == '__main__':
    input_str = "¬ pq (aa , b0, f ( x1, dd1)) ∨ (p( y) ∧ t(c, g(k)) → q(b ) ∧r (c,d) ↔ s(z)) "
    formula = Formula.parse(input_str)
    print(formula)