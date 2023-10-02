from random import choice
from itertools import permutations
from collections import Counter


def get_command_with_validation(print_out_note: str, avaliable_options: list) -> str:
    command = input(print_out_note)
    while command not in avaliable_options:
        print("Ошибка, введите цифру.")
        command = input(print_out_note)
    return command


def print_game_rules() -> None:
    print(
        """ПРАВИЛА ИГРЫ:
    1.Компьютер загадывает 4-ех значное число.
    2.Вы вводите 4-ех число, которое, как вам кажется, верное.
    3.Компьютер выводит количество:
    Коров (цифры, присутствующие в числе, стоящие НЕ на своих местах)
    Быков (цифры, присутствующие в загаданном числе, стоящие на своих местах)
    4. После этого вы повторяете свою попытку.
    5. Цель: отгадать загаданное число за наименьшее количество попыток.
    Удачи!"""
    )


def count_cows_and_bulls(goal_number: str, user_number_guess: str) -> Counter:
    counter_cows_and_bulls = Counter({"cows": 0, "bulls": 0})
    for numeral in user_number_guess:
        if numeral in goal_number:
            if user_number_guess.index(numeral) == goal_number.index(numeral):
                counter_cows_and_bulls["bulls"] += 1
            else:
                counter_cows_and_bulls["cows"] += 1
    return counter_cows_and_bulls


def start_game() -> None:
    numbers_options = [
        "".join(number)
        for number in permutations(
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], r=4
        )
        if number[0] != "0"
    ]
    goal_number = choice(numbers_options)
    user_attempts = 0
    user_number_guess = ""
    print("Число загадано, игра началась!")
    while user_number_guess != goal_number:
        user_number_guess = input(
            f"Попытка №{user_attempts + 1}. Введите предполагаемое число: "
        )
        user_attempts += 1
        if user_number_guess == goal_number:
            break
        else:
            cows_and_bulls = count_cows_and_bulls(goal_number, user_number_guess)
            cows_number, bulls_number = cows_and_bulls["cows"], cows_and_bulls["bulls"]
            print(f"Коров: {cows_number}, Быков: {bulls_number}")
    print(
        f"Ура! Получилось! Загаданное число было {goal_number}. Вы угадали с {user_attempts} попытки."
    )


if __name__ == "__main__":
    print('Добро пожаловать в игру "Быки и Коровы"!')
    command = None
    while command != "9":
        command = get_command_with_validation(
            "Выберите одну из опций:\n1. Начать игру\n2. Правилы игры\n9. Выйти\nВаш выбор: ",
            ["1", "2", "9"],
        )
        if command == "1":
            start_game()
        elif command == "2":
            print_game_rules()
    print("До Свидания!")
