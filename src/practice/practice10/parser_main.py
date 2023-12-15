import src.practice.practice10.parser as prs


ERROR = "Cannot parse with string"
RESULT = "result:"


def main() -> None:
    string = input("Input a string: ")
    try:
        parsed_string = prs.parse_tokens(string.split(" "))
    except TypeError:
        print(ERROR)
        return
    print(RESULT)
    prs.pretty_print(parsed_string)


if __name__ == "__main__":
    main()
