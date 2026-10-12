# Assistant réglementaire UMOA

![CI](https://github.com/mory2154/assistant-reglementaire-umoa/actions/workflows/ci.yml/badge.svg)

> 🚧 Projet en construction, développé étape par étape.

Assistant de questions-réponses sur la réglementation bancaire **BCEAO / UMOA**,
en français. Objectif : **citer l'article source** de chaque affirmation, et
**refuser plutôt qu'inventer** quand la réponse n'est pas dans les textes.
Le LLM et les embeddings tournent **en local** (Ollama) : aucune donnée ne
quitte l'infrastructure.

## Pourquoi ce projet

La réglementation bancaire de la BCEAO et de l’UMOA est dense, évolutive et parfois difficile à exploiter rapidement, notamment pour les professionnels de la conformité, les juristes et les auditeurs. Ce projet vise à faciliter l’accès à une information réglementaire fiable grâce à un assistant capable de répondre en français à partir des textes officiels, en citant précisément les articles qui justifient ses réponses. Conçu avec une architecture RAG et des modèles d’IA exécutés localement via Ollama, il privilégie la traçabilité, la confidentialité et la maîtrise des données. Son principe fondamental est simple : **fournir des réponses vérifiables et reconnaître ses limites plutôt que d’inventer une information réglementaire.**

## État d'avancement

- [x] Cadrage du besoin et critères de succès — [docs/cadrage.md](docs/cadrage.md)
- [x] Fondations : Poetry, ruff, mypy strict, pytest, pre-commit, CI GitHub Actions
- [x] Configuration par variables d'environnement
- [x] Ports et adaptateurs (LLM, embeddings) avec adaptateurs factices
- [ ] Corpus réglementaire : collecte et gouvernance
- [ ] Extraction des PDF et découpage par article
- [ ] Indexation (PostgreSQL + pgvector)
- [ ] Recherche hybride
- [ ] Génération avec citations et refus
- [ ] Évaluation
- [ ] API, interface, sécurité, déploiement

## Architecture cible

```
PDF officiels → extraction → découpage par article → embeddings → PostgreSQL / pgvector
                                                                        │
Question → recherche hybride → LLM local → réponse citée + garde-fous ◀─┘
```

Le code métier dépend de contrats (`src/regumoa/ports.py`), pas d'un
fournisseur : Ollama en production, modèles factices déterministes en test.
Décisions détaillées : [docs/adr/](docs/adr/).

## Démarrage

Prérequis : Python 3.12+ et Poetry 2.x.

```bash
git clone https://github.com/mory2154/assistant-reglementaire-umoa.git
cd assistant-reglementaire-umoa
poetry install
cp .env.example .env
poetry run pre-commit install
poetry run pytest
```

## Qualité

```bash
poetry run ruff check .          # lint
poetry run ruff format --check . # format
poetry run mypy src tests        # typage strict
poetry run pytest                # tests
```

Les mêmes vérifications tournent avant chaque commit (pre-commit) et sur
chaque pull request (CI, Python 3.12 et 3.13).

## Auteur

Dr. Namory Fofana
