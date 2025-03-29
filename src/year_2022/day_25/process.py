

def snaf_to_dec(snafu: str) -> int:
    dec_digits: list[int] = []
    for snafu_digit in snafu[::-1]:
        try:
            dec_digit = int(snafu_digit)
        except ValueError as exc:
            if snafu_digit == '-':
                dec_digit = -1
            elif snafu_digit == '=':
                dec_digit = -2
            else:
                raise ValueError('Unknown snafu digit') from exc
        dec_digits.append(dec_digit)
    return sum([digit * 5 ** power for power, digit in enumerate(dec_digits)])


def dec_to_snaf(dec: int) -> str:
    assert dec > 0, "Negative number? No chance."
    snafu_digits = []
    dec_operand = dec
    while True:
        div_quot, div_rem = divmod(dec_operand, 5)
        if div_quot == 0 and div_rem == 0:
            return ''.join(reversed(snafu_digits))
        if div_rem in (3, 4):
            div_quot += 1
            div_rem -= 5
            snaf_digit = {-2: '=', -1: '-'}[div_rem]
        else:
            snaf_digit = str(div_rem)
        snafu_digits.append(snaf_digit)
        dec_operand = div_quot


def calc_fuel_requirement(reqs: str) -> str:
    dec_sum = sum([snaf_to_dec(snaf) for snaf in reqs.splitlines()])
    return dec_to_snaf(dec_sum)


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


def main() -> None:
    fuel_reqs = read_file()
    print(
        "SNAFU number for Bob's console:",
        calc_fuel_requirement(fuel_reqs),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
