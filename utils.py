from random import *


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
