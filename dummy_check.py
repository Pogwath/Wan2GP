class A:
    def __init__(self):
        self.term_glossary = {}

    def apply(self, text):
        if not self.term_glossary:
            return text
        return "changed"

print(A().apply("hello"))
