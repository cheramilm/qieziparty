# coding:utf-8
from block import *

game = QieziGame()
QieziGame.print_headers()
QieziGame.print_core_parameters()
game.start_player()
game.welcome_player()
while 1 == 1:
    try:
        game.start_game(blockTemplates)
    except SystemExit:
        print(splitter)
        again_answer = Utils.get_int_input("再来一局？%s：" % (Utils.choose(selects)))
        if again_answer != 1:
            print("欢迎下次再玩！")
            break
