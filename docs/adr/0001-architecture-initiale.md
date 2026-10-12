# ADR 0001 — Architecture initiale

- **Statut** : accepté
- **Date** : 2026-10-12

## Contexte

Assistant de questions-réponses sur la réglementation bancaire BCEAO/UMOA,
en français, pour des professionnels de la conformité, du risque et du droit.

Contraintes du domaine :
- une réponse fausse ou non sourcée a un coût réel ;
- les textes sont structurés (titres, chapitres, articles) et versionnés ;
- les établissements financiers sont réticents à envoyer leurs données
  vers des API externes.

## Décisions

| # | Décision | Justification |
|---|---|---|
| 1 | Architecture **RAG simple**, pas multi-agents | Le besoin est de répondre à partir d'un corpus : l'architecture la plus simple qui résout le problème. |
| 2 | **LLM et embeddings locaux** via Ollama | Aucune donnée ne quitte l'infrastructure ; argument de confidentialité pour les banques. |
| 3 | **Ports et adaptateurs** (`regumoa.ports`) | Le pipeline ne dépend que de contrats : tests sans modèle, changement de fournisseur sans réécriture. |
| 4 | **Orchestration écrite à la main** | Contrôle total, peu de dépendances, chaque étape explicable et testable. |
| 5 | **PostgreSQL + pgvector** (à venir) | Déjà présent dans les SI bancaires ; vecteurs et plein texte français dans un seul moteur. |
| 6 | **Citations obligatoires et refus explicite** | Toute affirmation renvoie à un article ; hors corpus, l'assistant le dit. |
| 7 | **Poetry**, ruff, mypy strict, pytest, pre-commit, CI | Environnement reproductible et qualité vérifiée à chaque commit et à chaque PR. |

## Alternatives écartées

- **LangChain / LlamaIndex** : accélèrent un prototype, mais ajoutent des
  couches d'abstraction difficiles à déboguer et à expliquer.
- **API LLM dans le cloud** : meilleure qualité brute, mais incompatible avec
  l'exigence de confidentialité. Reste possible plus tard via un adaptateur.
- **Base vectorielle dédiée** (Chroma, Qdrant) : un composant de plus à
  exploiter, sans gain décisif à l'échelle du MVP.

## Conséquences

- La qualité dépend d'un modèle local de taille modeste : la précision de la
  recherche et la rigueur du prompt doivent compenser. Un jeu d'évaluation
  mesurera l'écart.
- Les tests et la CI n'exécutent jamais de vrai modèle ; des tests
  d'intégration séparés tourneront sur une machine équipée d'Ollama.
