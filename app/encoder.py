ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def encode(n: int) -> str:
    if n == 0:
        return ALPHABET[0]
    digits = []
    while n:
        digits.append(ALPHABET[n % 62])
        n //= 62
    return "".join(reversed(digits))


def decode(s: str) -> int:
    result = 0
    for ch in s:
        result = result * 62 + ALPHABET.index(ch)
    return result
