from typing import Any


GREET_USER = "Добро пожаловать в программу для решения квадратных и линейных уравнений"
INFO_STRING = "Вам нужно ввести 3 числа (A, B, C) через пробел, где A B и C - коэффициенты уравнения Ax^2 + Bx + C = 0(Если нужно решить линейное уравнение, то укажите первым числом 0)"
INPUT_INVITATION = "Введите 3 числа (коэффициенты квадратного уравнения): "
BAD_INPUT = "Неверный формат!"


def is_float_number(input_str: str) -> bool:
    try:
        float(input_str)
    except ValueError:
        return False
    return True


def solve_linear_function(first_coefficient: float, second_coefficient: float) -> Any:
    if first_coefficient == 0:
        if second_coefficient == 0:
            return ("корень - любое вещественное число",)
        return ("корня данного уравнения не существует",)
    return (-second_coefficient / first_coefficient,)


def solve_quadratic_function(
    first_coefficient: float, second_coefficient: float, third_coefficient: float
) -> Any:
    discriminant = second_coefficient**2 - 4 * first_coefficient * third_coefficient
    if discriminant < 0:
        return ("дискриминант уравнения меньше 0, решений нет",)
    result_1 = (-second_coefficient + (discriminant) ** 0.5) / (2 * first_coefficient)
    result_2 = (-second_coefficient - (discriminant) ** 0.5) / (2 * first_coefficient)
    return result_1, result_2


def main() -> None:
    print(GREET_USER)
    print(INFO_STRING)
    user_input = input(INPUT_INVITATION).split(" ")
    while len(user_input) != 3 or any(
        not is_float_number(number) for number in user_input
    ):
        print(BAD_INPUT)
        return None
    first_num, second_num, third_num = (
        float(user_input[0]),
        float(user_input[1]),
        float(user_input[2]),
    )
    if first_num == 0:
        result = solve_linear_function(second_num, third_num)
    else:
        result = solve_quadratic_function(first_num, second_num, third_num)
        if len(result) > 1 and result[0] == result[1]:
            result = [result[0]]
    print(f"Ответ: {' '.join([str(element) for element in result])}")


if __name__ == "__main__":
    main()
