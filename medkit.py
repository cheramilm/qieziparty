from constants import *


class Medkit:
    name = ''
    value = 0
    position = 0

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        if self.value > 0:
            return "『%s』，补充茄汁：『%d』" % (self.name, self.value)
        else:
            return "『%s』" % self.name

    def better_than_me(self, another):
        if another.value >= self.value:
            return 1
        else:
            return 0


noneMedkit = Medkit(noneMedkitName, 0)
medkitTemplates = [Medkit('大包复合肥', 70), Medkit('中包复合肥', 50), Medkit('小包复合肥', 30), Medkit('袋装复合肥', 10)]
