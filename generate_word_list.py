
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
        return completed_words