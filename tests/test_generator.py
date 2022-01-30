from buzz import generator


def test_sample_single_word():
    a = ('foo', 'bar', 'foobar')
    word = generator.sample(a)
    assert word in a


def test_sample_multiple_words():
    a = ('foo', 'bar', 'foobar')
    words = generator.sample(a, 2)
    assert len(words) == 2
    assert words[0] in a
    assert words[1] in a
    assert words[0] is not words[1]


def test_generate_buzz_of_at_least_five_words():
    phrase = generator.generate_buzz()
    assert len(phrase.split()) >= 5

