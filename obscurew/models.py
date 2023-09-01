class Word:
    def __init__(self, term, meaning):
        self.term = term
        self.meaning = meaning

    def __str__(self):
        return f'{self.term}'