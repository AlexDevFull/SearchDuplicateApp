import time

def path_file():
    a = input('url: ')
    global start_time
    start_time = time.time()
    path = a.replace('\\', r'/') + '/' if ((a[-1] != '\\') & (a[-1] != '/')) else a.replace('\\', r'/')
    return path


def clean_file_name(path):
    file_name = path.split('/')[-1]
    return file_name

def run_dic(dic, i, size):
    repeat_name_dic = {}
    for k, v in dic.items():
        if clean_file_name(k) == i:
            repeat_name_dic[k] = v
            for k, v in repeat_name_dic.items():
                if v == size:
                    return k, v

def file_crawling(path):
    import os
    os.chdir(f"{path}")
    file_dic = {}
    compare = []

    def file_size(file):
        return os.stat(file).st_size

    def recursive_crawling(path):
        search = os.listdir(path)
        for i in search:
            try:
                if '.' not in i:
                    recursive_crawling(path + i + "/")
                else:
                    if i in map(clean_file_name, file_dic):
                        gen_file = run_dic(file_dic, i, file_size(path + i))
                        # if file_size(path + i) == gen_file[-1]:
                        if gen_file:
                            compare.append([(path + i, file_size(path + i)),(gen_file[0],gen_file[-1])])
                        else:
                            file_dic[path + i] = file_size(path + i)
                    else:
                        file_dic[path + i] = file_size(path + i)
            except NotADirectoryError:
                continue
                file_dic[i] = file_size(path + i)
    recursive_crawling(path)

    # print(file_dic)
    return compare




b = file_crawling(path_file())

with open('dublicate.txt', 'w') as f:
    for i in b:
        a = f'файл - \t\t{i[1][0]}\t размер: {i[1][1]} \n\tдубль - {i[0][0]}\t размер: {i[0][1]}\n\n\n'
        f.write(a)
run_time = time.time() - start_time
print(f'{round(run_time, 3)} сек.')
print('Поиск успешно завершен.')
time.sleep(10)






