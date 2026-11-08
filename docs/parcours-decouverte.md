## Parcours de découverte du projet

Ce parcours fait passer de « je lance les tests » à « je fais évoluer l'architecture ».
Chaque étape suit le même format : **objectif**, **à lire**, **à faire**, **à retenir**.
Les exercices sont à faire sur une branche de travail, puis à jeter ou garder.

Durée indicative : 10 étapes d'environ 1 h, à répartir sur une ou deux semaines.

### Correspondance avec le projet TypeScript

| Projet TypeScript (playwrightDemo) | Ce projet Python |
| --- | --- |
| `npm ci` / `package-lock.json` | `uv sync` / `uv.lock` |
| `playwright.config.base.ts` | `[tool.pytest.ini_options]` dans `pyproject.toml` |
| `fixtures/page-fixtures.ts` | `framework/fixtures/pages.py` |
| projet `setup` + `storageState` | `framework/fixtures/auth.py` + `tests/ui/<rôle>/conftest.py` |
| projets guest / customer / admin | dossiers `tests/ui/guest`, `customer`, `admin` |
| `config/env.ts` | `framework/config/settings.py` |
| `await page.click()` | `page.click()` (API synchrone, pas d'`await`) |
| `Promise.all([waitForResponse, click])` | `with page.expect_response(...): click()` |
| ESLint / `tsc` | ruff / mypy |

---

### Étape 1 · Mise en route

**Objectif :** installer le projet et voir tous les tests passer.

**À lire :** [README.md](../README.md).

**À faire :**
1. `uv sync`, puis `uv run playwright install chromium`.
2. Vérifier que `.env` contient les identifiants (sinon, copier `.env.example`).
3. `uv run pytest` : les 9 tests doivent passer.
4. `uv run pytest --headed --slowmo 500` : regarder les tests se dérouler.

**À retenir :** `uv run` exécute une commande dans l'environnement Python du projet. Sans lui, Python ne trouve pas les dépendances.

---

### Étape 2 · Lancer, filtrer, déboguer

**Objectif :** maîtriser les commandes du quotidien.

**À lire :** [docs/commandes.md](commandes.md).

**À faire :**
1. Lancer un seul fichier, puis un seul test avec `-k`.
2. Lancer la suite smoke : `uv run pytest -m smoke`. Combien de tests ? Où sont déclarés les marqueurs ?
3. Faire échouer un test volontairement (changer `"Mon compte"` dans `tests/ui/customer/test_account.py`).
   Ouvrir `test-results/` : trace, capture, vidéo. Ouvrir la trace avec `uv run playwright show-trace <chemin>/trace.zip`.
4. Ajouter `page.pause()` dans un test et le lancer avec `--headed` : explorer le Playwright Inspector.
5. Annuler les modifications.

**À retenir :** en cas d'échec, la trace est la première chose à ouvrir, comme dans le projet TypeScript.
Le UI mode (`--ui`) n'existe pas en Python : voir [le comparatif UI mode / Trace Viewer](commandes.md#pas-de-ui-mode-en-python--trace-viewer-à-la-place).

---

### Étape 3 · Lire un test de bout en bout

**Objectif :** suivre le chemin complet d'un test, du test jusqu'au navigateur.

**À lire, dans cet ordre :**
1. [tests/ui/guest/test_search.py](../tests/ui/guest/test_search.py)
2. [framework/fixtures/pages.py](../framework/fixtures/pages.py) (d'où vient `home_page`)
3. [framework/pages/home_page.py](../framework/pages/home_page.py), puis [components/search_bar.py](../framework/pages/components/search_bar.py)
4. [docs/architecture.md](architecture.md), section « Flux d'un test »

**À faire :**
1. Lancer `uv run pytest --fixtures-per-test tests/ui/guest/test_search.py -k Pliers`.
   Repérer pour chaque fixture le fichier qui la définit.
2. Répondre : pourquoi le test ne contient-il aucun nombre de produits attendu ?

**Notions Python :**
- `def test_x(home_page: HomePage) -> None` : `: HomePage` et `-> None` sont des **annotations de type**, comme en TypeScript. pytest injecte `home_page` d'après le **nom** du paramètre.
- `@pytest.mark.parametrize` : un test lancé une fois par valeur (comme une boucle `for` sur des tests en TypeScript).
- `pytestmark = pytest.mark.ui` : applique un marqueur à tout le fichier.

**À retenir :** un test ne contient que le **quoi** (scénario, assertions). Le **comment** est dans les pages.

---

### Étape 4 · Les page objects

**Objectif :** écrire sa première page.

**À lire :** [framework/pages/base_page.py](../framework/pages/base_page.py), [login_page.py](../framework/pages/login_page.py), [docs/conventions.md](conventions.md) section « Page objects ».

**À faire :** créer une page de contact et un test du formulaire vide.
1. `framework/pages/contact_page.py` : classe `ContactPage(BasePage)` avec `path = "contact"`,
   le bouton `contact-submit` et les messages d'erreur `first-name-error`, `email-error`...
2. Ajouter la fixture `contact_page` dans `framework/fixtures/pages.py`.
3. `tests/ui/guest/test_contact.py` : ouvrir la page, cliquer sur Envoyer,
   vérifier « Le prénom est requis » et « L'email est requis ».
4. Lancer `uv run ruff check .` et `uv run mypy`.

**Notions Python :**
- `path: ClassVar[str]` : attribut de **classe** (commun à toutes les instances), comme `static` en Java.
- `-> Self` : la méthode renvoie l'objet lui-même, ce qui permet `login_page = LoginPage(page).open()`.
- `super().__init__(page)` : appelle le constructeur de `BasePage` (`super(page)` en Java et TypeScript).

**À retenir :** une page = un `path` + des locators + des actions métier, **sans assertion**.

---

### Étape 5 · Les fixtures pytest

**Objectif :** comprendre le mécanisme central du projet.

**À lire :** [framework/fixtures/](../framework/fixtures/) (tous les fichiers), [conftest.py](../conftest.py), [tests/ui/customer/conftest.py](../tests/ui/customer/conftest.py).

**À faire :**
1. Dans `framework/fixtures/data.py`, repérer le `yield` : qu'est-ce qui s'exécute avant, et après le test ?
2. Lancer `uv run pytest tests/api -s --setup-show` : observer l'ordre de création et de destruction des fixtures et leur portée (`S` = session, `F` = function).
3. Répondre : pourquoi `base_url` est-elle dans le `conftest.py` racine et pas dans `framework/fixtures/browser.py` ? (le commentaire de la fixture donne la réponse)
4. Répondre : comment les tests de `tests/ui/customer/` reçoivent-ils la session du client, sans rien demander ?

**Notions Python :**
- `@pytest.fixture` est un **décorateur** : il transforme la fonction en fixture.
- `scope="session"` : créée une seule fois pour toute l'exécution (par défaut : une fois par test).
- `yield` : tout ce qui suit s'exécute **après** le test, même s'il échoue (le teardown).
- Une fixture peut en **redéfinir** une autre du même nom, et recevoir l'ancienne valeur en paramètre.
  C'est ainsi que `browser_context_args` est enrichi à chaque niveau.
- `{**args, "locale": "fr-FR"}` : copie d'un dictionnaire avec une clé en plus (le `{...args}` de TypeScript).

**À retenir :** les fixtures remplacent à la fois le `@BeforeEach`/`@AfterEach` de JUnit et l'injection de dépendances.

---

### Étape 6 · Configuration et environnements

**Objectif :** savoir d'où vient chaque valeur.

**À lire :** [framework/config/settings.py](../framework/config/settings.py), [environments/demo.env](../environments/demo.env), [.env.example](../.env.example).

**À faire :**
1. `ENV=inconnu uv run pytest tests/api` : lire le message d'erreur.
2. `CUSTOMER_EMAIL= uv run pytest` : quels tests échouent, lesquels passent ? Pourquoi ?
3. Créer `environments/qa.env` (mêmes URLs que `demo`) et lancer `ENV=qa uv run pytest -m smoke`.
4. Supprimer `qa.env`.

**Notions Python :**
- `@dataclass(frozen=True)` : classe de données non modifiable (comme un `record` Java).
- `@property` : méthode lue comme un attribut (`settings.customer`), calculée au moment de l'accès.
- `@cache` : le résultat est calculé une seule fois, puis réutilisé.

**À retenir :** variables réelles > `.env` > `environments/<ENV>.env`. Un secret ne va jamais dans `environments/`.

---

### Étape 7 · La couche API et pydantic

**Objectif :** ajouter un appel API et comprendre la validation des réponses.

**À lire :** [framework/api/](../framework/api/), [tests/api/](../tests/api/).

**À faire :**
1. Ajouter `ProductsApi.get(product_id: str) -> Product`, qui appelle `GET /products/{id}`.
2. Écrire un test d'API : rechercher « Pliers », puis récupérer le premier produit par son id et vérifier que le nom est identique.
3. Casser volontairement le modèle : renommer `price` en `prix` dans `Product`. Lancer les tests d'API et lire l'erreur pydantic. Annuler.

**Notions Python :**
- `class Product(ApiModel)` avec `name: str` : pydantic **vérifie à l'exécution** que la réponse contient bien ces champs et ces types. C'est ce qui manquait en TypeScript, où les types disparaissent à l'exécution.
- `model_validate(json)` : transforme le JSON en objet validé.

**À retenir :** le même client API sert aux tests d'API **et** à préparer les données des tests UI.

---

### Étape 8 · Sessions et données isolées

**Objectif :** comprendre comment les tests restent indépendants.

**À lire :** [framework/fixtures/auth.py](../framework/fixtures/auth.py), [framework/fixtures/data.py](../framework/fixtures/data.py), [framework/data/users.py](../framework/data/users.py), [docs/architecture.md](architecture.md) sections « Sessions par rôle » et « Données isolées ».

**À faire :**
1. Lancer `uv run pytest -n 2`, puis regarder le dossier `.auth/` : pourquoi un fichier par worker ?
2. Écrire une fixture `customer_token` dans `framework/fixtures/data.py`, qui utilise `new_customer` et renvoie son jeton de connexion.
3. Réécrire `tests/api/test_users_api.py` pour utiliser `customer_token`.
4. Répondre : quel test faudrait-il écrire avec `new_customer` plutôt qu'avec la session partagée du client ? (indice : tout ce qui modifie le compte)

**À retenir :** compte partagé pour **lire**, données créées par le test pour **modifier**.

---

### Étape 9 · Qualité et CI

**Objectif :** savoir ce qui bloque un build et pourquoi.

**À lire :** `pyproject.toml` (sections ruff et mypy), [Jenkinsfile](../Jenkinsfile).

**À faire :**
1. Retirer le `-> None` d'un test : lancer `uv run mypy`. Remettre.
2. Passer un `int` à `login_page.submit(...)` : lancer `uv run mypy`. Annuler.
3. Mal ordonner deux imports : lancer `uv run ruff check . --fix`.
4. Lancer les tests exactement comme Jenkins (voir l'étape « Run Tests »), avec le serveur Docker :
   `PLAYWRIGHT_SERVER=ws://127.0.0.1:3000/ uv run pytest -n 4 --reruns 2 --html=reports/report.html --self-contained-html`.
   Ouvrir `reports/report.html`.

**À retenir :** ruff et mypy attrapent avant l'exécution ce que Java attrape à la compilation.

---

### Étape 10 · Faire évoluer le projet

**Objectif :** vérifier que l'architecture accepte une évolution sans modifier l'existant.

**À lire :** [docs/evolutions.md](evolutions.md).

**À faire (au choix, une ou plusieurs) :**
- Ajouter une suite `regression` et l'appliquer à quelques tests.
- Ajouter l'export JSON (`pytest-json-report`).
- Lancer les tests smoke sur Firefox en plus de Chromium.
- Bonus : passer `test_search.py` en BDD avec `pytest-bdd`, en réutilisant les fixtures existantes.

Pour chaque évolution, noter les fichiers modifiés. Si un fichier existant a dû être modifié en profondeur, c'est un point d'architecture à discuter.

---

### Bilan

À la fin du parcours, vous savez :

- [ ] lancer, filtrer et déboguer les tests, et lire une trace ;
- [ ] suivre un test jusqu'au navigateur à travers les fixtures ;
- [ ] écrire une page, un composant et sa fixture ;
- [ ] écrire une fixture avec setup et teardown, et choisir sa portée ;
- [ ] ajouter un environnement et expliquer l'ordre de priorité de la configuration ;
- [ ] ajouter un appel API validé par pydantic ;
- [ ] isoler les données d'un test ;
- [ ] expliquer ce que bloquent ruff, mypy et le pipeline Jenkins ;
- [ ] faire évoluer le projet sans casser l'existant.
