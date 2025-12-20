# ahp_utils.py
# Fonctions pour le calcul AHP (Analytic Hierarchy Process)

import numpy as np

def calculate_weights(matrix):
    """
    Calcule les poids à partir d'une matrice AHP.
    matrix: np.array carrée nxn
    Retourne un tableau numpy avec les poids normalisés.
    """
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_index = np.argmax(np.real(eigvals))
    weights = np.real(eigvecs[:, max_index])
    weights = weights / np.sum(weights)
    return weights

def consistency_ratio(matrix):
    """
    Calcule le ratio de cohérence (CR) d'une matrice AHP.
    CR = CI / RI
    """
    n = matrix.shape[0]
    eigvals, _ = np.linalg.eig(matrix)
    max_eigval = np.max(np.real(eigvals))
    CI = (max_eigval - n) / (n - 1)
    
    # Random Index (RI) selon Saaty
    RI_dict = {1:0, 2:0, 3:0.58, 4:0.90, 5:1.12, 6:1.24, 7:1.32, 8:1.41, 9:1.45, 10:1.49}
    RI = RI_dict.get(n, 1.49)  # valeur par défaut si n > 10
    CR = CI / RI if RI != 0 else 0
    return CR
