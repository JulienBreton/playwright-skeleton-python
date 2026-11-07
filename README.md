# Playwright Skeleton Python

Modèle de départ pour un projet d'automatisation de tests avec **Playwright** et **pytest**.
Il sert de base à un nouveau projet : l'architecture vise la stabilité des contrôles et leur
évolution (nouveaux exports, réorganisation des tests, tests d'API, BDD...).

Les exemples ciblent le site de démo [practicesoftwaretesting.com](https://practicesoftwaretesting.com).

### Démarrage rapide

Prérequis : [uv](https://docs.astral.sh/uv/) (il installe lui-même la bonne version de Python).

```bash
uv sync                               # installe Python 3.14 et les dépendances
uv run playwright install chromium    # navigateur local (inutile avec un serveur Playwright)
cp .env.example .env                  # puis renseigner les identifiants
uv run pytest                         # lance tous les contrôles
```

### Structure

```
framework/            Code réutilisable, aucun test ici
  config/             Configuration et environnements (settings.py)
  pages/              Page objects + components/ (éléments partagés entre pages)
  api/                Clients API typés + modèles pydantic (validation des réponses)
  data/               Fabriques de données de test (clients uniques...)
  fixtures/           Fixtures pytest rangées par thème (navigateur, API, auth, données, pages)
tests/                Les contrôles
  ui/guest/           Sans connexion
  ui/customer/        Session client injectée (voir conftest.py du dossier)
  ui/admin/           Session administrateur injectée
  api/                Contrôles d'API, sans navigateur
environments/         Un fichier .env par environnement (URLs, aucun secret)
docs/                 Architecture, conventions, évolutions, commandes
conftest.py           Enregistre les fixtures du framework
pyproject.toml        Dépendances + configuration pytest, ruff, mypy
Jenkinsfile           Pipeline : lint, typage, tests, rapports
docker-compose.yml    Serveur Playwright pour la CI
```

### Documentation

- [Parcours de découverte](docs/parcours-decouverte.md) : 10 étapes pour prendre en main le projet
- [Architecture](docs/architecture.md) : rôle de chaque couche et flux d'un test
- [Conventions](docs/conventions.md) : règles à respecter pour garder le projet maintenable
- [Faire évoluer le projet](docs/evolutions.md) : ajouter un export, une API, du BDD, un environnement...
- [Commandes](docs/commandes.md) : lancer, filtrer, déboguer, générer les rapports

### Démarrer un nouveau projet à partir de ce modèle

1. Copier le dépôt et renommer le projet dans `pyproject.toml`.
2. Remplacer les URLs dans `environments/demo.env` (ou créer un nouvel environnement).
3. Remplacer les page objects, clients API et tests d'exemple par ceux de l'application testée.
4. Garder l'architecture, les conventions et les garde-fous (ruff, mypy, CI).
