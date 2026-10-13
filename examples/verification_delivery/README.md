# Verification delivery fixtures / Flujos sintéticos / 核验交付模拟

English: Python 3.10+ standard library only; no account, credential, network or payment. These fixtures teach application branching and persisted state, not real verification. The example.invalid link is deliberately non-executable. A live hosted link and signed provider callback require an authorized adapter, which this example does not implement. Approved grants only local fixture permissions after tenant/user/session binding and explicit customer policy. Free production phone checks currently do not return line type; an OTP recommendation does not send an OTP.

Español: Solo biblioteca estándar de Python 3.10+; sin cuenta, credenciales, red ni pagos. Son ejemplos sintéticos de decisiones y estado persistente, no verificaciones reales. El enlace example.invalid no funciona a propósito. Un enlace real y una firma de webhook requieren un adaptador autorizado no implementado aquí. Approved solo concede permisos locales de prueba tras comprobar organización, usuario, sesión y política. La ruta gratuita actual no devuelve el tipo de línea; recomendar OTP no envía un código.

中文：仅需 Python 3.10+ 标准库，不需要账号、凭证、联网或付款。模拟用于验证业务分支与持久化状态，不核验真人。example.invalid 链接刻意不可打开；真实链接及签名回调需另行接入授权适配器。Approved 仅在绑定与明确业务规则通过后更新本地模拟权限。免费生产路线不返回 line-type；需 OTP 不代表发送验证码。

```bash
cd examples/verification_delivery
python3 -m unittest -v test_delivery
python3 delivery.py phone --branch normal
python3 delivery.py phone --branch unknown
python3 delivery.py phone --branch provider_failure
python3 delivery.py phone --branch otp
python3 delivery.py identity --db /tmp/gridzen-delivery-fixture.sqlite
```

Input: task/branch, synthetic identifiers and customer policy boolean. Output: mode/state/next; identity status, permission_granted and grant_count. Phone unknown/failure never becomes a negative identity claim. Recover expires pending/review/unknown sessions at a bounded deadline; it recommends authorized refresh without making a provider call. Restart preserves state in SQLite; duplicate and late events do not grant twice. Unknown is distinct from unsupported, and a future live adapter must report real evidence explicitly rather than relabel these fixtures.

Entradas: tarea/rama, identificadores sintéticos y política. Salidas: modo/estado/siguiente paso, estado de sesión y contador de permisos. La recuperación expira sesiones pendientes; no consulta al proveedor. SQLite mantiene el estado tras reinicio. Eventos repetidos no duplican permisos. Desconocido y no compatible son distintos.

输入：任务、分支、合成标识和规则布尔值。输出：mode/state/next、会话状态及授权次数。未知与不支持区分；超时恢复不调用上游；SQLite 支持重启；重复与迟到事件不重复授权。正常输出示例：`{"mode":"synthetic_fixture","state":"simulated","valid":true,"line_type":"mobile","otp_sent":false,"live_line_type_available":false}`。

All tests are deterministic engineering checks. They do not prove an external project adopted the example, Agent superiority, search indexing or production success.

A new verified Declined correction can revoke a fixture permission; old pending events cannot downgrade an approved session. Reopening declined or expired sessions requires a separate customer review, not replaying an old Approved event. Production ordering and correction rules must follow the actual provider contract.

## Local hosted-link flow / Enlace local / 本地托管链接流程

```bash
python3 server.py --db /tmp/gridzen-hosted-fixture.sqlite --port 8787
# In a second terminal / Otra terminal / 第二个终端:
curl -s http://127.0.0.1:8787/sessions -H 'Content-Type: application/json' -d '{}'
# Open http://127.0.0.1:8787/verify/fixture-session and approve the fixture.
curl -s http://127.0.0.1:8787/sessions/fixture-session
curl -s http://127.0.0.1:8787/recover -H 'Content-Type: application/json' -d '{}'
```

The local link is executable but synthetic; it collects no identity information. The demo accepts fixture callbacks only. It does not authenticate a real webhook signature and must never be exposed as a production verification service. Restart with the same database to retain pending state. Session deadline is 60 seconds; start with a fresh database for an independent run. For Docker n8n, run this loopback service on the same host network; do not expose it publicly.

El enlace local funciona como simulación, no recoge documentos. No valida firmas reales. Reinicie con la misma base para recuperar el estado; plazo de 60 segundos. No publique este servidor.

本地链接可运行但仍是模拟，不采集资料、不验证真实回调签名、不可公网部署。重启使用同一数据库恢复状态；60 秒超时，独立实验使用新数据库。生产签名与真实托管链接仍未测试。
