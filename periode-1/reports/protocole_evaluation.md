1__PROTOCOLE D'EVALUATION

Avant de procéder à l'entraînement des modèles de classification, il est nécessaire de diviser le jeu de données en plusieurs sous-ensembles distincts. Ce découpage permet d'obtenir une évaluation fiable des performances des modèles tout en limitant les risques de surapprentissage. L'objectif est de mesurer la capacité du modèle à généraliser sur de nouvelles données qu'il n'a jamais observées auparavant.


Le jeu de données a été séparé en trois ensembles distincts :


    Ensemble d'entraînement : 164763 observations (70 %)
    Ensemble de validation : 47070 observations (20 %)
    Ensemble de test : 23537 observations (10 %)


Une stratification a été appliquée lors du découpage afin de conserver la même distribution des classes dans chacun des sous-ensembles. Cette méthode garantit que les proportions d'URL légitimes et d'URL de phishing restent similaires dans les ensembles d'entraînement, de validation et de test.

1.1__ Rôle de chaque ensemble

Ensemble d'entraînement


L'ensemble d'entraînement est utilisé pour apprendre les relations entre les caractéristiques des URL et leur classe associée. Les algorithmes exploitent ces données afin d'ajuster leurs paramètres internes.


Ensemble de validation

L'ensemble de validation sert à comparer les différents modèles de Machine Learning ainsi qu'à ajuster leurs paramètres. Il permet de sélectionner le modèle présentant les meilleures performances avant l'évaluation finale.


Ensemble de test


L'ensemble de test est utilisé uniquement à la fin du processus. Les données qu'il contient ne sont jamais utilisées pendant l'entraînement ou la validation. Cet ensemble fournit une estimation réaliste des performances du modèle sur des données inédites.

1.2__ Protocole d'évaluation


L'évaluation des modèles suivra les étapes suivantes :


    Entraînement du modèle sur l'ensemble d'entraînement.
    Évaluation sur l'ensemble de validation.
    Comparaison des performances des différents modèles.
    Sélection du modèle le plus performant.
    Évaluation finale du modèle retenu sur l'ensemble de test.


Cette procédure garantit une comparaison équitable entre les modèles tout en préservant l'indépendance des données de test.


1.3__ Métriques d'évaluation


Pour mesurer les performances des modèles, plusieurs indicateurs seront utilisés :



    Accuracy : proportion de prédictions correctes parmi l'ensemble des prédictions réalisées.
    Precision : proportion d'URL prédites comme malveillantes qui le sont réellement.
    Recall : capacité du modèle à détecter les URL de phishing présentes dans le jeu de données.
    F1-Score :compromis entre la précision et le rappel permettant une évaluation globale des performances.

1.4__ Prévention du surapprentissage


Afin de limiter le risque de surapprentissage, les ensembles de validation et de test sont strictement séparés de l'ensemble d'entraînement. Les performances finales seront calculées uniquement sur l'ensemble de test afin d'obtenir une évaluation impartiale et représentative du comportement du modèle dans un contexte réel.
