from GUI.mainGUI import Ui_MainWindow
from GUI.resultGUI import Ui_ResultWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from search_duplicate import search_starts
import sys
import os


class PathLabel(Ui_MainWindow):
    """ Класс обработки выбора пути поиска """

    def _choise_path_in_explorer(self) -> None:
        """ Функция выбора активации окна проводника windows """
        # Открывает окно проводника и сохраняет выбранную папку в переменную path
        path = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if path:
            # предварительно очищаем поле от предыдущего пути
            self.path_label.clear()
            # Добавляем выбранную папку в поле для ввода
            self._append_path_in_label(path)

    def _append_path_in_label(self, path):
        # Добавляет значение в поле "путь для поиска"
        self.path_label.append(path)

    @property
    def get_value_path_text(self) -> str:
        # Достаём значение с поля для ввода
        return self.path_label.toPlainText()


class MainGUIActions(QtWidgets.QMainWindow, PathLabel, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.changes_form()

    def changes_form(self):
        self.select_btn.clicked.connect(self.activates_select_button)
        self.search_btn.clicked.connect(self.activates_search_button)

    def activates_select_button(self):
        """ Функция активации кнопки выбора 'пути поиска' """
        self._choise_path_in_explorer()

    def activates_search_button(self):
        path = self.get_value_path_text
        results_dictionary = search_starts(f'{path}/')
        self.open_new_window(results_dictionary)

    def open_new_window(self, results_dictionary: dict):
        self.ResultWindow = ResultGUIActions(results_dictionary)
        self.ResultWindow.show()


class ResultGUIActions(QtWidgets.QMainWindow, Ui_ResultWindow):
    def __init__(self, results_dic):
        self.results_dic = results_dic
        super().__init__()
        self.setupUi(self)
        self.form_change()

    def form_change(self):
        self.original_listWidget.addItems(self.results_dic.keys())
        self.original_listWidget.itemClicked.connect(self.shows_result_duplicates)
        self.original_listWidget.itemDoubleClicked.connect(self.open_file_in_program)
        self.dup_listWidget.itemDoubleClicked.connect(self.open_file_in_program)

    def test(self, item):
        print(item)

    def shows_result_duplicates(self, item):
        self.dup_listWidget.clear()
        key = item.text()
        self.dup_listWidget.addItems(self.results_dic[key])

    def open_file_in_program(self, item):
        """ Открывает файлы в программе по умолчанию Windows """
        os.startfile(item.text())


def application():
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = MainGUIActions()
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
