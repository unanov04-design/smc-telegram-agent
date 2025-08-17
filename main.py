from fastapi import FastAPI, Request
import httpx, os

BOT = os.getenv("BOT_TOKEN")   # лишаємо старі назви змінних
CHAT = os.getenv("CHAT_ID")

app = FastAPI()

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/tv")
async def tv(req: Request):
    a = await req.json()

    sym   = a.get("sym","-");  tf   = a.get("tf","-")
    patt  = a.get("pattern",""); side = a.get("side","")
    entry = a.get("entry","");   sl   = a.get("sl",""); tp = a.get("tp","")
    rr    = a.get("rr","");      sess = a.get("session","")

    # пояснення
    bias  = a.get("htf_bias","n/a")
    poi   = a.get("poi","")
    asia  = a.get("asia","none")
    smt   = a.get("smt","none")
    news  = a.get("news","clear")
    note  = a.get("note","")

    bullets = []
    if bias != "n/a": bullets.append(f"• HTF bias (D1): {bias}")
    if poi:          bullets.append(f"• POI (H1): {poi} | Pattern: {patt}")
    if asia!="none": bullets.append(f"• Asia sweep: {asia}")
    if smt!="none":  bullets.append(f"• SMT (DXY): {smt}")
    bullets.append(f"• News: {news}")
    bullets.append(f"• Session: {sess}")

    text = (
        f"📊 SMC Signal — {sym} {tf} ({side})\n"
        f"Entry: {entry}  SL:{sl}  TP:{tp}  RR:{rr}\n"
        + "\n".join(bullets) +
        (f"\n📝 {note}" if note else "")
    )

    async with httpx.AsyncClient(timeout=15) as x:
        await x.post(f"https://api.telegram.org/bot{BOT}/sendMessage",
                     json={"chat_id": CHAT, "text": text})
    return {"ok": True}

