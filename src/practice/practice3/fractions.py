def get_max_divisor() -> int:
    max_divisor = input("Введите максимальный знаменатель дроби: ")
    while not max_divisor.isdigit():
        max_divisor = input("Ошибка. Введите число: максимальный знаменатель дроби: ")
    return int(max_divisor)


def find_greatest_common_divisor(first_number: int, second_number: int) -> int:
    while first_number % second_number != 0:
        first_number, second_number = second_number, first_number % second_number
    return second_number


def find_all_prime_fractions(max_divisor: int) -> list:
    prime_fractions = list()
    for divisor in range(1, max_divisor + 1):
        for dividend in range(1, divisor):
            if find_greatest_common_divisor(divisor, dividend) == 1:
                prime_fractions.append((dividend, divisor))
    return prime_fractions


if __name__ == "__main__":
    max_divisor = get_max_divisor()
    prime_fractions = find_all_prime_fractions(max_divisor)
    prime_fractions.sort(key=lambda fraction: fraction[0] / fraction[1])
    print(f"Простые несократимые дроби со знаменателем, не превыщающим {max_divisor}:")
    for fraction in prime_fractions:
        print(f"{fraction[0]}/{fraction[1]}", end=" ; ")
