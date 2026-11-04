# Audit du dataset original

## Objectif et périmètre

L'audit porte sur le fichier PhiUSIIL local, avant toute transformation. Il distingue les incohérences internes, les écarts à une convention définie et les limites de reproductibilité. Aucun site n'est ouvert : les URL sont des données textuelles. La recherche générale sur le phishing et le découpage ne sont pas traités dans ce document.

Le fichier contient **235,795 lignes et 56 colonnes**. La cible vaut 0 pour le phishing et 1 pour les URL légitimes. Les 54 variables déclarées par UCI s'ajoutent à la cible et à l'identifiant FILENAME. Les effectifs sont de 100 945 phishing et 134 850 légitimes.

## Article de référence et disponibilité des entrées

Prasad et Chandra décrivent une collecte de sites légitimes depuis Open PageRank et de phishing depuis PhishTank, OpenPhish et MalwareWorld, avec téléchargement de pages de phishing d'octobre 2022 à mai 2023 (section 3.1, page 5). Ces sources différentes justifient d'examiner un biais de provenance, sans établir à elles seules la cause de chaque contraste.

Leur méthode associe des caractéristiques d'URL, du HTML et des scores dérivés. Les variables HTML ne sont pas retenues pour notre application, dont l'extraction est strictement locale. URLCharProb et TLDLegitimateProb dépendent de fréquences issues d'un corpus de dix millions de références ; URLSimilarityIndex utilise une liste de références et une comparaison pondérée (pages 6 à 8). L'article donne des principes et des algorithmes, mais ne garantit pas ici la disponibilité des ressources et de toutes les conventions nécessaires à une reproduction exacte des colonnes du CSV.

Il serait donc incorrect de conclure que toutes les variables de l'article sont fausses. Nous choisissons une autre convention d'extraction, explicite et reproductible, adaptée aux entrées réellement disponibles au backend.

## Qualité initiale et doublons

Aucune cellule manquante classique n'est détectée. Ce constat ne signifie pas que toutes les informations sont présentes : 32 719 titres valent le texte « 0 », dont cinq avec HasTitle = 1. Ces titres ne sont pas utilisés dans le dataset reconstruit.

Il n'y a aucune ligne entièrement identique hors FILENAME. Cependant, **425 URL distinctes apparaissent deux fois**, soit 850 lignes concernées et 425 copies en excès. Les caractéristiques originales de ces copies peuvent différer. Aucune de ces URL n'a de labels contradictoires. L'affirmation de l'article concernant l'unicité des enregistrements n'exclut donc pas les répétitions d'URL.

On observe 5526 domaines originaux répétés, dont 54 présents dans les deux classes. Les domaines répétés ne sont pas supprimés automatiquement : ils peuvent héberger des pages distinctes. Ils devront être pris en compte par le responsable du découpage.

## Conventions comparées aux colonnes originales

Chaque comparaison indique les lignes comparables, les exclusions, l'accord global et l'accord par classe. Les variables TLD sont comparées sur les hôtes DNS, en excluant les IP. Pour les ratios, une tolérance absolue de 0,0005 avec marge numérique de 1e-12 permet d'examiner l'hypothèse d'un arrondi à trois décimales. Une égalité à cette tolérance n'est pas une égalité bit à bit.

| variable | comparables | ecarts | accord_pct |
| --- | --- | --- | --- |
| Domain | 235795 | 36 | 99.985 |
| DomainLength | 235795 | 36 | 99.985 |
| TLD | 235187 | 17 | 99.993 |
| TLDLength | 235187 | 17 | 99.993 |
| IsDomainIP | 235795 | 30 | 99.987 |
| IsHTTPS | 235795 | 493 | 99.791 |
| NoOfLettersInURL | 235795 | 235795 | 0.000 |
| LetterRatioInURL | 235795 | 235794 | 0.000 |
| NoOfDegitsInURL | 235795 | 1210 | 99.487 |
| DegitRatioInURL | 235795 | 21512 | 90.877 |
| NoOfEqualsInURL | 235795 | 249 | 99.894 |
| NoOfQMarkInURL | 235795 | 12 | 99.995 |
| NoOfAmpersandInURL | 235795 | 3172 | 98.655 |
| NoOfOtherSpecialCharsInURL | 235795 | 235528 | 0.113 |
| SpacialCharRatioInURL | 235795 | 235609 | 0.079 |
| HasObfuscation | 235795 | 402 | 99.830 |
| NoOfObfuscatedChar | 235795 | 797 | 99.662 |
| ObfuscationRatio | 235795 | 798 | 99.662 |

Les comptages de lettres et de caractères spéciaux sur toute l'URL diffèrent largement des colonnes originales. Ce résultat signale un périmètre de calcul différent, pas automatiquement une erreur du dataset.

## Quatre accords internes et un diagnostic distinct

Les relations DomainLength = len(Domain), TLDLength = len(TLD), LetterRatioInURL = NoOfLettersInURL / URLLength et DegitRatioInURL = NoOfDegitsInURL / URLLength concordent à 100 % avec la tolérance annoncée pour les ratios. Ces quatre constats utilisent les champs originaux ; ils ne prouvent pas que ces champs sont eux-mêmes reproductibles depuis le texte de l'URL.

| variable | convention | ecarts | accord_pct |
| --- | --- | --- | --- |
| DomainLength | longueur du champ Domain original | 0 | 100.000 |
| TLDLength | longueur du champ TLD original | 0 | 100.000 |
| LetterRatioInURL | comptage original / URLLength original | 0 | 100.000 |
| DegitRatioInURL | comptage original / URLLength original | 0 | 100.000 |
| SpacialCharRatioInURL | comptage original / URLLength original | 6569 | 97.214 |

Le contrôle du ratio des caractères spéciaux conserve des écarts. Pour IsHTTPS, le test du schéma du parseur révèle 493 écarts dans le CSV. En revanche, chercher « https » n'importe où dans le texte reproduit la colonne originale. Cela est compatible avec une recherche textuelle dans la préparation, sans démontrer le code des auteurs. Une URL HTTP avec un paramètre contenant une URL HTTPS reste HTTP pour notre extraction.

Le test d'adresse IP sur l'hôte présente 30 écarts avec IsDomainIP original. Des exemples contiennent une suite ressemblant à une IP au début d'un nom DNS. Notre convention exige que l'hôte entier soit reconnu comme adresse IPv4 ou IPv6.

Le nombre de labels moins deux et la continuité sur l'hôte sans www ni dernier label donnent des accords élevés, mais restent des sondes. Le premier ne remplace pas une liste des suffixes publics. Le second n'est pas retenu dans notre ensemble initial de 18 caractéristiques.

## Scores externes : contrôle de cohérence seulement

| groupe | score | groupes_valeurs_distinctes | lignes |
| --- | --- | --- | --- |
| TLD | TLDLegitimateProb | 0 | 0 |
| URL | URLCharProb | 136 | 272 |
| URL | URLSimilarityIndex | 21 | 42 |

Les variations à URL identique peuvent provenir de traitements ou de références différents. Leur cause n'est pas établie. La constance de TLDLegitimateProb par TLD est cohérente avec son principe, sans valider le corpus de calcul. Aucun de ces scores n'est utilisé dans la reconstruction.

## Décision

Conserver le CSV original intact, reconstruire 18 caractéristiques depuis URL, conserver label sans le réinterpréter et employer la même fonction dans la préparation et le futur backend. Les exemples détaillés sont exportés dans audit_exemples_ecarts.csv ; ils sont analysés comme chaînes inertes. URLLength n'est pas réaudité dans les comparaisons de cette étape ; sa nouvelle valeur est simplement calculée par len(URL.strip()).

## Références

Prasad, A. et Chandra, S. (2024). PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning. Computers & Security, 136, 103545. DOI : https://doi.org/10.1016/j.cose.2023.103545. Sections 3.1, 4.1 et 5.3.

UCI Machine Learning Repository. PhiUSIIL Phishing URL (Website), dataset 967. https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset.
