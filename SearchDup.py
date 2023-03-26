import os
import time


def standardizes_url(url):
    """ --- Приводит введеный урл к стандарту --- """
    if (url[-1] != '\\') & (url[-1] != '/'):
        path = url.replace('\\', r'/') + '/'
    else:
        path = url.replace('\\', r'/')
    return path
    # path = url.replace('\\', r'/') + '/' if ((url[-1] != '\\') & (url[-1] != '/')) else url.replace('\\', r'/')


def file_size(file):
    """ --- Возвращает размер файла в байтах --- """
    return os.stat(file).st_size


def clean_file_name(path):
    """ --- Возбращает имя файла без пути --- """
    file_name = path.split('/')[-1]
    return file_name


def run_dic(dic, i, size):
    """ --- Возвращает имя и размер файла который идентичен тому что есть --- """
    repeat_name_dic = {}
    for k, v in dic.items():
        if clean_file_name(k) == i:
            repeat_name_dic[k] = v
            for k, v in repeat_name_dic.items():
                if v == size:
                    return k, v


def save_result_infile(result):
    """ --- Записывает результаты в файл --- """
    with open('dublicate.txt', 'w') as f:
        for i in result:
            res = f'файл - \t\t{i[1][0]}\t размер: {i[1][1]} \n\tдубль - {i[0][0]}\t размер: {i[0][1]}\n\n\n'
            f.write(res)


def file_crawling(path):
    os.chdir(f"{path}")
    file_dic = {}
    compare = []

    def recursive_crawling(path):
        search = os.listdir(path)
        for i in search:
            try:
                if '.' not in i:
                    recursive_crawling(path + i + "/")
                else:
                    if i in map(clean_file_name, file_dic):
                        gen_file = run_dic(file_dic, i, file_size(path + i))
                        if gen_file:
                            compare.append([(path + i, file_size(path + i)), (gen_file[0], gen_file[-1])])
                        else:
                            file_dic[path + i] = file_size(path + i)
                    else:
                        file_dic[path + i] = file_size(path + i)
            except NotADirectoryError:
                continue
                file_dic[i] = file_size(path + i)

    recursive_crawling(path)

    return compare


if __name__ == '__main__':
    url = input('url: ')
    start_time = time.time()
    result = file_crawling(standardizes_url(url))
    save_result_infile(result)
    run_time = time.time() - start_time
    print(f'{round(run_time, 3)} сек.')
    print('Поиск успешно завершен.')
    time.sleep(10)
