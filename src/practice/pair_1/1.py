def calculate_incomplete_quotient(a: int, b: int) -> int:
    current_residue = a
    incomplete_quotient = 0    
    while current_residue >= b:
        current_residue -= b
        incomplete_quotient += 1
    return incomplete_quotient


if __name__ == '__main__':
    print('Добро пожаловать в приложение для нахождения неполного частного от деления a на b')
    dividend = input('Введите делимое: ')
    while not dividend.isdigit():
        dividend = input('Неправильный ввод, пожалуйста, введите целое число: ')
    divider = input('Теперь введите делитель: ')
    while not divider.isdigit():
        divider = input('Неправильный ввод, пожалуйста, введите целое число: ')
    print('Ответ:', calculate_incomplete_quotient(int(dividend), int(divider)))