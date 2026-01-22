import json
import os
import random

MEMORY_FILE = 'brain.json'

def load_brain():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    # 最初は空っぽ（無能状態）
    return {}

def save_brain(brain):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(brain, f, ensure_ascii=False, indent=4)

def learn(text, brain):
    """文章をバラバラにして、文字のつながりを覚える"""
    if len(text) < 2: return
    
    # 文字のつながりを記録（例：「こんにちは」なら「こ」の次は「ん」）
    for i in range(len(text) - 1):
        current_char = text[i]
        next_char = text[i+1]
        
        if current_char not in brain:
            brain[current_char] = []
        brain[current_char].append(next_char)
    
    # 文末の印
    last_char = text[-1]
    if last_char not in brain:
        brain[last_char] = []
    brain[last_char].append(None) # Noneは「ここで終わり」の意味

def generate_reply(user_input, brain):
    """覚えた文字のつながりをたどって、適当に文章を作る"""
    if not brain:
        return "（なにか教えて…）"

    # ユーザーが言った言葉の中からスタート地点を選ぶ（なければランダム）
    start_candidates = [c for c in user_input if c in brain]
    if not start_candidates:
        current_char = random.choice(list(brain.keys()))
    else:
        current_char = random.choice(start_candidates)

    result = []
    # 最大20文字までつなげる
    for _ in range(20):
        if current_char is None: break
        result.append(current_char)
        
        # 次の文字を記憶の中からランダムに選ぶ
        next_chars = brain.get(current_char, [None])
        current_char = random.choice(next_chars)
    
    return "".join(result)

def main():
    brain = load_brain()
    print("AI: ... (まだ何も知らない。何か話しかけて！)")

    while True:
        user_input = input("あなた: ").strip()
        if user_input.lower() in ["終了", "exit", "quit"]:
            print("AI: バイバイ！")
            break

        # 1. ユーザーの言葉から返信を作る
        reply = generate_reply(user_input, brain)
        print(f"AI: {reply}")

        # 2. ユーザーの言葉を学習して記憶を更新する
        learn(user_input, brain)
        save_brain(brain)

if __name__ == "__main__":
    main()