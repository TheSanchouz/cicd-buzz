import sys

from buzz import generator


def test_stdout_random_sample():
    phrase = generator.generate_buzz()
    print(phrase, file=sys.stdout)


if __name__ == '__main__':
    test_stdout_random_sample()
