import copy
import operator
import sys
from person import *
from map import *
from utils import *


class Block:
    name = ''
    range = 0
    exploredRange = 0
    equipments = []
    enemies = []

    def __init__(self, name, new_range):
        self.name = name
        self.range = new_range

    def __str__(self):
        return "『%s(%d公里)』" % (self.name, self.range)

    @staticmethod
    def search(array, from_position, to_position):
        if to_position > from_position:
            for obj in array:
                if from_position <= obj.position <= to_position:
                    return obj
                elif obj.position > to_position:
                    return None
        else:
            for obj in reversed(array):
                if to_position <= obj.position <= from_position:
                    return obj
                elif obj.position < to_position:
                    return None

    def next_target(self, from_position, to_position):
        target = Block.search(self.equipments, from_position, to_position)
        target2 = Block.search(self.enemies, from_position, to_position)
        if target is None:
            return target2
        elif target2 is None:
            return target
        else:
            if to_position > from_position:
                if target.position > target2.position:
                    return target2
                else:
                    return target
            else:
                if target.position > target2.position:
                    return target
                else:
                    return target2

    def add_equipment(self, equipment, position):
        e_name = equipment.name
        if e_name != handName and e_name != footName and e_name != hairName and e_name != noneMedkitName:
            self.equipments.append(equipment)
            equipment.position = position

    @staticmethod
    def init_equipments(equipments, templates, times=1):
        for i in range(len(templates)):
            for j in range(i + times):
                equipments.append(copy.copy(templates[i]))

    def init(self):
        self.exploredRange = 0
        self.equipments.clear()
        self.enemies.clear()
        vehicles = []
        Block.init_equipments(vehicles, vehicleTemplates)
        weapons = []
        Block.init_equipments(weapons, weaponTemplates)
        helmets = []
        Block.init_equipments(helmets, helmetTemplates, 4)
        medkits = []
        Block.init_equipments(medkits, medkitTemplates)

        self.enemies = [
            Person('紫茄大王', randint(50, maxBlood), randint(2, 6), copy.copy(foot), Utils.random_item(weapons),
                   Utils.random_item(helmets)),
            Person('红茄骑士', randint(20, maxBlood), randint(1, 5), copy.copy(foot), Utils.random_item(weapons),
                   Utils.random_item(helmets)),
            Person('绿茄剑士', randint(10, maxBlood), randint(0, 4), copy.copy(foot), Utils.random_item(weapons),
                   Utils.random_item(helmets)),
            Person('白茄士兵', randint(10, maxBlood), randint(0, 3), copy.copy(foot), Utils.random_item(weapons),
                   Utils.random_item(helmets)),
            Person('圆茄巨人', randint(10, maxBlood), randint(0, 3), copy.copy(foot), Utils.random_item(weapons),
                   Utils.random_item(helmets)),
            Person('矮茄娃娃', randint(10, maxBlood), randint(0, 3), copy.copy(foot), Utils.random_item(weapons),
                   Utils.random_item(helmets))]
        for index in range(5):
            self.enemies.append(
                Person('菜茄%d号' % (index + 1), randint(1, maxBlood / 2), randint(0, 1), copy.copy(foot), copy.copy(hand),
                       copy.copy(hair)))
        for index in range(5 - int(self.range / 200)):
            Utils.random_item(self.enemies)

        self.equipments.extend(vehicles)
        self.equipments.extend(weapons)
        self.equipments.extend(helmets)
        self.equipments.extend(medkits)
        for equipment in self.equipments:
            equipment.position = randint(1, self.range)

        for enemy in self.enemies:
            enemy.position = randint(1, self.range)
        self.sort()

    def sort(self):
        sorter = operator.attrgetter('position')
        self.equipments.sort(key=sorter)
        self.enemies.sort(key=sorter)

    def print_brief_info(self, current_player, current_round, open_all = 0):
        Utils.print(splitter)
        Utils.print("区域：『%s』\t您的位置『%d』/%d，剩余装备数量：『%d』\t剩余玩家数量：『%d』" % (
            self.name, current_player.position, self.range, len(self.equipments),
            len(self.enemies)))
        Map.print_map(self, current_player, current_round, open_all)

    def poison(self, current_player, current_round):
        self.enemies.append(current_player)
        area_size = self.range / areas
        max_poison = int(current_round / poisonRound)
        for enemy in self.enemies:
            area_index = int(enemy.position / area_size)
            poison_level = max_poison - area_index
            if poison_level > len(poisonStatus) - 1:
                poison_level = len(poisonStatus) - 1
            elif poison_level < 0:
                poison_level = 0
            enemy.poison(poisonValues[poison_level])
            if enemy.died():
                if enemy == current_player:
                    Utils.print("很遗憾，您跑毒失败，回归大自然。。。")
                    sys.exit()
                else:
                    Utils.input("玩家『%s』被毒杀，回归大自然。。。" % enemy.name)
                    self.enemies.remove(enemy)

        self.enemies.remove(current_player)


blockTemplates = [Block('可可西里*', 1000), Block('喀纳斯', 800), Block('神农架', 600), Block('西双版纳', 400), Block('卧龙', 200)]
