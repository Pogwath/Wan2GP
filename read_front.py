with open('models/TTS/index_tts2/utils/front.py', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    print(f"{i:4d}: {line}", end='')
