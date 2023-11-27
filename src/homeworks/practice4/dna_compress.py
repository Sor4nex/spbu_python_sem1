from typing import Iterator
import string

INTRODUCTION = (
    "This program helps to compress and decompress DNA string.\n"
    "Example: aaabbbb will be compressed to a3b4, a2b1c4 will be decompressed to aabcccc."
)
COMMAND_INPUT_INVITATION = (
    "Type the number of command:\n" "\t1.Compress\n" "\t2.Decompress\n" "Your input: "
)
COMPRESS_VALUE_INPUT_INVITATION = "Type string to compress: "
DECOMPRESS_VALUE_INPUT_INVITATION = "Type string to decompress: "
SUCCESSFUL_RESULT = "Result:"

ERROR_COMPRESS_INPUT = "Error: you should type in non-null string with no numbers, spaces or punctuation, only with symbols(e.g.<aabbccdedd>)"
ERROR_DECOMPRESS_INPUT = "Error: you should type in non-null string in the format <AiBj...>, where A,B - symbols; i,j - relevant values count(e.g.<a3b4c1>)"
ERROR_COMMAND_INPUT = "Error: you should type NUMBER from the list(<1> or <2>)"


def is_input_to_compress_incorrect(input_to_compress: str) -> bool:
    return any(
        restricted_char in input_to_compress
        for restricted_char in string.digits + string.punctuation + " "
    )


def convert_compressed_str_to_list(input_to_decompress: str) -> list[str]:
    if len(input_to_decompress) == 0:
        raise ValueError("input argument length equals 0")
    current_symbol = input_to_decompress[0]
    current_symbol_count = ""
    input_converted = []
    for i in range(1, len(input_to_decompress)):
        symbol = input_to_decompress[i]
        if symbol in string.punctuation + " ":
            raise ValueError("input string do not match the scheme")
        if symbol.isdigit():
            if current_symbol_count == "" and symbol == "0":
                raise ValueError("input string do not match the scheme")
            current_symbol_count += symbol
            continue
        if current_symbol_count == "" or symbol == current_symbol:
            raise ValueError("input string do not match the scheme")
        input_converted.append(current_symbol + current_symbol_count)
        current_symbol, current_symbol_count = symbol, ""
    if current_symbol_count == "":
        raise ValueError("input string do not match the scheme")
    input_converted.append(current_symbol + current_symbol_count)
    return input_converted


def compress_dna(input_dna: list[str]) -> Iterator[str]:
    char_switches = (
        [False]
        + list(
            map(lambda i: input_dna[i - 1] == input_dna[i], range(1, len(input_dna)))
        )
        + [False]
    )
    for i in range(len(char_switches) - 1):
        if not char_switches[i]:
            yield input_dna[i] + str(char_switches.index(False, i + 1) - i)


def decompress_dna(input_dna_compressed: list[str]) -> Iterator[str]:
    return map(
        lambda single_gen: single_gen[0] * int(single_gen[1:]), input_dna_compressed
    )


def main() -> None:
    print(INTRODUCTION)
    command_input = input(COMMAND_INPUT_INVITATION)
    if command_input == "1":
        string_to_compress = input(COMPRESS_VALUE_INPUT_INVITATION)
        if (
            is_input_to_compress_incorrect(string_to_compress)
            or len(string_to_compress) == 0
        ):
            print(ERROR_COMPRESS_INPUT)
            return None
        compressed_dna = compress_dna(list(string_to_compress))
        print(SUCCESSFUL_RESULT, "".join(compressed_dna))
        return None
    elif command_input == "2":
        string_to_decompress = input(DECOMPRESS_VALUE_INPUT_INVITATION)
        try:
            string_to_decompress = convert_compressed_str_to_list(string_to_decompress)
        except ValueError:
            print(ERROR_DECOMPRESS_INPUT)
            return None
        decompressed_dna = decompress_dna(string_to_decompress)
        print(SUCCESSFUL_RESULT, "".join(decompressed_dna))
        return None
    print(ERROR_COMMAND_INPUT)


if __name__ == "__main__":
    main()
