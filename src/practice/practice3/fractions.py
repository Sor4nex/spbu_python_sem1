from math import gcd


def user_input_max_divisor() -> int:
    max_divisor = input("Введите максимальный знаменатель дроби: ")
    while not max_divisor.isdigit():
        max_divisor = input("Ошибка. Введите число: максимальный знаменатель дроби: ")
    return int(max_divisor)


def find_all_prime_fractions(max_divisor: int) -> list[tuple[int, int]]:
    prime_fractions = list()
    for divisor in range(1, max_divisor + 1):
        for dividend in range(1, divisor):
            if gcd(divisor, dividend) == 1:
                prime_fractions.append((dividend, divisor))
    return prime_fractions


if __name__ == "__main__":
    max_divisor = user_input_max_divisor()
    prime_fractions = find_all_prime_fractions(max_divisor)
    prime_fractions.sort(key=lambda fraction: fraction[0] / fraction[1])
    print(f"Простые несократимые дроби со знаменателем, не превыщающим {max_divisor}:")
    print(
        " ; ".join([f"{dividend}/{divisor}" for dividend, divisor in prime_fractions])
    )
