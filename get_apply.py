import re

with open('models/TTS/index_tts2/utils/front.py', 'r') as f:
    text = f.read()

m = re.search(r'    def apply_glossary_terms\(self, text, lang="zh"\):(.*?)    def load_glossary\(self, glossary_dict\):', text, re.DOTALL)
print("    def apply_glossary_terms(self, text, lang=\"zh\"):" + m.group(1))
