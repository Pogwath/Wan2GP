import sys
import types
from unittest.mock import MagicMock

for mod_name in ['torch', 'numpy', 'diffusers', 'mmgp', 'gradio', 'sentencepiece', 'torchaudio', 'einops', 'transformers', 'easydict', 'torchvision', 'yaml']:
    mock = types.ModuleType(mod_name)
    mock.__spec__ = getattr(types.ModuleType, '__spec__', None)
    if mod_name == 'torch':
        mock.Tensor = MagicMock
        mock.nn = MagicMock()
        mock.device = MagicMock
        mock.FloatTensor = MagicMock
    if mod_name == 'sentencepiece':
        mock.SentencePieceProcessor = MagicMock
    sys.modules[mod_name] = mock

sys.modules['shared.utils'] = MagicMock()
sys.modules['shared'] = MagicMock()

from models.TTS.index_tts2.utils.front import TextNormalizer
norm = TextNormalizer(enable_glossary=True)
norm.load_glossary({'M.2': {'zh': 'M二', 'en': 'M dot 2'}})
res = norm.apply_glossary_terms('M.2', lang='zh')
assert res == 'M二', res
print('Success!')
