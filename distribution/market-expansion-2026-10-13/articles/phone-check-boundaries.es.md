# Añada una comprobación telefónica sin prometer titularidad

Añada una comprobación previa al registro y distinga inválido de no disponible. El formato o validez no demuestra titularidad ni entrega de SMS. Este ejemplo no devuelve tipo de línea ni envía OTP.

## Qué va a construir

Añada una comprobación previa al registro y distinga inválido de no disponible. El formato o validez no demuestra titularidad ni entrega de SMS. Este ejemplo no devuelve tipo de línea ni envía OTP.

## Ejecute y compruebe los tres resultados



```bash
for scenario in success reject unavailable; do
  curl -fsS https://gridzen.ai/console/api/quickstart/trial \
    -H 'Content-Type: application/json' \
    -d '{"task":"signup_phone","scenario":"'"$scenario"'"}'
done
```

## Resultado esperado (sintético)



```json
{
  "mode": "synthetic_fixture",
  "source": "local_response_trial",
  "task": "signup_phone",
  "scenario": "success",
  "verified": false,
  "real_person_verified": false,
  "billable": false,
  "amount_minor": 0,
  "upstream_calls": 0,
  "result": {
    "source": "mock_transport",
    "mode": "simulation",
    "identity_match": "not_checked",
    "ownership": "not_checked",
    "checked_at": 1791873442.4611905,
    "status": "completed",
    "number_valid": true
  },
  "business_decision": "caller_owned",
  "next_step": "connect_verified_account_for_persisted_sandbox",
  "production_available_from_this_trial": false
}
```

## Decida el siguiente paso de su aplicación

El éxito es una rama sintética, no aprobación de una persona real. Para rechazo, muestre recuperación o revisión. Si no está disponible, conserve desconocido y no conceda permisos. En producción, vincule tenant, cuenta y sesión, valide la notificación, consulte el estado autorizado y aplique la política de negocio.

## Límites y conexión a producción

No envíe documentos, números reales ni credenciales a esta prueba. Producción es un piloto gratuito aprobado por el responsable. La ruta telefónica solo cubre validez básica; identidad requiere cuota gratuita confirmada y permisos aplicables. Los cobros reales están desactivados.

[Run the account-free synthetic trial](https://gridzen.ai/console/start?lang=es) · [Get integration guidance](https://gridzen.ai/console/assessment?lang=es)
