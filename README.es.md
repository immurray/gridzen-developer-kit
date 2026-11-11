# Kit de desarrollo Gridzen 0.7.2

[Integración directa o GridZen: evalúe su tarea](docs/verification-evaluation.md#español) · [Preparación y costes](https://gridzen.ai/console/learn?lang=es&source=developer_kit#decision-fit)

[Plan por verificación y requisitos de activación](https://gridzen.ai/console/quote?lang=es) · [JSON](https://gridzen.ai/console/api/commercial/options)

## Ejecutar ejemplos de tareas

- [Primera integración de identidad](https://gridzen.ai/console/learn/identity-first-run?lang=es)
- [Límites de teléfonos de registro](https://gridzen.ai/console/learn/phone-check-boundaries?lang=es)
- [Recuperar callbacks retrasados](https://gridzen.ai/console/learn/callback-recovery?lang=es)
- [Permisos después de verificar](https://gridzen.ai/console/learn/business-permission-boundary?lang=es)

[SQLite](examples/verification_delivery/) · [n8n](examples/n8n/)

Los ejemplos son sintéticos. Los precios publicados por producto y su disponibilidad se rigen por la consola del comerciante; la activación comercial sigue sin estar disponible.


## Probar inmediatamente sin registro

Abra la [prueba inmediata de GridZen](https://gridzen.ai/console/start?lang=es) para simular comprobaciones telefónicas e incorporación de identidad sin cuenta, clave ni aprobación. Los escenarios de éxito, rechazo e indisponibilidad no llaman a proveedores reales ni verifican personas. Los agentes pueden usar el [MCP de prueba sin clave](https://gridzen.ai/console/downloads/quickstart_mcp.py) con `mcp==2.3.0` y `httpx==0.28.1` en un entorno virtual.

Conecte una cuenta sandbox con correo verificado para guardar registros y recibir callbacks. El acceso real depende de cada producto: algunas rutas permiten pruebas limitadas y otras siguen sin estar disponibles. Consulta capacidades y permisos autenticados; un precio publicado no habilita compras. El paquete y el MCP Registry remoto tienen versiones independientes; instalar no concede permisos de comerciante.

Investigación sobre 198 países y territorios, planificación de integraciones, cinco resultados simulados, CLI/SDK HTTP de Python, MCP local y 14 Skills. El MCP público de investigación y simulación no llama a proveedores reales; los perfiles de comerciante requieren autorización separada. Ningún resultado simulado verifica a una persona real.

Prueba y guía: https://gridzen.ai/developers/ . El selector permite cambiar entre español, inglés y chino, y recuerda la elección. La investigación es del 2026-10-07; las fuentes y sus restricciones se conservan en el idioma original.

## Instalación

Descarga y descomprime gridzen-developer-kit.zip. Ejecuta lo siguiente desde el directorio que contiene la carpeta extraída. Se requiere Python 3.11 o posterior.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install './gridzen-developer-kit[mcp]'
gridzen plan --country ID --event onboarding
gridzen simulate --country ID --capability bank_account_match --scenario timeout
python gridzen-developer-kit/examples/customer_tasks.py
```

En Windows, activa con `.venv\Scripts\activate`. La CLI y MCP local funcionan sin conexión tras instalar las dependencias; el SDK HTTP y el ejemplo de Python llaman al entorno público de pruebas.

## MCP y Skills

Añade un servidor stdio local a un cliente compatible y sustituye command por la ruta instalada:

```json
{"mcpServers":{"gridzen":{"command":"/absolute/path/to/.venv/bin/gridzen-mcp","args":[]}}}
```

Prueba: «Planifica una verificación de incorporación para Indonesia y simula una espera agotada del proveedor». Las cinco herramientas consultan cobertura, planifican, generan simulaciones, recuperan pruebas y explican resultados. La configuración depende del cliente; no hay endpoint MCP remoto de producción.

Copia cada carpeta de `skills/` al directorio de habilidades del agente, conservando `SKILL.md` y sus referencias. Los 6 Skills de investigación/flujos cubren selección, integración de pruebas, explicación de resultados, preparación de permisos, políticas de revisión de evidencia y planificación de pilotos en México. Los identificadores permanecen en inglés; el agente puede explicar los resultados en español.

## Interpretación

- match: coincidencia simulada; no autoriza altas reales ni acciones en producción.
- mismatch: discrepancia simulada; no demuestra fraude.
- not_found: sin registro simulado; no concluyente.
- timeout: espera agotada simulada; no concluyente.
- unsupported: canal no compatible simulado; no concluyente.

Todos los resultados conservan `simulated=true`, `verified=false` y `live_available=false`. Solo se aceptan los campos documentados de país, capacidad y escenario; no datos personales, documentos, cuentas bancarias ni credenciales. Los ID representan pruebas reutilizables, no transacciones reales.

Se incluyen ejemplos de Python y Next.js. Esquema API: https://gridzen.ai/developers/api/openapi.json . La evidencia de investigación no equivale a autorización comercial. Para evaluar un piloto real, envía país, capacidad y volumen previsto a open@gridzen.ai.

## Distribución pública y MCP remoto (0.2.0)

URL: `https://gridzen.ai/developers/mcp`, sin cuenta ni clave API.
Los cinco servicios ofrecen investigación y simulación; no hay proveedores
activos. La conexión remota envía los argumentos documentados a Gridzen.
El servidor local stdio sigue funcionando sin conexión después de instalarse.

Skills: `npx skills add immurray/gridzen-developer-kit`.
Código: https://github.com/immurray/gridzen-developer-kit . El paquete de PyPI
aún no está publicado: utilice GitHub Releases o la descarga del sitio web.
Código original bajo MIT; consulte NOTICE.md para los derechos de terceros.

## Publicación en directorios

El código, las descargas, la entrada oficial de MCP Registry y tres páginas de Skills.sh están publicados. La propuesta del catálogo de Docker está pendiente de revisión. Consulta [el registro de publicación](https://github.com/immurray/gridzen-developer-kit/blob/main/distribution/STATUS.md).


## 14 bundled Skills (0.7.2)

`python -m pip install gridzen-developer-kit` installs the CLI, stdio MCP dependencies
and all 14 Skill directories.

The 14 Skills comprise 6 research/workflow Skills and 8 single-task profiles. Of the 8 profiles, 3 run offline and 5 merchant profiles require separate authorization. Five public MCP tools provide research/synthetic operations. No live identity verification. No extra MCP
dependency installation is required. Check available versions on
[PyPI](https://pypi.org/project/gridzen-developer-kit/).

```sh
gridzen coverage --country MX
gridzen skills
gridzen-mcp
```

Connect `gridzen-mcp` as your client's stdio server, or use the remote endpoint
`https://gridzen.ai/developers/mcp`. `gridzen skills` prints the installed directories;
copy a complete directory into your assistant's configured Skills directory to
activate it. Installing a wheel does not automatically activate a client's Skills.

The existing select/integrate/explain Skills remain available. Added offline
workflows, version 1.0.0, cover evaluation scope, evidence-review policies and
provider-rights readiness. Each includes MIT, README, complete response fixtures
and agent acceptance prompts. They make no third-party calls and grant no real
verification, legal approval or regulatory conclusion.

## Configura diez clientes

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gridzen-developer-kit
gridzen setup --client all --project .
gridzen setup --client all --project . --apply
```

Usa Python 3.11+ en un entorno virtual. Primero revisa el resultado y después añade --apply. No cambia configuraciones globales. Desktop y Cline requieren importación manual; los demás necesitan confianza del proyecto. Configuración no equivale a aceptación del cliente o modelo.

[Instructions / 使用说明](https://gridzen.ai/developers/harnesses.html) · [Compatibility / 测试记录](clients/compatibility.json)


## Customer tasks and voluntary feedback (0.6.0)

```sh
gridzen plan --country US --event onboarding --task signup_phone
gridzen plan --country US --event onboarding --task identity_onboarding
gridzen plan --country US --event onboarding --task identity_onboarding --stage production
python examples/customer_tasks.py
gridzen feedback --task signup_phone --country US --outcome blocked --blocker missing_workflow_step --output task-summary.json
# Only after choosing to share:
gridzen feedback --input task-summary.json --share
```

Phone intelligence is not OTP or ownership verification. Identity fixtures are not hosted document/liveness sessions. Provider intake Skills are for provider operations/BYO, not a universal customer gate.

Remote APIs count fixed task/capability/country/stage/error categories for 90 days, including technical failures. They store no arguments, identity data, credentials, raw chats or per-user tracking. Local feedback is off by default. After explicit opt-in, CLI and stdio MCP automatically upload category-only events. Reading static Skills remains unobservable. Optional feedback requires explicit consent, contains only fixed categories, and is unverified self-reported evidence. A SHA-256 hash of its random receipt ID is retained 30 days for 30-day retry deduplication; the ID itself is not stored. Counters are capped at 10,000 requests/day and 500 summaries/day per database; missing history or offline usage is unknown. Requests are not unique customers.

## Optional automatic local feedback (0.6.0)

```sh
gridzen telemetry status
# Run only after reading and agreeing to category-only automatic sharing:
gridzen telemetry enable --consent
gridzen plan --country US --event onboarding --task signup_phone
# Send one queued event per invocation after reconnecting:
gridzen telemetry flush
# Disable future uploads and clear the pending queue:
gridzen telemetry disable
```

No network calls occur from local CLI/MCP when disabled. Consent is saved per OS user, not silently added to a project. Events contain only documented categories, ISO country, and a random per-event receipt, with no conversation, identity fields, credentials, user or project IDs. Feedback failures do not fail tool execution. The local queue is capped at 1,000 events/30 days; reconnect or `flush` retries one queued event, with a one-second HTTP timeout. Uploads are self-reported usage, not authenticated customers or completed verification. No background daemon is installed. Merely reading a Skill is unobservable; after consent, an Agent can explicitly record a fixed-category task summary.

La telemetría está desactivada por defecto. Tras consentimiento explícito, CLI y stdio envían categorías automáticamente. `gridzen telemetry disable` desactiva y borra la cola. Sin conexión: máximo 1000 eventos durante 30 días. Cada llamada o flush reintenta un evento; no hay servicio en segundo plano. No se envían conversaciones, identidad, credenciales ni IDs de usuarios/proyectos. Leer un Skill no se observa; un Agent puede registrar un resumen tras consentimiento previo. Son datos autodeclarados, no clientes autenticados.

Local queued events expire after 30 days and are removed on the next enqueue/flush. Daily aggregates use server receipt date; delayed uploads are not proof that work occurred on that date.

## Piloto independiente con aprobación del responsable

El paquete y sus cinco herramientas públicas conservan sus límites de investigación y simulación. Puede solicitar un piloto independiente de validez básica del teléfono e incorporación de identidad: [solicitud](https://gridzen.ai/console/pilot?lang=es), [guía](https://gridzen.ai/console/pilot-guide?lang=es), [alcance](https://gridzen.ai/es/guides/customer-pilot/).

Solicitar no activa producción. El responsable confirma derechos del proveedor, acuerdos, capacidades, límites y vencimiento; solo se usan cupos gratuitos confirmados. El piloto utiliza un cliente MCP separado y una clave comercial. No envíe documentos, caras ni claves del proveedor al MCP público. La validez básica no proporciona OTP ni prueba de titularidad.

Se validaron una consulta real de teléfono y la lectura de una sesión histórica Approved del operador mediante API/MCP. Falta validar la finalización humana de una sesión nueva y su webhook final real. Pruebas internas, descargas e interés declarado no demuestran demanda. Esta actualización documental no cambia versiones de PyPI ni Registry.


Use `gridzen start --task identity_onboarding --lang es` para encontrar la prueba anónima, la cuenta gratuita de sandbox y el asistente. El comando no hace llamadas de red. La medición de progreso requiere consentimiento opcional en la consola. Completar el sandbox no verifica a una persona real; la activación comercial sigue sin estar disponible.

## Guías y ejemplos ejecutables

[Identity](https://gridzen.ai/console/learn/identity-first-run) · [Phone](https://gridzen.ai/console/learn/phone-check-boundaries) · [Callbacks](https://gridzen.ai/console/learn/callback-recovery) · [Permissions](https://gridzen.ai/console/learn/business-permission-boundary)

[SQLite fixture](examples/verification_delivery/README.md) · [n8n fixture](examples/n8n/README.md)

Synthetic only / Solo sintético / 仅模拟；不涉及真人核验或生产批准；付费开通仍不可用。
