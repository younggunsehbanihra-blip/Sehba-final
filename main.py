import requests, time, json, os, threading
from flask import Flask
from groq import Groq

GROQ_API_KEY = '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'
TELEGRAM_TOKEN = '8631670973:AAFsXylA3d3OMYH3TSWT3AJ9cumCvZniY'
TELEGRAM_CHAT_ID = '8851728637'

FICHIER = "stats.json"
last_id = 0
client = Groq(api_key=GROQ_API_KEY)
app = Flask(__name__)
@app.route('/')
def home(): return "ONLINE"

def load():
    if os.path.exists(FICHIER):
        try:
            with open(FICHIER,"r") as f: return json.load(f)
        except: pass
    return {"gagnants":0,"perdants":0,"clv":0}
def save(d):
    with open(FICHIER,"w") as f: json.dump(d,f)
memo = load()

def tg(txt):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id":TELEGRAM_CHAT_ID,"text":txt,"parse_mode":"HTML"}, timeout=10)
    except: pass

def groq_call(p):
    c = client.chat.completions.create(messages=[{"role":"user","content":p}], model="openai/gpt-oss-120b", temperature=0.2, max_tokens=1000)
    return c.choices[0].message.content

def bot_loop():
    global last_id
    tg(f"🚀 V10.2 GRATUIT ONLINE - Tape /analyse")
    while True:
        try:
            r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last_id+1}&timeout=5", timeout=10).json()
            for u in r.get("result",[]):
                last_id = u["update_id"]
                txt = u.get("message",{}).get("text","").lower()
                if "/stats" in txt: tg(f"📊 {memo['gagnants']}/50")
                elif "/win" in txt: memo['gagnants']+=1; save(memo); tg(f"✅ {memo['gagnants']}/50")
                elif "/lose" in txt: memo['perdants']+=1; save(memo); tg(f"❌ {memo['gagnants']}/{memo['gagnants']+memo['perdants']}")
                elif "/analyse" in txt or "/coupon" in txt:
                    rep = groq_call("Genere 2 COUPONS SNIPER 2.20-2.80")
                    tg(f"<b>🎯 COUPON</b>\n<pre>{rep}</pre>")
        except: pass
        time.sleep(3)

threading.Thread(target=bot_loop, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
