import os.path
import sys


def check_file_existence(input_file_name: str) -> True:
    return os.path.exists(input_file_name)


def parse_given_argument(args: list) -> tuple:
    left_border = float(args[1]) if args[1].isdigit() else None
    right_border = float(args[2]) if args[2].isdigit() else None
    file_name_input = args[3]
    file_name_output = args[4]
    return left_border, right_border, file_name_input, file_name_output


def classify_input_file(
    file_name: str, left_border: float, right_border: float
) -> tuple[list, list, list]:
    left_interval = []
    right_interval = []
    middle_segment = []
    with open(file_name, "r") as file:
        for line in file:
            for number in line.strip().split(" "):
                number = float(number)
                if number < left_border:
                    left_interval.append(number)
                elif number > right_border:
                    right_interval.append(number)
                else:
                    middle_segment.append(number)
    return left_interval, middle_segment, right_interval


def write_result_in_output_file(
    file_name: str,
    left_interval: list[float],
    middle_segment: list[float],
    right_interval: list[float],
) -> None:
    with open(file_name, "w") as file:
        for number_left in left_interval:
            print(number_left, file=file)
        print("", file=file)
        for number_middle in middle_segment:
            print(number_middle, file=file)
        print("", file=file)
        for number_right in right_interval:
            print(number_right, file=file)


if __name__ == "__main__":
    if len(sys.argv[1:]) != 4:
        print("Error: Not enough or too many arguments")
        sys.exit(0)
    left_border, right_border, file_name_input, file_name_output = parse_given_argument(
        sys.argv
    )
    if not check_file_existence(file_name_input):
        print(f"Error: no such file {file_name_input}")
        sys.exit(0)
    elif check_file_existence(file_name_output):
        print(f"Error: such file already exists: {file_name_output} or bad format")
        sys.exit(0)
    elif left_border > right_border:
        print(f"Error: first number cant be greater, then second one")
        sys.exit(0)
    left_interval, middle_segment, right_interval = classify_input_file(
        file_name_input, left_border, right_border
    )
    write_result_in_output_file(
        file_name_output, left_interval, middle_segment, right_interval
    )
