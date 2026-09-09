with open("models/TTS/index_tts2/utils/front.py", "r") as f:
    text = f.read()

import re

# find __init__
m = re.search(r'    def __init__\(self, enable_glossary=False\):(.*?)    def match_email', text, re.DOTALL)
print("--- INIT ---")
print(m.group(0))

m2 = re.search(r'    def load_glossary\(self, glossary_dict\):(.*?)    def load_glossary_from_yaml', text, re.DOTALL)
print("--- LOAD ---")
print(m2.group(0))

m3 = re.search(r'    def load_glossary_from_yaml\(self, glossary_path\):(.*?)    def save_glossary_to_yaml', text, re.DOTALL)
print("--- LOAD YAML ---")
print(m3.group(0))
