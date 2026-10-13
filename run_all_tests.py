import sys
import types
from unittest.mock import MagicMock
import unittest

def create_mock_module(name):
    mock = types.ModuleType(name)
    mock.__spec__ = getattr(types.ModuleType, '__spec__', None)
    mock.__path__ = []
    return mock

def setup_mocks():
    mock_modules = [
        'torch', 'torch.nn', 'torch.nn.functional', 'torch.cuda', 'torch.backends.cuda',
        'diffusers', 'diffusers.utils', 'diffusers.utils.torch_utils',
        'transformers', 'transformers.modeling_outputs', 'transformers.models', 'transformers.models.gemma3',
        'einops', 'easydict', 'sentencepiece', 'wetext', 'tn', 'tn.chinese.normalizer', 'tn.english.normalizer',
        'yaml', 'numpy', 'mmgp', 'mmgp.offload', 'gradio', 'torchaudio', 'torchvision', 'tokenizers', 'librosa', 'tqdm',
        'safetensors.torch', 'models.wan.ovi.modules.mmaudio.test_vae', 'torch._prims_common',
    ]
    for mod in mock_modules:
        sys.modules[mod] = create_mock_module(mod)

    for mod in mock_modules:
        if mod == 'torch':
            sys.modules[mod].cuda = MagicMock()
            sys.modules[mod].cuda.get_device_capability = lambda *args, **kwargs: (8, 0)
            sys.modules[mod].Size = MagicMock()
            sys.modules[mod].Tensor = MagicMock()
            sys.modules[mod].device = MagicMock()
            sys.modules[mod].FloatTensor = MagicMock()
            sys.modules[mod].dtype = MagicMock()
            sys.modules[mod].nn = sys.modules['torch.nn']
            sys.modules[mod].nn.Module = MagicMock
            sys.modules[mod].float32 = MagicMock()
            sys.modules[mod].float16 = MagicMock()
            sys.modules[mod].bfloat16 = MagicMock()
        if mod == 'diffusers':
            sys.modules[mod].SchedulerMixin = type('DummyMixin', (), {})
        if mod == 'diffusers.utils':
            sys.modules[mod].logging = MagicMock()

    sys.modules['easydict'].EasyDict = dict
    sys.modules['einops'].rearrange = MagicMock()

setup_mocks()

if __name__ == '__main__':
    unittest.main(module=None, argv=['unittest', 'discover'])
