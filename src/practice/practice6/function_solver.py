from math import isnan, isinf


GREET_USER = "Добро пожаловать в программу для решения квадратных и линейных уравнений"
INFO_STRING = (
    "Вам нужно ввести 3 числа (A, B, C) через пробел, где A B и C - коэффициенты уравнения Ax^2 + Bx + C = "
    "0(Если нужно решить линейное уравнение, то укажите первым числом 0)"
)
INPUT_INVITATION = "Введите 3 числа (коэффициенты квадратного уравнения): "
BAD_INPUT = "Неверный формат!"


def is_float_number(input_str: str) -> bool:
    try:
        float(input_str)
    except ValueError:
        return False
    return True


def parse_user_input(input_str: str) -> bool:
    input_str = input_str.split(" ")
    if len(input_str) != 3:
        return False
    for coefficient in input_str:
        if not is_float_number(coefficient.strip()):
            return False
    return True


def solve_linear_function(first_coefficient: float, second_coefficient: float) -> float:
    return -second_coefficient / first_coefficient


def solve_quadratic_function(
    first_coefficient: float, second_coefficient: float, third_coefficient: float
) -> tuple[float, ...]:
    discriminant = second_coefficient**2 - 4 * first_coefficient * third_coefficient
    if discriminant < 0:
        raise ArithmeticError("дискриминант уравнения меньше 0, решений нет")
    elif discriminant == 0:
        result1 = (-second_coefficient + (discriminant) ** 0.5) / (
            2 * first_coefficient
        )
        return (result1,)
    result1 = (-second_coefficient + discriminant**0.5) / (2 * first_coefficient)
    result2 = (-second_coefficient - discriminant**0.5) / (2 * first_coefficient)
    return result1, result2


def solve_function(
    first_coefficient: float, second_coefficient: float, third_coefficient: float
) -> tuple[float, ...]:
    if first_coefficient == 0:
        if second_coefficient == 0:
            if third_coefficient == 0:
                raise ValueError("корень - любое вещественное число")
            raise ValueError("корня данного уравнения не существует")
        return (solve_linear_function(second_coefficient, third_coefficient),)
    return solve_quadratic_function(
        first_coefficient, second_coefficient, third_coefficient
    )


def main() -> None:
    print(GREET_USER + "\n" + INFO_STRING)
    user_input = input(INPUT_INVITATION).strip()
    if not parse_user_input(user_input):
        print(BAD_INPUT)
        return None
    coefficients = [float(number.strip()) for number in user_input.split(" ")]
    if any(isinf(num) or isnan(num) for num in coefficients):
        print(BAD_INPUT)
        return None
    try:
        result = solve_function(*coefficients)
    except (ValueError, ArithmeticError) as error:
        result = (str(error),)
    print("Ответ:", *result)


if __name__ == "__main__":
    main()
