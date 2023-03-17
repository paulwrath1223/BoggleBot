from colorama import Fore
import copy
from generate_word_list import process_word_list
import time

test_words = ["bi", "banister"]

board_x_dim = 4
board_y_dim = 4
alphabet = "abcdefghijklmnopqrstuvwyxz"



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
        self.letter_multiplier = 1
        self.word_multiplier = 1
        self.modifier = modifier
        if modifier != 0:
            match modifier:
                case 1:
                    self.letter_multiplier = self.letter_multiplier * 2
                case 2:
                    self.letter_multiplier = self.letter_multiplier * 3
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
    tile_array = [[Tile, Tile, Tile, Tile],
                  [Tile, Tile, Tile, Tile],
                  [Tile, Tile, Tile, Tile],
                  [Tile, Tile, Tile, Tile]]

    def __init__(self):
        self.solved_words = []

        # for y in range(board_y_dim):
        #     for x in range(board_x_dim):
        #         self.tile_array[y][x] = Tile(x, y, 'a')
        #         print(f"self.tile_array[{y}][{x}] = {self.tile_array[y][x]}")
        #         print(f"Tile({x}, {y}, 'a') = {Tile(x, y, 'a')}")

    def possible_words(self, all_words_list: [str]):
        tile_letters_as_string = self.get_all_letters()
        possible_word_list = []
        for word in all_words_list:
            if a_can_be_made_from_b(word, tile_letters_as_string):
                possible_word_list.append(word)
        return possible_word_list

    def print_board(self):
        # print(self.tile_array)
        for y in range(board_y_dim):
            for x in range(board_x_dim):
                # print(self.tile_array[y][x])
                current_tile = self.tile_array[y][x]
                # print(f"{x}, {y}: ", end="\t")
                match current_tile.modifier:
                    case 0:
                        print(Fore.LIGHTWHITE_EX + current_tile.letter, end=" ")
                    case 1:
                        print(Fore.LIGHTBLUE_EX + current_tile.letter, end=" ")
                    case 2:
                        print(Fore.LIGHTGREEN_EX + current_tile.letter, end=" ")
                    case 3:
                        print(Fore.LIGHTRED_EX + current_tile.letter, end=" ")
                    case 4:
                        print(Fore.LIGHTYELLOW_EX + current_tile.letter, end=" ")
                    case _:
                        raise Exception("modifier must be an int 0-4")
            print()

    def set_tile(self, x: int, y: int, letter: str, modifier: int = 0):
        temp_tile = Tile(x, y, letter, modifier)
        self.tile_array[y][x] = temp_tile
        # print(f"setting tile {x}, {y} to {temp_tile}")

    def get_tile(self, x: int, y: int):
        return self.tile_array[y][x]

    def get_all_letters(self):
        all_letters = ""
        for tile_rows in self.tile_array:
            for tile in tile_rows:
                all_letters += tile.letter
        return all_letters

    def add_word(self, word):
        current_word_as_string = word.get_word_as_string()
        current_word_points = word.get_points()
        for past_word in self.solved_words:
            if past_word.get_word_as_string() == current_word_as_string:
                if past_word.get_points() < current_word_points:
                    self.solved_words.remove(past_word)
                else:
                    return
        self.solved_words.append(copy.deepcopy(word))

    def solve(self, all_words_list: [str]):
        word_list = self.possible_words(all_words_list)
        for x in range(board_x_dim):
            for y in range(board_y_dim):
                current_tile = self.tile_array[y][x]
                current_letter = current_tile.letter
                current_word = Word([current_tile])
                valid_words = []
                for word in word_list:
                    if word[0] == current_letter:
                        valid_words.append(word)
                if len(valid_words) > 0:
                    # print(f"calling solve_tick with word {current_word} and valid words {valid_words}")
                    self.solve_tick(current_word, valid_words)
        # return self.solved_words
        return sorted(self.solved_words, key=lambda x1: x1.get_points(), reverse=True)

    def solve_tick(self, word, word_list: [str]):
        # print(f"solve_tick called with {word.get_word_as_string()}, {word_list}")
        # word = copy.deepcopy(word_ref)
        # word_list = copy.deepcopy(word_list_ref)
        word.check_word(self, word_list)
        next_tiles = word.get_next_letters(self)
        # print(f"solve_tick next tiles = {next_tiles}")
        if len(next_tiles) == 0:
            return
        for tile in next_tiles:
            # print(f"{word.get_word_as_string()} checking tile {tile}")
            current_letter = tile.letter
            potential_word_string = word.get_word_as_string() + current_letter
            # print(f"potential_word_string: {potential_word_string}")
            valid_words = []
            for possible_word in word_list:
                if len(possible_word) > len(word.tiles):
                    # print(f"possible_word[0:len(word.tiles)]: {possible_word[0:len(word.tiles)+1]}")
                    if possible_word[0:len(word.tiles) + 1] == potential_word_string:
                        valid_words.append(possible_word)
            # print(f"valid words with next letter \'{current_letter}\': {valid_words}")
            if len(valid_words) > 0:
                word.add_tile(tile)
                self.solve_tick(word, valid_words)
                word.back()
        return


def get_letter_points(letter):
    letter_values = ["atsiero", "lndu", "ygh", "bpmcf", "kv", "", "w", "x", "", "jzq"]
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
        length_bonus = 0
        if len(self.tiles) <= 2:
            return 1
        elif len(self.tiles) == 5:
            length_bonus = 3
        elif len(self.tiles) == 6:
            length_bonus = 6
        elif len(self.tiles) == 7:
            length_bonus = 10
        elif len(self.tiles) == 8:
            length_bonus = 15
        elif len(self.tiles) >= 9:
            length_bonus = 20

        global_mult = 1
        letter_sum = 0
        for tile in self.tiles:
            global_mult = global_mult * tile.word_multiplier
            letter_sum += get_letter_points(tile.letter) * tile.letter_multiplier
        # if self.get_word_as_string() == "banister":
        #     print(f"letter points: {letter_sum}\nlegth bonus: {length_bonus}\nmultiplier: {global_mult}")
        return length_bonus + letter_sum * global_mult

    def get_next_letters(self, board_in: Board):

        current_tile_coords = (self.tiles[len(self.tiles) - 1]).locate()
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
                next_tiles.append(board_in.get_tile(coord[0], coord[1]))

        next_tiles_as_string = ""
        for temp_tile in next_tiles:
            next_tiles_as_string = next_tiles_as_string + temp_tile.letter + ", "
        # print(f"get_next_letters({self.get_word_as_string()}, board) = {next_tiles_as_string}")
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

        if len(self.tiles) > 1:
            if current_word_as_string in word_list:
                board_in.add_word(self)
                # print(f"{current_word_as_string} is a valid word")
                return True
        # print(f"{current_word_as_string} is a not valid word")
        return False

    def back(self):
        self.tiles.pop(len(self.tiles) - 1)


def a_can_be_made_from_b(a: str, b: str):
    a_list = [0] * len(alphabet)
    for i in range(len(alphabet)):
        a_list[i] = a.count(alphabet[i])
    for j in range(len(alphabet)):
        if b.count(alphabet[j]) < a_list[j]:
            return False
    return True


main_board = Board()
main_board.set_tile(0, 0, 't', 0)
main_board.set_tile(0, 1, 'a', 2)
main_board.set_tile(0, 2, 's', 0)
main_board.set_tile(0, 3, 'w', 0)

main_board.set_tile(1, 0, 't', 0)
main_board.set_tile(1, 1, 'n', 4)
main_board.set_tile(1, 2, 't', 0)
main_board.set_tile(1, 3, 'f', 0)

main_board.set_tile(2, 0, 'p', 2)
main_board.set_tile(2, 1, 'e', 0)
main_board.set_tile(2, 2, 'i', 0)
main_board.set_tile(2, 3, 'a', 0)

main_board.set_tile(3, 0, 'r', 0)
main_board.set_tile(3, 1, 'a', 0)
main_board.set_tile(3, 2, 'l', 2)
main_board.set_tile(3, 3, 'y', 0)

main_board.print_board()
print()

all_words = process_word_list()

# tic = time.perf_counter()
# for i in range(1, 1000):
#     all_solved_words = main_board.solve(all_words)
#     print(f"finished {i} solves, averaging {((time.perf_counter() - tic)/i):0.4f} seconds each")

all_solved_words = main_board.solve(all_words)

print(Fore.LIGHTWHITE_EX + f"Found {len(all_solved_words)} words!\n")

for solved_word_1 in all_solved_words:
    print(solved_word_1)
