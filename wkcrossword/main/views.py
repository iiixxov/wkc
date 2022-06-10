import wikipedia
wikipedia.set_lang("ru")
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
                for i in range(pos[0] - 1, pos[0] - char_index - 2, -1):
                    if sub[i][pos[1]] == ' ' and sub[i][pos[1] - 1] == ' ' and sub[i][pos[1] + 1] == ' ':
                        sub_char_indexes.add((i, pos[1], is_vertical))
                        sub[i][pos[1]] = word[ind]
                        ind -= 1
                        if i == pos[0] - char_index - 1:
                            sub[i][pos[1]] = self.n
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
                for i in range(pos[1] - 1, pos[1] - char_index - 2, -1):
                    if sub[pos[0]][i] == ' ' and sub[pos[0] + 1][i] == ' ' and sub[pos[0] - 1][i] == ' ':
                        sub_char_indexes.add((pos[0], i, is_vertical))
                        sub[pos[0]][i] = word[ind]
                        ind -= 1
                        if i == pos[1] - char_index - 1:
                            sub[pos[0]][i] = self.n
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
            for char in enumerate(word[1]):
                # print(char)
                for char_index in self.char_indexes:
                    # print(char, f[char_index[0]][char_index[1]], is_vertical)
                    if char[1] == self.f[char_index[0]][char_index[1]]:
                        if self.insert(not char_index[2], word[1], char[0], (char_index[0], char_index[1])):
                            self.n_words.append(str(self.n)+'. ' + word[1].capitalize())
                            self.n += 1
                            self.words.pop(word[0])
                            self.word_start = 0
                            return True
        self.word_start += 1
        return True

    def __init__(self, size, words_input):
        self.char_indexes = set()
        self.n_words = []
        self.f = [[' '] * size for _ in range(size)]
        self.words = sorted(words_input, key=len, reverse=True)
        self.n = 1
        self.insert(False, self.words[0], len(self.words[0])//2, (size//2,size//2))
        self.n_words.append(str(self.n)+'. '+self.words[0].capitalize())
        self.n = 2
        self.words.pop(0)
        self.word_start = 0
        self.not_fit = []
        while self.words:
            if not self.word_loop():
                self.not_fit = list(self.words)
                break
        self.table = self.list_copy(self.f)
###############################
from django.shortcuts import render
from django.http import HttpResponse
from .forms import Words_input
###############################
# Create your views here.
def index(request):
    form = Words_input
    if request.POST:
        words = request.POST['words'].split()
        crossword = Crossword(int(request.POST['size']), words)
        words = crossword.n_words
        words = list(map(lambda x: [x], words))
        print(words)
        if request.POST['difinition'] == '2':
            for i in range(len(words)):
                for word in wikipedia.search(words[i][0][3:])[:4]:
                    try:
                        difinition = wikipedia.summary(word).replace('\n', '')
                        words[i].append(difinition[difinition.find('—')+1:])
                    except:
                        pass
        elif request.POST['difinition'] == '1':
            for i in range(len(words)):
                ind = 0
                flag = True
                while flag:
                    try:
                        difinition = wikipedia.summary(wikipedia.search(words[i][0][3:])[ind]).replace('\n', '')
                        words[i].append(difinition[difinition.find('—')+1:])
                        flag = False
                    except:
                        ind += 1
        #print(words)
        table = crossword.table
        not_fit = crossword.not_fit

        return render(request, 'crossword/index.html', {'difinition':request.POST['difinition'],'size':int(request.POST['size']),'lenght':len(words), 'form':form, 'table':table, 'words':words, 'not_fit':not_fit} )
    return render(request, 'crossword/index.html', {'form': form})
