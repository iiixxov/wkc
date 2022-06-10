class Crossword:
    def list_copy(self, field):
        new = list(field)
        for i in range(len(field)):
            new[i] = list(field[i])
        return new

    def insert(self, is_vertical, word, char_index, pos):
        sub = self.list_copy(self.f)
        sub_char_indexes = set(self.char_indexes)
        try:
            if is_vertical:
                sub[pos[0]][pos[1]] = word[char_index]
                sub_char_indexes.add((pos[0], pos[1], is_vertical))
                ind = char_index - 1
                for i in range(pos[0] - 1, pos[0] - char_index - 1, -1):
                    if sub[i][pos[1]] == ' ' and sub[i][pos[1] - 1] == ' ' and sub[i][pos[1] + 1] == ' ':
                        sub_char_indexes.add((i, pos[1], is_vertical))
                        sub[i][pos[1]] = word[ind]
                        ind -= 1
                    else:
                        return False
                ind = char_index + 1
                for i in range(pos[0] + 1, pos[0] + (len(word) - char_index)):
                    if sub[i][pos[1]] == ' ' and sub[i][pos[1] + 1] == ' ' and sub[i][pos[1] - 1] == ' ':
                        sub_char_indexes.add((i, pos[1], is_vertical))
                        sub[i][pos[1]] = word[ind]
                        ind += 1
                    else:
                        return False
            if not is_vertical:
                sub[pos[0]][pos[1]] = word[char_index]
                sub_char_indexes.add((pos[0], pos[1], is_vertical))
                ind = char_index - 1
                for i in range(pos[1] - 1, pos[1] - char_index - 1, -1):
                    if sub[pos[0]][i] == ' ' and sub[pos[0] + 1][i] == ' ' and sub[pos[0] - 1][i] == ' ':
                        sub_char_indexes.add((pos[0], i, is_vertical))
                        sub[pos[0]][i] = word[ind]
                        ind -= 1
                    else:
                        return False
                ind = char_index + 1
                for i in range(pos[1] + 1, pos[1] + (len(word) - char_index)):
                    if sub[pos[0]][i] == ' ' and sub[pos[0] - 1][i] == ' ' and sub[pos[0] + 1][i] == ' ':
                        sub_char_indexes.add((pos[0], i, is_vertical))
                        sub[pos[0]][i] = word[ind]
                        ind += 1
                    else:
                        return False
        except IndexError:
            return False
        self.char_indexes = set(sub_char_indexes)
        self.f = self.list_copy(sub)
        return True

    def word_loop(self):
        if self.word_start > len(self.words):
            return False
        for word in enumerate(self.words[self.word_start:]):
            # print(word, word_start)
            for char in enumerate(word[1][1:-1]):
                # print(char)
                for char_index in self.char_indexes:
                    # print(char, f[char_index[0]][char_index[1]], is_vertical)
                    if char[1] == self.f[char_index[0]][char_index[1]] and self.is_vertical != char_index[2]:
                        if self.insert(self.is_vertical, word[1][1:-1], char[0], (char_index[0], char_index[1])):
                            self.words.pop(word[0])
                            self.is_vertical = not self.is_vertical
                            self.word_start = 0
                            return True
        self.word_start += 1
        return True

    def __init__(self, size, words_input):
        self.char_indexes = set()
        self.f = [[' '] * size for _ in range(size)]
        self.words = sorted(list(map(lambda x: ' '+x+' ' , words_input)), key=len, reverse=True)
        self.insert(False, self.words[0][1:-1], len(self.words)//2, (size//2,size//2))
        self.words.pop(0)
        self.is_vertical = True
        self.word_start = 0
        while self.words:
            if not self.word_loop():
                self.not_fit = list(self.words)
                break
        self.table = self.list_copy(self.f)


