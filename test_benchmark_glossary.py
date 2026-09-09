import time
import re
from functools import lru_cache

class TextNormalizer:
    def __init__(self, enable_glossary=False):
        self.term_glossary = dict()

    def load_glossary(self, glossary_dict):
        if glossary_dict and isinstance(glossary_dict, dict):
            self.term_glossary.update(glossary_dict)

class OldTextNormalizer(TextNormalizer):
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

class NewTextNormalizer(TextNormalizer):
    def load_glossary(self, glossary_dict):
        super().load_glossary(glossary_dict)
        self._glossary_dirty = True

    def apply_glossary_terms(self, text, lang="zh"):
        if not self.term_glossary:
            return text

        if getattr(self, '_glossary_dirty', True):
            sorted_terms = sorted(self.term_glossary.keys(), key=len, reverse=True)
            lower_map = {term.lower(): term for term in sorted_terms}
            pattern_str = "|".join(re.escape(term) for term in sorted_terms)
            compiled_pattern = re.compile(pattern_str, re.IGNORECASE)

            self._glossary_lower_map = lower_map
            self._compiled_glossary_pattern = compiled_pattern
            self._glossary_dirty = False

        def replacer(match):
            matched_str = match.group()
            original_term = self._glossary_lower_map.get(matched_str.lower(), matched_str)
            term_value = self.term_glossary.get(original_term, matched_str)
            if isinstance(term_value, dict):
                return term_value.get(lang, original_term)
            return term_value

        return self._compiled_glossary_pattern.sub(replacer, text)


glossary = {
    "M.2 NVMe SSD": {"en": "M dot two NVMe SSD", "zh": "M 二 NVMe SSD"},
    "PCIe 5.0": {"en": "PCIE five", "zh": "PCIE 五点零"},
    "GPT-5-Nano": {"en": "GPT five Nano", "zh": "GPT 五 Nano"},
    "CosyVoice2": {"en": "Cosy Voice two", "zh": "Cosy Voice 二"},
    "Fish-Speech": {"en": "Fish Speech", "zh": "Fish Speech"},
    "XTTS": {"en": "X T T S", "zh": "X T T S"},
    "F5-TTS": {"en": "F five T T S", "zh": "F 五 T T S"},
}

text = "such as XTTS, CosyVoice2, Fish-Speech, and F5-TTS. GPT-5-Nano is the smallest and fastest variant. I use M.2 NVMe SSD and PCIe 5.0."

old_norm = OldTextNormalizer()
old_norm.load_glossary(glossary)

new_norm = NewTextNormalizer()
new_norm.load_glossary(glossary)

# Correctness check
old_res = old_norm.apply_glossary_terms(text, lang="zh")
new_res = new_norm.apply_glossary_terms(text, lang="zh")

print("Old output:", old_res)
print("New output:", new_res)
assert old_res == new_res, "Outputs do not match!"

# Benchmark
iterations = 10000

start = time.time()
for _ in range(iterations):
    old_norm.apply_glossary_terms(text, lang="zh")
old_time = time.time() - start

start = time.time()
for _ in range(iterations):
    new_norm.apply_glossary_terms(text, lang="zh")
new_time = time.time() - start

print(f"Old time: {old_time:.4f}s")
print(f"New time: {new_time:.4f}s")
print(f"Speedup: {old_time/new_time:.2f}x")
