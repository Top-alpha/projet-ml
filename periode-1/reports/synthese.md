# Synthèse des travaux réalisés

Le fichier original de 235 795 lignes et 56 colonnes est conservé intact. L'audit distingue les écarts de convention des erreurs démontrées et justifie une extraction locale adaptée à une URL saisie par l'utilisateur. La reconstruction génère 18 caractéristiques selon des règles explicites, sans téléchargement ni label comme entrée.

Les 235 795 lignes sont reconstruites sans échec. L'analyse retrouve les répétitions d'URL, mesure les nouvelles distributions, identifie les redondances et documente les limites de représentativité. Les vecteurs lexicaux ne suffisent pas à distinguer toutes les URL : 292 groupes de caractéristiques contiennent des labels différents.

Le nettoyage place 425 copies d'URL en quarantaine et conserve 235 370 lignes : 134 850 légitimes et 100 520 phishing. Les 21 colonnes restent inchangées et tous les contrôles finaux sont satisfaits. Aucun modèle n'est entraîné et aucun split n'est produit.

Les trois modèles envisagés sont la régression logistique, l'arbre de décision et le Random Forest. Leur comparaison devra employer les mêmes données et caractéristiques. Les transformations apprises, dont encodage et standardisation, seront ajustées sur l'entraînement uniquement. La présente période ne choisit ni modèle gagnant ni seuil de probabilité.

La cohérence technique entre entraînement et backend est assurée par une fonction unique. Elle ne garantit pas la généralisation : l'absence de chemins dans les URL légitimes et la dépendance des exemples à leur source restent des limites majeures. Les faux positifs, faux négatifs, la calibration et la robustesse relèvent de la suite du projet.
