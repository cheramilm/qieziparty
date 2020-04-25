from constants import *
from random import *


class Weapon:
    name = ''
    attackValue = 0
    leftTimes = 0
    totalTimes = 0
    position = 0

    def __init__(self, name, attack_value, left_times):
        self.name = name
        self.attackValue = attack_value
        self.leftTimes = left_times
        self.totalTimes = left_times

    def __str__(self):
        return "『%s』， 攻击力：『%d』，剩余攻击次数：『%d』" % (self.name, self.attackValue, self.leftTimes)

    def better_than_me(self, another):
        if another.attackValue >= self.attackValue and another.leftTimes >= self.leftTimes:
            return 1
        elif another.attackValue * another.leftTimes > self.attackValue * self.leftTimes * 2:
            return 1
        elif another.attackValue > self.attackValue == handAttack:
            return 1
        else:
            return 0

    def single_attack(self):
        return self.attackValue * (self.leftTimes / self.totalTimes) + 0.1

    def to_hand(self):
        self.name = handName
        self.attackValue = handAttack
        self.leftTimes = handTimes
        self.totalTimes = handTimes

    @staticmethod
    def burst(value):
        if random() <= burstRate:
            print("叮！棍子暴走了，小心了！！！")
            return value * 2
        else:
            return value

    def attack(self):
        if self.leftTimes > 0:
            self.leftTimes = self.leftTimes - 1
            init_attack = self.attackValue
            if self.leftTimes == 0:
                self.to_hand()
            return self.burst(init_attack)
        else:
            if self.name != handName:
                print("『%s』剩余攻击力为『0』，自动丢弃！" % self.name)
                self.to_hand()
                return self.burst(self.attackValue)
            else:
                if random() <= burstRate:
                    print("有一根茄棍获得神农垂青，突然暴起了！！！")
                    return handBurstAttack
                else:
                    print("茄棍过于疲劳，无力攻击，等神农垂青吧，好悲哀啊。。。")
                    return 0


hand = Weapon(handName, handAttack, handTimes)
weaponTemplates = [Weapon('檀木棍', 130, 5), Weapon('梨木棍', 25, 40), Weapon('柚木棍', 22, 40), Weapon('桦木棍', 20, 35),
                   Weapon('椴木棍', 15, 8), Weapon('树枝', 2, 50)]
