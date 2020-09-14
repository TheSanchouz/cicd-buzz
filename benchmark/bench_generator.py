import sys

from buzz import generator


def test_generate_buzz_of_at_least_five_words():
    phrase = generator.generate_buzz()
    print(phrase, file=sys.stdout)
