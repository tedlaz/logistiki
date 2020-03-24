def startswith_any(txts_tuple: tuple, filters_tuple: tuple) -> bool:
    """
    txt: The text to filter
    txt_tuple: A tuple with filter values
    Checks if any element of txts_tuple starts with any element of
           filters_tuple
    """
    for txt in txts_tuple:
        for txt_filter in filters_tuple:
            if txt.startswith(txt_filter):
                return True
    return False


def dec2grp(anum):
    return f'{anum}'.replace('.', ',')


if __name__ == '__main__':
    print(startswith_any(('60.05.04', '60.06.13'), ('60.00', '60.06')))
