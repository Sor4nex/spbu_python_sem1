from random import choice
from itertools import permutations


def get_command_with_validation(
    print_out_note: str, avaliable_options: list[str]
) -> str:
    command = input(print_out_note)
    while command not in avaliable_options:
        print("Ошибка, введите цифру.")
        command = input(print_out_note)
    return command


def get_user_number_guess(user_attempts: int) -> list[int]:
    user_input_guess = input(
        f"Попытка №{user_attempts + 1}. Введите предполагаемое число: "
    )
    while (
        not user_input_guess.isdigit()
        or any(user_input_guess.count(numeral) > 1 for numeral in user_input_guess)
        or len(user_input_guess) != 4
    ):
        print("Ошибка. Вы должны ввести 4-ёх значное число с неповторяющимися цифрами.")
        user_input_guess = input(
            f"Попытка №{user_attempts + 1}. Введите предполагаемое число: "
        )
    return list(int(numeral) for numeral in user_input_guess)


def count_cows_and_bulls(
    goal_number_list: list[int], user_number_guess_list: list[int]
) -> tuple[int, int]:
    cows_counter = bulls_counter = 0
    for i, numeral in enumerate(user_number_guess_list):
        if numeral in goal_number_list:
            if i == goal_number_list.index(numeral):
                bulls_counter += 1
            else:
                cows_counter += 1
    return cows_counter, bulls_counter


def start_game() -> None:
    number_options = [
        list(int(numeral) for numeral in number)
        for number in permutations(
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], r=4
        )
        if number[0] != "0"
    ]
    goal_number_list = choice(number_options)
    goal_number_str = "".join(str(numeral) for numeral in goal_number_list)
    user_attempts = 0
    user_number_guess_list = []
    print(goal_number_list)
    print("Число загадано, игра началась!")
    while user_number_guess_list != goal_number_list:
        user_number_guess_list = get_user_number_guess(user_attempts)
        user_attempts += 1
        if user_number_guess_list == goal_number_list:
            break
        cows_and_bulls = count_cows_and_bulls(goal_number_list, user_number_guess_list)
        cows_number, bulls_number = cows_and_bulls[0], cows_and_bulls[1]
        print(f"Коров: {cows_number}, Быков: {bulls_number}")
    print(
        f"Ура! Получилось! Загаданное число было {goal_number_str}. Вы угадали с {user_attempts} попытки."
    )


COMMAND_OPTIONS_STRING = (
    "Выберите одну из опций:\n1. Начать игру\n2. Правилы игры\n9. Выйти\nВаш выбор: "
)
GAME_RULES_STRING = """ПРАВИЛА ИГРЫ:
    1.Компьютер загадывает 4-ех значное число.
    2.Вы вводите 4-ех число, которое, как вам кажется, верное.
    3.Компьютер выводит количество:
    Коров (цифры, присутствующие в загаданном числе, стоящие НЕ на своих местах)
    Быков (цифры, присутствующие в загаданном числе, стоящие на своих местах)
    4. После этого вы повторяете свою попытку.
    5. Цель: отгадать загаданное число за наименьшее количество попыток.
    Удачи!"""


if __name__ == "__main__":
    print('Добро пожаловать в игру "Быки и Коровы"!')
    command = None
    while command != "9":
        command = get_command_with_validation(
            COMMAND_OPTIONS_STRING,
            ["1", "2", "9"],
        )
        if command == "1":
            start_game()
        elif command == "2":
            print(GAME_RULES_STRING)
    print("До Свидания!")
