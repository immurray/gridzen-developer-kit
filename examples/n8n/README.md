# Identity delivery fixture for n8n

**Synthetic only.** This workflow never creates a real identity session, validates a real signature, sends OTP, charges money or changes real customer permissions. It calls the same Python fixture state machine as the runnable examples.

1. Start `python3 examples/verification_delivery/server.py --db /tmp/gridzen-n8n-fixture.sqlite --port 8787`.
2. Import `identity-delivery-fixture.json` into n8n 2.42.7 (the isolated acceptance version), or a compatible version. No credentials are embedded.
3. Run **Start fixture**: a single fixture is created; a persisted Wait resumes after 65 seconds to recover a 60-second deadline. Reusing the same fixture does not create duplicates. A fresh independent experiment uses a fresh local SQLite database.
4. Activate the workflow locally. Send the callback below before the deadline, then repeat it. Expect `grant_count=1`, not 2. Change `tenant` to `fixture-wrong`: expect HTTP 422, no permission.
5. Stop the fixture service: callback error output remains unknown, not approved. Restart the service with the same database to retain state.

```bash
curl -fsS http://127.0.0.1:8787/sessions -H 'Content-Type: application/json' -d '{}'
curl -s http://127.0.0.1:5678/webhook/gridzen-fixture-callback -H 'Content-Type: application/json' -d '{"event":"fixture-approved","status":"Approved","policy":true}'
curl -s http://127.0.0.1:5678/webhook/gridzen-fixture-status
```

The HTTP nodes assume n8n and the fixture share the same **loopback network namespace**. Separate Docker containers do not share localhost. For isolated acceptance use `--network none` on n8n and `--network container:<n8n-container>` on the fixture; do not expose ports. For other local deployments adapt the HTTP node address deliberately, keeping the fixture private. This is a test template, not a live KYC product.

The import is inactive by default. Review before activation; never point fixture callbacks at a real permission endpoint. There is no second implementation of verification policy in the workflow.

中文：该模板复用本地模拟状态机，不核验真人、不含凭证、默认不激活。等待65秒后检查60秒截止时间；重复事件只授权一次，异常保持未知。Docker容器须明确共享环回网络，否则localhost不可互通。真实核验需要独立供应商签名验证与客户业务规则。

Español: Plantilla sintética, sin credenciales y desactivada por defecto. Reutiliza el estado local; espera 65 segundos para recuperar el plazo de 60. Los duplicados no conceden permisos dos veces. Los contenedores deben compartir explícitamente la red de loopback. Producción requiere firmas y política autorizadas.
