from __future__ import annotations

import os
import time
import httpx


class TelegramControlBot:
    def __init__(self):
        self.token = os.environ["TELEGRAM_BOT_TOKEN"]
        self.allowed = {int(x) for x in os.getenv("TELEGRAM_ALLOWED_CHAT_IDS", "").split(",") if x.strip()}
        if not self.allowed:
            raise SystemExit("TELEGRAM_ALLOWED_CHAT_IDS is required; refusing an open control bot")
        self.api_base = os.getenv("SYNERGY_COMPANY_API", "http://127.0.0.1:8788")
        self.api_token = os.getenv("SYNERGY_API_TOKEN", "")
        self.offset = 0

    def api_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}

    def tg(self, method: str, payload: dict):
        with httpx.Client(timeout=35.0) as c:
            r = c.post(f"https://api.telegram.org/bot{self.token}/{method}", json=payload)
            r.raise_for_status(); return r.json()

    def send(self, chat_id: int, text: str):
        self.tg("sendMessage", {"chat_id": chat_id, "text": text[:4000]})

    def handle(self, chat_id: int, text: str):
        if chat_id not in self.allowed:
            return
        cmd, *rest = text.strip().split(maxsplit=1)
        actor = f"telegram:{chat_id}"
        with httpx.Client(base_url=self.api_base, headers=self.api_headers(), timeout=30.0) as c:
            if cmd == "/status":
                r = c.get("/v1/status"); r.raise_for_status(); self.send(chat_id, str(r.json()))
            elif cmd == "/opportunities":
                r = c.get("/v1/opportunities"); r.raise_for_status(); self.send(chat_id, str(r.json()[:10]))
            elif cmd in {"/approve", "/reject", "/dispatch"} and rest:
                action_id = rest[0].strip()
                if cmd == "/dispatch": r = c.post(f"/v1/actions/{action_id}/dispatch")
                else:
                    verb = "approve" if cmd == "/approve" else "reject"
                    r = c.post(f"/v1/actions/{action_id}/{verb}", json={"actor": actor, "reason": "telegram command"})
                r.raise_for_status(); self.send(chat_id, str(r.json()))
            elif cmd in {"/pause", "/resume"}:
                r = c.post(f"/v1/{cmd[1:]}", json={"actor": actor, "reason": "telegram command"}); r.raise_for_status(); self.send(chat_id, str(r.json()))
            elif cmd == "/repos":
                r = c.get("/v1/repositories"); r.raise_for_status(); self.send(chat_id, f"Registered repositories: {len(r.json())}")
            else:
                self.send(chat_id, "Commands: /status /opportunities /approve ID /reject ID /dispatch ID /pause /resume /repos")

    def run(self):
        while True:
            data = self.tg("getUpdates", {"timeout": 30, "offset": self.offset})
            for u in data.get("result", []):
                self.offset = max(self.offset, u["update_id"] + 1)
                msg = u.get("message") or {}
                if "text" in msg:
                    self.handle(int(msg["chat"]["id"]), msg["text"])
            time.sleep(float(os.getenv("TELEGRAM_POLL_SECONDS", "2")))


if __name__ == "__main__": TelegramControlBot().run()
