import sys
import types
from unittest.mock import MagicMock
import importlib.util

mock_common = types.ModuleType('models.TTS.index_tts2.utils.common')
mock_common.tokenize_by_CJK_char = MagicMock()
mock_common.de_tokenized_by_CJK_char = MagicMock()
sys.modules['models.TTS.index_tts2.utils.common'] = mock_common

sys.modules['sentencepiece'] = MagicMock()
sys.modules['wetext'] = MagicMock()
sys.modules['tn'] = MagicMock()
sys.modules['tn.chinese.normalizer'] = MagicMock()
sys.modules['tn.english.normalizer'] = MagicMock()
sys.modules['yaml'] = MagicMock()

spec = importlib.util.spec_from_file_location("models.TTS.index_tts2.utils.front", "models/TTS/index_tts2/utils/front.py")
front = importlib.util.module_from_spec(spec)
sys.modules["models.TTS.index_tts2.utils.front"] = front
spec.loader.exec_module(front)

import time
normalizer = front.TextNormalizer()
normalizer.term_glossary = {
    f"term_{i}": {"en": f"term_{i}_en", "zh": f"term_{i}_zh"} for i in range(100)
}
normalizer.term_glossary["M.2"] = {"en": "M dot two", "zh": "M 二"}

start = time.time()
for _ in range(1000):
    normalizer.apply_glossary_terms("m.2 is awesome and term_50 is good", "en")
end = time.time()
print(f"Current approach time: {end - start:.4f}s")
