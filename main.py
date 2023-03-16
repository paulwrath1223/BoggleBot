all_words = ["cat", "fat", "mogus"]  # TODO
board_x_dim = 4
board_y_dim = 4
alphabet = "abcdefghijklmnopqrstuvwyxz"
letter_values = ["ATSIERO", "LNDU", "YGH", "BPMCF", "KV", "", "W", "X", "", "JZQ"]


class Tile:
    def __init__(self, x: int, y: int, letter: str, modifier: int = 0):
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
        self.valid_words = []
        self.tile_array = [[] * board_x_dim] * board_y_dim
        for y in range(board_y_dim):
            for x in range(board_x_dim):
                self.tile_array[y][x] = Tile(x, y, 'a')

    def set_tile(self, x: int, y: int, letter: str, modifier: int = 0):
        self.tile_array[y][x] = Tile(x, y, letter, modifier)

    def get_tile(self, x: int, y: int):
        return self.tile_array[y][x]

    def get_all_letters(self):
        all_letters = ""
        for tile_rows in self.tile_array:
            for tile in tile_rows:
                all_letters += tile.letter
        return all_letters

    def add_word(self, word):
        self.valid_words.append(word)


def get_letter_points(letter):
    for i in range(len(letter_values)):
        if letter in letter_values[i]:
            return i+1
    return 1


class Word:
    def __init__(self, tiles=None):
        if tiles is None:
            tiles = []
        self.tiles = tiles

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def get_points(self):
        global_mult = 1
        letter_sum = 0
        for tile in self.tiles:
            global_mult = global_mult * tile.word_multiplier
            letter_sum += tile.value
        return letter_sum * global_mult

    def get_next_letters(self, board_in: Board):
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
            if (0 <= coord[0] < board_y_dim) and (0 <= coord[1] < board_x_dim):
                next_tiles.append(board_in.get_tile(coord[1], coord[0]))
        return next_tiles

    def get_valid_next_words(self, word_list: [str]):
        current_word_as_string = ""
        valid_next_words = []
        for tile in self.tiles:
            current_word_as_string += tile.letter
        word_length = len(current_word_as_string)
        for word in word_list:
            if word[0:word_length] == current_word_as_string:
                valid_next_words.append(word)
        return valid_next_words

    def check_word(self, board_in: Board, word_list: [str]):
        current_word_as_string = ""
        for tile in self.tiles:
            current_word_as_string += tile.letter
        if current_word_as_string in word_list:
            board_in.add_word(self)
            return True
        return False


def a_can_be_made_from_b(a: str, b: str):
    a_list = [0]*len(alphabet)
    for i in range(len(alphabet)):
        a_list[i] = a.count(alphabet[i])
    for j in range(len(alphabet)):
        if b.count(alphabet[j]) < a_list[j]:
            return False
    return True


def possible_words(board_in: Board):
    tile_letters_as_string = board_in.get_all_letters()
    possible_word_list = []
    for word in all_words:
        if a_can_be_made_from_b(word, tile_letters_as_string):
            possible_word_list.append(word)
    return possible_word_list











