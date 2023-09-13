def rearrange_array() -> None:
    usr_inp = input('Введите целые числа, элементы массива, через пробел: ')
    given_array = [int(elem) if elem.isdigit() else None for elem in usr_inp.split(' ')]
    while None in given_array or len(given_array) < 3:
        usr_inp = input('Один или несколько элементов не являются целыми числами, введите числа через пробел: ')
        given_array = [int(elem) if elem.isdigit() else None for elem in usr_inp.split(' ')]
    m_index = input('Введите индекс окончания среза: ')
    while not m_index.isdigit() or int(m_index) > len(given_array) - 1:
        m_index = input('Индекс не является числом, введите целое число: ')
    m_index = int(m_index)
    given_array.reverse()
    given_array[:-m_index], given_array[-m_index:] = given_array[-m_index:], given_array[:-m_index]
    given_array.reverse()
    print("Результат:", given_array)


if __name__ == '__main__':
    rearrange_array()
