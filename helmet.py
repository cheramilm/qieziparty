from constants import *


class Helmet:
    name = ''
    level = 0
    originalName = ''
    fullValue = 0
    leftValue = 0
    position = 0

    def __init__(self, name, level, left_value):
        self.name = name
        self.originalName = name
        self.level = level
        self.fullValue = left_value
        self.leftValue = left_value

    def __str__(self):
        return "『%s』，剩余防护力：『%d』" % (self.name, self.leftValue)

    def better_than_me(self, another):
        if another.leftValue >= self.leftValue:
            return 1
        else:
            return 0

    def protect(self, value):
        if self.fullValue == 0:
            return value
        if self.leftValue >= value:
            self.leftValue = self.leftValue - value
            if 0.6 <= self.leftValue / self.fullValue < 0.8:
                self.name = self.originalName + '(破)'
            elif self.leftValue / self.fullValue < 0.6:
                self.name = self.originalName + '(残)'
            return 0
        else:
            self.leftValue = self.leftValue - value
            return_value = abs(self.leftValue)
            self.leftValue = 0
            if self.name != hairName:
                print("『%s』被打烂" % self.originalName)
                self.name = hairName
                self.level = 0
                self.leftValue = 0
            return return_value


hair = Helmet(hairName, 0, 0)
helmetTemplates = [Helmet('坚果盔子', 3, 230), Helmet('树皮盔子', 2, 160), Helmet('叶子盔子', 1, 110)]
