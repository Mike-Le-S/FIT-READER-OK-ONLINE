# Fit File Analyzer

Une application web minimaliste pour charger, analyser et afficher un résumé des fichiers `.fit` de Garmin.

## Fonctionnalités

- Charger des fichiers `.fit` via une interface de glisser-déposer ou un bouton de sélection.
- Afficher un résumé complet de l'activité (données globales, FC, allure, puissance, etc.).
- Copier le résumé formaté en un clic.

## Configuration du projet

1.  **Prérequis**:
    *   Python 3.7+ installé.
    *   `pip` (gestionnaire de paquets Python) installé.

2.  **Cloner le dépôt (si applicable) ou télécharger les fichiers.**

3.  **Créer un environnement virtuel (recommandé)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Linux/macOS
    venv\Scripts\activate    # Sur Windows
    ```

4.  **Installer les dépendances**:
    Naviguez vers le répertoire du projet (où se trouve `requirements.txt`) et exécutez :
    ```bash
    pip install -r requirements.txt
    ```

5.  **Lancer l'application**:
    ```bash
    python app.py
    ```
    L'application sera accessible à l'adresse `http://127.0.0.1:5000`.

## Intégration du FitSDK

Ce projet utilise le SDK officiel Garmin FitSDK (version spécifiée dans `requirements.txt`) pour lire et décoder les fichiers `.fit`. L'installation est gérée via `pip`.
