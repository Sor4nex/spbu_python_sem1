def calculate_equation(x: float) -> float:
    squared_x = x ** 2 # first multiplication
    return squared_x * (squared_x + x + 1) + x + 1 # second multipication


if __name__ == "__main__":
    input_function_arg = input("Calculating x^4+x^3+x^2+x+1, enter x: ")
    while not input_function_arg.isdigit():
        input_function_arg = input(input_function_arg + " can`t be converted into a number, please, enter a number: ")
    print('The result is:', calculate_equation(float(input_function_arg)))
