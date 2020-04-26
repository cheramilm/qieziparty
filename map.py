from medkit import *
from vehicle import *
from weapon import *
from helmet import *


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
    def print_map(current_block, current_player, current_round):
        Utils.print(mapHeader)
        line_map = [['|'], ['|'], ['|'], ['|'], ['|'], ['|']]
        current_block.enemies.append(current_player)
        current_block.sort()
        area_size = current_block.range / areas
        for enemy in current_block.enemies:
            if enemy.position > current_block.exploredRange:
                break
            area_index = int(enemy.position / area_size)
            Map.build_map(line_map, 0, area_index, enemy.name[0:1])
        Map.build_map(line_map, 0, 41, '\t 『茄』|')
        current_block.enemies.remove(current_player)
        Utils.print(''.join(line_map[0]))
        for equipment in current_block.equipments:
            if equipment.position > current_block.exploredRange:
                break
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
        max_poison = int(current_round / poisonRound)
        for index in range(areas):
            poison_level = max_poison - index
            if poison_level > len(poisonStatus) - 1:
                poison_level = len(poisonStatus) - 1
            elif poison_level < 0:
                poison_level = 0
            Map.build_map(line_map, 5, index, poisonStatus[poison_level])

        Map.build_map(line_map, 5, 41, '\t 『毒』|')
        Utils.print(''.join(line_map[1]))
        Utils.print(''.join(line_map[2]))
        Utils.print(''.join(line_map[3]))
        Utils.print(''.join(line_map[4]))
        Utils.print(''.join(line_map[5]))
        Utils.print(mapFooter)
