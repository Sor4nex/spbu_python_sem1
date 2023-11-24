INPUT_INVITE = "input number of fibonacci you want to get: "
ERROR_MESSAGE = "error: number should be an integer from 0 to 90"
ANSWER = "result: {}-th Fibonacci number is {}"


def is_int(input_str: str) -> bool:
    if input_str == "0":
        return True
    return input_str.isdigit() and input_str[0] != "0"


def count_n_fibonacci(numb_of_fib: int) -> int:
    if numb_of_fib == 0:
        return 0
    if numb_of_fib <= 2:
        return 1
    fib_first, fib_second = 1, 1
    for i in range(numb_of_fib - 2):
        fib_first, fib_second = fib_second, fib_first + fib_second
    return fib_second


def main() -> None:
    num_of_fib = input(INPUT_INVITE)
    if not is_int(num_of_fib):
        print(ERROR_MESSAGE)
        return
    num_of_fib = int(num_of_fib)
    if num_of_fib < 0 or num_of_fib > 90:
        print(ERROR_MESSAGE)
        return
    result_fib = count_n_fibonacci(num_of_fib)
    print(ANSWER.format(num_of_fib, result_fib))


if __name__ == "__main__":
    main()
