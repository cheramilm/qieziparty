from constants import *
from utils import *


class Vehicle:
    name = ''
    speed = 0
    leftTimes = 0
    position = 0

    def __init__(self, name, speed, left_times):
        self.name = name
        self.speed = speed
        self.leftTimes = left_times

    def __str__(self):
        return "『%s』， 速度：『%d』，剩余次数：『%d』" % (self.name, self.speed, self.leftTimes)

    def to_foot(self):
        self.name = footName
        self.speed = footSpeed
        self.leftTimes = footTimes

    def better_than_me(self, another):
        if another.speed >= self.speed and another.leftTimes >= self.leftTimes:
            return 1
        elif another.speed * another.leftTimes > self.speed * self.leftTimes * 2:
            return 1
        elif another.speed > self.speed == footSpeed:
            return 1
        else:
            return 0

    def run(self):
        if self.leftTimes > 0:
            self.leftTimes = self.leftTimes - 1
            return self.speed
        else:
            if self.name != footName:
                Utils.print("『%s』剩余次数为『0』，自动丢弃！" % self.name)
                self.to_foot()
                return self.speed
            else:
                Utils.print("茄根已经不能支撑您壮硕的娇躯，爬着走吧！！！")
                return 1


foot = Vehicle(footName, footSpeed, footTimes)
vehicleTemplates = [Vehicle('西瓜皮', 70, 10), Vehicle('橘子皮', 50, 5), Vehicle('香蕉皮', 30, 10), Vehicle('榴莲壳', 10, 100)]
