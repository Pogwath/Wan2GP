import sys
import types
from unittest.mock import MagicMock

sys.modules['torch'] = types.ModuleType('torch'); sys.modules['torch'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['torch'].Tensor = MagicMock()
sys.modules['torch'].Size = MagicMock()
sys.modules['torch'].nn = types.ModuleType('torch.nn'); sys.modules['torch'].nn.__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['torch'].nn.Module = MagicMock
sys.modules['torch.nn'] = sys.modules['torch'].nn
sys.modules['torch.nn.functional'] = MagicMock()
sys.modules['torchaudio'] = types.ModuleType('torchaudio'); sys.modules['torchaudio'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['numpy'] = types.ModuleType('numpy'); sys.modules['numpy'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['sentencepiece'] = types.ModuleType('sentencepiece'); sys.modules['sentencepiece'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['diffusers'] = types.ModuleType('diffusers'); sys.modules['diffusers'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['transformers'] = types.ModuleType('transformers'); sys.modules['transformers'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['transformers.models'] = types.ModuleType('transformers.models'); sys.modules['transformers.models'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['einops'] = types.ModuleType('einops'); sys.modules['einops'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['einops'].rearrange = MagicMock()
sys.modules['gradio'] = types.ModuleType('gradio'); sys.modules['gradio'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['easydict'] = types.ModuleType('easydict'); sys.modules['easydict'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['easydict'].EasyDict = MagicMock()
sys.modules['torchvision'] = types.ModuleType('torchvision'); sys.modules['torchvision'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['mmgp'] = types.ModuleType('mmgp'); sys.modules['mmgp'].__spec__ = getattr(types.ModuleType, '__spec__', None)
sys.modules['mmgp'].offload = MagicMock()

sys.modules['models.wan.ovi.modules.mmaudio.test_vae'] = MagicMock()
sys.modules['models.CosyVoice'] = MagicMock()

if __name__ == '__main__':
    import unittest
    unittest.main(module=None, argv=['unittest', 'discover'])
