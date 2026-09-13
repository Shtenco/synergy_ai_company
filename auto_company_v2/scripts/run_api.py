from company_v2.core.settings import Settings
import uvicorn

s = Settings()
if s.bind_host not in {"127.0.0.1", "::1", "localhost"} and not s.api_token:
    raise SystemExit("Refusing non-loopback bind without SYNERGY_API_TOKEN")
uvicorn.run("company_v2.app:app", host=s.bind_host, port=s.bind_port, reload=False)
