def validate_user_input() -> int:
    user_input = input("Input number: ")
    signed = False
    while not user_input.isdigit():
        if user_input[0] == "-":
            signed = True
            user_input = user_input[1:]
            continue
        user_input = input("Error!: input number: ")
    if not signed:
        return int(user_input)
    return -int(user_input)


def get_encoding_bit_depth(first_decimal: int, second_decimal: int) -> int:
    for bit_depth in range(8, 100, 8):
        sum_decimal_abs = abs(first_decimal) + abs(second_decimal)
        if sum_decimal_abs <= 2 ** (bit_depth - 1) - 1:
            return bit_depth


def invert_direct_encoding_binary(input_binary_number: str) -> str:
    return "".join(["0" if digit == "1" else "1" for digit in input_binary_number])


def binary_decimal_to_straight(input_decimal: int, needed_bit_depth: int = 8) -> str:
    input_decimal_negative = False
    if input_decimal < 0:
        input_decimal = -input_decimal
        input_decimal_negative = True
    output_binary = ""
    while input_decimal > 0:
        output_binary += str(input_decimal % 2)
        input_decimal //= 2
    output_binary = output_binary[::-1].rjust(needed_bit_depth - 1, "0")
    if input_decimal_negative:
        return "1" + output_binary
    return "0" + output_binary


def binary_straight_to_reverse(input_binary_straight: str) -> str:
    if input_binary_straight[0] == "0":
        return input_binary_straight
    return "1" + invert_direct_encoding_binary(input_binary_straight)[1:]


def binary_reverse_to_additional(input_binary_reverse: str) -> str:
    if input_binary_reverse[0] == "0":
        return input_binary_reverse
    return operation_plus_binary(
        input_binary_reverse, "1".rjust(len(input_binary_reverse), "0")
    )


def convert_decimal_to_binary(input_decimal: int, needed_bit_depth: int = 8) -> str:
    binary_straight = binary_decimal_to_straight(input_decimal, needed_bit_depth)
    binary_reverse = binary_straight_to_reverse(binary_straight)
    binary_additional = binary_reverse_to_additional(binary_reverse)
    return binary_additional


def convert_binary_to_decimal(input_binary_additional: str) -> int:
    input_binary = binary_reverse_to_straight(
        binary_additional_to_reverse(input_binary_additional)
    )[1:]
    output_decimal = 0
    for i in range(len(input_binary)):
        coefficent = len(input_binary) - i - 1
        output_decimal += int(input_binary[i]) * (2**coefficent)
    if input_binary_additional[0] == "1":
        return -output_decimal
    return output_decimal


def binary_additional_to_reverse(input_binary_additional: str) -> str:
    if input_binary_additional[0] == "0":
        return input_binary_additional
    return operation_plus_binary(
        input_binary_additional, "1" * len(input_binary_additional)
    )


def binary_reverse_to_straight(input_binary_reverse: str) -> str:
    if input_binary_reverse[0] == "0":
        return input_binary_reverse
    return "1" + invert_direct_encoding_binary(input_binary_reverse)[1:]


def operation_plus_binary(
    first_binary: str, second_binary: str, *, encoding_type: str = "additional"
):
    def add_additional_term(
        binary_number: str, digit_before_additional_term: str, additional_term: str
    ) -> tuple[str, str]:
        if additional_term == "1":
            if digit_before_additional_term == "0":
                return binary_number + "1", "0"
            else:
                return binary_number + "0", "1"
        return binary_number + digit_before_additional_term, "0"

    result_binary = ""
    additional_term = "0"
    for digit_index_binary in range(len(first_binary) - 1, -1, -1):
        digit_of_first_binary = first_binary[digit_index_binary]
        digit_of_second_binary = second_binary[digit_index_binary]
        if digit_of_first_binary == digit_of_second_binary:
            result_binary, additional_term = add_additional_term(
                result_binary, "0", additional_term
            )
            if digit_of_first_binary == "1":
                additional_term = "1"
        else:
            result_binary, additional_term = add_additional_term(
                result_binary, "1", additional_term
            )
    result_binary = result_binary[::-1]
    if additional_term == "1" and encoding_type == "back":
        result_binary = operation_plus_binary(
            result_binary, "1".rjust(len(result_binary), "0")
        )
    return result_binary


def invert_additional_encoding_binary(input_binary_additional: str) -> str:
    input_binary_straight = binary_reverse_to_straight(
        binary_additional_to_reverse(input_binary_additional)
    )
    if input_binary_straight[0] == "0":
        return binary_reverse_to_additional(
            binary_straight_to_reverse("1" + input_binary_straight[1:])
        )
    return binary_reverse_to_additional(
        binary_straight_to_reverse("0" + input_binary_straight[1:])
    )


def operation_minus_binary(first_binary: str, second_binary: str) -> str:
    return operation_plus_binary(
        first_binary, invert_additional_encoding_binary(second_binary)
    )


def main() -> None:
    first_decimal = validate_user_input()
    second_decimal = validate_user_input()
    needed_bit_depth = get_encoding_bit_depth(first_decimal, second_decimal)
    first_binary = convert_decimal_to_binary(first_decimal, needed_bit_depth)
    second_binary = convert_decimal_to_binary(second_decimal, needed_bit_depth)
    binary_sum = operation_plus_binary(first_binary, second_binary)
    decimal_sum = convert_binary_to_decimal(binary_sum)
    binary_difference = operation_minus_binary(first_binary, second_binary)
    decimal_difference = convert_binary_to_decimal(binary_difference)
    print(
        f"""First decimal: {first_decimal}, in binary: {first_binary}
Second decimal: {second_decimal}, in binary: {second_binary}
Binary sum: {first_binary} + {second_binary} = {binary_sum}, in decimal: {decimal_sum}
Binary difference: {first_binary} - {second_binary} = {binary_difference}, in decimal: {decimal_difference}"""
    )


if __name__ == "__main__":
    main()
