from GUI.mainGUI import Ui_MainWindow
from GUI.resultGUI import Ui_ResultWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFile
from search_duplicate import search_starts
import sys
import os


class PathLabel(Ui_MainWindow):
    """ Класс обработки выбора пути поиска """
    actual_path = ""

    def _choise_path_in_explorer(self) -> None:
        """ Функция выбора активации окна проводника windows """
        # Открывает окно проводника и сохраняет выбранную папку в переменную path
        path = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        if path:
            # предварительно очищаем поле от предыдущего пути
            self.path_label.clear()
            # Добавляем выбранную папку в поле для ввода
            self._append_path_in_label(path)

    def _append_path_in_label(self, path) -> None:
        # Добавляет значение в поле "путь для поиска"
        self.path_label.append(path)
        if path != self.actual_path:
            self.search_btn.setEnabled(True)
            self.actual_path = path

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

    def activates_select_button(self) -> None:
        """ Функция активации кнопки выбора 'пути поиска' """
        self._choise_path_in_explorer()

    def activates_search_button(self) -> None:
        path = self.get_value_path_text
        results_dictionary = search_starts(f'{path}/')
        if results_dictionary:
            self.open_new_window(results_dictionary)
            self.search_btn.setEnabled(False)
        else:
            self.change_process_label("Nothing found")
            self.search_btn.setEnabled(False)

    def change_process_label(self, message) -> None:
        self.process_label.setText(message)

    def open_new_window(self, results_dictionary: dict) -> None:
        self.ResultWindow = ResultGUIActions(results_dictionary)
        self.ResultWindow.show()


class ResultGUIActions(QtWidgets.QMainWindow, Ui_ResultWindow):
    def __init__(self, results_dic):
        self.results_dic = results_dic
        super().__init__()
        self.setupUi(self)
        self.changes_form()
        self.changes_title(self.results_dic)
        self.work_path = ''

    def changes_form(self):
        self.update_values_original_in_form()
        self.original_listWidget.itemClicked.connect(self.shows_result_duplicates)
        self.original_listWidget.itemDoubleClicked.connect(self.open_file_in_program)
        self.dup_listWidget.itemDoubleClicked.connect(self.open_file_in_program)
        self.dup_listWidget.itemClicked.connect(self.get_full_path)
        self.del_pushButton.pressed.connect(self.move_to_trash)

    def get_full_path(self, item) -> None:
        """ Получает имя файла и записывает его в переменную """
        self.work_path = item.text()
        self.activates_delete_button(True)

    def activates_delete_button(self, flag: bool) -> None:
        self.del_pushButton.setEnabled(flag)

    def update_values_original_in_form(self) -> None:
        """ Добавляет в форму значения оригиналов из словаря """
        self.original_listWidget.clear()
        if self.results_dic:
            self.original_listWidget.addItems(self.results_dic.keys())
        else:
            ResultGUIActions.close(self)

    def move_to_trash(self) -> None:
        """ Перемещает файл в корзину """
        QFile.moveToTrash(self.work_path)
        update_duplicate_list = self.return_update_duplicates_list(self.work_path)
        self.show_update_duplicates_list(update_duplicate_list)
        self.changes_title(self.results_dic)
        self.activates_delete_button(False)

    def remove_key_without_values(self) -> None:
        """ Удаляет ключ из словаря с пустым значением """
        dic = self.results_dic
        self.results_dic = dict(filter(lambda x: x[1], dic.items()))

    def return_update_duplicates_list(self, elem):
        """ Возвращает новый список дубликатов после удаления элемента """
        for key, value in self.results_dic.items():
            for k, item in enumerate(value):
                if item == elem:
                    del value[k]
                    if value == []:
                        self.activates_delete_button(False)
                        self.remove_key_without_values()
                        self.update_values_original_in_form()
                    return value
                else:
                    continue

    def show_update_duplicates_list(self, dup_list: list) -> None:
        self.dup_listWidget.clear()
        self.dup_listWidget.addItems(dup_list)

    def shows_result_duplicates(self, item) -> None:
        self.dup_listWidget.clear()
        key = item.text()
        self.dup_listWidget.addItems(self.results_dic[key])
        self.del_pushButton.setEnabled(False)

    def changes_title(self, dic: dict) -> None:
        original_count = len(dic)
        dup_count = self.counting_duplicates(dic)
        self.title_label.setText(f"Found {original_count} files and {dup_count} duplicates")

    def counting_duplicates(self, dic: dict) -> int:
        dup_count = []
        for i in dic.values():
            if len(i) != 1:
                for item in i:
                    dup_count.append(item)
            else:
                dup_count.append(i)
        return len(dup_count)

    def open_file_in_program(self, item) -> None:
        """ Открывает файлы в программе по умолчанию Windows """
        os.startfile(item.text())


def application():
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = MainGUIActions()
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
