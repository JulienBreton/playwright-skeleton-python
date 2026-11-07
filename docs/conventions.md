## Conventions

Ces règles garantissent que le projet reste lisible et stable quand l'équipe et le nombre de tests grandissent.
Celles marquées 🔒 sont vérifiées automatiquement (ruff, mypy, pytest) et bloquent la CI.

### Langue

- Code (classes, méthodes, variables, noms de tests) : **anglais**.
- Commentaires, docstrings et documentation : **français**.

### Nommage

- Fichiers et fonctions en `snake_case`, classes en `PascalCase`. 🔒
- Une page : `<nom>_page.py` contenant la classe `<Nom>Page`.
- Un client API : `<ressource>_api.py` contenant la classe `<Ressource>Api`.
- Un test décrit le comportement attendu : `test_<action>_<résultat attendu>`
  (ex : `test_login_rejected_with_invalid_credentials`).

### Page objects

- Toute page hérite de `BasePage` et déclare son chemin `path`.
- Un élément présent sur plusieurs pages devient un composant (`pages/components/`).
- Les locators sont des attributs créés dans `__init__`, un seul locator par élément.
- Priorité des locators : `get_by_test_id` > `get_by_role` > `get_by_label` > CSS en dernier recours.
- Les méthodes décrivent une intention métier (`login`, `search`) et non un geste technique.
- **Pas d'assertion métier dans une page.** Seule exception : une attente de synchronisation
  (`wait_until_loaded`), nommée comme telle.
- Une action qui déclenche un appel API utile au test renvoie la réponse typée (ex : `SearchBar.search`).

### Tests

- Les page objects et clients API sont **injectés par fixture**, jamais instanciés dans le test.
- Assertions web-first (`expect(locator).to_have_text(...)`) pour l'interface : elles réessaient jusqu'au timeout.
- Pas de `time.sleep` ni d'attente fixe.
- Pas de valeur qui dépend des données du site (nombre de produits...) : comparer à la réponse de l'API.
- Un test qui modifie des données utilise ses propres données (`new_customer`), jamais un compte partagé.
- Chaque module déclare son type : `pytestmark = pytest.mark.ui` ou `pytest.mark.api`.
- Seuls les marqueurs déclarés dans `pyproject.toml` sont autorisés. 🔒

### Typage et qualité

- Toutes les fonctions sont annotées, y compris les tests (`-> None`). 🔒 (mypy strict)
- Pas de `Any` sans raison (seuls les dictionnaires d'options Playwright en utilisent).
- `uv run ruff format .` avant chaque commit. 🔒
- Toute nouvelle dépendance passe par `uv add` (versions verrouillées dans `uv.lock`).

### Secrets

- Aucun identifiant dans le code ni dans `environments/`.
- En local : `.env` (copié depuis `.env.example`). En CI : Jenkins > Credentials.
