# Projekt Zaliczeniowy - DevOps Lab

Projekt przedstawia kompletną ścieżkę CI/CD dla aplikacji webowej opartej na technologii Flask, zintegrowaną z chmurą Microsoft Azure.

## 1. Architektura aplikacji
Aplikacja została skonteneryzowana przy użyciu **Docker** i składa się z trzech głównych usług:
- **Web App**: Aplikacja Flask (Python).
- **Database**: Baza danych PostgreSQL.
- **Reverse Proxy**: Nginx obsługujący ruch przychodzący.
- **Seeder**: Kontener pomocniczy, który automatycznie inicjalizuje bazę danych danymi testowymi i zapisuje logi w wolumenie.

## 2. Infrastruktura jako Kod (IaC)
Zasoby w chmurze Azure zostały zdefiniowane przy użyciu języka **Bicep**.
- Plik definicji: `infra/main.bicep`
- Utworzone zasoby: **Azure Container Registry (ACR)** o nazwie `acrprojekt2026`.

## 3. Automatyzacja CI/CD (GitHub Actions)

Mój pipeline został podzielony na dwa kluczowe etapy:

### Etap CI (Continuous Integration)
Uruchamia się automatycznie przy każdym `push` oraz `pull_request` na gałąź `main`.
- **Multi-stage Build**: Wykorzystanie etapów `builder`, `test` oraz `final` w Dockerfile w celu optymalizacji rozmiaru obrazu.
- **Testy**: Automatyczne uruchamianie testów jednostkowych (`pytest`) wewnątrz kontenera.
- **Bezpieczeństwo**: Automatyczne skanowanie kodu za pomocą **CodeQL Analysis**.
- **Rejestracja**: Wypchnięcie (push) gotowego obrazu do Azure Container Registry.

### Etap CD (Continuous Deployment)
Zgodnie z wymaganiami, etap ten uruchamia się **ręcznie** (workflow_dispatch) lub po dodaniu **tagu wersji** (np. `v1.0`).
- Pobiera najnowsze obrazy z ACR (`docker compose pull`).
- Restartuje usługi w środowisku docelowym (`docker compose up -d`).
