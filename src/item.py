class Item:
    """
    Base class for all items in the program.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Constant(Item):
    """
    常量项
    """
    def __str__(self):
        return self.name

class Variable(Item):
    """
    变量项
    """
    def __str__(self):
        return self.name


class Function(Item):
    """
    函数项
    """
    def __init__(self):
        super().__init__()
        self.items = [] # 参数项列表

    def __str__(self):
        items_str = ",".join(self.items)
        return f"{self.name}({items_str})"

