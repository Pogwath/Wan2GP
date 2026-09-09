import sys
import types
from unittest.mock import MagicMock
import unittest

for mod_name in ['torch', 'numpy', 'diffusers', 'mmgp', 'gradio', 'sentencepiece', 'torchaudio', 'einops', 'transformers', 'easydict', 'torchvision', 'yaml']:
    mock = types.ModuleType(mod_name)
    mock.__spec__ = getattr(types.ModuleType, '__spec__', None)

    if mod_name == 'torch':
        mock.nn = types.ModuleType('torch.nn')
        mock.nn.__spec__ = getattr(types.ModuleType, '__spec__', None)
        mock.nn.functional = types.ModuleType('torch.nn.functional')
        mock.Size = MagicMock()
        mock.Tensor = MagicMock()
        mock.cuda = MagicMock()
        mock.cuda.get_device_capability = lambda *args, **kwargs: (8, 0)
        mock.device = MagicMock
        mock.nn.Module = MagicMock
        mock._prims_common = types.ModuleType('torch._prims_common')
        mock._prims_common.DeviceLikeType = MagicMock()
        sys.modules['torch.nn'] = mock.nn
        sys.modules['torch.nn.functional'] = mock.nn.functional
        sys.modules['torch._prims_common'] = mock._prims_common

    if mod_name == 'transformers':
        mock.models = types.ModuleType('transformers.models')
        sys.modules['transformers.models'] = mock.models
        mock.models.gemma3 = types.ModuleType('transformers.models.gemma3')
        mock.models.gemma3.Gemma3ForConditionalGeneration = MagicMock
        sys.modules['transformers.models.gemma3'] = mock.models.gemma3

    if mod_name == 'einops':
        mock.rearrange = MagicMock()

    if mod_name == 'easydict':
        mock.EasyDict = MagicMock

    if mod_name == 'mmgp':
        mock.offload = MagicMock()

    sys.modules[mod_name] = mock

sys.modules['models.wan.ovi.modules.mmaudio.test_vae'] = MagicMock()

if __name__ == '__main__':
    unittest.main(module=None, argv=['run_tests_mocked.py', 'discover'])
