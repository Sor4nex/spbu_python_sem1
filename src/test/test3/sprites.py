import random


SPRITE_PARTICLE = "█"
SPRITE_PARTICLE_ABSENSE = "░"
ERROR_INPUT_SIZE = (
    "error: input number either too small or cannot be converted into number"
)
INPUT_INVITATION = "input sprite size: "
USER_INFO = 'to exit type "EXIT". to generate new sprite hit enter button'


def get_size_from_user() -> int:
    input_size = input(INPUT_INVITATION)
    while not input_size.isdigit():
        print(ERROR_INPUT_SIZE)
        input_size = input(INPUT_INVITATION)
    return int(input_size)


def generate_sprite(sprite_size: int) -> list[list[int]]:
    generation_function = random.choice(
        [
            generate_vertical_symmetric,
            generate_horizontal_symmetric,
            generate_both_symmetric,
        ]
    )
    return generation_function(sprite_size)


def generate_horizontal_symmetric(sprite_size: int) -> list[list[int]]:
    vertical_symmetric_sprite = generate_vertical_symmetric(sprite_size)
    return [
        [vertical_symmetric_sprite[i][j] for i in range(sprite_size)]
        for j in range(sprite_size)
    ]


def generate_vertical_symmetric(spite_size: int) -> list[list[int]]:
    sprite = []
    sprite_half_size = int(spite_size / 2)
    for _ in range(spite_size):
        sprite_row_half = [random.randint(0, 1) for _ in range(sprite_half_size)]
        if spite_size % 2 == 0:
            sprite.append(sprite_row_half + sprite_row_half[::-1])
        else:
            sprite.append(
                sprite_row_half + [random.randint(0, 1)] + sprite_row_half[::-1]
            )
    return sprite


def generate_both_symmetric(spite_size: int) -> list[list[int]]:
    sprite = [[] for _ in range(spite_size)]
    sprite_half_size = int(spite_size / 2)
    for i in range(sprite_half_size):
        sprite_row_half = [random.randint(0, 1) for _ in range(sprite_half_size)]
        if spite_size % 2 == 0:
            sprite[i] = sprite_row_half + sprite_row_half[::-1]
            sprite[-i - 1] = sprite_row_half + sprite_row_half[::-1]
            continue
        sprite[i] = sprite_row_half + [random.randint(0, 1)] + sprite_row_half[::-1]
        sprite[-i - 1] = (
            sprite_row_half + [random.randint(0, 1)] + sprite_row_half[::-1]
        )
    if spite_size % 2 != 0:
        row = [random.randint(0, 1) for _ in range(sprite_half_size)]
        sprite[sprite_half_size] = row + [random.randint(0, 1)] + row[::-1]
    return sprite


def print_sprite(sprite: list[list[int]]) -> None:
    result_string = ""
    for row in sprite:
        row = [
            SPRITE_PARTICLE if row[i] == 1 else SPRITE_PARTICLE_ABSENSE
            for i in range(len(row))
        ]
        result_string += "".join(row) + "\n"
    print(result_string)


def main() -> None:
    sprites_size = get_size_from_user()
    print(USER_INFO)
    command = ""
    while command != "exit":
        sprite = generate_sprite(sprites_size)
        print_sprite(sprite)
        command = input("command: ")


if __name__ == "__main__":
    main()
