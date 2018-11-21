import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
import about  # Это наш конвертированный файл окна About
import Lee
import numpy as np

class MainWindow(QtWidgets.QMainWindow, about.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

class ExampleApp(design.Ui_Lee, MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.open_file.triggered.connect(self.open)
        self.save_file.triggered.connect(self.save)
        self.About.triggered.connect(self.about)
        self.build.clicked.connect(self.build_maze)
        self.b = None
        self.p = None

    def open(self):
        try:
            fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть файл')[0]
            s = open(fname).read()
            array = [row.strip() for row in s]
            arr = self.split_on(array)
            p = 0
            le = ''
            for i in arr[0]: le += arr[0][p]; p += 1
            leng = int(le)
            self.len.setText(str(leng))
            start = self.separation([i for i in self.split_two(arr[1])])
            self.start.setText(str(start))
            finish = self.separation([i for i in self.split_two(arr[2])])
            self.finish.setText(str(finish))
            barriers = self.fuck([[b for b in i] for i in self.split_one(arr[3])])
            self.barriers.setText(str(barriers))

            field = Lee.Field(leng, tuple(start), tuple(finish), barriers)
            field.emit()
            self.b = np.array(field._show())
            self.field.setText(str(self.b))
        except FileNotFoundError:
            print('No such file in directory')
        except IndexError:
            self.field.setText('В выбранном файле содержаться некорректные данные!')
        except ValueError:
            self.field.setText('В выбранном файле содержаться некорректные данные!')
        else:
            try:
                path = field.get_path()
                self.p = [p for p in path]
                self.Way.setText(str(self.p))
            except:
                self.Way.setText('Невозможно проложить путь.')
    
    def save(self):
        try:
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить файл', 'Result.txt')[0]
            s = open(fname, 'w')
            s.write('Maze:\n')
            s.write(str(self.b))
            s.write('\n\nWay:\n')
            s.write(str(self.p))
        except FileNotFoundError:
            print('FileNotFoundError')

    def about(self):
        global window
        window = MainWindow()
        window.show()
    
    def split_on(self, what, delimiter = ''):
        splitted = [[]]
        for item in what:
            if item == delimiter:
                splitted.append([])
            else:
                splitted[-1].append(item)
        
        return splitted

    def split_one(self, what, delimiter = ';'):
        splitted = [[]]
        for item in what:
            if item == delimiter:
                splitted.append([])
            else:
                splitted[-1].append(item)

        return splitted

    def split_two(self, what, delimiter = ','):
        splitted = [[]]
        for item in what:
            if item == delimiter:
                splitted.append([])
            else:
                splitted[-1].append(item)

        return splitted

    def fuck(self, tup):
        split = []
        for i in tup:
            split.append(tuple(self.separation(self.split_two(i))))
        return split

    def separation(self, tup):
        separat = []
        for i in tup:
            b = ''
            for k in i:
                kk = k + b
                b = k
            separat.append(int(kk[::-1]))
        return separat

    def build_maze(self):
        try:
            leng = int(self.len.text())
            start = self.separation([i for i in self.split_two(self.start.text())])
            finish = self.separation([i for i in self.split_two(self.finish.text())])
            barriers = self.fuck([[b for b in i] for i in self.split_one(self.barriers.text())])
            field = Lee.Field(leng, tuple(start), tuple(finish), barriers)
            field.emit()
            self.b = np.array(field._show())
            self.field.setText(str(self.b))
        except ValueError:
            self.field.setText('Неккоректное значение аргумента')
        except UnboundLocalError:
            self.field.setText('Видимо какие-то поля не были заполнены. Так нельзя. Заполните все поля!')
        except IndexError:
            self.field.setText('Ваши данные не входят в диапазон элементов')
        else:
            try:
                path = field.get_path()
                self.p = [p for p in path]
                self.Way.setText(str(self.p))
            except:
                self.Way.setText('Невозможно проложить путь.')

        


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
