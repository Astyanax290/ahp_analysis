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

def check_raster_compatibility(layer, reference, tr, tolerance=1e-6):
    """
    Vérifie la compatibilité spatiale stricte entre deux rasters.
    Retourne: tuple (bool, message utilisateur traduit)
    """

    if reference is None:
        return True, tr("Premier raster défini comme référence.")

    # CRS
    if layer.crs() != reference.crs():
        return False, tr(
            "❌ CRS incompatible:\n"
            "Référence : {ref}\n"
            "Sélectionné : {sel}"
        ).format(
            ref=reference.crs().authid(),
            sel=layer.crs().authid()
        )

    # Résolution
    if not (
        abs(reference.rasterUnitsPerPixelX() - layer.rasterUnitsPerPixelX()) < tolerance and
        abs(reference.rasterUnitsPerPixelY() - layer.rasterUnitsPerPixelY()) < tolerance
    ):
        return False, tr(
            "❌ Résolution incompatible:\n"
            "Référence : {rx:.6f} x {ry:.6f}\n"
            "Sélectionné : {sx:.6f} x {sy:.6f}"
        ).format(
            rx=reference.rasterUnitsPerPixelX(),
            ry=reference.rasterUnitsPerPixelY(),
            sx=layer.rasterUnitsPerPixelX(),
            sy=layer.rasterUnitsPerPixelY()
        )

    # Emprise
    if not reference.extent().intersects(layer.extent()):
        return False, tr(
            "❌ Aucun recouvrement spatial.\n"
            "Les rasters doivent se superposer."
        )

    return True, tr("✅ Raster compatible.")

