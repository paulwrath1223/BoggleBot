# takes a text file of all words and changes 'qu' to 'q' also removes words with 'q' not followed by 'u'


def process_word_list():
    print("called process_word_list")
    completed_words = []
    with open('all_words.txt') as f:

        line = f.readline()
        while line:

            if len(line) > 1:
                if 'q' in line:
                    if "qu" in line:
                        completed_words.append(line.replace("qu", "q").replace("\n", ""))
                else:
                    completed_words.append(line.replace("\n", ""))
            line = f.readline()
        return completed_words
