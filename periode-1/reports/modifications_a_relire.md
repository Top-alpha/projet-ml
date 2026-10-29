# Modifications à relire — analyse exploratoire

- Sections 0 à 2 : code conservé. Sorties recalculées ; numérotation « 2.3 Doublons » corrigée. Plan mis à jour.
- Section 2.2 : ajout d’une réserve en italique sur la différence entre association descriptive et performance d’un modèle.
- Section 2.5 : ajout d’une réserve en italique sur le test d’égalité textuelle. La section 8 distingue effectivement chemins, paramètres et fragments.
- Section 3 : 32 719 titres « 0 » au total, dont 32 714 avec HasTitle=0 et cinq avec HasTitle=1. L’écart ne constitue pas nécessairement une erreur.
- Section 8 : 28 489 URL avec chemin non racine ou paramètres, contre 28 689 inégalités textuelles dans le premier test ; le constat d’absence de chemins chez les légitimes est confirmé.
- Sections 3 à 9 : cellules complétées ou remplacées avec explications, tableaux, dix figures et interprétations. Aucun entraînement ni préparation de splits.
- Rapport d’analyse exploratoire rédigé à partir des constats du notebook.

## Vérification technique

Le lancement d’un noyau Jupyter a échoué car l’environnement interdit l’ouverture des ports locaux requis. Les cellules ont été exécutées dans l’ordre avec Python/IPython, dans un espace de variables neuf, avec les bibliothèques de `.venv`. Les sorties et figures sont sauvegardées dans le notebook. Cette vérification ne remplace pas un dernier « redémarrer puis tout exécuter » dans votre propre interface Jupyter.

Les données brutes et les fichiers des autres étudiants ne sont pas modifiés. Aucun site du CSV n’a été ouvert. Les causes de collecte, la validité actuelle des URL et les performances d’un modèle ne sont pas établies par cette analyse.
