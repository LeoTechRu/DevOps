# Intelligent Data ERP Archive

`/int/leonid/archive/intdata-erp` хранит historical code snapshot бывшего top-level контура `/int/erp`.

- Статус: decommissioned 22 марта 2026 года.
- Runtime на машине удалён; active systemd/vhost/docker/db ownership больше нет.
- Дальнейшая разработка не планируется, кроме отдельного клиентского запроса.
- Полный code snapshot лежит в `snapshot/` и перенесён без `.git`, `openspec`, `GEMINI.md` и `.env.example`.

В архиве сохранены:

- ERPNext/Odoo compose-слой;
- SSO helpers и Python integration code;
- generated Apache/Nginx configs;
- deploy scripts и repo-local docs.
