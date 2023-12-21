def format_large_number(number):
    units = ['', 'K', 'M', 'B', 'T']
    unit_index = 0

    while abs(number) >= 1000 and unit_index < len(units) - 1:
        number /= 1000.0
        unit_index += 1

    return f"{number:.1f}{units[unit_index]}"
