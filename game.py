import sys
import datetime
from person import *


class Game:
    player = None
    block = None
    startTime = 0
    round = 0

    @staticmethod
    def print_headers():
        Utils.print("%s茄子派对迷雾版%s%s" % (marker, version, marker))
        Utils.print("%s本游戏由茄子派对工作室荣誉出品%s" % (marker, marker))
        Utils.print(
            "%s抵制不良游戏 拒绝盗版游戏 \n%s注意自我保护 谨防受骗上当 \n%s适度游戏益脑 沉迷游戏伤身 \n%s合理安排时间 享受健康生活" % (center, center, center, center))
        Utils.print(splitter)

    @staticmethod
    def print_core_parameters():
        Utils.print(splitter)
        value = '爆击率：『{:.0%}』  基础准心：『{:.0%}』  等级准心差：『{:.0%}』  次数准心差：『{:.1%}』'.format(burstRate, initSight, levelSight,
                                                                                     attackTimeSight)
        Utils.print("系统核心参数\n%s" % value)

    def start_player(self):
        Utils.print(splitter)
        name = Utils.input("您的茄号：")
        self.player = Person(name, maxBlood, initKill, foot, hand, hair)

    def show_player(self):
        Utils.print("您当前的状态：")
        Utils.print(self.player)

    def welcome_player(self):
        Utils.print("欢迎进入茄子派对!!!!")
        self.show_player()

    def end(self, message):
        Utils.print("\n\n\n")
        Utils.print("%s%s%s" % (marker, message, marker))
        Utils.print(self.player)
        Utils.print("本局耗时一共『%d』分钟" % int((datetime.datetime.now() - self.startTime).seconds/60))
        sys.exit()

    @staticmethod
    def choose_blocks(message, array, chosen_message, fail_message):
        Utils.print(splitter)
        index = Utils.get_int_input(message % (Utils.choose(array, '\n')), 1)
        if 1 <= index <= len(array):
            Utils.print(chosen_message % (array[index - 1]))
            return array[index - 1]
        else:
            Utils.input(fail_message)
            sys.exit()

    def choose_object(self, obj, message, chosen_message, fail_message):
        self.show_player()
        answer = Utils.get_int_input(message % (str(obj), Utils.choose(selects)))
        if answer == 1:
            self.block.equipments.remove(obj)
            self.player.equip(obj, self.block)
            Utils.print(chosen_message % obj)
            self.show_player()
        else:
            self.player.position = obj.position
            Utils.print(fail_message % obj)

    def choose_fight(self, enemy, message, win_message, fail_message):
        self.show_player()
        answer = Utils.get_int_input(message % (
            str(enemy), "您的胜率：『%s』(仅供参考，回归大自然也正常啦^_^)" % (self.player.win_rate(enemy)), Utils.choose(fightSelects)))
        if answer != 2:
            if answer == 1:
                fight_result = self.player.fight(enemy)
            elif answer == 4:
                self.player.shot_one_and_run(enemy)
                self.player.position = enemy.position
                return
            else:
                fight_result = self.player.fight(enemy, 0)
            if fight_result == 1:
                Utils.print(win_message % enemy.name)
                self.block.enemies.remove(enemy)
            elif fight_result == 2:
                Utils.print("谁也奈何不了谁，不如暂时相忘于江湖吧！")
                self.player.position = self.player.position + 1
            else:
                self.end(fail_message % enemy.name)
                sys.exit()
        else:
            attacked = enemy.attack()
            self.player.attacked(attacked)
            Utils.print("您被『%s』发现并被攻击『%d』！" % (enemy.name, attacked))
            if self.player.died():
                self.end(fail_message % enemy.name)
            self.player.position = enemy.position

    def start_game(self, blocks):
        self.block = Game.choose_blocks("准备跳伞，请选择您降落的位置\n%s：", blocks, "您成功落地到：%s",
                                        "您掉落到未知世界\n您已回归大自然，等待发芽吧^_^")
        self.block.init()
        self.player.init_player()
        self.startTime = datetime.datetime.now()
        self.round = 0
        search_mode = 0
        while self.player.position < self.block.range:
            if len(self.block.enemies) == 0:
                self.end("敌人都已回归大自然，恭喜您提前吃瓜！")
                sys.exit()
            self.round = self.round + 1
            self.block.poison(self.player, self.round)
            if search_mode == 0:
                self.block.print_brief_info(self.player, self.round)
                Utils.print(splitter)
            if self.player.direction == 0:
                next_position = self.player.position + self.player.run()
                if self.block.exploredRange < next_position:
                    self.block.exploredRange = next_position
                target = self.block.next_target(self.player.position + 1, next_position)
            elif self.player.stay == 1:
                next_position = self.player.position
                target = self.block.next_target(self.player.position, next_position)
            else:
                next_position = self.player.position - self.player.run()
                if next_position < 0:
                    next_position = 0
                target = self.block.next_target(self.player.position - 1, next_position)
            if target is None:
                self.player.position = next_position
                if search_mode == 1 or search_mode == 2:
                    Utils.print('啥也没有，继续找，我就不信了！位置：『%d』' % self.player.position)
                    time.sleep(1)
                    continue
                else:
                    run_answer = Utils.get_int_input("跑了这么久啥都没看到，本茄来错片场了吗？%s：" % (Utils.choose(directions)))
                    if run_answer == 4:
                        search_mode = 1
                        self.player.stay = 0
                    elif run_answer == 5:
                        search_mode = 2
                        self.player.stay = 0
                    elif run_answer == 2:
                        self.player.direction = 1
                        self.player.stay = 0
                    elif run_answer == 1:
                        self.player.direction = 0
                        self.player.stay = 0
                    elif run_answer == 3:
                        self.player.stay = 1
                        Utils.input('这里风光不错，值得多看看。。。')
                    else:
                        search_mode = 1
                        self.player.stay = 0
            elif isinstance(target, Person):
                search_mode = 0
                self.choose_fight(target, "！！！前方发现一个敌人！！！\n%s\n%s\n是否要战斗 %s :", "成功打败敌人『%s』",
                                  "很遗憾，您被『%s』回归大自然了！")
            else:
                if search_mode == 2:
                    self.pick_better_equipment(target)
                    self.player.position = next_position
                    Utils.print('啥敌人也没有，继续找，我就不信了，位置：『%d』' % self.player.position)
                    time.sleep(1)
                    continue
                else:
                    if self.pick_better_equipment(target) == 1:
                        time.sleep(1)
                    elif isinstance(target, Medkit) and self.player.blood + target.value <= maxBlood:
                        self.player.blood = self.player.blood + target.value
                        self.block.equipments.remove(target)
                        Utils.print("不能浪费了，先补充下茄子吧！")
                        self.show_player()
                    else:
                        search_mode = 0
                        self.choose_object(target, "\n前方发现一个装备 %s\n是否替换现有装备 %s :", "成功获取装备：%s",
                                           "很遗憾，您错过了装备：%s")

            if self.player.position > self.block.range:
                self.player.position = self.block.range
        self.end("您真是跑毒高手啊，恭喜您吃瓜！")
        sys.exit()

    def pick_better_equipment(self, target):
        if self.player.is_better_equipment(target) == 1:
            self.block.equipments.remove(target)
            self.player.equip(target, self.block)
            Utils.print("发现更好装备：%s，自动替换现有装备" % target)
            return 1
        else:
            return 0
