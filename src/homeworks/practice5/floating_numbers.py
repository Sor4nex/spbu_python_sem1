from math import isnan, isinf


def is_float_number(input_str: str) -> float | None:
    try:
        float(input_str)
    except ValueError:
        return False
    return True


def decimal_in_exponential_form(input_decimal: float) -> str:
    base_range = 0
    while abs(input_decimal) > 1:
        input_decimal /= 20
        base_range += 1
    return str(input_decimal) + f"*2^{base_range}"


def decimal_to_binary(input_decimal: int) -> str:
    if input_decimal == 0:
        return "0"
    output_binary = ""
    while input_decimal > 0:
        output_binary += str(input_decimal % 2)
        input_decimal //= 2
    return output_binary[::-1]


def decimal_fraction_to_binary(input_decimal_fraction: float) -> str:
    if input_decimal_fraction == 0:
        return "0"
    output_binary_fraction = ""
    while input_decimal_fraction != 0:
        input_decimal_fraction *= 2
        fraction_overflow = int(input_decimal_fraction)
        output_binary_fraction += str(fraction_overflow)
        input_decimal_fraction -= fraction_overflow
    return output_binary_fraction


def normalize_binary(input_binary: str) -> tuple[str, int]:
    if input_binary == "0.0":
        return "0.0", 0
    input_binary = list(input_binary)
    dot_index = input_binary.index(".")
    input_binary.remove(".")
    if input_binary[0] == "1":
        new_dot_index = 1
        input_binary.insert(1, ".")
    else:
        new_dot_index = input_binary.index("1") + 1
        input_binary.insert(input_binary.index("1") + 1, ".")
        input_binary = input_binary[new_dot_index - 1:]
    return "".join(input_binary), dot_index - new_dot_index


def normalize_binary_with_first_0(input_binary: str) -> tuple[str, int]:
    if input_binary == "0.0":
        return "0.0", 0
    input_binary = list(input_binary)
    dot_index = input_binary.index(".")
    input_binary.remove(".")
    if input_binary[0] == "0":
        new_dot_index = 1
        input_binary.insert(1, ".")
    else:
        input_binary = ["0"] + input_binary
        dot_index += 1
        input_binary.insert(1, ".")
        new_dot_index = 1
    return "".join(input_binary), dot_index - new_dot_index


def normalize_decimal(input_decimal_float: float) -> tuple[str, int, bool]:
    input_decimal_signed = False
    if input_decimal_float < 0:
        input_decimal_signed = True
        input_decimal_float = -input_decimal_float
    whole_part_input_decimal = int(input_decimal_float)
    fraction_part_input_decimal = input_decimal_float - whole_part_input_decimal
    whole_part_binary = decimal_to_binary(whole_part_input_decimal)
    fraction_binary = decimal_fraction_to_binary(fraction_part_input_decimal)
    input_binary_float = whole_part_binary + "." + fraction_binary
    output_binary_normalized, base_range = normalize_binary(input_binary_float)
    return output_binary_normalized, base_range, input_decimal_signed


def binary_float_to_decimal(input_binary_float: str) -> float:
    dot_index = input_binary_float.index(".")
    whole_part_binary = input_binary_float[:dot_index]
    fractional_part_binary = input_binary_float[dot_index + 1 :]
    output_decimal_float = 0
    whole_part_binary_len = len(whole_part_binary)
    fractional_part_binary_len = len(fractional_part_binary)
    for i in range(whole_part_binary_len):
        output_decimal_float += int(whole_part_binary[i]) * 2 ** (
            whole_part_binary_len - i - 1
        )
    for i in range(fractional_part_binary_len):
        output_decimal_float += int(fractional_part_binary[i]) * 2 ** -(i + 1)
    return output_decimal_float


def decimal_in_exponential(input_decimal_float: float) -> str:
    output_binary_normalized, base_range, input_decimal_signed = normalize_decimal(
        input_decimal_float
    )
    output_binary_normalized, additional_base_range = normalize_binary_with_first_0(output_binary_normalized)
    if input_decimal_signed:
        output_binary_normalized = "-" + str(output_binary_normalized)
    else:
        output_binary_normalized = "+" + str(output_binary_normalized)
    return output_binary_normalized + f"*2^{base_range + additional_base_range}"


def decimal_float_to_binary(
    input_decimal_float: float, needed_range: int = 8, precision: int = 23
) -> str:
    output_binary_normalized, base_range, input_decimal_signed = normalize_decimal(
        input_decimal_float
    )
    mantissa = output_binary_normalized[2:]
    if len(mantissa) <= precision:
        mantissa = mantissa.ljust(precision, "0")
    else:
        mantissa = mantissa[:precision]
    characteristic = decimal_to_binary(base_range + 2 ** (needed_range - 1) - 1)
    sign = "1" if input_decimal_signed else "0"
    return sign + " " + characteristic + " " + mantissa


def main() -> None:
    input_decimal_float = input("Input number: ")
    if not is_float_number(input_decimal_float):
        print("Error: given number is not a float type")
        return None
    input_decimal_float = float(input_decimal_float)
    if isnan(input_decimal_float) or isinf(input_decimal_float):
        print("Error: given number cannot be inf or nan")
        return None
    print(f"Result: {decimal_in_exponential(input_decimal_float)}")
    float_mode = input(
        """Input preferable float containing type:
1. FP64
2. FP32
3. FP16
Your choice: """
    )
    while float_mode not in ["1", "2", "3"]:
        float_mode = input(
            """Error: input(NUMBER of) preferable float containing type:
        1. FP64
        2. FP32
        3. FP16
        Your choice: """
        )
    if float_mode == "1":
        print(
            f"{input_decimal_float} in FP64: {decimal_float_to_binary(input_decimal_float, 11, 52)}"
        )
    elif float_mode == "2":
        print(
            f"{input_decimal_float} in FP32: {decimal_float_to_binary(input_decimal_float)}"
        )
    else:
        print(
            f"{input_decimal_float} in FP16: {decimal_float_to_binary(input_decimal_float, 5, 10)}"
        )


if __name__ == "__main__":
    main()
