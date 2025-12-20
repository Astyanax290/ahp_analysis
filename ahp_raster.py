# ahp_raster.py
# Fonctions pour charger et pondérer des rasters avec QGIS

from qgis.core import QgsRasterLayer, QgsRasterCalculator, QgsRasterCalculatorEntry

def load_raster(path):
    """
    Charge un raster depuis le chemin donné.
    Retourne un QgsRasterLayer valide ou lève une exception si invalide.
    """
    layer = QgsRasterLayer(path, path.split("/")[-1])
    if not layer.isValid():
        raise ValueError(f"Raster {path} non valide")
    return layer

def weighted_raster(rasters, weights, output_path):
    """
    Crée un raster pondéré à partir d'une liste de rasters et de poids.
    
    rasters: liste de QgsRasterLayer
    weights: liste de poids correspondants
    output_path: chemin du raster de sortie
    """
    if len(rasters) != len(weights):
        raise ValueError("Le nombre de rasters et de poids doit être identique.")
    
    entries = []
    expr_parts = []
    for i, raster in enumerate(rasters):
        entry = QgsRasterCalculatorEntry()
        entry.ref = f"r{i}@1"
        entry.raster = raster
        entry.bandNumber = 1
        entries.append(entry)
        expr_parts.append(f"{weights[i]}*{entry.ref}")
    
    expr = " + ".join(expr_parts)
    calc = QgsRasterCalculator(
        expr,
        output_path,
        "GTiff",
        rasters[0].extent(),
        rasters[0].width(),
        rasters[0].height(),
        entries
    )
    calc.processCalculation()
