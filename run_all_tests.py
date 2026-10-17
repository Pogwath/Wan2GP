import sys
import types
from unittest.mock import MagicMock

def create_safe_mock(name):
    mock = types.ModuleType(name)
    mock.__spec__ = getattr(types.ModuleType, '__spec__', None)
    mock.__path__ = []
    return mock

mocks = [
    'torch', 'torch.cuda', 'torch.cuda.amp', 'torch.nn', 'torch.nn.functional', 'torch.backends', 'torch.backends.cuda', 'torch._prims_common', 'torch.compiler',
    'numpy', 'diffusers', 'diffusers.utils', 'diffusers.utils.torch_utils', 'diffusers.configuration_utils', 'diffusers.schedulers',
    'diffusers.schedulers.scheduling_utils', 'huggingface_hub',
    'mmgp', 'mmgp.offload', 'safetensors', 'safetensors.torch',
    'transformers', 'transformers.models', 'transformers.models.gemma3', 'transformers.modeling_outputs',
    'easydict', 'einops', 'gradio', 'sentencepiece', 'torchaudio', 'torchvision', 'tokenizers', 'librosa', 'tqdm',
    'wetext', 'tn', 'tn.chinese.normalizer', 'tn.english.normalizer', 'yaml', 'models.wan.ovi.modules.mmaudio.test_vae',
    'models.ltx2.ltx_pipelines', 'models.ltx2.ltx_pipelines.utils'
]

for m in mocks:
    sys.modules[m] = create_safe_mock(m)

torch_mock = sys.modules['torch']
torch_mock.Size = MagicMock()
torch_mock.Tensor = MagicMock()
torch_mock.device = MagicMock()
torch_mock.FloatTensor = MagicMock()
torch_mock.dtype = MagicMock()
torch_mock.float32 = MagicMock()
torch_mock.bfloat16 = MagicMock()
torch_mock.float16 = MagicMock()
torch_mock.Generator = MagicMock()
torch_mock.nn = sys.modules['torch.nn']
torch_mock.nn.Module = MagicMock()
torch_mock.nn.ModuleList = MagicMock()
torch_mock.nn.Linear = MagicMock()
torch_mock.cuda = sys.modules['torch.cuda']
torch_mock.cuda.amp = sys.modules['torch.cuda.amp']
torch_mock.cuda.get_device_capability = lambda *args, **kwargs: (8, 0)
torch_mock.compiler = sys.modules['torch.compiler']
torch_mock.compiler.disable = MagicMock(return_value=lambda x: x)
sys.modules['torch._prims_common'].DeviceLikeType = MagicMock()
sys.modules['diffusers'].SchedulerMixin = type('DummyMixin', (), {})
sys.modules['diffusers.configuration_utils'].ConfigMixin = type('ConfigMixin', (), {})
sys.modules['diffusers.configuration_utils'].register_to_config = lambda x: x
sys.modules['diffusers.utils'].logging = MagicMock()
sys.modules['diffusers.schedulers.scheduling_utils'].KarrasDiffusionSchedulers = MagicMock()
sys.modules['diffusers.schedulers.scheduling_utils'].SchedulerMixin = type('DummyMixin', (), {})
sys.modules['diffusers.schedulers.scheduling_utils'].SchedulerOutput = type('DummySchedulerOutput', (), {})
sys.modules['einops'].rearrange = MagicMock()
sys.modules['easydict'].EasyDict = MagicMock()
sys.modules['transformers.models.gemma3'].Gemma3ForConditionalGeneration = MagicMock()
sys.modules['models.ltx2.ltx_pipelines'].DistilledPipeline = MagicMock()
sys.modules['models.ltx2.ltx_core.text_encoders.gemma'] = MagicMock()

import unittest
if __name__ == '__main__':
    unittest.main(module=None, argv=['unittest', 'discover'])
