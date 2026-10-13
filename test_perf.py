import time
import re
from functools import lru_cache

class TextNormalizerOriginal:
    def __init__(self):
        self.term_glossary = {f"Term{i}": f"Rep{i}" for i in range(100)}
        self.term_glossary["LongTermNameHere"] = "RepLong"

    def apply_glossary_terms(self, text, lang="zh"):
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

class TextNormalizerOptimized:
    def __init__(self):
        self.term_glossary = {f"Term{i}": f"Rep{i}" for i in range(100)}
        self.term_glossary["LongTermNameHere"] = "RepLong"
        self._compiled_glossary_keys = None
        self._sorted_compiled_patterns = []

    def load_glossary(self, glossary_dict):
        self.term_glossary.update(glossary_dict)
        self._compiled_glossary_keys = None # invalidate cache

    def _ensure_glossary_cache(self):
        current_keys = tuple(self.term_glossary.keys())
        if self._compiled_glossary_keys != current_keys:
            sorted_terms = sorted(current_keys, key=len, reverse=True)
            patterns = []
            for term in sorted_terms:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                patterns.append((term, pattern))
            self._sorted_compiled_patterns = patterns
            self._compiled_glossary_keys = current_keys # update last

    def apply_glossary_terms(self, text, lang="zh"):
        if not self.term_glossary:
            return text

        self._ensure_glossary_cache()
        transformed_text = text
        text_lower = transformed_text.lower() # fast substring pre-check

        for term, pattern in self._sorted_compiled_patterns:
            term_lower = term.lower()
            if term_lower in text_lower:
                term_value = self.term_glossary[term]
                if isinstance(term_value, dict):
                    replacement = term_value.get(lang, term_value.get(lang, term))
                else:
                    replacement = term_value
                transformed_text = pattern.sub(replacement, transformed_text)
                text_lower = transformed_text.lower()
        return transformed_text

def run_bench():
    text = "This is a test with LongTermNameHere and Term42 and Term99 and some other text that doesn't match."

    orig = TextNormalizerOriginal()
    opt = TextNormalizerOptimized()

    # Warmup
    for _ in range(10):
        orig.apply_glossary_terms(text)
        opt.apply_glossary_terms(text)

    n = 10000

    t0 = time.time()
    for _ in range(n):
        orig.apply_glossary_terms(text)
    t1 = time.time()

    t2 = time.time()
    for _ in range(n):
        opt.apply_glossary_terms(text)
    t3 = time.time()

    print(f"Original: {t1-t0:.4f}s")
    print(f"Optimized: {t3-t2:.4f}s")
    print(f"Speedup: {(t1-t0)/(t3-t2):.2f}x")

run_bench()
