## Commandes

Toutes les commandes passent par `uv run`, qui utilise l'environnement Python du projet.

### Lancer les tests

| Commande | Effet |
| --- | --- |
| `uv run pytest` | tous les tests, navigateur invisible |
| `uv run pytest --headed` | navigateur visible, en plein écran |
| `uv run pytest --headed --slowmo 500` | ralentit chaque action de 500 ms |
| `uv run pytest tests/ui/guest/` | un dossier |
| `uv run pytest tests/ui/guest/test_login.py` | un fichier |
| `uv run pytest -k "search"` | les tests dont le nom contient « search » |
| `uv run pytest -m smoke` | une suite (marqueur) |
| `uv run pytest -m "ui and not smoke"` | combinaison de marqueurs |
| `uv run pytest -n 4` | 4 workers en parallèle |
| `uv run pytest --reruns 2` | rejoue 2 fois un test en échec |
| `ENV=demo uv run pytest` | cible un environnement (`environments/<ENV>.env`) |
| `PLAYWRIGHT_SERVER=ws://127.0.0.1:3000/ uv run pytest` | utilise le serveur Playwright Docker |

### Déboguer

- `uv run pytest --headed -x` : s'arrête au premier échec.
- `page.pause()` dans un test : ouvre le Playwright Inspector (pas à pas, Pick locator).
- `uv run playwright show-trace test-results/<test>/trace.zip` : ouvre la trace d'un test en échec.
- `uv run playwright codegen https://practicesoftwaretesting.com` : enregistre des actions pour trouver les locators.

En cas d'échec, `test-results/<test>/` contient la trace, la capture d'écran et la vidéo.

### Rapports

```bash
uv run pytest --junitxml=reports/junit.xml \
              --html=reports/report.html --self-contained-html \
              --alluredir=allure-results
```

### Qualité du code

| Commande | Effet |
| --- | --- |
| `uv run ruff check .` | lint |
| `uv run ruff check . --fix` | corrige automatiquement ce qui peut l'être |
| `uv run ruff format .` | formate le code |
| `uv run mypy` | vérifie les types (mode strict) |

### Serveur Playwright (Docker)

```bash
docker compose up -d     # démarre le serveur sur le port 3000
docker compose down      # l'arrête
```

### Dépendances

| Commande | Effet |
| --- | --- |
| `uv sync` | installe les dépendances de `uv.lock` |
| `uv add <paquet>` | ajoute une dépendance |
| `uv add --dev <paquet>` | ajoute un outil de développement |
| `uv lock --upgrade` | met à jour les versions verrouillées |
