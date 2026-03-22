# Intelligent Data ITSM Archive

`/int/leonid/archive/intdata-itsm` хранит historical code snapshot бывшего top-level контура `/int/itsm`.

- Статус: decommissioned 22 марта 2026 года.
- Flowable/ITSM runtime на машине удалён; active systemd/vhost/docker ownership больше нет.
- Дальнейшая разработка не планируется, кроме отдельного клиентского запроса.
- Полный code snapshot лежит в `snapshot/` и перенесён без `.git`, `openspec` и `GEMINI.md`.

В архиве сохранены:

- Python ITSM module, DTO, repository и models;
- Flowable adapters и BPMN;
- db migrations и config layer;
- docs и devops-скрипты для workflow-контура.
