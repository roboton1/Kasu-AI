from flask import Flask, render_template, request, jsonify
import json, os, random

app = Flask(__name__)

# ファイル保存先
BRAIN_FILE = 'brain.json'
CONFIG_FILE = 'config.json'

def load_data(file, default):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 学習・返信ロジック（前回のマルコフ連鎖を流用）
def learn(text, brain):
    if len(text) < 2: return
    for i in range(len(text) - 1):
        c, n = text[i], text[i+1]
        if c not in brain: brain[c] = []
        brain[c].append(n)
    if text[-1] not in brain: brain[text[-1]] = []
    brain[text[-1]].append(None)

def generate_reply(user_input, brain):
    if not brain: return "（まだ何も知らないよ。何か教えて！）"
    chars = [c for c in user_input if c in brain]
    curr = random.choice(chars) if chars else random.choice(list(brain.keys()))
    res = []
    for _ in range(30):
        if curr is None: break
        res.append(curr)
        curr = random.choice(brain.get(curr, [None]))
    return "".join(res)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('msg', '')
    brain = load_data(BRAIN_FILE, {})
    
    # 返信作成 -> 学習
    reply = generate_reply(user_msg, brain)
    learn(user_msg, brain)
    
    save_data(BRAIN_FILE, brain)
    return jsonify({'reply': reply})

@app.route('/settings', methods=['POST'])
def settings():
    data = request.json
    save_data(CONFIG_FILE, data)
    return jsonify({'status': 'ok'})

@app.route('/get_config')
def get_config():
    config = load_data(CONFIG_FILE, {'name': '無名のAI', 'image': 'https://placehold.jp/150x150.png'})
    return jsonify(config)

if __name__ == '__main__':
    app.run(debug=True)