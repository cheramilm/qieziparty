# coding:utf-8
import copy
import sys
import operator
import time
from random import *

version = "2020.04.21内测版"
marker = "=================================="
center = "\t\t\t\t    "
splitter = '=================================================================================================='
mapHeader = '________________________________________________________________________________________________'
mapFooter = '￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣'
selects = ['是', '否*']
fightSelects = ['是', '否*', '决一胜负']
directions = ['前进', '后退', '原地休息', '全力搜索*', '全力搜索敌人']
maxBlood = 100
initKill = 0
warningBlood = 50
burstRate = 0.05
initSight = 0.7
levelSight = 0.05
attackTimeSight = 0.001
footName = '茄根'
footSpeed = 5
footTimes = 100
handName = '茄棍'
handAttack = 1
handBurstAttack = 5
handTimes = 100
hairName = '茄蒂'
noneMedkitName = '无'
areas = 40
levels = ['青铜', '白银', '黄金', '铂金', '钻石', '王者', '战神']
numbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四']
poisonStatus = ['', '', '', '', '', '', '', '', '', '']
player = None


class QieziGame:
    @staticmethod
    def print_headers():
        print("%s茄子派对迷雾版%s%s" % (marker, version, marker))
        print("%s本游戏由茄子派对工作室荣誉出品%s" % (marker, marker))
        print(
            "%s抵制不良游戏 拒绝盗版游戏 \n%s注意自我保护 谨防受骗上当 \n%s适度游戏益脑 沉迷游戏伤身 \n%s合理安排时间 享受健康生活" % (center, center, center, center))
        print(splitter)

    @staticmethod
    def print_core_parameters():
        print(splitter)
        value = '爆击率：『{:.0%}』  基础准心：『{:.0%}』  等级准心差：『{:.0%}』  次数准心差：『{:.1%}』'.format(burstRate, initSight, levelSight,
                                                                                     attackTimeSight)
        print("系统核心参数\n%s" % value)

    @staticmethod
    def start_player():
        print(splitter)
        name = input("您的茄号：")
        global player
        player = Person(name, maxBlood, initKill, foot, hand, hair)

    @staticmethod
    def show_player():
        print("您当前的状态：")
        global player
        print(player)

    @staticmethod
    def welcome_player():
        print("欢迎进入茄子派对!!!!")
        QieziGame.show_player()

    @staticmethod
    def win(person, message):
        print("\n\n\n")
        print("%s%s%s" % (marker, message, marker))
        print(person)

    @staticmethod
    def choose_blocks(message, array, chosen_message, fail_message):
        print(splitter)
        index = Utils.get_int_input(message % (Utils.choose(array, '\n')), 1)
        if 1 <= index <= len(array):
            print(chosen_message % (array[index - 1]))
            return array[index - 1]
        else:
            input(fail_message)
            sys.exit()


class Utils:
    @staticmethod
    def choose(array, separator=' '):
        result = ''
        for index in range(len(array)):
            result = result + str(index + 1) + '. ' + str(array[index]) + separator
        return result

    @staticmethod
    def get_int_input(message, default_value=0):
        answer = input(message)
        try:
            return int(answer)
        except ValueError:
            return default_value

    @staticmethod
    def random_item(array):
        if len(array) - 1 < 0:
            return None
        index = randint(0, len(array) - 1)
        obj = array[index]
        del array[index]
        return obj


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
                print("『%s』剩余次数为『0』，自动丢弃！" % self.name)
                self.to_foot()
                return self.speed
            else:
                print("茄根已经不能支撑您壮硕的娇躯，爬着走吧！！！")
                return 1


foot = Vehicle(footName, footSpeed, footTimes)
vehicleTemplates = [Vehicle('西瓜皮', 70, 10), Vehicle('橘子皮', 50, 5), Vehicle('香蕉皮', 30, 10), Vehicle('榴莲壳', 10, 100)]


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


class Person:
    name = ''
    blood = 100
    kill = 0
    weapon = None
    helmet = None
    vehicle = None
    medkit = noneMedkit
    level = ''
    attackTimes = 0
    position = 0
    direction = 0

    def __init__(self, name, blood, kill, vehicle=None, weapon=None, helmet=None, medkit=noneMedkit):
        self.name = name
        self.blood = blood
        self.kill = kill
        self.weapon = weapon
        self.helmet = helmet
        self.vehicle = vehicle
        self.medkit = medkit
        self.set_level()

    def __str__(self):
        return "茄号：『%s』 茄汁：『%d』 等级：『%s』 准心：『%s』\n皮子：%s\n棍子：%s\n盔子：%s\n肥料：%s" % (
            self.name, self.blood, self.level, '{:.1%}'.format(self.sight()), self.vehicle, self.weapon, self.helmet,
            self.medkit)

    def init_player(self):
        self.blood = maxBlood
        self.kill = initKill
        self.vehicle = foot
        self.weapon = hand
        self.helmet = hair
        self.attackTimes = 0
        self.position = 0
        self.direction = 0
        self.set_level()

    def win_rate(self, enemy):
        player_total_blood = self.total_blood()
        enemy_total_blood = enemy.total_blood()
        player_sight = self.sight()
        enemy_sight = enemy.sight()
        kill_enemy_times = enemy_total_blood / self.single_attack() + 0.01
        killed_times = player_total_blood / enemy.single_attack()
        return format(killed_times / kill_enemy_times / (enemy_sight / player_sight), '.0%')

    def is_better_equipment(self, equipment):
        if isinstance(equipment, Vehicle):
            return self.vehicle.better_than_me(equipment)
        elif isinstance(equipment, Weapon):
            return self.weapon.better_than_me(equipment)
        elif isinstance(equipment, Helmet):
            return self.helmet.better_than_me(equipment)
        elif isinstance(equipment, Medkit):
            return self.medkit.better_than_me(equipment)
        else:
            return 0

    def equip(self, equipment, target_block):
        self.position = equipment.position
        equipment.position = -1
        if isinstance(equipment, Vehicle):
            target_block.add_equipment(self.vehicle, self.position)
            self.vehicle = equipment
        elif isinstance(equipment, Weapon):
            target_block.add_equipment(self.weapon, self.position)
            player.weapon = equipment
        elif isinstance(equipment, Helmet):
            target_block.add_equipment(self.helmet, self.position)
            player.helmet = equipment
        elif isinstance(equipment, Medkit):
            target_block.add_equipment(self.medkit, self.position)
            player.medkit = equipment
        else:
            input("您是神农下凡吗？可惜服务器出bug了。。。")

    def set_level(self):
        if self.kill < len(levels):
            self.level = levels[self.kill]
        else:
            self.level = levels[len(levels) - 1]

    def add_kill(self):
        self.kill = self.kill + 1
        self.set_level()

    def sight(self):
        total_sight = self.kill * levelSight + self.attackTimes * attackTimeSight + initSight
        if total_sight > 1:
            return 1
        else:
            return total_sight

    def total_blood(self):
        init_total_blood = self.blood + self.helmet.leftValue + self.medkit.value
        if init_total_blood < 0:
            init_total_blood = 0
        return init_total_blood

    def total_attack(self):
        return self.weapon.leftTimes * self.weapon.attackValue + handTimes

    def single_attack(self):
        return self.weapon.single_attack() * self.sight()

    def run(self):
        return self.vehicle.run()

    def attack(self):
        init_attack = self.weapon.attack()
        current_sight = random()
        self.attackTimes = self.attackTimes + 1
        if self.sight() >= current_sight:
            return init_attack
        else:
            print("怎么回事，竟然打偏了，是等级太低还是风？一定是风太大了！！！")
            return 0

    def attacked(self, value):
        attack_left = self.helmet.protect(value)
        self.blood = self.blood - attack_left

    def healing(self):
        if self.blood < warningBlood and self.medkit != noneMedkit:
            answer = Utils.get_int_input("您当前茄汁『%d』不足，有一个肥料：%s，是否使用：%s" % (self.blood, str(self.medkit), Utils.choose(selects)))
            if answer == 1:
                self.blood = self.blood + self.medkit.value
                self.medkit = noneMedkit
                if self.blood > maxBlood:
                    self.blood = maxBlood

    def fight(self, enemy, confirm=1):
        print("您总茄汁：『%d』，『%s』总茄汁：『%d』" % (self.total_blood(), enemy.name, enemy.total_blood()))
        self.healing()
        fight_times = 1
        while self.blood > 0 and enemy.blood > 0:
            if confirm == 1:
                time.sleep(1)
            self.healing()
            if confirm == 1 and fight_times % 10 == 0:
                answer = Utils.get_int_input("又打了10个来回了，还继续吗？%s：" % (Utils.choose(fightSelects)))
                if answer == 2:
                    return 2
                elif answer == 3:
                    confirm = 0
            fight_times = fight_times + 1
            attacked = self.attack()
            enemy.attacked(attacked)
            print("您攻击了『%s』，攻击力『%d』，对方剩余总茄汁：『%d』" % (enemy.name, attacked, enemy.total_blood()))
            if enemy.blood <= 0:
                self.add_kill()
                print("您用『%d』招击杀了对手，『%d』杀！！！" % (fight_times, self.kill))
                return 1
            attacked = enemy.attack()
            self.attacked(attacked)
            print("您被『%s』攻击了，攻击力『%d』，您剩余总茄汁：『%d』" % (enemy.name, attacked, self.total_blood()))
            if self.blood <= 0:
                enemy.add_kill()
                return 0


class Block:
    name = ''
    range = 0
    exploredRange = 0
    equipments = []
    enemies = []
    player = None

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

    def choose_object(self, obj, message, chosen_message, fail_message):
        QieziGame.show_player()
        answer = Utils.get_int_input(message % (str(obj), Utils.choose(selects)))
        if answer == 1:
            self.equipments.remove(obj)
            self.player.equip(obj, self)
            print(chosen_message % obj)
            QieziGame.show_player()
        else:
            self.player.position = obj.position
            print(fail_message % obj)

    def choose_fight(self, enemy, message, win_message, fail_message):
        QieziGame.show_player()
        answer = Utils.get_int_input(message % (
            str(enemy), "您的胜率：『%s』(仅供参考，回归大自然也正常啦^_^)" % (self.player.win_rate(enemy)), Utils.choose(fightSelects)))
        if answer == 1 or answer == 3:
            if answer == 1:
                fight_result = self.player.fight(enemy)
            else:
                fight_result = self.player.fight(enemy, 0)
            if fight_result == 1:
                print(win_message % enemy.name)
                self.enemies.remove(enemy)
            elif fight_result == 2:
                print("谁也奈何不了谁，不如暂时相忘于江湖吧！")
                self.player.position = self.player.position + 1
            else:
                print(fail_message % enemy.name)
                sys.exit()
        else:
            attacked = enemy.attack()
            self.player.attacked(attacked)
            print("您被『%s』发现并被攻击『%d』！" % (enemy.name, attacked))
            if self.player.blood <= 0:
                print(fail_message % enemy.name)
                sys.exit()
            self.player.position = enemy.position

    def add_equipment(self, equipment, position):
        e_name = equipment.name
        if e_name != handName and e_name != footName and e_name != hairName and e_name != noneMedkitName:
            self.equipments.append(equipment)
            equipment.position = position

    @staticmethod
    def init_equipments(equipments, templates):
        for i in range(len(templates)):
            for j in range(i + 1):
                equipments.append(copy.copy(templates[i]))

    def init(self):
        self.equipments.clear()
        self.enemies.clear()
        vehicles = []
        Block.init_equipments(vehicles, vehicleTemplates)
        weapons = []
        Block.init_equipments(weapons, weaponTemplates)
        helmets = []
        Block.init_equipments(helmets, helmetTemplates)
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


blocks = [Block('可可西里*', 1000), Block('喀纳斯', 800), Block('神农架', 600), Block('西双版纳', 400), Block('卧龙', 200)]


def print_brief_info(current_block, current_player):
    print(splitter)
    print("区域：『%s』\t您的位置『%d』/%d，剩余装备数量：『%d』\t剩余玩家数量：『%d』" % (
        current_block.name, current_player.position, current_block.range, len(current_block.equipments),
        len(current_block.enemies)))
    Map.print_map(current_block, current_player)


class Map:
    @staticmethod
    def build_map(line_map, index, position, value):
        position = position + 1
        if len(line_map[index]) - 1 == position:
            line_map[index][position] = '多'
            return
        for i in range(len(line_map[index]), position):
            line_map[index].append('　')
        line_map[index].append(value)

    @staticmethod
    def print_map(current_block, current_player):
        print(mapHeader)
        line_map = [['|'], ['|'], ['|'], ['|'], ['|'], ['|']]
        current_block.enemies.append(current_player)
        current_block.sort()
        area_size = current_block.range / areas
        for enemy in current_block.enemies:
            area_index = int(enemy.position / area_size)
            Map.build_map(line_map, 0, area_index, enemy.name[0:1])
        Map.build_map(line_map, 0, 41, '\t 『茄』|')
        print(''.join(line_map[0]))
        current_block.enemies.remove(current_player)
        for equipment in current_block.equipments:
            area_index = int(equipment.position / area_size)
            if isinstance(equipment, Vehicle):
                Map.build_map(line_map, 1, area_index, equipment.name[0:1])
            elif isinstance(equipment, Weapon):
                Map.build_map(line_map, 2, area_index, equipment.name[0:1])
            elif isinstance(equipment, Helmet):
                Map.build_map(line_map, 3, area_index, equipment.name[0:1])
            elif isinstance(equipment, Medkit):
                Map.build_map(line_map, 4, area_index, equipment.name[0:1])
        Map.build_map(line_map, 1, 41, '\t 『皮』|')
        Map.build_map(line_map, 2, 41, '\t 『棍』|')
        Map.build_map(line_map, 3, 41, '\t 『盔』|')
        Map.build_map(line_map, 4, 41, '\t 『肥』|')
        Map.build_map(line_map, 5, 41, '\t 『毒』|')
        print(''.join(line_map[1]))
        print(''.join(line_map[2]))
        print(''.join(line_map[3]))
        print(''.join(line_map[4]))
        print(''.join(line_map[5]))
        print(mapFooter)


def start_game(person):
    current_block = QieziGame.choose_blocks("准备跳伞，请选择您降落的位置\n%s：", blocks, "您成功落地到：%s", "您掉落到未知世界\n您已回归大自然，等待发芽吧^_^")
    current_block.init()
    person.init_player()
    current_block.player = person
    search_mode = 0
    while person.position < current_block.range:
        if len(current_block.enemies) == 0:
            QieziGame.win(person, "敌人都已回归大自然，恭喜您提前吃瓜！")
            sys.exit()
        if search_mode == 0:
            print_brief_info(current_block, person)
            print(splitter)
        if person.direction == 0:
            next_position = person.position + person.run()
            if current_block.exploredRange < next_position:
                current_block.exploredRange = next_position
            target = current_block.next_target(person.position + 1, next_position)
        else:
            next_position = person.position - person.run()
            if next_position < 0:
                next_position = 0
            target = current_block.next_target(person.position - 1, next_position)
        if target is None:
            person.position = next_position
            if search_mode == 1 or search_mode == 2:
                print('啥也没有，继续找，我就不信了！位置：『%d』' % person.position)
                continue
            else:
                run_answer = Utils.get_int_input("跑了这么久啥都没看到，本茄来错片场了吗？%s：" % (Utils.choose(directions)))
                if run_answer == 4:
                    search_mode = 1
                elif run_answer == 5:
                    search_mode = 2
                elif run_answer == 2:
                    person.direction = 1
                elif run_answer == 1:
                    person.direction = 0
                elif run_answer == 3:
                    input('这里风光不错，值得多看看。。。')
                else:
                    search_mode = 1
        elif isinstance(target, Person):
            search_mode = 0
            current_block.choose_fight(target, "！！！前方发现一个敌人！！！\n%s\n%s\n是否要战斗 %s :", "成功打败敌人『%s』", "很遗憾，您被『%s』回归大自然了！")
        else:
            if search_mode == 2:
                person.position = next_position
                print('啥敌人也没有，继续找，我就不信了，位置：『%d』' % person.position)
                continue
            else:
                if person.is_better_equipment(target) == 1:
                    current_block.equipments.remove(target)
                    person.equip(target, current_block)
                    print("发现更好装备：%s，自动替换现有装备" % target)
                else:
                    search_mode = 0
                    current_block.choose_object(target, "\n前方发现一个装备 %s\n是否替换现有装备 %s :", "成功获取装备：%s", "很遗憾，您错过了装备：%s")

        if person.position > current_block.range:
            person.position = current_block.range
    QieziGame.win(person, "您真是跑毒高手啊，恭喜您吃瓜！")
    sys.exit()


QieziGame.print_headers()
QieziGame.print_core_parameters()
QieziGame.start_player()
QieziGame.welcome_player()
while 1 == 1:
    try:
        # noinspection PyTypeChecker
        start_game(player)
    except SystemExit:
        print(splitter)
        again_answer = Utils.get_int_input("再来一局？%s：" % (Utils.choose(selects)))
        if again_answer != 1:
            print("欢迎下次再玩！")
            break
