import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def extraire_date(photo_path):
    try:
        # Ouvrir l'image pour extraire les métadonnées EXIF
        image = Image.open(photo_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == "DateTimeOriginal":  # Date originale de la photo
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass

    # Si pas de métadonnées EXIF, utiliser la date de modification du fichier
    timestamp = os.path.getmtime(photo_path)
    return datetime.fromtimestamp(timestamp)

def organiser_photos_par_date(photo_path, dossier_sortie):
    # Extraire la date de la photo
    date = extraire_date(photo_path)
    if not date:
        date = datetime.fromtimestamp(os.path.getmtime(photo_path))  # Si aucune date trouvée, utiliser la date de modification

    # Créer les dossiers en fonction de l'année, du mois et de la semaine
    dossier_annee = os.path.join(dossier_sortie, str(date.year))
    dossier_mois = os.path.join(dossier_annee, date.strftime('%m'))
    semaine_numero = date.strftime('%U')  # Numéro de la semaine (00-53)
    dossier_semaine = os.path.join(dossier_mois, f"semaine_{semaine_numero}")

    if not os.path.exists(dossier_semaine):
        os.makedirs(dossier_semaine)

    return dossier_semaine

def renommer_et_regrouper_photos(dossier_cible, dossier_sortie):
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    fichiers_rencontres = set()

    for racine, sous_dossiers, fichiers in os.walk(dossier_cible):
        for fichier in fichiers:
            if fichier.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")):
                chemin_source = os.path.join(racine, fichier)

                # Extraire la date et générer le nouveau chemin
                dossier_destination = organiser_photos_par_date(chemin_source, dossier_sortie)

                # Extraire la date pour le renommage
                date = extraire_date(chemin_source)
                if date:
                    nouveau_nom = f"IMG_{date.strftime('%Y%m%d_%H%M%S')}{os.path.splitext(fichier)[1]}"
                else:
                    nouveau_nom = f"IMG_INCONNU{os.path.splitext(fichier)[1]}"

                # Vérifier si le fichier existe déjà dans le dossier de destination
                chemin_destination = os.path.join(dossier_destination, nouveau_nom)
                if os.path.exists(chemin_destination):
                    # Supprimer le fichier existant
                    os.remove(chemin_destination)

                # Copier le fichier dans le dossier de destination avec le nouveau nom
                shutil.copy2(chemin_source, chemin_destination)

    print(f"Toutes les photos ont été renommées et regroupées dans : {dossier_sortie}")

# Exemple d'utilisation
dossier_cible = r"C:\Users\mazar\Desktop\test"  # Remplacez par le chemin réel
dossier_sortie = r"C:\Users\mazar\Desktop\photo trie"  # Remplacez par le chemin réel
renommer_et_regrouper_photos(dossier_cible, dossier_sortie)