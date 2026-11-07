## Faire évoluer le projet

Chaque évolution courante s'ajoute **sans modifier l'existant** : un fichier, une fixture ou une option en plus.

### Ajouter une page

1. Créer `framework/pages/<nom>_page.py` : classe qui hérite de `BasePage`, avec son `path`.
2. Ajouter la fixture correspondante dans `framework/fixtures/pages.py`.
3. L'utiliser dans un test en la demandant en paramètre.

### Ajouter un client API

1. Déclarer les modèles de données dans `framework/api/models.py` (seulement les champs utiles).
2. Créer `framework/api/<ressource>_api.py` : classe qui hérite de `BaseApiClient`.
3. Ajouter la fixture dans `framework/fixtures/api.py`.

Le client sert aussi bien aux tests d'API (`tests/api/`) qu'à préparer les données des tests UI.

### Ajouter une donnée de test isolée

1. Ajouter une fabrique dans `framework/data/` (valeurs uniques, ex : `uuid4`).
2. Ajouter une fixture dans `framework/fixtures/data.py` : création via l'API avant `yield`, suppression après.

### Ajouter un export (rapport)

Les exports sont des plugins pytest activés par une option, sans toucher au code :

| Export | Ajout | Option |
| --- | --- | --- |
| JUnit XML | intégré à pytest | `--junitxml=reports/junit.xml` |
| HTML | `pytest-html` (installé) | `--html=reports/report.html --self-contained-html` |
| Allure | `allure-pytest` (installé) | `--alluredir=allure-results` |
| JSON | `uv add pytest-json-report` | `--json-report --json-report-file=reports/report.json` |

Pour un export maison, écrire un hook pytest (`pytest_runtest_logreport`, `pytest_sessionfinish`)
dans un nouveau module `framework/plugins/<nom>.py` et l'ajouter à `pytest_plugins` dans `conftest.py`.

### Ajouter un environnement

1. Créer `environments/<nom>.env` avec `BASE_URL` et `API_URL`.
2. Lancer avec `ENV=<nom> uv run pytest` (ou définir `ENV` dans Jenkins).

### Ajouter un rôle (ex : vendeur)

1. Ajouter les identifiants dans `Settings` (`framework/config/settings.py`) et dans `.env.example`.
2. Ajouter une fixture `<role>_storage_state` dans `framework/fixtures/auth.py`.
3. Créer `tests/ui/<role>/conftest.py` sur le modèle de `tests/ui/customer/conftest.py`.

### Réorganiser les tests

Les suites reposent sur des **marqueurs** (`smoke`, `ui`, `api`), pas sur les dossiers :
déplacer un fichier ne change pas les suites. Pour une nouvelle suite (ex : `regression`),
la déclarer dans `markers` du `pyproject.toml` puis l'appliquer avec `@pytest.mark.regression`.

Seule contrainte liée aux dossiers : la session injectée par les `conftest.py` de `tests/ui/customer/` et `tests/ui/admin/`.

### Passer au BDD

1. `uv add pytest-bdd`.
2. Écrire les scénarios dans `features/*.feature` (Gherkin).
3. Écrire les steps dans `tests/bdd/` : ils demandent les **mêmes fixtures** (pages, API, données) que les tests en code.

Les deux approches cohabitent : BDD pour les parcours métier lus par le métier, code pour le reste.

### Ajouter un navigateur

`uv run pytest --browser chromium --browser firefox` : chaque test est lancé sur chaque navigateur.
Pour le rendre permanent, modifier `--browser` dans `addopts` du `pyproject.toml`.

### Mettre à jour Playwright

La version de `playwright` (`pyproject.toml`) et celle de l'image Docker (`docker-compose.yml`)
doivent rester identiques. Mettre à jour les deux ensemble.
