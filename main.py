all_words = ["cat", "fat", "mogus"]  # TODO
board_x_dim = 4
board_y_dim = 4


class Tile:
    def __init__(self, x, y, letter, modifier=0):
        # 0 = no modifier
        # 1 = DL = Double Letter
        # 2 = TL = Triple Letter
        # 3 = DW = Double Word
        # 4 = TW = Triple Word
        self.x = x
        self.y = y
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

    def locate(self):
        return self.x, self.y


class Board:
    def __init__(self):
        self.tile_array = [[] * board_x_dim] * board_y_dim
        for y in range(board_y_dim):
            for x in range(board_x_dim):
                self.tile_array[y][x] = Tile(x, y, 'a')

    def set_tile(self, x, y, letter, modifier=0):
        self.tile_array[y][x] = Tile(x, y, letter, modifier)

    def get_tile(self, x, y):
        return self.tile_array[y][x]


def get_letter_points(letter):
    return 1  # TODO


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

    def get_next_letters(self, board_in):
        current_tile_coords = (self.tiles[len(self.tiles)]).locate()
        next_tiles = []
        next_coords = []
        for a in range(-1, 2):
            for b in range(-1, 2):
                next_coords.append((current_tile_coords[0]+a, current_tile_coords[1]+b))
        for tile in self.tiles:
            tile_coords = tile.locate()
            if tile_coords in next_coords:
                next_coords.remove(tile_coords)
        for coord in next_coords:
            next_tiles.append(board_in[coord[1]][coord[0]])




















