import os


class SearchDuplicate:


    def __init__(self, initial_search_path):
        self.initial_search_path = self.standardizes_url(initial_search_path)
        self.name_and_size = {}
        self.result_origin_files = {}
        self.result_duplicate_files = {}

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
                        if self.checks_exist_shortname_in_dictionary(file_name):
                            original_file_name = self.checks_size_equal(file_name, file_size)
                            if original_file_name:
                                self.adds_result_to_dictionary(original_file_name, self.result_origin_files)
                                self.adds_result_duplicate_to_dictionary(full_file_name, original_file_name)
                            else:
                                self.adds_result_to_dictionary(full_file_name, self.name_and_size)
                        else:
                            self.adds_result_to_dictionary(full_file_name, self.name_and_size)
                except NotADirectoryError:
                    continue

        recursive_crawling(path)

    @property
    def get_origin_files(self) -> dict:
        return self.result_origin_files

    @property
    def get_duplicate_files(self) -> dict:
        return self.result_duplicate_files

    def checks_exist_shortname_in_dictionary(self, file_name: str) -> bool:
        """ --- Проверяет есть ли ссылка на файл в словаре --- """
        return file_name in map(self.clean_file_name, self.name_and_size)

    def checks_size_equal(self, name: str, size: int) -> str:
        """ --- Проверяет размер файла на соответствие --- """
        for item in self.name_and_size:
            if name in item:
                if size == self.name_and_size[item]:
                    return item
            else:
                continue

    def adds_result_to_dictionary(self, file_name: str, dictionary: dict) -> None:
        """ --- Добавляет ссылку на файл и размер файла в словарь --- """
        dictionary[file_name] = self.file_size(file_name)

    def adds_result_duplicate_to_dictionary(self, file_name: str, key_file_name: str) -> None:
        """ --- Добавляет дубликат в list-значение словаря --- """
        duplicate_list = self.result_duplicate_files.get(key_file_name, None)
        if duplicate_list:
            duplicate_list.append(file_name)
            self.result_duplicate_files[key_file_name] = duplicate_list
        else:
            self.result_duplicate_files[key_file_name] = [file_name]

    def file_size(self, file: str) -> int:
        """ --- Возвращает размер файла в байтах --- """
        return os.stat(file).st_size

    def clean_file_name(self, path: str) -> str:
        """ --- Возбращает имя файла без пути --- """
        file_name = path.split('/')[-1]
        return file_name


def search_starts(initial_search_path):
    obj = SearchDuplicate(initial_search_path)
    obj.file_crawling()
    # Результатирующий словарь оригинальных файлов с их размерами
    # result = obj.get_origin_files
    # Результатирующий словарь оригинальных файлов с их дублями
    result = obj.get_duplicate_files
    return result


if __name__ == '__main__':
    search_starts('D:\TestFolder\\')

