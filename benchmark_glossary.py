import time
import re
from functools import lru_cache

class OldTextNormalizer:
    def __init__(self):
        self.term_glossary = {f"term{i}": f"rep{i}" for i in range(100)}
        self.term_glossary["PCIe 5.0"] = "PCIE five"

    def apply_glossary_terms(self, text, lang="zh"):
        if not self.term_glossary:
            return text

        sorted_terms = sorted(self.term_glossary.keys(), key=len, reverse=True)
        @lru_cache(maxsize=42)
        def get_term_pattern(term: str):
            return re.compile(re.escape(term), re.IGNORECASE)
        transformed_text = text
        for term in sorted_terms:
            term_value = self.term_glossary[term]
            if isinstance(term_value, dict):
                replacement = term_value.get(lang, term_value.get(lang, term))
            else:
                replacement = term_value
            pattern = get_term_pattern(term)
            transformed_text = pattern.sub(replacement, transformed_text)

        return transformed_text

@lru_cache(maxsize=128)
def _get_term_pattern(term: str):
    return re.compile(re.escape(term), re.IGNORECASE)

class NewTextNormalizer:
    def __init__(self):
        self.term_glossary = {f"term{i}": f"rep{i}" for i in range(100)}
        self.term_glossary["PCIe 5.0"] = "PCIE five"
        self._sorted_terms_cache = sorted(self.term_glossary.keys(), key=len, reverse=True)

    def apply_glossary_terms(self, text, lang="zh"):
        if not self.term_glossary:
            return text

        transformed_text = text
        for term in self._sorted_terms_cache:
            term_value = self.term_glossary[term]
            if isinstance(term_value, dict):
                replacement = term_value.get(lang, term_value.get(lang, term))
            else:
                replacement = term_value
            pattern = _get_term_pattern(term)
            transformed_text = pattern.sub(replacement, transformed_text)

        return transformed_text

text = "This is a test text with PCIe 5.0 and term50 and term99."

old_norm = OldTextNormalizer()
new_norm = NewTextNormalizer()

# Warmup
for _ in range(10):
    old_norm.apply_glossary_terms(text)
    new_norm.apply_glossary_terms(text)

start = time.time()
for _ in range(10000):
    old_norm.apply_glossary_terms(text)
old_time = time.time() - start

start = time.time()
for _ in range(10000):
    new_norm.apply_glossary_terms(text)
new_time = time.time() - start

print(f"Old time: {old_time:.4f}s")
print(f"New time: {new_time:.4f}s")
print(f"Speedup: {old_time/new_time:.2f}x")
