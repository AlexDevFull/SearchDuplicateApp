import os


class SearchDuplicate:
    file_dic = {}
    result_dic = {}

    def __init__(self, initial_search_path):
        self.initial_search_path = self.standardizes_url(initial_search_path)

    @staticmethod
    def standardizes_url(url: str) -> str:
        """ --- Приводит введеный урл к стандарту --- """
        if '\\' in url:
            url = url.replace('\\', '/')
        return url

    def file_crawling(self):
        path = self.initial_search_path
        os.chdir(f"{path}")

        def recursive_crawling(path):
            search = os.listdir(path)
            for file_name in search:
                full_file_name = path + file_name
                file_size = self.file_size(full_file_name)
                try:
                    if os.path.isdir(full_file_name):
                        recursive_crawling(full_file_name + "/")
                    else:
                        if self.check_exist_in_dictionary(file_name):
                            origin_file_data = self.get_values_dic(file_name, file_size)
                            if origin_file_data:
                                origin_file_name, origin_file_size = origin_file_data
                                if origin_file_name not in self.result_dic:
                                    self.result_dic[origin_file_name] = [[full_file_name], file_size]
                                else:
                                    self.result_dic[origin_file_name] = [
                                        self.result_dic[origin_file_name][0] + [full_file_name], file_size]
                            else:
                                self.adds_result_to_dictionary(full_file_name)
                        else:
                            self.adds_result_to_dictionary(full_file_name)
                except NotADirectoryError:
                    continue

        recursive_crawling(path)

    @property
    def get_compare(self) -> dict:
        return self.result_dic

    def check_exist_in_dictionary(self, file_name: str) -> bool:
        """ --- Проверяет есть ли ссылка на файл в словаре --- """
        return file_name in map(self.clean_file_name, self.file_dic)

    def adds_result_to_dictionary(self, file_name: str) -> None:
        """ --- Добавляет ссылку на файл и размер файла в словарь --- """
        self.file_dic[file_name] = self.file_size(file_name)

    def file_size(self, file: str) -> int:
        """ --- Возвращает размер файла в байтах --- """
        return os.stat(file).st_size

    def clean_file_name(self, path: str) -> str:
        """ --- Возбращает имя файла без пути --- """
        file_name = path.split('/')[-1]
        return file_name

    def get_values_dic(self, file_name: str, size: int) -> tuple:
        """ --- Возвращает имя и размер файла из словаря который идентичен найденному --- """
        for key, value in self.file_dic.items():
            if self.clean_file_name(key) == file_name and value == size:
                return key, value

    def save_result_infile(self, result) -> None:
        """ --- Записывает результаты в файл --- """
        with open('duplicates.txt', 'w') as f:
            for origin_file, duplicate_files_and_size in result.items():
                res = f'файл - \t\t{origin_file}\t размер: {duplicate_files_and_size[1]}\n'
                f.write(res)
                for duplicate_files in duplicate_files_and_size[0]:
                    res = f'\tдубль - {duplicate_files}\t размер: {duplicate_files_and_size[1]}\n'
                    f.write(res)
                f.write('\n')


def search_starts(initial_search_path):
    obj = SearchDuplicate(initial_search_path)
    obj.file_crawling()
    result = obj.get_compare
    obj.save_result_infile(result)


if __name__ == '__main__':
    search_starts('D:\TestFolder\\')
