import os.path
import string
import sys
from collections import Counter


def check_file_existence(file_name: str) -> bool:
    return os.path.exists(file_name)


def count_latin_letters_from_file(input_file_name: str) -> Counter:
    result_letters_count = Counter()
    with open(input_file_name, "r", encoding="UTF-8") as file:
        for line in file:
            line_count = Counter(line)
            result_letters_count.update(line_count)
    del result_letters_count["\n"]
    return result_letters_count


def write_result_in_output_file(output_file_name: str, result_counter: Counter) -> None:
    result_to_write = []
    for letter in string.ascii_letters:
        letter_count = result_counter.get(letter, None)
        if letter_count is not None:
            result_to_write.append(f'"{letter}": {letter_count}\n')
    with open(output_file_name, "w", encoding="UTF-8") as output:
        output.writelines(result_to_write)


def main(args: list) -> None:
    args = args[1:]
    if len(args) != 2:
        print("Error: too many or not enough arguments")
        return None
    file_for_input, file_for_output = args
    if not check_file_existence(file_for_input):
        print(f"Error: file {file_for_input} does not exist")
        return None
    if check_file_existence(file_for_output):
        print(f"Error: file {file_for_output} already exists")
        return None
    result_letter_count = count_latin_letters_from_file(file_for_input)
    write_result_in_output_file(file_for_output, result_letter_count)


if __name__ == "__main__":
    main(sys.argv)
