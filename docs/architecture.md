## Architecture

### Principe : séparer le « comment » du « quoi »

| Couche | Dossier | Rôle | Dépend de |
| --- | --- | --- | --- |
| Tests | `tests/` | **Quoi** vérifier : scénarios et assertions | fixtures, pages, api |
| Fixtures | `framework/fixtures/` | Préparer l'environnement d'un test et l'injecter | pages, api, data, config |
| Pages | `framework/pages/` | **Comment** interagir avec l'interface (locators, actions) | Playwright |
| API | `framework/api/` | **Comment** dialoguer avec l'API (requêtes, modèles) | Playwright, pydantic |
| Données | `framework/data/` | Construire des données de test uniques | modèles API |
| Config | `framework/config/` | URLs, secrets, environnement ciblé | variables d'environnement |

Règle : une couche ne dépend que des couches en dessous d'elle.
Un test ne contient ni locator ni URL ; une page ne contient pas d'assertion métier.

### Flux d'un test

```
test_login_with_new_customer(login_page, account_page, new_customer)
         │                       │            │              │
         │                  fixtures/pages.py │       fixtures/data.py
         │                       │            │         │  crée un client via l'API (UsersApi)
         │                       └── page ────┘         │  ... puis le supprime après le test
         │                            │
         │                 pytest-playwright : browser → context → page
         │                            │
         │                 fixtures/browser.py : base_url, locale, serveur distant, plein écran
         ▼
   assertions (expect) dans le test uniquement
```

### Configuration

Ordre de priorité (le premier trouvé gagne) :

1. variables d'environnement réelles (Jenkins, terminal) ;
2. fichier `.env` (secrets locaux, ignoré par git) ;
3. fichier `environments/<ENV>.env` (URLs, versionné), `demo` par défaut.

Les identifiants sont lus **à la demande** : un identifiant manquant ne fait échouer que les tests qui en ont besoin.

### Local et CI : une seule configuration

Les options communes sont dans `pyproject.toml` (`[tool.pytest.ini_options]`).
Les différences passent en ligne de commande, il n'y a donc pas de fichier de configuration dupliqué :

| | Local | CI (Jenkinsfile) |
| --- | --- | --- |
| Navigateur | lancé localement, `--headed` en option (plein écran) | serveur Playwright distant (`PLAYWRIGHT_SERVER`) |
| Parallélisme | aucun par défaut | `-n 4` (pytest-xdist) |
| Retries | aucun | `--reruns 2` (pytest-rerunfailures) |
| Exports | aucun | JUnit XML, HTML, Allure |

### Sessions par rôle

`framework/fixtures/auth.py` se connecte **une fois par rôle et par worker** et enregistre la session (storage state) dans `.auth/`.
Le `conftest.py` de `tests/ui/customer/` et de `tests/ui/admin/` injecte cette session dans tous les tests du dossier.

Ces comptes sont **partagés** entre les tests : ils ne servent qu'aux contrôles qui ne modifient pas de données.

### Données isolées

La fixture `new_customer` crée un client unique via l'API avant le test et le supprime après, même si le test échoue.
C'est le modèle à suivre pour toute donnée modifiée par un test (panier, commande...) :
les tests restent indépendants, peuvent tourner en parallèle et dans n'importe quel ordre.

### Validation des réponses d'API

Les réponses sont converties en modèles pydantic (`framework/api/models.py`).
Si l'API change de format, le test échoue immédiatement avec un message explicite.
Les réponses capturées pendant un test UI (ex : la recherche) utilisent les mêmes modèles.
