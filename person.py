from utils import *
from medkit import *
from vehicle import *
from weapon import *
from helmet import *
import time

player = None


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
            self.weapon = equipment
        elif isinstance(equipment, Helmet):
            target_block.add_equipment(self.helmet, self.position)
            self.helmet = equipment
        elif isinstance(equipment, Medkit):
            target_block.add_equipment(self.medkit, self.position)
            self.medkit = equipment
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
            answer = Utils.get_int_input(
                "您当前茄汁『%d』不足，有一个肥料：%s，是否使用：%s" % (self.blood, str(self.medkit), Utils.choose(selects)))
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
