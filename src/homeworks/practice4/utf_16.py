INPUT_REQUEST = "Enter a string: "
OUTPUT_INTRO = "UTF-16 encoding:"
OUTPUT_TEMPLATE = "{}:\t{}\t{}"

ZERO_LEN_ERROR = "Error: cannot encode zero-length str"


def divide_by_octets_bin(bin_str: str) -> str:
    bin_str = bin_str.removeprefix("0b")
    return " ".join(bin_str[i - 8 : i] for i in range(8, len(bin_str) + 1, 8))


def get_char_hex_unicode(input_char: str) -> str:
    decimal_unicode = ord(input_char)
    hex_unicode = "U+" + hex(decimal_unicode).removeprefix("0x").rjust(4, "0")
    return hex_unicode.upper()


def get_char_binary_unicode(input_char: str) -> str:
    decimal_unicode = ord(input_char)
    if decimal_unicode < 65536:
        binary_unicode = bin(decimal_unicode).removeprefix("0b").rjust(16, "0")
        return binary_unicode
    bin_unicode = bin(decimal_unicode - 65536).removeprefix("0b").rjust(20, "0")
    major_bits = bin(int(bin_unicode[:10], 2) + 55296).removeprefix("0b")
    minor_bits = bin(int(bin_unicode[10:], 2) + 56320).removeprefix("0b")
    return major_bits + minor_bits


def parse_codepoints(input_string: str) -> dict[str, dict[str, str]]:
    parsed_codepoints = {}
    for codepoint in input_string:
        parsed_codepoints[codepoint] = {
            "unicode_decimal": str(ord(codepoint)),
            "unicode_bin": get_char_binary_unicode(codepoint),
            "unicode_hex": get_char_hex_unicode(codepoint),
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
    parsed_chars = parse_codepoints(input_string)
    print(OUTPUT_INTRO)
    print_parsed_input(input_string, parsed_chars)


if __name__ == "__main__":
    main()
