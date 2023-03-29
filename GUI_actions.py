from GUI.mainGUI import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from search_duplicate import search_starts
import sys


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


class GUIActions(QtWidgets.QMainWindow, PathLabel, Ui_MainWindow):
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
        search_starts(f'{path}/')


def application():
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = GUIActions()
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
