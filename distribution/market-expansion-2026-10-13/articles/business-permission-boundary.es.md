# Separe los resultados de verificación de los permisos

Convierta un resultado en una decisión de aplicación acotada. Pruebe vinculación de cuenta, política explícita, eventos duplicados y rechazos en una base local. El permiso del ejemplo es una marca de demostración.

## Qué va a construir

Convierta un resultado en una decisión de aplicación acotada. Pruebe vinculación de cuenta, política explícita, eventos duplicados y rechazos en una base local. El permiso del ejemplo es una marca de demostración.

## Ejecute y compruebe los tres resultados



```bash
for scenario in success reject unavailable; do
  curl -fsS https://gridzen.ai/console/api/quickstart/trial \
    -H 'Content-Type: application/json' \
    -d '{"task":"identity_onboarding","scenario":"'"$scenario"'"}'
done
```

## Resultado esperado (sintético)



```json
{
  "mode": "synthetic_fixture",
  "source": "local_response_trial",
  "task": "identity_onboarding",
  "scenario": "success",
  "verified": false,
  "real_person_verified": false,
  "billable": false,
  "amount_minor": 0,
  "upstream_calls": 0,
  "result": {
    "status": "Approved",
    "reason": "synthetic_scenario",
    "hosted_url": null
  },
  "business_decision": "caller_owned",
  "next_step": "connect_verified_account_for_persisted_sandbox",
  "production_available_from_this_trial": false
}
```

## Estado local: reinicio, duplicados y plazos

El script usa identificadores sintéticos. Ejecute el código y las pruebas del repositorio enlazado; no requiere cuenta ni clave. Los callbacks reales necesitan validación de firma autorizada.

```bash
git clone https://github.com/immurray/gridzen-developer-kit.git
cd gridzen-developer-kit
python3 examples/verification_delivery/delivery.py identity --db /tmp/gridzen-local-delivery.sqlite3
python3 -m venv .venv
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest examples/verification_delivery/test_delivery.py -q
```

## Decida el siguiente paso de su aplicación

El éxito es una rama sintética, no aprobación de una persona real. Para rechazo, muestre recuperación o revisión. Si no está disponible, conserve desconocido y no conceda permisos. En producción, vincule tenant, cuenta y sesión, valide la notificación, consulte el estado autorizado y aplique la política de negocio.

## Límites y conexión a producción

No envíe documentos, números reales ni credenciales a esta prueba. Producción es un piloto gratuito aprobado por el responsable. La ruta telefónica solo cubre validez básica; identidad requiere cuota gratuita confirmada y permisos aplicables. Los cobros reales están desactivados.

[Run the account-free synthetic trial](https://gridzen.ai/console/start?lang=es) · [Get integration guidance](https://gridzen.ai/console/assessment?lang=es)
