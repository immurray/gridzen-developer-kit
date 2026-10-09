# Kit de desarrollo Gridzen 0.1.1

Investigación sobre 198 países y territorios, planificación de integraciones, cinco resultados simulados, CLI/SDK HTTP de Python, MCP local y seis Skills. No hay canales de proveedores reales activos. Ningún resultado simulado verifica a una persona real.

Prueba y guía: https://gridzen.ai/developers/ . El selector permite cambiar entre español, inglés y chino, y recuerda la elección. La investigación es del 2026-10-07; las fuentes y sus restricciones se conservan en el idioma original.

## Instalación

Descarga y descomprime gridzen-developer-kit.zip. Ejecuta lo siguiente desde el directorio que contiene la carpeta extraída. Se requiere Python 3.11 o posterior.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install './gridzen-developer-kit[mcp]'
gridzen plan --country ID --event payout
gridzen simulate --country ID --capability bank_account_match --scenario timeout
python gridzen-developer-kit/examples/payout.py
```

En Windows, activa con `.venv\Scripts\activate`. La CLI y MCP local funcionan sin conexión tras instalar las dependencias; el SDK HTTP y el ejemplo de Python llaman al entorno público de pruebas.

## MCP y Skills

Añade un servidor stdio local a un cliente compatible y sustituye command por la ruta instalada:

```json
{"mcpServers":{"gridzen":{"command":"/absolute/path/to/.venv/bin/gridzen-mcp","args":[]}}}
```

Prueba: «Planifica una verificación de pagos para Indonesia y simula una espera agotada del proveedor». Las cinco herramientas consultan cobertura, planifican, generan simulaciones, recuperan pruebas y explican resultados. La configuración depende del cliente; no hay endpoint MCP remoto de producción.

Copia cada carpeta de `skills/` al directorio de habilidades del agente, conservando `SKILL.md` y sus referencias. Los tres Skills permiten elegir una verificación, integrar pruebas y explicar resultados. Los identificadores permanecen en inglés; el agente puede explicar los resultados en español.

## Interpretación

- match: coincidencia simulada; no autoriza altas ni pagos reales.
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

El código, las descargas, la entrada oficial de MCP Registry y tres páginas de Skills.sh están publicados. La propuesta del catálogo de Docker está pendiente de revisión. Consulta [el registro de publicación](distribution/STATUS.md).


## Six bundled Skills (0.4.0)

`python -m pip install gridzen-developer-kit` installs the CLI, stdio MCP dependencies
and all six Skill directories. Version 0.4.0 is published on
[PyPI](https://pypi.org/project/gridzen-developer-kit/0.4.0/); clean installation,
CLI, stdio MCP and all six bundled Skill directories were verified. No extra MCP
dependency installation is required.

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
workflows, version 1.0.0: `mexico-pilot-scoper`, `payout-policy-designer`, and
`provider-rights-readiness`. Each includes MIT, README, complete response fixtures
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
