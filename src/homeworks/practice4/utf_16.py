INPUT_REQUEST = "Enter a string: "
OUTPUT_INTRO = "UTF-16 encoding:"
OUTPUT_TEMPLATE = "{}:\t{}\t{}"

ZERO_LEN_ERROR = "Error: cannot encode zero-length str"


def get_max_codepoint(input_str: str) -> int:
    return max(map(lambda x: ord(x), input_str))


def divide_by_octets_bin(bin_str: str) -> str:
    bin_str = bin_str.removeprefix("0b")
    return " ".join(bin_str[i - 8 : i] for i in range(8, len(bin_str) + 1, 8))


def get_needed_bit_length(input_string: str) -> tuple[int, int]:
    max_codepoint = get_max_codepoint(input_string)
    needed_length_bin, needed_length_hex = 16, 4
    if max_codepoint > 65535:
        needed_length_bin, needed_length_hex = 32, 6
    return needed_length_bin, needed_length_hex


def get_char_hex_unicode(input_char: str, needed_length: int = 4) -> str:
    decimal_unicode = ord(input_char)
    hex_unicode = "U+" + hex(decimal_unicode).removeprefix("0x").rjust(
        needed_length, "0"
    )
    return hex_unicode.upper()


def get_char_binary_unicode(input_char: str, needed_length: int = 16) -> str:
    decimal_unicode = ord(input_char)
    binary_unicode = (
        bin(decimal_unicode).removeprefix("0b").rjust(needed_length, "0").upper()
    )
    return binary_unicode


def parse_codepoints(
    input_string: str, needed_length_bin: int = 16, needed_length_hex: int = 4
) -> dict[str, dict[str, str]]:
    parsed_codepoints = {}
    for codepoint in input_string:
        parsed_codepoints[codepoint] = {
            "unicode_decimal": str(ord(codepoint)),
            "unicode_bin": get_char_binary_unicode(codepoint, needed_length_bin),
            "unicode_hex": get_char_hex_unicode(codepoint, needed_length_hex),
        }
    return parsed_codepoints


def print_parsed_input(input_str: str, parsed_chars: dict[str, dict[str, str]]) -> None:
    for char in input_str:
        char_unicode_bin = divide_by_octets_bin(parsed_chars[char]["unicode_bin"])
        print(
            OUTPUT_TEMPLATE.format(
                char, parsed_chars[char]["unicode_hex"], char_unicode_bin
            )
        )


def main() -> None:
    input_string = input(INPUT_REQUEST)
    if len(input_string) == 0:
        print(ZERO_LEN_ERROR)
        return None
    needed_length_bin, needed_length_hex = get_needed_bit_length(input_string)
    parsed_chars = parse_codepoints(input_string, needed_length_bin, needed_length_hex)
    print(OUTPUT_INTRO)
    print_parsed_input(input_string, parsed_chars)


if __name__ == "__main__":
    main()
