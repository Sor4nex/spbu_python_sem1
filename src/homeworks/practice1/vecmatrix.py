def vector_calculator() -> None:
    print("Первый вектор.")
    vector1 = create_vector()
    print("Второй вектор.")
    vector2 = create_vector()
    if len(vector1) != len(vector2) or len(vector1) < 2 or len(vector2) < 2:
        print("Ошибка: Неправильная размерность")
        return None
    vector1_len, vector2_len = calculate_vector_length(
        vector1
    ), calculate_vector_length(vector2)
    scalar = calculate_scalar(vector1, vector2)
    angle = calculate_vectors_angle(scalar, vector1_len, vector2_len)
    print("Длинна вектора №1 =", vector1_len)
    print("Длинна вектора №2 =", vector2_len)
    print("Скалярное произведение векторов =", scalar)
    print("Угол между векторами cos=", str(angle))


def create_vector() -> tuple:
    usr_inp = input("Введите координаты вектора через пробел: ").strip().split(" ")
    while any(not element.isdigit() for element in usr_inp):
        usr_inp = (
            input("Произошла ошибка, введите координаты через пробел: ")
            .strip()
            .split(" ")
        )
    return tuple(int(coord) for coord in usr_inp)


def calculate_vector_length(vector: tuple) -> float:
    return sum([vector[i] ** 2 for i in range(len(vector))]) ** 0.5


def calculate_scalar(vector1: tuple, vector2: tuple) -> float:
    return sum([vector1[i] * vector2[i] for i in range(len(vector1))])


def calculate_vectors_angle(
    scalar: float, vector1_len: float, vector2_len: float
) -> float:
    result_angle = scalar / (vector1_len * vector2_len)
    return result_angle


def matrix_calculator() -> None:
    usr_inp = (
        input(
            "Введите через пробел два числа. Кол-во строк в матрицах, затем стоблцов: "
        )
        .strip()
        .split(" ")
    )
    while any(not element.isdigit() for element in usr_inp) or len(usr_inp) != 2:
        usr_inp = (
            input("Ошибка, введите два числа через пробел. Кол-во строк и столбцов: ")
            .strip()
            .split(" ")
        )
    length, width = int(usr_inp[0]), int(usr_inp[1])
    print("Первая матрица.")
    matrix1 = create_matrix(length, width)
    print("Вторая матрица.")
    matrix2 = create_matrix(length, width)
    task = input(
        "Выберите действие:\n\t\t1.Сложение\n\t\t2.Произведение\n\t\t3.Транспонирование\nВведите цифру: "
    )
    while task not in ["1", "2", "3"]:
        task = input("Ошибка. Введите одну цифру: ")
    print("Результат:")
    if task == "1":
        result_matrix = calculate_matrix_addition(matrix1, matrix2)
        for i in range(length):
            print(" ".join([str(el) for el in result_matrix[i]]))
    elif task == "2":
        result_matrix = calculate_matrix_composition(matrix1, matrix2)
        for i in range(length):
            print(" ".join([str(el) for el in result_matrix[i]]))
    else:
        print("Для первой матрицы:")
        result_matrix = calculate_matrix_transpose(matrix1)
        for i in range(width):
            print(" ".join([str(el) for el in result_matrix[i]]))
        print("Для второй матрицы:")
        result_matrix = calculate_matrix_transpose(matrix2)
        for i in range(width):
            print(" ".join([str(el) for el in result_matrix[i]]))


def create_matrix(height: int, width: int) -> list:
    result = list()
    for i in range(height):
        print(f"Введите {width} чисел строки {i + 1} матрицы через пробел:")
        single_str = input().strip().split(" ")
        while (
            any(not element.isdigit() for element in single_str)
            or len(single_str) != width
        ):
            print(f"Ошибка. Введите {width} чисел строки {i + 1} матрицы через пробел:")
            single_str = input().strip().split(" ")
        result.append([int(el) for el in single_str])
    return result


def calculate_matrix_addition(matrix1: list, matrix2: list) -> list:
    return [
        [matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))]
        for i in range(len(matrix1))
    ]


def calculate_matrix_composition(matrix1: list, matrix2: list) -> list:
    return [
        [matrix1[i][j] * matrix2[i][j] for j in range(len(matrix1[0]))]
        for i in range(len(matrix1))
    ]


def calculate_matrix_transpose(matrix: list) -> list:
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]


if __name__ == "__main__":
    print(
        "Добро пожаловать в приложение для вычислений операций, связанных с матрицами и векторами."
    )
    print("Пожалуйста, укажите тип данных для работы (внесите в поле одну цифру):")
    task = input("""\t\t1.Вектора\t\t2.Матрицы\nОперация: """)
    while task not in ["1", "2"]:
        print("Неверно выбрано действие, пожалуйста, выберите цифру.")
        task = input("\t\t1.Вектора\n\t\t2.Матрицы\nОперация: ")
    if task == "1":
        vector_calculator()
    else:
        matrix_calculator()
