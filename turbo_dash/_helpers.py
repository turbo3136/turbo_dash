import string
import random


def generate_random_string(length: int = 16) -> str:
    return ''.join(
        [random.choice(string.ascii_lowercase + string.digits) for n in range(length)]
    )
