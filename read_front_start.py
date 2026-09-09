with open('models/TTS/index_tts2/utils/front.py', 'r') as f:
    lines = f.readlines()
for i in range(min(400, len(lines))):
    print(f"{i:4d}: {lines[i]}", end='')
