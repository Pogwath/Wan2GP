import sys
import importlib.util
from unittest.mock import MagicMock

# Create mocks
sys.modules['sentencepiece'] = MagicMock()
sys.modules['yaml'] = MagicMock()
sys.modules['wetext'] = MagicMock()
sys.modules['tn'] = MagicMock()
sys.modules['tn.chinese.normalizer'] = MagicMock()
sys.modules['tn.english.normalizer'] = MagicMock()

import types
mock_common = types.ModuleType('models.TTS.index_tts2.utils.common')
mock_common.tokenize_by_CJK_char = lambda x: []
mock_common.de_tokenized_by_CJK_char = lambda x, do_lower_case=False: ""
sys.modules['models.TTS.index_tts2.utils.common'] = mock_common
sys.modules['.common'] = mock_common

# Load file directly
spec = importlib.util.spec_from_file_location("front", "models/TTS/index_tts2/utils/front.py")
front = importlib.util.module_from_spec(spec)
sys.modules["front"] = front
spec.loader.exec_module(front)

normalizer = front.TextNormalizer(enable_glossary=True)
normalizer.load_glossary({
    "PCIe 5.0": {"zh": "PCIE 五点零"},
    "M.2": {"zh": "M 二"}
})

text = "My PC uses a PCIe 5.0 graphics card and an m.2 ssd."
res = normalizer.apply_glossary_terms(text, lang="zh")
print(res)
assert "PCIE 五点零" in res
assert "M 二" in res

print("Tests passed!")
