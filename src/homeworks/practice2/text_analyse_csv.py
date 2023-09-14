import csv
import os.path


def get_txt_from_user() -> str:
    print('Введите имя .txt файла для анализа (файл должен лежать в той же директории):')
    source_file_name = formate_file_extension(input())
    while not os.path.isfile(source_file_name):
        print('Ошибка. Указанного файла не существует!\nВведите имя .txt файла из этой директории:')
        source_file_name = formate_file_extension(input())
    return source_file_name


def get_csv_from_user() -> str:
    print('Введите имя .csv файла для получения результата анализа:')
    csv_file_name = formate_file_extension(input(), 'csv')
    return csv_file_name


def formate_file_extension(usr_inp: str, mode: str = 'txt') -> str:
    if mode == 'txt':
        return usr_inp + ('.txt' if usr_inp[-4:] != '.txt' else '')
    elif mode == 'csv':
        return usr_inp + ('.csv' if usr_inp[-4:] != '.csv' else '')


def analyse_words_frequency(file_name) -> dict:
    func_output = dict()
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            if line[0] == '\n':
                continue
            for word in line.strip().split(' '):
                if word in func_output.keys():
                    func_output[word] += 1
                else:
                    func_output[word] = 1
        file.close()
    return func_output


def return_results_csv(csv_file_name: str, words_frequency: dict) -> None:
    with open(csv_file_name, 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(['Word', 'Frequency'])
        for word in words_frequency.keys():
            csv_writer.writerow([word, words_frequency[word]])


if __name__ == '__main__':
    source_file_name = get_txt_from_user()
    csv_file_name = get_csv_from_user()
    words_frequency_analysis = analyse_words_frequency(source_file_name)
    return_results_csv(csv_file_name, words_frequency_analysis)
    print('Успешно! Результат сохранен в файл', csv_file_name)
