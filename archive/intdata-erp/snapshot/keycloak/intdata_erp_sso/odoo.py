import os
import sys
try:
    import odoo  # type: ignore
    from odoo import api, SUPERUSER_ID  # type: ignore
    from odoo.tools import config as odoo_config  # type: ignore
except ImportError as exc:  # pragma: no cover
    print(f"[odoo_keycloak] Не удалось импортировать odoo: {exc}", file=sys.stderr)
    sys.exit(1)


def _env():
    db_name = os.environ.get("ODOO_DB_NAME")
    if not db_name:
        raise RuntimeError("Не задана переменная ODOO_DB_NAME")
    odoo_config.parse_config(["-d", db_name])
    registry = odoo.registry(db_name)
    return registry


def configure():
    required = {
        "KEYCLOAK_BASE_URL": os.environ.get("KEYCLOAK_BASE_URL", "").rstrip("/"),
        "KEYCLOAK_REALM": os.environ.get("KEYCLOAK_REALM"),
        "ODOO_KEYCLOAK_CLIENT_ID": os.environ.get("ODOO_KEYCLOAK_CLIENT_ID"),
        "ODOO_KEYCLOAK_CLIENT_SECRET": os.environ.get("ODOO_KEYCLOAK_CLIENT_SECRET"),
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise RuntimeError(f"Отсутствуют обязательные переменные окружения: {', '.join(missing)}")

    base_url = required["KEYCLOAK_BASE_URL"]
    realm = required["KEYCLOAK_REALM"]
    client_id = required["ODOO_KEYCLOAK_CLIENT_ID"]
    client_secret = required["ODOO_KEYCLOAK_CLIENT_SECRET"]

    scope = os.environ.get("ODOO_KEYCLOAK_SCOPE", "openid email profile")
    display_name = os.environ.get("ODOO_KEYCLOAK_NAME", "Keycloak (IntData)")
    allow_signup = os.environ.get("ODOO_KEYCLOAK_ALLOW_SIGNUP", "false").lower() in {"1", "true", "yes", "on"}

    realm_base = f"{base_url}/realms/{realm}/protocol/openid-connect"
    auth_endpoint = f"{realm_base}/auth"
    token_endpoint = f"{realm_base}/token"
    userinfo_endpoint = f"{realm_base}/userinfo"

    registry = _env()
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        module = env["ir.module.module"].sudo().search([("name", "=", "auth_oauth")], limit=1)
        if module and module.state != "installed":
            module.button_immediate_install()
            env.cr.commit()

        provider_model = env["auth.oauth.provider"].sudo()
        provider = provider_model.search([("client_id", "=", client_id)], limit=1)
        values = {
            "name": display_name,
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_endpoint": auth_endpoint,
            "validation_endpoint": token_endpoint,
            "data_endpoint": userinfo_endpoint,
            "scope": scope,
            "enabled": True,
            "body_request_type": "json",
        }
        if provider:
            provider.write(values)
        else:
            values.update({"sequence": 5})
            provider = provider_model.create(values)

        params = env["ir.config_parameter"].sudo()
        params.set_param("auth_oauth.provider_keycloak", provider.id)
        params.set_param("auth_oauth.sign_up", "True" if allow_signup else "False")
        modules = params.get_param("server_wide_modules", default="web")
        if "auth_oauth" not in modules:
            params.set_param("server_wide_modules", modules + ",auth_oauth")

        env.cr.commit()
    print("[odoo_keycloak] Провайдер Keycloak обновлён", flush=True)


if __name__ == "__main__":
    try:
        configure()
    except Exception as exc:  # pragma: no cover
        print(f"[odoo_keycloak] Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)
