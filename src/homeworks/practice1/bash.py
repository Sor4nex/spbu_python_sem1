import sys


def calculate_byte_size(string: str) -> int:
    return len(string.encode('utf-8'))


def parse_args(args: list) -> dict:
    parsed_arguments = {'operation': None, 'txt_file': None}
    for i in range(len(args)):
        if args[i] in ['wc', 'head', 'tail']:
            if parsed_arguments['operation'] is not None:
                parsed_arguments['Error'] = 'multiply operations invocation'
                break
            parsed_arguments['operation'] = args[i]
        if '.txt' in args[i]:
            if parsed_arguments['operation'] is None:
                parsed_arguments['Error'] = 'no operation was invocated or invalid argument order'
                break
            parsed_arguments['txt_file'] = args[i]
        elif args[i] in ['-c', '-n', '-m', '-l', '-w']:
            if parsed_arguments['operation'] is None:
                parsed_arguments['Error'] = 'no operation was invocated or invalid argument order'
                break
            if (parsed_arguments['operation'] == 'wc' and args[i] == '-n') \
                    or ((parsed_arguments['operation'] == 'head' or parsed_arguments['operation'] == 'tail')
                        and args[i] in ['-l', '-w', '-m']):
                parsed_arguments['Error'] = 'invalid argument given'
            parsed_arguments[args[i]] = (int(args[i + 1]) if i < len(args) - 1 and args[i + 1].isdigit() else None)
    if parsed_arguments['operation'] is None:
        parsed_arguments['Error'] = 'no operation was invocated, or invalid argument order'
    elif parsed_arguments['txt_file'] is None:
        parsed_arguments['Error'] = 'no file was given'
    return parsed_arguments


def operation_wc(parsed_arguments: dict) -> list:
    func_output = list()
    no_arguments = True if len(parsed_arguments.keys()) == 2 else False
    counters = {'lines': 0, 'words': 0, 'size': 0, 'symbols': 0}
    with open(parsed_arguments['txt_file'], 'r', encoding='utf-8') as given_file:
        single_string = given_file.readline()
        while single_string != '':
            counters['lines'] += 1 if ('\n' in single_string) else 0
            counters['words'] += len(single_string.split(' ')) if '' != single_string.strip() else 0
            counters['size'] += calculate_byte_size(single_string)
            counters['symbols'] += len(single_string)
            single_string = given_file.readline()
    if ('-l' in parsed_arguments) or no_arguments:
        func_output.append(counters['lines'])
    if ('-w' in parsed_arguments) or no_arguments:
        func_output.append(counters['words'])
    if ('-c' in parsed_arguments) or no_arguments:
        func_output.append(counters['size'])
    if '-m' in parsed_arguments:
        func_output.append(counters['symbols'])
    func_output.append(parsed_arguments['txt_file'])
    return func_output


def operation_head(parsed_arguments: dict) -> list:
    func_output = list()
    needs = {'lines': 10, 'size': None}
    if '-n' in parsed_arguments.keys():
        needs['lines'] = parsed_arguments['-n'] if parsed_arguments['-n'] is not None else 10
    elif '-c' in parsed_arguments.keys():
        needs['lines'] = None
        needs['size'] = parsed_arguments['-c'] if parsed_arguments['-c'] is not None else 10
    with open(parsed_arguments['txt_file'], encoding='utf-8') as given_file:
        if needs['size'] is None:
            single_string = given_file.readline().strip()
            while needs['lines'] != 0:
                func_output.append(single_string)
                needs['lines'] -= 1
                single_string = given_file.readline().strip()
        else:
            single_string = given_file.readline().strip()
            while needs['size'] > 1:
                if calculate_byte_size(single_string) <= needs['size']:
                    func_output.append(single_string)
                    needs['size'] -= calculate_byte_size(single_string)
                else:
                    for i in range(len(single_string), 0, -1):
                        if calculate_byte_size(single_string[:i]) <= needs['size']:
                            func_output.append(single_string[:i])
                            needs['size'] -= calculate_byte_size(single_string[:i])
                            break
                single_string = given_file.readline().strip()
    return func_output


def operation_tail(parsed_arguments: dict) -> list:
    func_output = list()
    with open(parsed_arguments['txt_file'], encoding='utf-8') as file:
        usr_input_txt = file.read().strip()
        file.close()
    if len(parsed_arguments.keys()) == 2:
        strs_output = usr_input_txt.split('\n')[-10:]
        for i in range(len(strs_output)):
            func_output.append(strs_output[i])
    else:
        if '-n' in parsed_arguments.keys():
            frst_str = (int(parsed_arguments['-n']) if parsed_arguments['-n'] is not None else 10)
            strs_output = usr_input_txt.split('\n')[-frst_str:]
            for i in range(len(strs_output)):
                func_output.append(strs_output[i])
        elif '-c' in parsed_arguments.keys():
            frst_symbol = (int(parsed_arguments['-c']) if parsed_arguments['-c'] is not None else 10)
            for i in range(len(usr_input_txt) - 1, 0, -1):
                if calculate_byte_size(usr_input_txt[i:]) > frst_symbol:
                    func_output.append(usr_input_txt[i+1:])
                    break
    return func_output


if __name__ == '__main__':
    operation = None
    parsed_arguments = parse_args(sys.argv)
    if 'Error' in parsed_arguments.keys():
        print('Error:', parsed_arguments['Error'])
        sys.exit(0)
    if parsed_arguments['operation'] == 'wc':
        print(*operation_wc(parsed_arguments))
    elif parsed_arguments['operation'] == 'head' or parsed_arguments['operation'] == 'tail':
        for string in operation_head(parsed_arguments) if parsed_arguments['operation'] == 'head' else operation_tail(
                parsed_arguments):
            print(string)
