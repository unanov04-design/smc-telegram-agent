from fastapi import FastAPI, Request
import httpx, os

BOT = os.getenv("BOT_TOKEN")
CHAT = os.getenv("CHAT_ID")

app = FastAPI()

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/tv")
async def tv(req: Request):
    try:
        a = await req.json()
    except Exception:
        return {"ok": False, "error": "Invalid JSON"}

    sym = a.get("sym", "-")
    tf = a.get("tf", "-")
    pattern = a.get("pattern", "")
    entry = a.get("entry", "")
    sl = a.get("sl", "")
    tp = a.get("tp", "")
    rr = a.get("rr", "")
    session = a.get("session", "")
    note = a.get("note", "")

    text = (f"🔔 {sym} {tf} | {pattern}\n"
            f"Entry: {entry}  SL:{sl}  TP:{tp}  RR:{rr}\n"
            f"Session: {session}\nNote: {note}")

    async with httpx.AsyncClient(timeout=15) as x:
        await x.post(f"https://api.telegram.org/bot{BOT}/sendMessage",
                     json={"chat_id": CHAT, "text": text})

    return {"ok": True}
