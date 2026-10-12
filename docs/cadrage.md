# Cadrage — Assistant réglementaire UMOA

- **Version** : 1.0 (MVP)
- **Date** : 2026-10-12
- **Auteur** : Namory Fofana
- **Statut** : validé

---

## 1. Problème

Les banques, fintechs, institutions de microfinance et professionnels de la
conformité perdent du temps à rechercher les textes réglementaires de la
BCEAO, de l'UMOA et de l'UEMOA. Aujourd'hui, ils consultent manuellement des
circulaires, instructions, décisions et autres documents officiels, ou
sollicitent des experts, avec des risques de lenteur, d'oubli et de mauvaise
lecture des textes.

**Ce que fait l'assistant** : il **retrouve, cite et explique** les
dispositions applicables à partir d'un corpus de textes officiels.

**Ce qu'il ne fait pas** : il n'**interprète** pas juridiquement une
situation particulière. L'interprétation et la décision restent humaines.

## 2. Utilisateurs (personas)

Les trois personas sont des professionnels experts : l'interface peut
employer le vocabulaire réglementaire sans le vulgariser.

### Aïcha — chargée de conformité, banque (Abidjan)
- **Besoin** : vérifier rapidement une règle prudentielle avant de valider un
  dossier ou de répondre à sa direction.
- **Aujourd'hui** : recherche dans des PDF de plusieurs centaines de pages, ou
  appel à un collègue.
- **Attente** : une réponse courte avec l'article exact, vérifiable et citable
  dans une note.
- **Cause d'abandon** : une seule réponse fausse relayée à sa direction.

### Karim — juriste, institution de microfinance (Abidjan)
- **Besoin** : identifier les textes applicables aux activités de son
  institution et vérifier ses obligations avant de rédiger une note juridique
  ou de conseiller sa direction.
- **Aujourd'hui** : consulte et compare plusieurs textes, sollicite parfois un
  expert pour confirmer sa lecture.
- **Attente** : une réponse structurée présentant les obligations, les
  articles concernés, les références officielles et, si possible, les
  modifications du texte.
- **Cause d'abandon** : des références inexistantes, une confusion entre un
  texte en vigueur et un texte abrogé, ou une interprétation présentée comme
  certaine sans justification.

### Serge — consultant en conformité réglementaire (Côte d'Ivoire)
- **Besoin** : accélérer ses missions d'audit et de conseil auprès de banques,
  fintechs et institutions de microfinance.
- **Aujourd'hui** : constitue manuellement sa documentation, parcourt les
  articles et compare les exigences aux pratiques de ses clients.
- **Attente** : une recherche rapide dans le corpus, des citations précises,
  des réponses directement exploitables dans ses rapports.
- **Cause d'abandon** : un corpus incomplet présenté comme exhaustif, des
  obligations oubliées, des réponses invérifiables.

### Exigences issues des personas

| Exigence | Origine | Module |
|---|---|---|
| Chaque texte porte un **statut** (en vigueur / abrogé / modifié) et une **date d'effet** | Karim | 3 |
| Chaque texte porte son **émetteur** (BCEAO, Conseil des Ministres de l'UMOA, Commission Bancaire, UEMOA…) | domaine | 3 |
| Les réponses précisent « **dans les textes dont je dispose** » | Serge | 7 |
| La **liste du corpus couvert** est publiée et consultable | Serge | 10 |
| Toute affirmation renvoie à un **article cité et vérifiable** | Aïcha, Karim | 7 |

## 3. Périmètre

### Principe directeur : l'erreur est asymétrique

| Issue | Effet |
|---|---|
| Réponse juste et sourcée | utile |
| « Je ne trouve pas cela dans les textes dont je dispose » | frustrant, sans danger |
| Réponse fausse affirmée avec assurance | **dangereuse** |

L'assistant **préfère refuser plutôt qu'inventer**. Le système privilégie la
précision sur la couverture.

### Questions dans le périmètre

| Type | Exemple | MVP | Difficulté |
|---|---|---|---|
| Factuelle ponctuelle | « Quels sont les délais de transmission des déclarations prudentielles ? » | ✅ | faible |
| Recherche de texte | « Quelle instruction de la BCEAO encadre les activités de paiement dans l'UMOA ? » | ✅ | moyenne |
| Vérification d'article | « Que prévoient les textes sur les exigences de fonds propres des établissements de crédit ? » | ✅ | faible |
| Synthèse multi-articles | « Quelles sont les principales obligations des institutions de microfinance ? » | ✅ réponse signalée comme **partielle** | haute |
| Comparaison de versions | « Qu'est-ce qui a changé entre deux versions d'une instruction ? » | ❌ **V2** | très haute |

Pour chaque question, l'assistant répond à partir du corpus, cite les
références précises et signale toute incertitude ou source insuffisante.

### Hors périmètre

| Catégorie | Exemple | Comportement attendu |
|---|---|---|
| Conseil juridique personnalisé | « Comment éviter une sanction de la BCEAO ? » | **Refus partiel** : présenter les textes relatifs aux sanctions, sans stratégie ni garantie ; renvoyer vers un conseil juridique. |
| Sujet sans rapport | « Quelle stratégie marketing adopter ? » | Refus poli rappelant la spécialité de l'assistant. |
| Certification de conformité | « Confirme que mon établissement respecte toutes les exigences. » | **Refus partiel** : proposer d'identifier les exigences pertinentes et une grille de vérification à faire valider par un professionnel. |
| Donnée susceptible d'avoir changé | « Quel est le taux directeur actuel ? » | Répondre uniquement « selon le texte du [date] », ou refuser ; ne jamais affirmer une valeur actuelle. |

## 4. Exigences non fonctionnelles

| Exigence | Cible | Justification |
|---|---|---|
| **Confidentialité** | Aucune question ni document ne quitte l'infrastructure : LLM et embeddings locaux (Ollama) | Données sensibles des établissements ; souveraineté et contrôle des flux. C'est l'argument principal du LLM local ; le coût est secondaire (le local implique matériel, exploitation, énergie). |
| **Latence perçue** | Premier mot affiché (TTFT) ≤ 3 s au P95 | Avec le streaming, l'utilisateur tolère une réponse longue si elle commence vite. |
| **Latence totale** | Réponse complète ≤ 15 s au P95 | Ne pas interrompre le travail de l'utilisateur. |
| **Langue** | Français | Langue des textes et des utilisateurs. |

Les cibles de latence sont des **hypothèses** : elles dépendent du matériel et
seront confirmées par un benchmark au module 7.

## 5. Critères de succès

| Niveau | Critère | Cible MVP | Mesure | Automatisable |
|---|---|---|---|---|
| Modèle — recherche | Le bon article figure dans les 5 premiers résultats (recall@5) | ≥ 85 % | Jeu de référence de 50 questions | ✅ en CI |
| Modèle — citations | Citations d'un article absent du corpus | **0** | Vérification automatique des identifiants ; **garantie par un garde-fou déterministe** qui bloque la réponse | ✅ |
| Modèle — fidélité | Affirmations soutenues par le passage cité | ≥ 90 % | LLM juge + relecture humaine de 20 réponses | 🟡 |
| Produit — refus | Questions hors périmètre correctement refusées | ≥ 90 % | 20 questions pièges | ✅ |
| Produit — sur-refus | Questions dans le périmètre refusées à tort | ≤ 15 % | Jeu de référence | ✅ |
| Contrainte — latence | TTFT P95 ≤ 3 s ; réponse complète P95 ≤ 15 s | à confirmer | Benchmark sur la machine cible | ✅ |
| Métier | Temps de recherche réduit de 50 % | **hypothèse à valider** | 10 questions chronométrées avec et sans l'outil | manuel |

## 6. Risques

| Risque | Parade | Module |
|---|---|---|
| **Hallucination** : réponse erronée ou référence inventée | Réponses fondées sur le corpus, citations obligatoires, refus si sources insuffisantes, garde-fou bloquant les citations inconnues | 7, 8 |
| **Textes obsolètes ou incomplets** : texte abrogé utilisé, modification ignorée | Manifeste du corpus avec statut et date d'effet, procédure de mise à jour, liste du corpus publiée | 3 |
| **Fuite de données confidentielles** | Hébergement local, contrôle des accès, journaux sans données sensibles | 11 |
| **Extraction PDF erronée** : tableaux cassés, scans, articles mal découpés (erreur silencieuse) | Tests sur extraits réels, contrôle qualité par document | 4 |
| **Excès de confiance des utilisateurs** : réponse recopiée sans vérifier la source | Sources cliquables, extrait affiché, mention « à vérifier dans le texte officiel » | 10 |
| **Prompt injection** : un texte donne des ordres au modèle | Séparation stricte instructions / contenu, tests adverses | 11 |

## 7. Décisions

| Décision | Statut |
|---|---|
| Comparaison de versions de textes reportée en **V2** (exige un corpus multi-versions) | ✅ validée |
| Tableau des critères de succès (section 5) adopté pour le MVP | ✅ validé |
| Corpus limité aux textes officiels publics | ✅ |

## 8. Définition du MVP terminé

Le MVP est terminé quand :
1. les critères automatisables de la section 5 sont mesurés en CI et atteignent leur cible ;
2. la relecture humaine de fidélité a été faite sur 20 réponses ;
3. la latence a été mesurée sur la machine cible ;
4. la liste du corpus couvert est publiée avec l'interface.
