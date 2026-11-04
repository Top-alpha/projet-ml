# Reconstruction et conventions de calcul

## Principe

Le nouveau dataset provient des URL et des labels du fichier original. Il ne s'agit ni d'une nouvelle collecte ni d'une création d'étiquettes. Les anciennes caractéristiques ne sont pas reprises comme entrées. La fonction extract_url_features, version 1.0.0, ne reçoit que l'URL et ne réalise aucun appel réseau.

Le fichier reconstruit possède **21 colonnes** : URL, Domain, label, 17 caractéristiques numériques et une caractéristique catégorielle TLD_calc. URL et Domain sont des métadonnées destinées à la traçabilité et aux contrôles ; label est la cible. Les 18 caractéristiques sont définies dans FEATURE_COLUMNS.

## Texte de référence et validation syntaxique

U = URL.strip(). Les espaces aux extrémités sont retirés pour le calcul, mais l'URL originale reste enregistrée jusqu'au nettoyage. Aucun caractère interne n'est supprimé, aucune séquence %HH n'est décodée et aucun chemin n'est tronqué. Les comptages portent sur toute la chaîne U, y compris schéma, port, identifiants éventuels, chemin, paramètres et fragment. Une lettre désigne exclusivement A-Z ou a-z, et un chiffre exclusivement 0-9. Les autres caractères Unicode font partie des autres caractères selon cette convention.

Seuls HTTP et HTTPS avec une autorité et un hôte sont acceptés. Les contrôles rejettent les espaces et contrôles internes, les ports invalides, les hôtes absents, les encodages ou zones IPv6 dans l'hôte et les noms DNS non pris en charge. Ce contrôle est syntaxique : il ne prouve ni l'existence ni la sûreté du site. Les échecs conservent leur ligne et leur label dans reconstructed, avec caractéristiques manquantes et motif dans extraction_errors.csv.

## Hôte et TLD

H est le hostname du parseur, en minuscules, sans port ni identifiants et sans point DNS final. Les noms DNS Unicode sont convertis en IDNA par la bibliothèque standard Python ; les comptages sur U restent réalisés sur le texte Unicode original. Les adresses IP restent celles du parseur, sans crochets IPv6. L'hôte n'est pas résolu par DNS. Les underscores sont tolérés dans les labels DNS, règle explicite de compatibilité syntaxique. Les labels DNS ont au plus 63 caractères et l'hôte DNS au plus 253.

TLD_calc est le dernier label DNS si H contient un point et n'est pas une IP. Il vaut la chaîne vide pour les IP et les noms sans point. Pour shop.exemple.co.uk, il vaut uk, pas co.uk. Le vide constitue ici une catégorie structurelle, pas une information manquante. La lecture CSV utilise keep_default_na=False pour la conserver.

## Calculs numériques

Les longueurs utilisent len, donc le nombre de points de code Python, pas la taille UTF-8 en octets. Le domaine IDNA peut ainsi avoir une longueur différente de la représentation Unicode saisie.

Les compteurs =, ? et & mesurent des caractères littéraux, pas un nombre de paramètres. Un %3F ne compte pas comme ?. Les autres caractères sont ceux qui ne sont ni des lettres ASCII, ni des chiffres ASCII, ni =, ?, &. La somme de ces six catégories couvre exactement U.

Le ratio de chaque catégorie retenue est son compteur divisé par len(U). Aucun ratio n'est arrondi lors du calcul ; le CSV conserve la précision numérique et les contrôles utilisent 1e-12.

Le percent-encoding est détecté par % suivi de deux chiffres hexadécimaux. %61%2F donne deux jetons, %ZZ n'en donne aucun. percent_encoded_count compte les jetons, pas leurs trois caractères de représentation. has_percent_encoding indique au moins un jeton ; percent_encoded_ratio vaut nombre de jetons / len(U). L'encodage ne constitue pas en lui-même une preuve d'obfuscation malveillante, d'où les nouveaux noms.

## Résultat de reconstruction

235,795 lignes entrantes, 235,795 lignes reconstruites et 0 échecs. Aucune URL ni étiquette n'est supprimée à cette étape. Les anciennes colonnes ne sont pas conservées dans le fichier reconstruit, mais restent disponibles dans raw/dataset.csv.

Les copies d'une même URL produisent désormais les mêmes caractéristiques. Cela explique pourquoi 425 copies de lignes complètes existent après reconstruction, alors que le fichier original n'en comportait aucune hors identifiant.

## Reproductibilité

Empreinte SHA-256 du brut : `a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6`.

Empreinte SHA-256 du reconstruit : `2041a7127c7a2c60f05d8bbf3cfa77ae137c0d467b0c7af0c3b722f33ee8819b`.

Les chemins, empreintes, version d'extraction, ordre des colonnes et liste des entrées figurent dans data/reconstructed/manifest.json. Les tests vérifient les cas ASCII, Unicode, IP, IPv6, ports, identifiants, encodage, URL invalides et absence de requêtes réseau.

## Usage futur

Le backend importe la même fonction, sans implémentation parallèle. TLD_calc devra être encodé avec gestion des catégories inconnues. La standardisation et les autres transformations apprises ne sont pas réalisées en période 1 ; elles devront être ajustées uniquement sur les données d'entraînement après découpage. Aucun label n'intervient dans l'extraction.
