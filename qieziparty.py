from block import *
from game import *
from utils import *

game = Game()
game.print_headers()
game.print_core_parameters()
game.start_player()
game.welcome_player()
while 1 == 1:
    try:
        game.start_game(blockTemplates)
    except SystemExit:
        Utils.print(splitter)
        again_answer = Utils.get_int_input("再来一局？%s：" % (Utils.choose(selects)))
        if again_answer != 1:
            Utils.print("欢迎下次再玩！")
            break
