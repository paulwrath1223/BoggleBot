
class Tile:
    def __init__(self, letter, modifier):
        # 0 = DL = Double Letter
        # 1 = TL = Triple Letter
        # 2 = DW = Double Word
        # 3 = TW = Triple Word

        self.letter = letter
        self.value = get_letter_points(letter)
        self.word_multiplier = 1
        match modifier:
            case 0:
                self.value = self.value * 2
            case 1:
                self.value = self.value * 3
            case 2:
                self.word_multiplier = self.word_multiplier * 2
            case 3:
                self.word_multiplier = self.word_multiplier * 3
            case _:
                raise Exception("modifier must be an int 0-3")



class board:
    def __init__(self):

def get_points(tile_array):
    global_mult = 1
    letter_sum = 0
    for tile in tile_array:
        global_mult = global_mult * tile.word_multiplier
        letter_sum += tile.value
    return letter_sum * global_mult

def get_letter_points(letter):
    return 1 # TODO
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
