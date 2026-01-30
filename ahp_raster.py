# ahp_raster.py
# Fonctions pour charger et pondérer des rasters avec QGIS

from qgis.core import QgsRasterLayer, QgsProject
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import QgsProcessingFeedback
import processing
import tempfile
import os

def load_raster(path):
    """
    Charge un raster depuis le chemin donné.
    Retourne un QgsRasterLayer valide ou lève une exception si invalide.
    """
    layer = QgsRasterLayer(path, path.split("/")[-1])
    if not layer.isValid():
        raise ValueError(f"Raster {path} non valide")
    return layer

def weighted_raster(rasters, weights, output_path=None, add_to_project=True):
    """
    Crée un raster pondéré à partir d'une liste de rasters et de poids.
    
    rasters: liste de QgsRasterLayer
    weights: liste de poids correspondants
    output_path: chemin du raster de sortie (si None, crée un fichier temporaire)
    add_to_project: si True, ajoute le raster au projet QGIS
    
    Retourne: tuple (résultat_calcul, chemin_sortie, layer ou None)
    """
    if len(rasters) != len(weights):
        raise ValueError("Nombre de rasters ≠ nombre de poids")

    expr_parts = []
    for i, (r, w) in enumerate(zip(rasters, weights)):
        expr_parts.append(f'("{r.name()}@1" * {w})')

    expression = " + ".join(expr_parts)

    first = rasters[0]

    params = {
        'EXPRESSION': expression,
        'LAYERS': rasters,
        'EXTENT': first.extent(),   # QGIS gère le recadrage
        'CRS': first.crs(),
        'CELLSIZE': 0,              # résolution auto
        'OUTPUT': output_path
    }

    result = processing.run("qgis:rastercalculator", params)

    output_layer = QgsRasterLayer(output_path, "AHP_Result")
    if output_layer.isValid() and add_to_project:
        QgsProject.instance().addMapLayer(output_layer)

    return output_layer

def check_raster_compatibility(layer, reference, tolerance=1e-6):
    """
    Vérifie la compatibilité spatiale stricte entre deux rasters.
    Retourne: tuple (bool, message utilisateur)
    
    Compatible Qt5/Qt6 - pas de dépendance à une fonction tr externe.
    """

    if reference is None:
        return True, "Premier raster défini comme référence."

    # CRS
    if layer.crs() != reference.crs():
        return False, (
            "❌ Incompatible CRS:\n"
            f"Référence : {reference.crs().authid()}\n"
            f"Sélectionné : {layer.crs().authid()}"
        )

    # Résolution
    if not (
        abs(reference.rasterUnitsPerPixelX() - layer.rasterUnitsPerPixelX()) < tolerance and
        abs(reference.rasterUnitsPerPixelY() - layer.rasterUnitsPerPixelY()) < tolerance
    ):
        return False, (
            "❌ Incompatible resolution:\n"
            f"Référence : {reference.rasterUnitsPerPixelX():.6f} x {reference.rasterUnitsPerPixelY():.6f}\n"
            f"Sélectionné : {layer.rasterUnitsPerPixelX():.6f} x {layer.rasterUnitsPerPixelY():.6f}"
        )

    # Emprise
    if not reference.extent().intersects(layer.extent()):
        return False, (
            "❌ ❌ No spatial overlap.\n"
            "Rasters must overlap spatially."
        )

    return True, "✅ Raster compatible."
