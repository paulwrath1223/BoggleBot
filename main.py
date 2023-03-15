all_words = ["cat", "fat", "mogus"]  # TODO


class Tile:
    def __init__(self, letter, modifier=0):
        # 0 = no modifier
        # 1 = DL = Double Letter
        # 2 = TL = Triple Letter
        # 3 = DW = Double Word
        # 4 = TW = Triple Word

        self.letter = letter
        self.value = get_letter_points(letter)
        self.word_multiplier = 1
        if modifier != 0:
            match modifier:
                case 1:
                    self.value = self.value * 2
                case 2:
                    self.value = self.value * 3
                case 3:
                    self.word_multiplier = self.word_multiplier * 2
                case 4:
                    self.word_multiplier = self.word_multiplier * 3
                case _:
                    raise Exception("modifier must be an int 0-4")


# class Board:
#     def __init__(self):
#         self.tile_array = [[Tile('a')] * 4] * 4


def get_letter_points(letter):
    return 1  # TODO


tile_array = [[Tile('a')] * 4] * 4


class Word:
    def __init__(self, tiles=None):
        if tiles is None:
            tiles = []
        self.tiles = tiles

    def get_points(self):
        global_mult = 1
        letter_sum = 0
        for tile in self.tiles:
            global_mult = global_mult * tile.word_multiplier
            letter_sum += tile.value
        return letter_sum * global_mult
