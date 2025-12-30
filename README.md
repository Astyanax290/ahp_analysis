## Analyse Multicritère Hiérarchique (AHP Raster)

### **Présentation**

Analyse Multicritère Hiérarchique (AHP Raster) est un plugin QGIS permettant de réaliser des analyses multicritères spatiales basées sur la méthode AHP (Analytic Hierarchy Process) de Saaty, appliquées à des données raster classifiées.

Le plugin s’adresse aux géographes, géomaticiens, urbanistes, chercheurs et étudiants, souhaitant combiner plusieurs critères spatiaux pondérés afin de produire une carte de décision synthétique.



### **Principe méthodologique**

Le plugin suit strictement les étapes de la méthode AHP :

Définition des critères

Assignation des rasters à chaque critère

Comparaison pair-à-pair des critères

Calcul des poids et vérification de la cohérence

Combinaison pondérée des rasters

Le ratio de cohérence (CR) est automatiquement calculé et doit être ≤ 0.1 pour valider l’analyse.



### **Prérequis**

QGIS ≥ 3.xx

Données raster :
normalisées
mêmes dimensions spatiales
mêmes projections
**Connaissances de base en analyse multicritère**



### **Cas d’usage**

* Analyse territoriale
  Aide à la décision spatiale
  Études d’aménagement
  Urbanisme, environnement, infrastructures



### **Limites connues**

Les rasters Cost ne sont pas inversés automatiquement

L’utilisateur est responsable de la préparation des données

L’analyse est limitée à des fichiers rasters. Ne fonctionne pas sur des vecteurs



### **Auteur**

Sewedo GNANSOUNOU

Projet développé dans un cadre académique.



### **Licence**

Ce projet est distribué sous licence GNU GPL v3.
Voir le fichier LICENSE pour plus de détails.



### **Perspectives d’évolution**

Inversion automatique des critères Cost
Export des poids et matrices (CSV)
Visualisation graphique des poids
Support multi échelles
Intégration d’autres méthodes AMC (WLC, ELECTRE…)

