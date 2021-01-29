def generate_items_text_lines(items):
    CHARS_IN_ROW = 48
    CHARS_IN_LEFT_COL = 30
    strings_to_print = []

    # Header
    LEFT_COL_HEADER = 'Ime izdelka (EAN)'
    RIGHT_COL_HEADER = 'Količina'
    spaces_in_between = CHARS_IN_ROW - len(LEFT_COL_HEADER) - len(RIGHT_COL_HEADER)
    strings_to_print.append('{}{}{}'.format(LEFT_COL_HEADER, ' ' * spaces_in_between, RIGHT_COL_HEADER))

    # Items
    for item in items:
        name = item['name']
        ean = str(item['ean'])
        quantity = str(item['quantity'])
        # Divide name into substrings of CHARS_IN_LEFT_COL length
        name_substrings = [name[0 + i:CHARS_IN_LEFT_COL + i] for i in range(0, len(name), CHARS_IN_LEFT_COL)]
        for i, name_substring in enumerate(name_substrings):
            if i == 0:
                # First row
                spaces_in_between = CHARS_IN_ROW - len(name_substring) - len(quantity)
                strings_to_print.append('{}{}{}'.format(name_substring, ' ' * spaces_in_between, quantity))
            else:
                # Every other row
                spaces_in_between = CHARS_IN_ROW - len(name_substring)
                strings_to_print.append('{}{}'.format(name_substring, ' ' * spaces_in_between))
        # Last row (EAN)
        ean_substring = '({})'.format(ean)
        spaces_in_between = CHARS_IN_ROW - len(ean_substring)
        strings_to_print.append('{}{}'.format(ean_substring, ' ' * spaces_in_between))

    return strings_to_print
