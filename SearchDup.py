import os


class SearchDuplicate:
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
        file_dic = {}
        compare = []

        def recursive_crawling(path):
            search = os.listdir(path)
            for i in search:
                try:
                    if os.path.isdir(i):
                        recursive_crawling(path + i + "/")
                    else:
                        if i in map(self.clean_file_name, file_dic):
                            gen_file = self.run_dic(file_dic, i, self.file_size(path + i))
                            if gen_file:
                                compare.append([(path + i, self.file_size(path + i)), (gen_file[0], gen_file[-1])])
                            else:
                                file_dic[path + i] = self.file_size(path + i)
                        else:
                            file_dic[path + i] = self.file_size(path + i)
                except NotADirectoryError:
                    continue
                    file_dic[i] = self.file_size(path + i)

        recursive_crawling(path)
        print(compare)
        return compare

    def file_size(self, file):
        """ --- Возвращает размер файла в байтах --- """
        return os.stat(file).st_size

    def clean_file_name(self, path):
        """ --- Возбращает имя файла без пути --- """
        file_name = path.split('/')[-1]
        return file_name

    def run_dic(self, dic, i, size):
        """ --- Возвращает имя и размер файла который идентичен тому что есть --- """
        repeat_name_dic = {}
        for k, v in dic.items():
            if self.clean_file_name(k) == i:
                repeat_name_dic[k] = v
                for k, v in repeat_name_dic.items():
                    if v == size:
                        return k, v

    def save_result_infile(self, result):
        """ --- Записывает результаты в файл --- """
        with open('duplicates.txt', 'w') as f:
            for i in result:
                res = f'файл - \t\t{i[1][0]}\t размер: {i[1][1]} \n\tдубль - {i[0][0]}\t размер: {i[0][1]}\n\n\n'
                f.write(res)


def main(initial_search_path):
    obj = SearchDuplicate(initial_search_path)
    result = obj.file_crawling()
    obj.save_result_infile(result)


if __name__ == '__main__':
    main('D:\TestFolder\\')
