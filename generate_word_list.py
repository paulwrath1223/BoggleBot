# takes a text file of all words and changes 'qu' to 'q' also removes words with 'q' not followed by 'u'


def process_word_list():
    completed_words = []
    with open('all_scrabble_words.txt') as f:
        line = f.readline()
        while line:
            if len(line) > 1:
                if 'q' in line:
                    if "qu" in line:
                        completed_words.append(line.replace("qu", "q").replace("\n", "").lower())
                else:
                    completed_words.append(line.replace("\n", "").lower())
            line = f.readline()
        completed_words.sort()
        return completed_words


def process_and_save_word_list():
    completed_words = []
    with open('all_scrabble_words.txt') as f:
        line = f.readline()
        while line:
            if len(line) > 1:
                if 'q' in line:
                    if "qu" in line:
                        completed_words.append(line.replace("qu", "q").replace("\n", "").lower())
                else:
                    completed_words.append(line.replace("\n", "").lower())
            line = f.readline()
    with open('formatted_scrabble_words.txt', 'w') as f:
        f.write('\n'.join(completed_words))
