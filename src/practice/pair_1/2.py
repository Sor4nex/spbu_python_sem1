def rearrange_array() -> None:
    usr_inp = input('Введите целые числа, элементы массива, через пробел: ')
    givven_array = [int(elem) if elem.isdigit() else None for elem in usr_inp.split(' ')]
    while None in givven_array or len(givven_array) < 3:
        usr_inp = input('Один или несколько элементов не являются целыми числами, введите числа через пробел: ')
        givven_array = [int(elem) if elem.isdigit() else None for elem in usr_inp.split(' ')]
    m_index = input('Введите индекс окончания среза: ')
    while not m_index.isdigit() or int(m_index) > len(givven_array) - 1:
        m_index = input('Индекс не является числом, введите целое число: ')
    m_index = int(m_index) - 1
    givven_array.reverse()
    givven_array[:m_index], givven_array[m_index:] = givven_array[m_index:], givven_array[:m_index]
    givven_array.reverse()
    print("Результат:", givven_array)



if __name__ == '__main__':
    rearrange_array()