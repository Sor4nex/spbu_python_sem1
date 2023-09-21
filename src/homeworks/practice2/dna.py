import os.path


def formate_file_extension(user_input: str) -> str:
    return user_input + ('.txt' if not user_input.endswith('.txt') else '')


def get_txts_from_user() -> tuple:
    print('Введите имя .txt файла с последовательностью ДНК и операциями:')
    source_file_name = formate_file_extension(input())
    while not os.path.isfile(source_file_name):
        print('Ошибка. Указанного файла не существует!\nВведите имя .txt файла из этой директории:')
        source_file_name = formate_file_extension(input())
    print('Введите имя .txt файла, куда будет выгружен результат преобразования последовательности:')
    output_file_name = formate_file_extension(input())
    return source_file_name, output_file_name


def operation_dna_delete(dna: str, start_pattern: str, end_pattern: str) -> str:
    first_index_of_start_pattern = dna.index(start_pattern)
    last_index_of_end_pattern = dna.index(end_pattern) + len(end_pattern)
    return dna[:first_index_of_start_pattern] + dna[last_index_of_end_pattern:]


def operation_dna_insert(dna: str, start_pattern: str, insert_snippet: str) -> str:
    last_index_of_start_pattern = dna.index(start_pattern) + len(start_pattern)
    return dna[:last_index_of_start_pattern] + insert_snippet + dna[last_index_of_start_pattern:]


def operation_dna_replace(dna: str, pattern_to_replace: str, replace_snippet: str) -> str:
    return dna.replace(pattern_to_replace, replace_snippet, 1)


def calculate_dna_transformation(source_file_name: str) -> list:
    all_dna_transformations = list()
    with open(source_file_name, 'r', encoding='utf-8') as file:
        file.readline()
        current_dna = file.readline().strip()
        all_dna_transformations.append(current_dna)
        file.readline()
        for line in file:
            operation, first_arg, second_arg = line.strip().split(' ')
            if operation == 'DELETE':
                current_dna = operation_dna_delete(current_dna, first_arg, second_arg)
            elif operation == 'INSERT':
                current_dna = operation_dna_insert(current_dna, first_arg, second_arg)
            else:
                current_dna = operation_dna_replace(current_dna, first_arg, second_arg)
            all_dna_transformations.append(current_dna)
    return all_dna_transformations


def return_results_txt(output_file_name: str, dna_transformations: list) -> None:
    with open(output_file_name, 'w', encoding='utf-8') as file:
        for dna in dna_transformations:
            print(dna, file=file)


if __name__ == '__main__':
    source_file_name, output_file_name = get_txts_from_user()
    all_dna_transformations = calculate_dna_transformation(source_file_name)
    return_results_txt(output_file_name, all_dna_transformations)
