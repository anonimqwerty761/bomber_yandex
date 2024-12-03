from tkinter import *
from random import choice


class Pole(object):  # создаем Класс поля, наследуемся от Object
    def __init__(self, master, row, column):  # Инициализация поля. master - окно Tk().
        self.button = Button(master, text='   ')  # Создаем для нашего поля атрибут 'button'
        self.mine = False  # Переменная наличия мины в поле
        self.value = 0  # Кол-во мин вокруг
        self.viewed = False  # Открыто/закрыто поле
        self.flag = 0  # 0 - флага нет, 1 - флаг стоит, 2 - стоит "?"
        self.around = []  # Массив, содержащий координаты соседних клеток
        self.clr = 'black'  # Цвет текста
        self.bg = None  # Цвет фона
        self.row = row  # Строка
        self.column = column  # Столбец

    def viewAround(self):
        return self.around

    def setAround(self):
        if self.row == 0:
            self.around.append([self.row + 1, self.column])
            if self.column == 0:
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
            elif self.column == len(buttons[self.row]) - 1:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row + 1, self.column - 1])
            else:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
                self.around.append([self.row + 1, self.column - 1])
        elif self.row == len(buttons) - 1:
            self.around.append([self.row - 1, self.column])
            if self.column == 0:
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row - 1, self.column + 1])
            elif self.column == len(buttons[self.row]) - 1:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row - 1, self.column - 1])
            else:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row - 1, self.column + 1])
                self.around.append([self.row - 1, self.column - 1])
        else:
            self.around.append([self.row - 1, self.column])
            self.around.append([self.row + 1, self.column])
            if self.column == 0:
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
                self.around.append([self.row - 1, self.column + 1])
            elif self.column == len(buttons[self.row]) - 1:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row + 1, self.column - 1])
                self.around.append([self.row - 1, self.column - 1])
            else:
                self.around.append([self.row, self.column - 1])
                self.around.append([self.row, self.column + 1])
                self.around.append([self.row + 1, self.column + 1])
                self.around.append([self.row + 1, self.column - 1])
                self.around.append([self.row - 1, self.column + 1])
                self.around.append([self.row - 1, self.column - 1])

    def view(self, event):
        if mines == []:  # При первом нажатии
            seter(0, self.around, self.row, self.column)  # Устанавливаем мины
        if self.value == 0:  # Устанавливаем цвета. Можно написать и для 6,7 и 8, но у меня закончилась фантазия
            self.clr = 'yellow'
            self.value = None
            self.bg = 'lightgrey'
        elif self.value == 1:
            self.clr = 'green'
        elif self.value == 2:
            self.clr = 'blue'
        elif self.value == 3:
            self.clr = 'red'
        elif self.value == 4:
            self.clr = 'purple'

        if self.mine and not self.viewed and not self.flag:  # Если в клетке есть мина, она еще не открыта и на ней нет флага
            self.button.configure(text='B', bg='red')  # Показываем пользователю, что тут есть мина
            self.viewed = True  # Говорим, что клетка раскрыта
            for q in mines:
                buttons[q[0]][q[1]].view('<Button-1>')  # Я сейчас буду вскрывать ВСЕ мины
            lose()  # Вызываем окно проигрыша

        elif not self.viewed and not self.flag:  # Если мины нет, клетка не открыта и флаг не стоит
            self.button.configure(text=self.value, fg=self.clr, bg=self.bg)  # выводим в текст поля значение
            self.viewed = True
            if self.value == None:  # Если вокруг нет мин
                for k in self.around:
                    buttons[k[0]][k[1]].view('<Button-1>')  # Открываем все поля вокруг

    def setFlag(self, event):
        if self.flag == 0 and not self.viewed:  # Если поле не открыто и флага нет
            self.flag = 1  # Ставим флаг
            self.button.configure(text='F', bg='yellow')  # Выводим флаг
            flags.append([self.row, self.column])  # Добавляем в массив флагов
        elif self.flag == 1:  # Если флаг стоим
            self.flag = 2  # Ставим значение '?'
            self.button.configure(text='?', bg='blue')  # Выводим его
            flags.pop(flags.index([self.row, self.column]))  # Удаляем флаг из массива флагов
        elif self.flag == 2:  # Если вопрос
            self.flag = 0  # Устанавливаем на отсутствие флага
            self.button.configure(text='   ', bg='white')  # Выводим пустоту
        if sorted(mines) == sorted(flags) and mines != []:  # если массив флагов идентичен массиву мин
            winer()  # Сообщаем о победе


def lose():
    loseWindow = Tk()
    loseWindow.title('Вы проигралиыыы')
    loseWindow.geometry('300x100')
    loseLabe = Label(loseWindow, text='В следующий раз повезет больше!')
    loseLabe.pack()
    mines = []
    loseWindow.mainloop()


def seter(q, around, row, column):  # Получаем массив полей вокруг и координаты нажатого поля
    if q == bombs:  # Если кол-во установленных бомб = кол-ву заявленных
        for i in buttons:  # Шагаем по строкам
            for j in i:  # Шагаем по полям в строке i
                for k in j.around:  # Шагаем по полям вокруг выбранного поля j
                    if buttons[k[0]][k[1]].mine:  # Если в одном из полей k мина
                        buttons[buttons.index(i)][i.index(j)].value += 1  # То увеличиваем значение поля j
        return
    a = choice(buttons)  # Выбираем рандомную строку
    b = choice(a)  # Рандомное поле
    if [buttons.index(a), a.index(b)] not in mines and [buttons.index(a), a.index(b)] not in around and [
        buttons.index(a), a.index(b)] != [row,
                                          column]:  # Проверяем, что выбранное поле не выбиралось до этого и, что не является полем на которую мы нажали (или окружающим ее полем)
        b.mine = True  # Ставим мину
        mines.append([buttons.index(a), a.index(b)])  # Добавляем ее в массив
        seter(q + 1, around, row, column)  # Вызываем установщик, сказав, что одна мина уже есть
    else:
        seter(q, around, row, column)  # Вызываем установщик еще раз


def winer():
    winWindow = Tk()
    winWindow.geometry('300x100')
    winWindow.title('Вы победили!')
    winLabe = Label(winWindow, text='Поздравляем!')
    winLabe.pack()
    winWindow.mainloop()


def cheat(event):
    for t in mines:
        buttons[t[0]][t[1]].setFlag('<Button-1>')


def game(high, lenght):  # получаем значения
    root = Tk()
    root.title('Игра Сапер by Эльназ')
    global buttons
    global mines
    global flags
    flags = []  # Массив, содержащий в себе места, где стоят флажки
    mines = []  # Массив, содержащий в себе места, где лежат мины
    buttons = [[Pole(root, row, column) for column in range(high)] for row in
               range(lenght)]  # Двумерный массив, в котором лежат поля
    for i in buttons:  # Цикл по строкам
        for j in i:  # Цикл по элементам строки
            j.button.grid(column=i.index(j), row=buttons.index(i), ipadx=7,
                          ipady=1)  # Размещаем все в одной сетке при помощи grid
            j.button.bind('<Button-1>', j.view)  # Биндим открывание клетки
            j.button.bind('<Button-3>', j.setFlag)  # Установка флажка
            j.setAround()  # Функция заполнения массива self.around
    buttons[0][0].button.bind('<Control-Button-1>', cheat)  # создаем комбинацию клавиш для быстрого решения
    root.resizable(False, False)
    root.mainloop()


def bombcounter():
    global bombs
    if mineText.get('1.0', END) == '\n':
        bombs = 10
    else:
        bombs = int(mineText.get('1.0', END))
    if highText.get('1.0', END) == '\n':
        high = 9
    else:
        high = int(highText.get('1.0', END))
    if lenghtText.get('1.0', END) == '\n':
        lenght = 9
    else:
        lenght = int(lenghtText.get('1.0', END))
    game(high, lenght)


settings = Tk()
settings.title('Настройки игры')
settings.geometry('200x150')
mineText = Text(settings, width=5, height=1)
mineLabe = Label(settings, height=1, text='Бомбы:')
highText = Text(settings, width=5, height=1)
highLabe = Label(settings, height=1, text='Ширина:')
lenghtText = Text(settings, width=5, height=1)
lenghtLabe = Label(settings, height=1, text='Высота:')
mineBut = Button(settings, text='Начать:', command=bombcounter)
mineBut.place(x=70, y=90)  # Размещаем это все
mineText.place(x=75, y=5)
mineLabe.place(x=5, y=5)
highText.place(x=75, y=30)
highLabe.place(x=5, y=30)
lenghtText.place(x=75, y=55)
lenghtLabe.place(x=5, y=55)
settings.mainloop()
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QTextEdit, QVBoxLayout, QWidget, QPushButton, QMessageBox, QMenuBar

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для Заметок")
        self.setGeometry(100, 100, 600, 400)

        self.notes = []
        self.current_note_index = -1

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.note_list = QListWidget()
        self.note_list.clicked.connect(self.load_note)

        self.note_edit = QTextEdit()

        self.add_note_button = QPushButton("Добавить Заметку")
        self.add_note_button.clicked.connect(self.add_note)

        self.delete_note_button = QPushButton("Удалить Заметку")
        self.delete_note_button.clicked.connect(self.delete_note)

        self.layout.addWidget(self.note_list)
        self.layout.addWidget(self.note_edit)
        self.layout.addWidget(self.add_note_button)
        self.layout.addWidget(self.delete_note_button)

        self.setMenuBar(self.create_menu())

    def create_menu(self):
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("Файл")

        save_action = file_menu.addAction("Сохранить")
        save_action.triggered.connect(self.save_notes)

        load_action = file_menu.addAction("Загрузить")
        load_action.triggered.connect(self.load_notes)

        return menu_bar

    def add_note(self):
        note_text = self.note_edit.toPlainText()
        if note_text:
            self.notes.append(note_text)
            self.note_list.addItem(note_text)
            self.note_edit.clear()
            self.current_note_index = len(self.notes) - 1

    def delete_note(self):
        if self.current_note_index >= 0:
            del self.notes[self.current_note_index]
            self.note_list.takeItem(self.current_note_index)
            self.note_edit.clear()
            self.current_note_index = -1

    def load_note(self):
        self.current_note_index = self.note_list.currentRow()
        if self.current_note_index >= 0:
            note_text = self.notes[self.current_note_index]
            self.note_edit.setPlainText(note_text)

    def save_notes(self):
        with open("notes.txt", "w") as f:
            for note in self.notes:
                f.write(note + "\n")

    def load_notes(self):
        try:
            with open("notes.txt", "r") as f:
                self.notes = f.read().splitlines()
                self.note_list.clear()
                for note in self.notes:
                    self.note_list.addItem(note)
                if self.notes:
                    self.current_note_index = 0
                    self.load_note()
                else:
                    self.current_note_index = -1
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл с заметками не найден.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec_())
"""