from colorama import Fore

all_words = ["cat", "fat", "mogus"]  # TODO
board_x_dim = 4
board_y_dim = 4
alphabet = "abcdefghijklmnopqrstuvwyxz"
letter_values = ["ATSIERO", "LNDU", "YGH", "BPMCF", "KV", "", "W", "X", "", "JZQ"]


class Tile:

    letter = None
    modifier = None
    x = None
    y = None

    def __init__(self, x: int = None, y: int = None, letter: str = None, modifier: int = 0):
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
        self.modifier = modifier
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

    def __str__(self):
        return self.letter + " at (" + str(self.x) + ", " + str(self.y) + ") with modifier: " + str(self.modifier)

    def locate(self):
        return self.x, self.y


class Board:

    def __init__(self):
        self.solved_words = []
        self.tile_array = [[Tile] * board_x_dim] * board_y_dim

        # for y in range(board_y_dim):
        #     for x in range(board_x_dim):
        #         self.tile_array[y][x] = Tile(x, y, 'a')
        #         print(f"self.tile_array[{y}][{x}] = {self.tile_array[y][x]}")
        #         print(f"Tile({x}, {y}, 'a') = {Tile(x, y, 'a')}")

    def print_board(self):
        # print(self.tile_array)
        for y in range(board_y_dim):
            for x in range(board_x_dim):
                # print(self.tile_array[y][x])
                current_tile = self.tile_array[y][x]
                # print(f"{x}, {y}: ", end="\t")
                match current_tile.modifier:
                    case 0:
                        print(current_tile.letter, end=" ")
                    case 1:
                        print(Fore.BLUE + current_tile.letter, end=" ")
                    case 2:
                        print(Fore.GREEN + current_tile.letter, end=" ")
                    case 3:
                        print(Fore.RED + current_tile.letter, end=" ")
                    case 4:
                        print(Fore.YELLOW + current_tile.letter, end=" ")
                    case _:
                        raise Exception("modifier must be an int 0-4")
            print()

    def set_tile(self, x: int, y: int, letter: str, modifier: int = 0):
        temp_tile = Tile(x, y, letter, modifier)
        self.tile_array[y][x] = temp_tile
        print(f"setting tile {x}, {y} to {temp_tile}")

    def get_tile(self, x: int, y: int):
        return self.tile_array[y][x]

    def get_all_letters(self):
        all_letters = ""
        for tile_rows in self.tile_array:
            for tile in tile_rows:
                all_letters += tile.letter
        return all_letters

    def add_word(self, word):
        self.solved_words.append(word)

    def solve(self, word_list: [str]):
        for x in range(board_x_dim):
            for y in range(board_y_dim):
                current_tile = self.tile_array[y][x]
                current_letter = current_tile.letter()
                current_word = Word([current_tile])
                valid_words = []
                for word in word_list:
                    if word[0] == current_letter:
                        valid_words += word
                self.solve_tick(current_word, valid_words)
        return sorted(self.solved_words, key=lambda x1: x1.get_points(), reverse=True)

    def solve_tick(self, word, word_list: [str]):
        word.check_word()
        next_tiles = word.get_next_letters(self)
        if len(next_tiles) == 0:
            return
        for tile in next_tiles:
            valid_words = []
            current_letter = tile.letter
            for word in word_list:
                if word[0] == current_letter:
                    valid_words += word
            if len(valid_words) == 0:
                return
            word.add_tile(tile)
            self.solve_tick(word, valid_words)
            return
        return


def get_letter_points(letter):
    for i in range(len(letter_values)):
        if letter in letter_values[i]:
            return i + 1
    return 1


class Word:
    def __init__(self, tiles: [Tile] = None):
        if tiles is None:
            tiles = []
        self.tiles = tiles

    def __str__(self):
        return str(self.get_points()) + " : " + self.get_word_as_string()

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def get_points(self):
        if len(self.tiles) <= 2:
            return 1
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
                next_coords.append((current_tile_coords[0] + a, current_tile_coords[1] + b))
        for tile in self.tiles:
            tile_coords = tile.locate()
            if tile_coords in next_coords:
                next_coords.remove(tile_coords)
        for coord in next_coords:
            if (0 <= coord[0] < board_y_dim) and (0 <= coord[1] < board_x_dim):
                next_tiles.append(board_in.get_tile(coord[1], coord[0]))
        return next_tiles

    def get_valid_next_words(self, word_list: [str]):
        current_word_as_string = self.get_word_as_string()
        valid_next_words = []
        word_length = len(current_word_as_string)
        for word in word_list:
            if word[0:word_length] == current_word_as_string:
                valid_next_words.append(word)
        return valid_next_words

    def get_word_as_string(self):
        current_word_as_string = ""
        for tile in self.tiles:
            current_word_as_string += tile.letter
        return current_word_as_string

    def check_word(self, board_in: Board, word_list: [str]):
        current_word_as_string = self.get_word_as_string()
        if current_word_as_string in word_list:
            board_in.add_word(self)
            return True
        return False

    def back_one_tile(self):
        self.tiles.pop(len(self.tiles))


def a_can_be_made_from_b(a: str, b: str):
    a_list = [0] * len(alphabet)
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


main_board = Board()
main_board.set_tile(0, 0, 'p', 0)
main_board.set_tile(0, 1, 't', 1)
main_board.set_tile(0, 2, 'v', 0)
main_board.set_tile(0, 3, 'p', 0)

main_board.set_tile(1, 0, 'i', 0)
main_board.set_tile(1, 1, 's', 0)
main_board.set_tile(1, 2, 'e', 0)
main_board.set_tile(1, 3, 'g', 0)

main_board.set_tile(2, 0, 't', 1)
main_board.set_tile(2, 1, 'r', 0)
main_board.set_tile(2, 2, 'i', 0)
main_board.set_tile(2, 3, 'n', 0)

main_board.set_tile(3, 0, 'm', 0)
main_board.set_tile(3, 1, 's', 0)
main_board.set_tile(3, 2, 'a', 3)
main_board.set_tile(3, 3, 'b', 0)

print(main_board.tile_array[1][2])

main_board.print_board()
