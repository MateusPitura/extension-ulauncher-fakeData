from src.fakeData.lorem import lorem


def generate_lorem(words):
    lorem_words = lorem.split()
    if words > len(lorem_words):
        return ' '.join(lorem_words)
    else:
        return ' '.join(lorem_words[:words])
