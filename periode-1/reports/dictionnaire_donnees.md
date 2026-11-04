# Dictionnaire du dataset reconstruit

U désigne URL.strip(). La convention est indépendante du label. Les noms Degit et Spacial sont conservés pour la correspondance avec le dataset original ; le suffixe calc signale leur recalcul. Les variables de percent-encoding sont renommées pour éviter une interprétation automatique comme malveillance.

| colonne | type | definition | role |
| --- | --- | --- | --- |
| URL | Texte | URL source, puis strip au nettoyage | Métadonnée, exclue des entrées |
| Domain | Texte | Hôte du parseur, minuscules et IDNA DNS, sans port/identifiants/point final | Métadonnée pour contrôles et groupes |
| label | Entier | Étiquette source : 0 phishing, 1 légitime | Cible, jamais une entrée |
| URLLength_calc | Entier | len(URL.strip()) | Entrée |
| DomainLength_calc | Entier | len(Domain) | Entrée |
| IsDomainIP_calc | Binaire | 1 si ipaddress reconnaît tout l’hôte | Entrée |
| IsHTTPS_calc | Binaire | 1 si le schéma du parseur vaut https | Entrée |
| TLDLength_calc | Entier | len(TLD_calc) | Entrée |
| NoOfLettersInURL_calc | Entier | Nombre de lettres ASCII A-Z et a-z dans U | Entrée |
| LetterRatioInURL_calc | Réel [0,1] | Nombre de lettres / len(U) | Entrée |
| NoOfDegitsInURL_calc | Entier | Nombre de chiffres ASCII 0-9 dans U | Entrée |
| DegitRatioInURL_calc | Réel [0,1] | Nombre de chiffres / len(U) | Entrée |
| NoOfEqualsInURL_calc | Entier | Nombre de = littéraux | Entrée |
| NoOfQMarkInURL_calc | Entier | Nombre de ? littéraux | Entrée |
| NoOfAmpersandInURL_calc | Entier | Nombre de & littéraux | Entrée |
| NoOfOtherSpecialCharsInURL_calc | Entier | Caractères hors lettres ASCII, chiffres ASCII et =?& | Entrée |
| SpacialCharRatioInURL_calc | Réel [0,1] | Nombre des autres caractères / len(U) | Entrée |
| has_percent_encoding | Binaire | Présence d’au moins un jeton %HH hexadécimal | Entrée |
| percent_encoded_count | Entier | Nombre de jetons %HH, sans décodage | Entrée |
| percent_encoded_ratio | Réel [0,1] | Nombre de jetons %HH / len(U) | Entrée |
| TLD_calc | Catégorie | Dernier label DNS ; vide pour IP ou hôte sans point | Entrée à encoder ultérieurement |

Le fichier possède 21 colonnes et 18 caractéristiques prédictives avant encodage. Les colonnes URL, Domain et label sont exclues des entrées numériques. Les ratios ne sont pas arrondis dans les fichiers. La catégorie vide de TLD est intentionnelle ; toutes les autres valeurs manquantes doivent être signalées.
