"""Allowlisted GridZen production pilot stdio MCP.
Install mcp==2.3.0 httpx==0.28.1 in a venv. Set GRIDZEN_API_KEY locally.
Never submit documents, faces or upstream credentials; KYC uses a hosted URL.
After explicit project measurement registration only, optional GRIDZEN_PROJECT_ID
links fixed-category business results; omit it to keep project measurement off.
"""

import os
import re
import inspect
from uuid import UUID
from typing import Any,Literal
import httpx
import logging
from pydantic import StrictInt, StrictBool

# Provider lookup URLs contain subject identifiers; never emit HTTP client traces.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
from mcp.server import MCPServer
from mcp.shared.exceptions import MCPError
from mcp.types import ToolAnnotations

BASE = "https://gridzen.ai/console/api/production"

# Product profiles reduce the tools advertised to an assistant. They do not
# replace the backend's merchant permissions, enrollment or funding checks.
PROFILES = {
    'mx-cep': ('mexico_cep_capabilities', 'submit_mexico_cep_check', 'get_mexico_cep_check', 'recover_mexico_cep_check'),
    'mx-account-name': ('mexico_account_name_capabilities', 'quote_mexico_account_name', 'verify_mexico_account_name', 'get_mexico_account_name', 'recover_mexico_account_name'),
    'ip-risk': ('production_capabilities', 'check_registration_risk', 'get_production_verification', 'refresh_production_verification'),
    'hosted-identity': ('production_capabilities', 'start_identity_onboarding', 'get_production_verification', 'refresh_production_verification'),
    'mx-identity-account': ('mexico_identity_account_capabilities', 'mexico_identity_account_enrollment', 'quote_mexico_identity_account', 'verify_mexico_identity_account', 'recover_mexico_identity_account'),
}


class ProductionAPI:
    def __init__(self, key, transport=None, project_id=None):
        if not key or not key.startswith("gz_test_"):
            raise ValueError(
                "Configure merchant GRIDZEN_API_KEY; production permission is separate"
            )
        self.key, self.transport = key, transport
        self.project_id=str(UUID(project_id)) if project_id else None

    async def call(self, method, path, body=None):
        return await self.request(method, BASE + path, body)

    async def task(self, path=''):
        return await self.request('GET', BASE.removesuffix('/production') + '/onboarding/tasks' + path)

    async def micro(self, method, path='', body=None):
        return await self.request(method, BASE.removesuffix('/production') + '/bank-account-name/micro' + path, body)

    async def cep(self,method,path='',body=None):
        return await self.request(method,BASE.removesuffix('/production')+'/payment-evidence/mx/cep'+path,body)

    async def identity_account(self,method,path='',body=None):
        return await self.request(method,BASE.removesuffix('/production')+'/bank-account-name/identity'+path,body)

    async def request(self, method, url, body=None):
        try:
            async with httpx.AsyncClient(
                timeout=30, follow_redirects=False, transport=self.transport, trust_env=False
            ) as client:
                response = await client.request(
                    method,
                    url,
                    headers={"Authorization": "Bearer " + self.key, **({"X-Gridzen-Project":self.project_id} if self.project_id else {})},
                    json=body,
                )
                if response.status_code >= 400:
                    try:
                        problem = response.json()
                        reason = problem.get('code') or problem.get('detail', '')
                        if isinstance(reason, dict):
                            reason = reason.get('code', '')
                    except (ValueError, AttributeError):
                        reason = ''
                    if not isinstance(reason, str) or not re.fullmatch(r'[A-Z][A-Z0-9_]{3,79}',reason):
                        reason = 'UPSTREAM_HTTP_ERROR'
                    raise MCPError(
                        code=-32000,
                        message=f"{reason}; GridZen production API HTTP {response.status_code}; preserve idempotency key and read existing record before retry",
                    )
                return response.json()
        except (httpx.HTTPError, ValueError):
            raise MCPError(
                code=-32000,
                message="Connection uncertain; preserve idempotency key, never create a replacement request automatically",
            ) from None


def make_server(api, profile=None):
    if profile is not None and profile not in PROFILES:
        raise ValueError('UNKNOWN_PRODUCT_PROFILE')
    tools = {}

    async def validate(ctx, call_next):
        if ctx.method == "tools/call" and isinstance(ctx.params, dict):
            args = ctx.params.get("arguments", {})
            name = ctx.params.get("name")
            fn = tools.get(name) if isinstance(name, str) else None
            if fn and (
                not isinstance(args, dict)
                or set(args) - set(inspect.signature(fn).parameters)
                or any(
                    (
                        type(v) is not bool
                        if k in {"consent_to_verify", "authorize_transfer", "authorized_to_query", "accept_disclosed_source_cost"}
                        else type(v) is not int or v<=0 if k=='amount_minor'
                        else not isinstance(v, str) or len(v) > (255 if k=='business_website' else 200 if k in {"account_name", "quote_token", "expected_name"} else 128 if k=='tracking_key' else 100)
                    )
                    for k, v in args.items()
                )
            ):
                raise MCPError(
                    code=-32602,
                    message="Only documented arguments accepted; do not submit identity documents or credentials",
                )
        return await call_next(ctx)

    server = MCPServer(
        "GridZen Production",
        version="0.3.0",
        middleware=[validate],
        instructions="Separately gated production routes. First read capabilities; enrollment is completed by the business representative in the console. Supplier costs may apply within server-enforced limits; current funding, checkout availability and charges follow the console status and accepted product quote. Paid identity and risk calls require explicit billing_mode=paid and confirmed prepaid credit; never purchase or top up automatically. Mutations require explicit subject consent and intended user action. Phone checks validity only, not possession. Identity documents and faces go directly to hosted provider. Registration-risk checks return IP-only signals, never identity verification. Return provider evidence, never infer fraud or approve a customer automatically. Reuse idempotency UUID on retry; no automatic replacement after ambiguous submission.",
    )
    read = ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    )
    write = ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    )
    transfer = ToolAnnotations(readOnlyHint=False, destructiveHint=True,
                               idempotentHint=True, openWorldHint=True)

    def consent(key, reference, approved):
        if approved is not True:
            raise MCPError(code=-32602, message="Explicit subject consent required")
        try:
            return str(UUID(key)), str(UUID(reference))
        except (ValueError, TypeError, AttributeError):
            raise MCPError(
                code=-32602, message="Use UUID request and consent references"
            ) from None

    @server.tool(annotations=read, structured_output=True)
    async def list_onboarding_tasks() -> dict[str, Any]:
        """Read tenant-owned task versions and next actions. Makes no provider request."""
        return await api.task()

    @server.tool(annotations=read, structured_output=True)
    async def get_onboarding_task(task_id: str) -> dict[str, Any]:
        """Read current evidence and workflow version before resuming work."""
        return await api.task('/' + str(UUID(task_id)))

    @server.tool(annotations=read, structured_output=True)
    async def get_onboarding_handoff(task_id: str) -> dict[str, Any]:
        """Read a redacted handoff; never replay a provider submission from history."""
        return await api.task('/' + str(UUID(task_id)) + '/handoff')

    @server.tool(annotations=read, structured_output=True)
    async def production_capabilities() -> dict[str, Any]:
        return await api.call("GET", "/capabilities")

    @server.tool(annotations=write, structured_output=True)
    async def check_signup_phone(
        phone: str,
        idempotency_key: str,
        consent_reference: str,
        consent_to_verify: bool,
    ) -> dict[str, Any]:
        """Free format/validity check of an explicitly authorized E.164 number. No OTP, ownership or paid line intelligence."""
        key, ref = consent(idempotency_key, consent_reference, consent_to_verify)
        return await api.call(
            "POST",
            "/verifications",
            {
                "mode": "production",
                "capability": "phone_validation",
                "phone": phone,
                "idempotency_key": key,
                "consent_reference": ref,
                "consent_to_verify": True,
            },
        )

    @server.tool(annotations=write, structured_output=True)
    async def start_identity_onboarding(
        idempotency_key: str, consent_reference: str, consent_to_verify: bool,
        billing_mode:Literal['trial','paid']|None=None,
    ) -> dict[str, Any]:
        """Create one hosted identity flow after consent. Explicit billing_mode='paid' consumes already purchased credit; it never buys credit or recharges. Read capabilities and accept service terms in the console first. User personally completes document/face steps."""
        key, ref = consent(idempotency_key, consent_reference, consent_to_verify)
        return await api.call(
            "POST",
            "/verifications",
            {
                "mode": "production",
                "capability": "identity_verification",
                **({'billing_mode':billing_mode} if billing_mode is not None else {}),
                "idempotency_key": key,
                "consent_reference": ref,
                "consent_to_verify": True,
            },
        )

    @server.tool(annotations=read, structured_output=True)
    async def get_production_verification(record_id: str) -> dict[str, Any]:
        return await api.call("GET", "/verifications/" + str(UUID(record_id)))

    @server.tool(annotations=write, structured_output=True)
    async def check_registration_risk(
        ip_address: str, idempotency_key: str, consent_reference: str, consent_to_verify: bool,
        billing_mode:Literal['trial','paid']|None=None,
    ) -> dict[str, Any]:
        """Request IP-only Insights. Explicit billing_mode='paid' spends already purchased credit, independently of trial caps. Does not purchase or recharge. Same request UUID prevents another charge. No identity/ownership conclusion or automatic approval."""
        key, ref = consent(idempotency_key, consent_reference, consent_to_verify)
        from ipaddress import ip_address as parse_ip
        try:
            address = parse_ip(ip_address)
            if not address.is_global:
                raise ValueError()
        except ValueError:
            raise MCPError(code=-32602, message="An authorized public registration IP is required") from None
        return await api.call("POST", "/verifications", {
            "mode": "production", "capability": "registration_risk", "ip_address": str(address),
            "idempotency_key": key, "consent_reference": ref, "consent_to_verify": True,
            **({'billing_mode':billing_mode} if billing_mode is not None else {}),
        })

    @server.tool(annotations=write, structured_output=True)
    async def refresh_production_verification(record_id: str) -> dict[str, Any]:
        return await api.call(
            "POST", "/verifications/" + str(UUID(record_id)) + "/refresh", {}
        )

    @server.tool(annotations=read, structured_output=True)
    async def mexico_account_name_capabilities() -> dict[str, Any]:
        """Read the funding mode, customer charge, supported receiving banks and execution gates. An operator-funded trial is not customer debt. Does not transfer money."""
        return await api.micro('GET', '/capabilities')

    @server.tool(annotations=read, structured_output=True)
    async def quote_mexico_account_name(clabe: str, account_name: str, account_holder_type: str, verification_mode: Literal['name_match','statement_amount']='name_match') -> dict[str, Any]:
        """Get an expiring quote. Show principal, provider and GridZen fees and maximum debit separately. No payment. Copy the exact quote_token and terms_version after explicit authorization."""
        return await api.micro('POST', '/quote', {'clabe':clabe, 'name':account_name,
                                                'account_holder_type':account_holder_type,'verification_mode':verification_mode})

    @server.tool(annotations=transfer, structured_output=True)
    async def verify_mexico_account_name(clabe: str, account_name: str, account_holder_type: str,
            quote_token: str, idempotency_key: str, consent_reference: str,
            consent_to_verify: bool, authorize_transfer: bool, verification_mode: Literal['name_match','statement_amount']='name_match',terms_version: str='') -> dict[str, Any]:
        """MONEY MOVEMENT: explicitly authorize the full quote, including principal, provider fees and any GridZen service fee. Pass its exact quote_token and terms_version. Funding is operator trial or actual merchant prepayment, never inferred debt. Not OTP or document identity. After ambiguity read the original request; never create a replacement automatically."""
        key, ref = consent(idempotency_key, consent_reference, consent_to_verify)
        if authorize_transfer is not True:
            raise MCPError(code=-32602, message='Explicit authorization for this money transfer is required')
        terms=terms_version or ('mx-micro-random-2026-10-23' if verification_mode=='statement_amount' else 'mx-micro-2026-10-20')
        if terms not in {'mx-micro-2026-10-20','mx-micro-random-2026-10-23','mx-micro-paid-2026-10-23'}:
            raise MCPError(code=-32602,message='Use the exact terms_version returned by the approved quote')
        return await api.micro('POST','/verifications',{'clabe':clabe,'name':account_name,
            'account_holder_type':account_holder_type,'quote_token':quote_token,
            'idempotency_key':key,'consent_reference':ref,'consent_to_verify':True,
            'authorize_transfer':True,'verification_mode':verification_mode,
            'terms_version':terms})

    @server.tool(annotations=read, structured_output=True)
    async def get_mexico_account_name(record_id: str) -> dict[str, Any]:
        """Read this merchant's current result; no supplier request or additional transfer."""
        return await api.micro('GET','/verifications/'+str(UUID(record_id)))

    @server.tool(annotations=read, structured_output=True)
    async def recover_mexico_account_name(idempotency_key: str) -> dict[str, Any]:
        """Reconcile an interrupted submission by its ORIGINAL request UUID. Never creates a payment."""
        return await api.micro('GET','/requests/'+str(UUID(idempotency_key)))

    @server.tool(annotations=read, structured_output=True)
    async def mexico_cep_capabilities() -> dict[str, Any]:
        """Read real existing-payment CEP access and capacity. No transfer, provider call or charge."""
        return await api.cep('GET','/capabilities')

    @server.tool(annotations=write, structured_output=True)
    async def submit_mexico_cep_check(idempotency_key: str, operation_date: str, tracking_key: str,
        amount_minor: StrictInt, issuer_code: str, receiver_code: str, account: str,
        authorization_reference: str, authorized_to_query: StrictBool, business_website: str,
        expected_name: str='') -> dict[str, Any]:
        """Queue one authorized EXISTING SPEI payment CEP check. Amount is integer MXN cents. Never creates a payment. Preserve original idempotency UUID after timeout."""
        if authorized_to_query is not True:raise MCPError(code=-32602,message='Explicit authorization required')
        return await api.cep('POST','/checks',{'idempotency_key':str(UUID(idempotency_key)),
            'operation_date':operation_date,'tracking_key':tracking_key,'amount_minor':amount_minor,
            'issuer_code':issuer_code,'receiver_code':receiver_code,'account':account,
            'authorization_reference':str(UUID(authorization_reference)),'authorized_to_query':True,
            'business_website':business_website,'expected_name':expected_name,
            'purpose':'payment_reconciliation','terms_version':'cep-existing-payment-2026-10-22'})

    @server.tool(annotations=read, structured_output=True)
    async def get_mexico_cep_check(record_id: str) -> dict[str, Any]:
        """Read tenant-owned CEP evidence, signature, transaction binding and name result. No new upstream request."""
        return await api.cep('GET','/checks/'+str(UUID(record_id)))

    @server.tool(annotations=read, structured_output=True)
    async def recover_mexico_cep_check(idempotency_key: str) -> dict[str, Any]:
        """Recover the original queued CEP task after an uncertain submission, without creating another task."""
        return await api.cep('GET','/requests/'+str(UUID(idempotency_key)))

    def identity_values(personal_number,clabe,bank_evidence_id,business_event):
        if not re.fullmatch(r'[A-Z0-9]{18}',personal_number) or not re.fullmatch(r'[0-9]{18}',clabe):
            raise MCPError(code=-32602,message='Valid CURP and supported CLABE required')
        return {'personal_number':personal_number,'clabe':clabe,
                'bank_evidence_id':str(UUID(bank_evidence_id)) if bank_evidence_id else None,'business_event':business_event}

    @server.tool(annotations=read,structured_output=True)
    async def mexico_identity_account_capabilities() -> dict[str,Any]:
        """Read current verification availability, supported inputs, access conditions and charges. No live verification is performed."""
        return await api.identity_account('GET','/capabilities')

    @server.tool(annotations=read,structured_output=True)
    async def mexico_identity_account_enrollment() -> dict[str,Any]:
        """Read identity-specific terms and enrollment; does not enable bank transfers or make a provider request."""
        return await api.identity_account('GET','/enrollment')

    @server.tool(annotations=write,structured_output=True)
    async def enroll_mexico_identity_account(legal_name:str,country:Literal['MX','AU','CA','GB','NZ','SG','US'],
        authorized_representative:bool,subjects_consented:bool,restricted_use_accepted:bool) -> dict[str,Any]:
        """Register only after the merchant explicitly accepts the returned terms and has subject authority. No charge, no transfer; never infer consent."""
        if any(v is not True for v in (authorized_representative,subjects_consented,restricted_use_accepted)):
            raise MCPError(code=-32602,message='Explicit representative, subject and restricted-use acceptance required')
        return await api.identity_account('POST','/enrollment',dict(legal_name=legal_name,country=country,
            authorized_representative=True,subjects_consented=True,restricted_use_accepted=True,
            terms_version='mx-identity-account-2026-10-24'))

    @server.tool(annotations=read,structured_output=True)
    async def quote_mexico_identity_account(personal_number:str,clabe:str,bank_evidence_id:str|None=None,
        business_event:Literal['first_binding','account_change','exception_review']='first_binding') -> dict[str,Any]:
        """Get a bound quote for identity and beneficiary-account verification from CURP and CLABE. Follow its current price, capabilities and required authorization. A quote creates no verification or payment; do not send real data to public research tools."""
        return await api.identity_account('POST','/quote',identity_values(personal_number,clabe,bank_evidence_id,business_event))

    @server.tool(annotations=transfer,structured_output=True)
    async def verify_mexico_identity_account(personal_number:str,clabe:str,
        idempotency_key:str,quote_token:str,consent_to_verify:bool,accept_disclosed_source_cost:bool,
        bank_evidence_id:str|None=None,authorize_transfer:bool=False,consent_reference:str|None=None,
        business_event:Literal['first_binding','account_change','exception_review']='first_binding') -> dict[str,Any]:
        """Submit identity and beneficiary-account verification and return the task state and verification evidence. MONEY MOVEMENT may apply: when the quote requires it, obtain explicit recipient authority, authorize_transfer=true and consent_reference UUID for the disclosed action and costs. Never infer consent. Preserve the original UUID after uncertainty; never create an automatic replacement."""
        if consent_to_verify is not True or accept_disclosed_source_cost is not True:
            raise MCPError(code=-32602,message='Explicit subject and disclosed source cost acceptance required')
        if not bank_evidence_id and (authorize_transfer is not True or not consent_reference):
            raise MCPError(code=-32602,message='Explicit verification-transfer authorization and consent UUID required')
        value=identity_values(personal_number,clabe,bank_evidence_id,business_event)
        if not bank_evidence_id:value.update(authorize_transfer=True,consent_reference=str(UUID(consent_reference)))
        value.update(idempotency_key=str(UUID(idempotency_key)),quote_token=quote_token,
                     consent_to_verify=True,accept_disclosed_source_cost=True,
                     terms_version='mx-identity-account-2026-10-24')
        return await api.identity_account('POST','/checks',value)

    @server.tool(annotations=read,structured_output=True)
    async def recover_mexico_identity_account(idempotency_key:str) -> dict[str,Any]:
        """Read the original identity/account task. No new query, payment or replacement request."""
        return await api.identity_account('GET','/requests/'+str(UUID(idempotency_key)))

    tools.update(
        {
            fn.__name__: fn
            for fn in (
                production_capabilities,
                check_signup_phone,
                start_identity_onboarding,
                check_registration_risk,
                get_production_verification,
                refresh_production_verification,
                list_onboarding_tasks,
                get_onboarding_task,
                get_onboarding_handoff,
                mexico_account_name_capabilities,
                quote_mexico_account_name,
                verify_mexico_account_name,
                get_mexico_account_name,
                recover_mexico_account_name,
                mexico_cep_capabilities,
                submit_mexico_cep_check,
                get_mexico_cep_check,
                recover_mexico_cep_check,
                mexico_identity_account_capabilities,
                mexico_identity_account_enrollment,
                enroll_mexico_identity_account,
                quote_mexico_identity_account,
                verify_mexico_identity_account,
                recover_mexico_identity_account,
            )
        }
    )
    if profile is not None:
        for name in tuple(tools):
            if name not in PROFILES[profile]:
                server.remove_tool(name)
                del tools[name]
    return server


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--product', choices=tuple(PROFILES))
    options = parser.parse_args()
    make_server(ProductionAPI(os.environ.get("GRIDZEN_API_KEY", ""), project_id=os.environ.get('GRIDZEN_PROJECT_ID') or None), options.product).run(
        transport="stdio"
    )
