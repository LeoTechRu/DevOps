import os
import sys

try:
    import frappe  # type: ignore
    from frappe import _  # noqa: F401  # required for translation context
except ImportError as exc:  # pragma: no cover
    print(f"[erpnext_keycloak] Не удалось импортировать frappe: {exc}", file=sys.stderr)
    sys.exit(1)


def _env():
    site = os.environ.get("ERPNEXT_SITE_NAME")
    if not site:
        raise RuntimeError("Отсутствует ERPNEXT_SITE_NAME")
    frappe.init(site=site)
    frappe.connect()
    return site


def configure():
    required = {
        "KEYCLOAK_BASE_URL": os.environ.get("KEYCLOAK_BASE_URL", "").rstrip("/"),
        "KEYCLOAK_REALM": os.environ.get("KEYCLOAK_REALM"),
        "ERPNEXT_KEYCLOAK_CLIENT_ID": os.environ.get("ERPNEXT_KEYCLOAK_CLIENT_ID"),
        "ERPNEXT_KEYCLOAK_CLIENT_SECRET": os.environ.get("ERPNEXT_KEYCLOAK_CLIENT_SECRET"),
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise RuntimeError(f"Отсутствуют обязательные переменные окружения: {', '.join(missing)}")

    base_url = required["KEYCLOAK_BASE_URL"]
    realm = required["KEYCLOAK_REALM"]
    client_id = required["ERPNEXT_KEYCLOAK_CLIENT_ID"]
    client_secret = required["ERPNEXT_KEYCLOAK_CLIENT_SECRET"]

    scope = os.environ.get("ERPNEXT_KEYCLOAK_SCOPE", "openid email profile")
    default_role = os.environ.get("ERPNEXT_KEYCLOAK_DEFAULT_ROLE", "Employee")
    redirect_url = os.environ.get("ERPNEXT_KEYCLOAK_REDIRECT_URL", f"https://{os.environ.get('ERPNEXT_SITE_NAME', 'erp.dev.intdata.pro')}/api/method/frappe.integrations.oauth2_logins.complete_login")

    realm_base = f"{base_url}/realms/{realm}/protocol/openid-connect"
    authorize_url = f"{realm_base}/auth"
    token_url = f"{realm_base}/token"
    user_info_url = f"{realm_base}/userinfo"

    site = _env()
    try:
        provider_name = "Keycloak"
        try:
            doc = frappe.get_doc("Social Login Key", provider_name)
        except frappe.DoesNotExistError:
            doc = frappe.new_doc("Social Login Key")
            doc.provider = provider_name
        doc.enable_social_login = 1
        doc.client_id = client_id
        doc.client_secret = client_secret
        doc.base_url = base_url
        doc.authorize_url = authorize_url
        doc.token_url = token_url
        doc.user_info_url = user_info_url
        doc.scope = scope
        doc.redirect_url = redirect_url
        doc.provider_name = provider_name
        doc.set_default_role = 1
        doc.default_role = default_role
        doc.save(ignore_permissions=True)
        frappe.db.commit()
    finally:
        frappe.destroy()
    print(f"[erpnext_keycloak] Провайдер Keycloak обновлён для сайта {site}")


if __name__ == "__main__":
    try:
        configure()
    except Exception as exc:  # pragma: no cover
        print(f"[erpnext_keycloak] Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)
