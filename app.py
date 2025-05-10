from flask import Flask, render_template, request, jsonify
import os
from garmin_fit_sdk import Decoder, Stream
import io
import logging
import copy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# S'assurer que le dossier d'upload existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Helper function pour formater les floats ou retourner N/A
def format_float(value, precision=1):
    if value is None:
        return "N/A"
    try:
        return f"{float(value):.{precision}f}"
    except (ValueError, TypeError):
        return "N/A"

# --- Constantes et Configuration Globale ---
EXPECTED_FILE_TYPE = "activity" # Valeur pour 'activity'

# Structure de données attendue pour l'extraction
# (sera remplie dans process_fit_data)
INITIAL_DATA_STRUCTURE = {
    "file_info": {
        "file_type": None,
        "manufacturer": None,
        "product_name": None,
        "serial_number": None,
        "time_created": None,
        "is_valid_fit_file": False # Ajout pour l'intégrité
    },
    "global_summary": {
        "activity_datetime": None,
        "activity_type": None,
        "total_duration_seconds": None, 
        "total_distance_meters": None, 
        "total_calories": None,
        "num_laps": 0,
        "laps": []
    },
    "heart_rate": {
        'avg_hr_session': None,
        'max_hr_session': None,
        'hr_over_time': [],
        "time_in_custom_zones": {} # Ajouté: ex. {"Zone 1 (123-137 bpm)": 120, ...} (secondes)
    },
    "pace_speed": {
        'avg_speed_mps_session': None,
        'max_speed_mps_session': None,
        'speed_over_time': []
    },
    "power": {
        'avg_power_session': None,
        'max_power_session': None,
        'power_over_time': []
    },
    "cadence": {
        'cadence_per_minute': []
    },
    "altitude": {
        'avg_altitude_session': None,
        'max_altitude_session': None,
        'min_altitude_session': None, # Ajouté
        'altitude_over_time': []
    },
    "temperature": {
        'avg_temperature_session': None,
        'temperature_over_time': []
    },
    "physiological": {
        'training_effect_aerobic': None,
        'training_effect_anaerobic': None,
        'exercise_load': None
    },
    "gps_dynamics": {
        'start_position_lat': None,
        'start_position_long': None,
        'end_position_lat': None,
        'end_position_long': None,
        'avg_gps_accuracy_records': None,
        'num_gps_records': 0,
        'gps_track_points': []
    },
    "running_dynamics": {
        "avg_step_length_cm": None,
        "avg_vertical_oscillation_cm": None,
        "avg_vertical_ratio_percent": None,
        "avg_ground_contact_time_ms": None,
        "avg_ground_contact_balance_percent": None,
        "avg_cadence_ppm": None
    },
    "respiration_summary": {
        "avg_respiration_rate_bpm": None,
        "min_respiration_rate_bpm": None,
        "max_respiration_rate_bpm": None
    },
    "errors": [] # Pour les erreurs spécifiques au traitement des données
}

# --- Fonctions de Traitement FIT ---
def process_fit_file(file_path):
    """ Charge un fichier .fit, le décode et collecte les messages. """
    messages = {}
    errors = [] # Pour stocker les erreurs de cette fonction
    is_valid_fit_file = False

    try:
        decoder = Decoder(file_path)
        is_valid_fit_file = True

        if not is_valid_fit_file:
            errors.append("Le fichier fourni n'est pas un fichier FIT valide.")
            # Retourner immédiatement si ce n'est pas un fichier FIT
            return {"errors": errors, "file_info": {"is_valid_fit_file": False}}

        # Dictionnaire pour stocker les messages par type
        # ex: {'file_id_mesgs': [FileIdMesg, ...], 'record_mesgs': [RecordMesg, ...]}
        def on_mesg(mesg_type, message):
            mesg_type_name = mesg_type.__name__ + 's' # ex: file_id_mesg -> file_id_mesgs
            if mesg_type_name not in messages:
                messages[mesg_type_name] = []
            messages[mesg_type_name].append(message)

        decoder.subscribe(on_mesg)

        # Démarrer le décodage
        decoder.decode() 

        # Vérifier l'intégrité après le décodage complet
        if not decoder.check_integrity():
            errors.append("Le fichier FIT est corrompu (échec de la vérification CRC).")
            # On continue le traitement mais on note l'erreur
            
    except Exception as e:
        errors.append(f"Erreur inattendue lors du traitement du fichier FIT : {e}")
        logging.error(f"Unexpected error: {e}")
    
    # Rassembler les données de base (même si des erreurs sont survenues)
    decoded_data = messages
    decoded_data['errors'] = errors # Attacher les erreurs au dictionnaire de messages
    # Mettre à jour le statut de validité général basé sur la détection initiale
    # (on pourrait avoir un fichier FIT valide mais avec des erreurs de CRC plus tard)
    if 'file_info' not in decoded_data:
        decoded_data['file_info'] = {}
    decoded_data['file_info']['is_valid_fit_file'] = is_valid_fit_file and not any("corrompu" in err.lower() for err in errors)

    return decoded_data

def process_fit_data(messages):
    """ Extrait les données structurées à partir des messages décodés. """
    data = copy.deepcopy(INITIAL_DATA_STRUCTURE)
    # Hériter des erreurs de process_fit_file et initialiser si besoin
    data['errors'] = messages.get('errors', []) 

    # Si process_fit_file a déjà signalé une erreur critique (ex: pas un fichier FIT)
    # on peut vouloir s'arrêter tôt ou limiter le traitement.
    if not messages.get('file_info', {}).get('is_valid_fit_file', True) and not messages:
        if not any("Le fichier fourni n'est pas un fichier FIT valide." in err for err in data['errors']):
            data['errors'].append("Traitement des données annulé car le fichier n'est pas un fichier FIT valide ou aucune donnée n'a pu être lue.")
        return data # Retourner la structure avec l'erreur

    # --- Extraction des Informations du Fichier (file_id_mesgs) ---
    file_info = data["file_info"]
    file_info['is_valid_fit_file'] = messages.get('file_info', {}).get('is_valid_fit_file', True)

    if 'file_id_mesgs' in messages and messages['file_id_mesgs']:
        file_id_msg = messages['file_id_mesgs'][0]
        file_info['file_type'] = file_id_msg.get('type')
        file_info['manufacturer'] = file_id_msg.get('manufacturer')
        file_info['product_name'] = file_id_msg.get('product_name')
        file_info['serial_number'] = file_id_msg.get('serial_number')
        file_info['time_created'] = file_id_msg.get('time_created')

    # --- Extraction du Résumé Global à partir des messages de session ---
    if 'session_mesgs' in messages and messages['session_mesgs']:
        # On prend la première session, généralement il n'y en a qu'une pour une activité simple
        session = messages['session_mesgs'][0]
        
        gs = data["global_summary"]
        gs['activity_datetime'] = str(session.get('start_time')) if session.get('start_time') else None
        gs['activity_type'] = session.get('sport')
        if session.get('sub_sport'): # Affiner avec le sous-sport si disponible
             gs['activity_type'] = f"{gs['activity_type']} ({session.get('sub_sport')})"

        gs['total_duration_seconds'] = session.get('total_elapsed_time') # en secondes
        gs['total_distance_meters'] = session.get('total_distance') # en mètres
        gs['total_calories'] = session.get('total_calories')

        # Extraction des données de FC globales pour la session
        hr_data = data["heart_rate"]
        hr_data['avg_hr_session'] = session.get('avg_heart_rate')
        hr_data['max_hr_session'] = session.get('max_heart_rate')

        # Extraction des données de vitesse globales pour la session
        pace_data = data["pace_speed"]
        pace_data['avg_speed_mps_session'] = session.get('enhanced_avg_speed', session.get('avg_speed')) # en m/s
        pace_data['max_speed_mps_session'] = session.get('enhanced_max_speed', session.get('max_speed')) # en m/s

        # Extraction des données de puissance globales pour la session
        power_data = data["power"]
        power_data['avg_power_session'] = session.get('avg_power') # en Watts
        power_data['max_power_session'] = session.get('max_power') # en Watts

        # Extraction des données de cadence globales pour la session
        cadence_data = data["cadence"]
        # Priorité à la cadence de course (spm), sinon cadence vélo (rpm)
        # Les champs exacts peuvent varier, ex: 'avg_running_cadence' ou 'avg_cadence'
        # 'avg_running_cadence' est en strides per minute (double de la guêtre pour certains)
        if session.get('avg_running_cadence') is not None:
            cadence_data['cadence_unit'] = 'spm' # steps per minute
        elif session.get('avg_cadence') is not None:
            cadence_data['cadence_unit'] = 'rpm' # revolutions per minute
        
        # Extraction des données d'altitude globales pour la session
        alt_data = data["altitude"]
        alt_data['avg_altitude_session'] = format_float(session.get('avg_altitude')) # en mètres
        alt_data['max_altitude_session'] = format_float(session.get('max_altitude')) # en mètres
        alt_data['min_altitude_session'] = format_float(session.get('min_altitude'))

        # Extraction des données de température globales pour la session
        temp_data = data["temperature"]
        temp_data['avg_temperature_session'] = session.get('avg_temperature') # en °C

        # Extraction des données physiologiques de la session
        physio_data = data["physiological"]
        physio_data['training_effect_aerobic'] = session.get('total_training_effect')
        physio_data['training_effect_anaerobic'] = session.get('total_anaerobic_training_effect')
        physio_data['exercise_load'] = session.get('training_load_peak')

        # Extraction des données GPS de la session (point de départ)
        gps_dyn_data = data["gps_dynamics"]
        gps_dyn_data['start_position_lat'] = session.get('start_position_lat') # en degrés
        gps_dyn_data['start_position_long'] = session.get('start_position_long') # en degrés

        # Running Dynamics from session
        rd_data = data["running_dynamics"]
        avg_step_length_mm = session.get('avg_step_length')
        if avg_step_length_mm is not None:
            rd_data['avg_step_length_cm'] = round(avg_step_length_mm / 10, 1) # mm en cm
        
        avg_vo_mm = session.get('avg_vertical_oscillation')
        if avg_vo_mm is not None:
            rd_data['avg_vertical_oscillation_cm'] = round(avg_vo_mm / 10, 1) # mm en cm

        rd_data['avg_vertical_ratio_percent'] = session.get('avg_vertical_ratio')
        rd_data['avg_ground_contact_time_ms'] = session.get('avg_stance_time')
        
        # avg_stance_time_balance est parfois un % (ex: 49.8 signifiant 49.8% Left)
        # ou un nombre différent. Le SDK peut le retourner comme un simple float.
        # On le stocke tel quel pour l'instant.
        rd_data['avg_ground_contact_balance_percent'] = session.get('avg_stance_time_balance')

        avg_cadence_spm = session.get('avg_running_cadence', session.get('avg_cadence'))
        if avg_cadence_spm is not None:
            rd_data['avg_cadence_ppm'] = avg_cadence_spm * 2

        # Respiration Summary from session
        resp_data = data["respiration_summary"]
        resp_data['avg_respiration_rate_bpm'] = session.get('enhanced_avg_respiration_rate')
        resp_data['min_respiration_rate_bpm'] = session.get('enhanced_min_respiration_rate')
        resp_data['max_respiration_rate_bpm'] = session.get('enhanced_max_respiration_rate')

    else:
        data['errors'].append("Message de session (session_mesgs) manquant. De nombreuses données globales ne seront pas disponibles.")

    # Extraction des Laps
    if 'lap_mesgs' in messages:
        gs = data["global_summary"]
        gs['num_laps'] = len(messages['lap_mesgs'])
        for lap_msg in messages['lap_mesgs']:
            lap_data = {
                "start_time": str(lap_msg.get('start_time')) if lap_msg.get('start_time') else None,
                "end_time": str(lap_msg.get('timestamp')) if lap_msg.get('timestamp') else None, # timestamp est souvent l'heure de fin du lap
                "duration_seconds": lap_msg.get('total_elapsed_time'),
                "distance_meters": lap_msg.get('total_distance'),
                "calories": lap_msg.get('total_calories'),
                "avg_speed_mps": lap_msg.get('avg_speed'), # m/s
                "avg_hr": lap_msg.get('avg_heart_rate'),
                "max_hr": lap_msg.get('max_heart_rate'),
                "lap_trigger": lap_msg.get('lap_trigger')
            }
            gs['laps'].append(lap_data)

    # Extraction de la fréquence cardiaque seconde par seconde (record messages)
    hr_data = data["heart_rate"]
    if 'record_mesgs' in messages:
        for record_msg in messages['record_mesgs']:
            timestamp = record_msg.get('timestamp')
            hr_value = record_msg.get('heart_rate')
            if timestamp and hr_value is not None: # s'assurer que les deux valeurs existent
                hr_data['hr_over_time'].append({
                    "time": str(timestamp),
                    "hr": hr_value
                })

    # Extraction de la vitesse/allure instantanée (record messages)
    pace_data = data["pace_speed"]
    if 'record_mesgs' in messages:
        for record_msg in messages['record_mesgs']:
            timestamp = record_msg.get('timestamp')
            speed_value = record_msg.get('enhanced_speed', record_msg.get('speed')) # en m/s
            if timestamp and speed_value is not None:
                pace_data['speed_over_time'].append({
                    "time": str(timestamp),
                    "speed_mps": speed_value
                })

    # Extraction de la puissance instantanée (record messages)
    power_data = data["power"]
    if 'record_mesgs' in messages:
        for record_msg in messages['record_mesgs']:
            timestamp = record_msg.get('timestamp')
            power_value = record_msg.get('power') # en Watts
            if timestamp and power_value is not None:
                power_data['power_over_time'].append({
                    "time": str(timestamp),
                    "power": power_value
                })

    # Extraction de la cadence instantanée (record messages) pour calcul par minute
    # et préparation pour l'agrégation par minute
    temp_cadence_records = []
    if 'record_mesgs' in messages:
        for record_msg in messages['record_mesgs']:
            timestamp = record_msg.get('timestamp')
            # La SDK peut retourner 'None' si le champ n'existe pas dans le message
            running_cadence_val = record_msg.get('running_cadence') # spm
            cadence_val = record_msg.get('cadence') # rpm
            
            chosen_cadence_value = None
            if running_cadence_val is not None:
                chosen_cadence_value = running_cadence_val
                # Assurer que l'unité de session correspond si elle n'est pas encore définie
                if data["cadence"].get('cadence_unit') is None: data["cadence"]['cadence_unit'] = 'spm'
            elif cadence_val is not None:
                chosen_cadence_value = cadence_val
                if data["cadence"].get('cadence_unit') is None: data["cadence"]['cadence_unit'] = 'rpm'

            if timestamp and chosen_cadence_value is not None:
                temp_cadence_records.append({
                    "datetime_obj": timestamp, # Garder comme objet datetime pour le tri/groupement
                    "cadence": chosen_cadence_value
                })
    
    # Calcul de la cadence moyenne par minute
    if temp_cadence_records:
        cadence_per_minute_agg = {}
        for record in temp_cadence_records:
            # Clé de groupement: l'heure et la minute
            minute_key = record["datetime_obj"].replace(second=0, microsecond=0)
            if minute_key not in cadence_per_minute_agg:
                cadence_per_minute_agg[minute_key] = []
            cadence_per_minute_agg[minute_key].append(record["cadence"])
        
        cad_data = data["cadence"]
        for minute_start, cadences_in_minute in sorted(cadence_per_minute_agg.items()):
            if cadences_in_minute:
                avg_cad_for_minute = sum(cadences_in_minute) / len(cadences_in_minute)
                cad_data['cadence_per_minute'].append({
                    "minute_start_time": str(minute_start), # Convertir en string pour JSON
                    "avg_cadence": round(avg_cad_for_minute, 1)
                })

    # Extraction de l'altitude instantanée (record messages)
    alt_data = data["altitude"]
    if 'record_mesgs' in messages:
        for record_msg in messages['record_mesgs']:
            timestamp = record_msg.get('timestamp')
            altitude_value = record_msg.get('enhanced_altitude', record_msg.get('altitude')) # en mètres
            if timestamp and altitude_value is not None:
                alt_data['altitude_over_time'].append({
                    "time": str(timestamp),
                    "altitude": altitude_value
                })

    # Extraction de la température instantanée (record messages)
    temp_data = data["temperature"]
    if 'record_mesgs' in messages:
        for record_msg in messages['record_mesgs']:
            timestamp = record_msg.get('timestamp')
            temperature_value = record_msg.get('temperature') # en °C
            if timestamp and temperature_value is not None:
                temp_data['temperature_over_time'].append({
                    "time": str(timestamp),
                    "temperature": temperature_value
                })

    # Extraction des données GPS des record_mesgs (trace, point final, précision)
    gps_dyn_data = data["gps_dynamics"]
    all_gps_accuracies = []
    last_lat, last_long = None, None

    if 'record_mesgs' in messages:
        for record_msg in messages['record_mesgs']:
            lat = record_msg.get('position_lat') # en degrés
            long = record_msg.get('position_long') # en degrés
            timestamp = record_msg.get('timestamp')

            if lat is not None and long is not None and timestamp is not None:
                gps_dyn_data['num_gps_records'] += 1
                # Utiliser enhanced_altitude (GPS) si disponible, sinon pas d'altitude spécifique GPS pour ce point
                alt_gps = record_msg.get('enhanced_altitude') # en mètres
                
                gps_dyn_data['gps_track_points'].append({
                    "time": str(timestamp),
                    "lat": lat,
                    "long": long,
                    "alt_gps": alt_gps
                })
                last_lat, last_long = lat, long

                gps_accuracy = record_msg.get('gps_accuracy') # en mètres
                if gps_accuracy is not None:
                    all_gps_accuracies.append(gps_accuracy)
        
        if last_lat is not None:
            gps_dyn_data['end_position_lat'] = last_lat
            gps_dyn_data['end_position_long'] = last_long

        if all_gps_accuracies:
            gps_dyn_data['avg_gps_accuracy_records'] = sum(all_gps_accuracies) / len(all_gps_accuracies)

    # Données Physiologiques additionnelles hors-session (si présentes)
    physio_data = data["physiological"]

    # User Profile Data (pour VO2max, zones FC perso, etc.)
    user_profile_mesgs = messages.get('user_profile_mesgs')
    if user_profile_mesgs:
        user_profile = user_profile_mesgs[0] # Prenant le premier message de profil utilisateur
        app.logger.debug(f"User Profile Data: {user_profile}")
        # VO₂max a été retiré des données physiologiques à afficher.
        # Si d'autres champs du profil utilisateur deviennent pertinents (ex: zones FC perso),
        # ils pourront être extraits ici.
        # La ligne incorrecte ( if physio_data['training_effect_aerobic'] is None: physio_data['training_effect_aerobic'] = user_profile.get('vo2_max') ) est supprimée.

    # HRV Data - Simple check de présence
    hrv_related_mesgs = ['hrv_mesgs'] # 'hrv' est plus générique
    for msg_type in hrv_related_mesgs:
        if msg_type in messages and messages[msg_type]:
            physio_data['hrv_status'] = f"Données HRV présentes ({msg_type})"
            # Pour une extraction détaillée, il faudrait parcourir messages[msg_type]
            break
    if not physio_data.get('hrv_status'):
        physio_data['hrv_status'] = "Non disponibles"

    # Training Status (exemple)
    # Le statut d'entrainement peut venir de plusieurs sources, 'training_status' est une possibilité.
    # Le SDK peut ne pas toujours décoder cela en message distinctif si ce n'est pas un message standard FIT
    # Souvent, ces infos sont dans des Developer Fields ou des messages spécifiques fabricant.
    # Pour cet exemple, on suppose qu'il pourrait être dans 'developer_data_id' ou 'field_description'
    # mais cela devient complexe. Une approche simple est de chercher un champ connu.
    # Pour l'instant, on va le laisser comme 'Non disponible' car la clé exacte est inconnue.
    if 'training_status_mesgs' in messages and messages['training_status_mesgs']:
        # Supposons qu'il y ait un champ 'status' dans ce message
        ts_msg = messages['training_status_mesgs'][0]
        physio_data['training_status'] = ts_msg.get('status', 'Valeur de statut inconnue') 
    else:
        physio_data['training_status'] = "Non disponible"

    # Calcul du temps passé dans les zones de FC personnalisées
    hr_data = data["heart_rate"]
    if hr_data.get('hr_over_time'):
        hr_series = hr_data['hr_over_time']
        custom_hr_zones_definitions = [
            ("Zone 1 (123-137 bpm)", 123, 137),
            ("Zone 2 (138-152 bpm)", 138, 152),
            ("Zone 3 (153-168 bpm)", 153, 168),
            ("Zone 4 (169-183 bpm)", 169, 183),
            ("Zone 5 (184+ bpm)", 184, 999) # 999 comme limite supérieure arbitraire pour la Z5
        ]
        time_in_zones_seconds = {name: 0 for name, _, _ in custom_hr_zones_definitions}

        if hr_series: # S'assurer qu'il y a des données
            for hr_point in hr_series:
                hr_value = hr_point.get('hr')
                if hr_value is not None:
                    for name, lower_bound, upper_bound in custom_hr_zones_definitions:
                        if lower_bound <= hr_value <= upper_bound:
                            time_in_zones_seconds[name] += 1 # Chaque point représente 1 seconde
                            break # Une FC ne peut être que dans une zone
        
        hr_data['time_in_custom_zones'] = time_in_zones_seconds

    # Fallback pour les données d'altitude si non présentes dans session_mesgs
    alt_data = data["altitude"]
    if alt_data.get('altitude_over_time'):
        # Récupérer uniquement les altitudes qui sont des nombres valides (float ou int)
        all_altitudes_from_records = [p['altitude'] for p in alt_data['altitude_over_time'] if isinstance(p['altitude'], (int, float))]
        
        if all_altitudes_from_records: # S'assurer qu'il y a des valeurs numériques valides
            if alt_data.get('avg_altitude_session') == "N/A": # Si N/A après la tentative de session
                avg_alt_calc = sum(all_altitudes_from_records) / len(all_altitudes_from_records)
                alt_data['avg_altitude_session'] = format_float(avg_alt_calc)
            
            if alt_data.get('max_altitude_session') == "N/A": # Si N/A après la tentative de session
                max_alt_calc = max(all_altitudes_from_records)
                alt_data['max_altitude_session'] = format_float(max_alt_calc)

            if alt_data.get('min_altitude_session') == "N/A": # Si N/A après la tentative de session
                min_alt_calc = min(all_altitudes_from_records)
                alt_data['min_altitude_session'] = format_float(min_alt_calc)

    # Vérification finale: si aucune donnée record n'a été trouvée, cela peut indiquer un problème ou un fichier très court
    if 'record_mesgs' not in messages or not messages['record_mesgs']:
        data['errors'].append("Aucun message d'enregistrement (record_mesgs) trouvé. Les données de séries temporelles (FC, vitesse, etc.) seront absentes.")

    return data

def format_summary_text(data):
    """Formate les données extraites en un résumé textuel clair.
    """
    gs = data.get("global_summary", {})
    hr = data.get("heart_rate", {})
    ps = data.get("pace_speed", {})
    pw = data.get("power", {})
    cd = data.get("cadence", {})
    alt = data.get("altitude", {})
    tmp = data.get("temperature", {})
    phy = data.get("physiological", {})
    gps = data.get("gps_dynamics", {})
    rd = data.get("running_dynamics", {})
    resp = data.get("respiration_summary", {})
    
    # Helper pour formater la durée de secondes en HH:MM:SS
    def format_duration(seconds):
        if seconds is None:
            return "N/A"
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
        else:
            return f"{minutes:02d}:{remaining_seconds:02d}"

    # Helper pour formater la distance de mètres en km
    def format_distance(meters):
        if meters is None:
            return "N/A"
        km = meters / 1000.0
        return f"{km:.2f} km"

    # Helper pour formater la vitesse de m/s en min/km (allure)
    def format_pace(speed_mps):
        if speed_mps is None or speed_mps == 0:
            return "N/A"
        # 1 m/s = 1 / (1000 * m/s) km/s = 1000 / (m/s) s/km
        # sec_per_km = 1000 / speed_mps
        try:
            sec_per_km = 1000.0 / float(speed_mps)
        except (ValueError, TypeError):
            return "N/A"
        minutes = int(sec_per_km // 60)
        seconds = int(sec_per_km % 60)
        return f"{minutes:02d}:{seconds:02d} min/km"
    
    summary_parts = []
    summary_parts.append("🎉 Résumé global de l'activité 🎉")
    summary_parts.append("-------------------------------------")
    summary_parts.append(f"📅 Date et heure : {gs.get('activity_datetime', 'N/A')}")
    summary_parts.append(f"🏃 Type d'activité : {gs.get('activity_type', 'N/A')}")
    summary_parts.append(f"⏱️ Durée totale : {format_duration(gs.get('total_duration_seconds'))}")
    summary_parts.append(f"📏 Distance totale : {format_distance(gs.get('total_distance_meters'))}")
    summary_parts.append(f"🔥 Calories brûlées : {gs.get('total_calories', 'N/A')} kcal")
    summary_parts.append(f"🔄 Nombre de tours (laps) : {gs.get('num_laps', 0)}")
    summary_parts.append("")

    # Section Fréquence Cardiaque
    summary_parts.append("❤️ Fréquence Cardiaque ❤️")
    summary_parts.append("---------------------------")
    summary_parts.append(f"  FC Moyenne (session) : {hr.get('avg_hr_session', 'N/A')} bpm")
    summary_parts.append(f"  FC Maximale (session) : {hr.get('max_hr_session', 'N/A')} bpm")
    if hr.get('hr_over_time'):
        summary_parts.append(f"  ✔️ Données FC seconde par seconde extraites ({len(hr['hr_over_time'])} points)")
    else:
        summary_parts.append("  ❌ Données FC seconde par seconde non disponibles")
    
    # Affichage du temps dans les zones de FC personnalisées
    time_in_custom_zones = hr.get('time_in_custom_zones')
    if time_in_custom_zones:
        summary_parts.append("  Temps dans les zones de FC personnalisées :")
        for zone_name, seconds_in_zone in time_in_custom_zones.items():
            summary_parts.append(f"    {zone_name} : {format_duration(seconds_in_zone)}")
    else:
        summary_parts.append("  (Données de temps en zones FC non calculées ou FC non disponible)")
    summary_parts.append("")

    # Section Allure & Vitesse
    summary_parts.append("🏃 Allure & Vitesse 🏃")
    summary_parts.append("------------------------")
    summary_parts.append(f"  Allure Moyenne (session) : {format_pace(ps.get('avg_speed_mps_session'))}")
    summary_parts.append(f"  Allure Maximale (session) : {format_pace(ps.get('max_speed_mps_session'))}") # Note: max speed convertie en allure min
    if ps.get('speed_over_time'):
        summary_parts.append(f"  ✔️ Données d'allure/vitesse instantanée extraites ({len(ps['speed_over_time'])} points)")
    else:
        summary_parts.append("  ❌ Données d'allure/vitesse instantanée non disponibles")
    summary_parts.append("  (Zones d'allure : à venir)")
    summary_parts.append("")

    # Section Puissance
    summary_parts.append("⚡ Puissance ⚡")
    summary_parts.append("------------------")
    avg_power = pw.get('avg_power_session')
    max_power = pw.get('max_power_session')
    summary_parts.append(f"  Puissance Moyenne (session) : {avg_power if avg_power is not None else 'N/A'} W")
    summary_parts.append(f"  Puissance Maximale (session) : {max_power if max_power is not None else 'N/A'} W")
    if pw.get('power_over_time'):
        summary_parts.append(f"  ✔️ Données de puissance instantanée extraites ({len(pw['power_over_time'])} points)")
    else:
        summary_parts.append("  ❌ Données de puissance instantanée non disponibles")
    summary_parts.append("")

    # Section Altitude
    summary_parts.append("🏔️ Altitude 🏔️")
    summary_parts.append("-----------------")
    avg_alt = alt.get('avg_altitude_session', 'N/A')
    max_alt = alt.get('max_altitude_session', 'N/A')
    min_alt = alt.get('min_altitude_session', 'N/A') # Ajouté
    summary_parts.append(f"  Altitude Moyenne (session) : {avg_alt} m")
    summary_parts.append(f"  Altitude Maximale (session) : {max_alt} m")
    summary_parts.append(f"  Altitude Minimale (session) : {min_alt} m") # Ajouté
    if alt.get('altitude_over_time'):
        summary_parts.append(f"  ✔️ Données de courbe d'altitude extraites ({len(alt['altitude_over_time'])} points)")
    else:
        summary_parts.append("  ❌ Données de courbe d'altitude non disponibles")
    summary_parts.append("")

    # Section Température
    summary_parts.append("🌡️ Température 🌡️")
    summary_parts.append("------------------")
    avg_temp = tmp.get('avg_temperature_session')
    summary_parts.append(f"  Température Moyenne (session) : {avg_temp}°C" if avg_temp is not None else "  Température Moyenne (session) : N/A")
    if tmp.get('temperature_over_time'):
        summary_parts.append(f"  ✔️ Données de température dans le temps extraites ({len(tmp['temperature_over_time'])} points)")
    else:
        summary_parts.append("  ❌ Données de température dans le temps non disponibles")
    summary_parts.append("")

    # Section Données Physiologiques
    summary_parts.append("🧠 Données Physiologiques 🧠")
    summary_parts.append("---------------------------")
    summary_parts.append(f"  Training Effect (Aérobie) : {phy.get('training_effect_aerobic', 'N/A')}")
    summary_parts.append(f"  Training Effect (Anaérobie) : {phy.get('training_effect_anaerobic', 'N/A')}")
    summary_parts.append(f"  Charge d'exercice : {phy.get('exercise_load', 'N/A')}")
    summary_parts.append("")

    # Section GPS & Dynamique
    summary_parts.append("📍 GPS & Dynamique 📍")
    summary_parts.append("---------------------")
    start_lat = gps.get('start_position_lat')
    start_long = gps.get('start_position_long')
    end_lat = gps.get('end_position_lat')
    end_long = gps.get('end_position_long')
    avg_acc = gps.get('avg_gps_accuracy_records')
    num_pts = gps.get('num_gps_records', 0)

    summary_parts.append(f"  Point de départ : Lat {start_lat:.5f}, Long {start_long:.5f}" if start_lat is not None and start_long is not None else "  Point de départ : N/A")
    summary_parts.append(f"  Point d'arrivée : Lat {end_lat:.5f}, Long {end_long:.5f}" if end_lat is not None and end_long is not None else "  Point d'arrivée : N/A")
    summary_parts.append(f"  Précision GPS moyenne (records) : {avg_acc:.1f} m" if avg_acc is not None else "  Précision GPS moyenne (records) : N/A")
    summary_parts.append(f"  ✔️ Trace GPS complète extraite ({num_pts} points)" if num_pts > 0 else "  ❌ Données de trace GPS non disponibles")
    summary_parts.append("")

    # Nouvelle section pour la Dynamique de Course (Session)
    summary_parts.append("\n⚙️ Dynamique de Course (Session) ⚙️")
    summary_parts.append("-----------------------------------")
    summary_parts.append(f"  Cadence Moyenne : {rd.get('avg_cadence_ppm', 'N/A')} ppm")
    summary_parts.append(f"  Longueur de foulée moyenne : {rd.get('avg_step_length_cm', 'N/A')} cm")
    summary_parts.append(f"  Oscillation verticale moyenne : {rd.get('avg_vertical_oscillation_cm', 'N/A')} cm")
    summary_parts.append(f"  Rapport vertical moyen : {rd.get('avg_vertical_ratio_percent', 'N/A')}% ")
    summary_parts.append(f"  Temps de contact au sol moyen : {rd.get('avg_ground_contact_time_ms', 'N/A')} ms")
    gct_balance = rd.get('avg_ground_contact_balance_percent')
    if gct_balance is not None:
        # Interprétation de l'équilibre GCT : si > 50%, plus de temps à droite. si < 50%, plus à gauche.
        # Un équilibre parfait est 50%. La SDK peut le donner comme %gauche (ex: 49.8% L)
        # Pour l'instant, on affiche la valeur brute et on clarifiera plus tard si besoin.
        # Garmin affiche souvent L 49.8% / R 50.2%
        # Supposons que la valeur est % de temps pied gauche
        if isinstance(gct_balance, (int, float)):
            left_gct_percent = gct_balance
            right_gct_percent = 100 - gct_balance if 0 <= gct_balance <= 100 else None
            if right_gct_percent is not None:
                summary_parts.append(f"  Équilibre TCS (G/D) : {left_gct_percent:.1f}% / {right_gct_percent:.1f}%")
            else:
                summary_parts.append(f"  Équilibre TCS : {gct_balance} %") # Afficher tel quel si pas standard
        else:
            summary_parts.append(f"  Équilibre TCS : {gct_balance}")
    else:
        summary_parts.append("  Équilibre TCS : N/A")

    # Nouvelle section pour la Fréquence Respiratoire (Session)
    summary_parts.append("\n🌬️ Fréquence Respiratoire (Session) 🌬️")
    summary_parts.append("--------------------------------------")
    summary_parts.append(f"  Respiration moyenne : {resp.get('avg_respiration_rate_bpm', 'N/A')} bpm")
    summary_parts.append(f"  Respiration min : {resp.get('min_respiration_rate_bpm', 'N/A')} bpm")
    summary_parts.append(f"  Respiration max : {resp.get('max_respiration_rate_bpm', 'N/A')} bpm")

    # Détails des Laps
    lap_details = data.get("laps", [])
    if lap_details:
        summary_parts.append("\n🏁 Détails des tours (laps) 🏁")
        summary_parts.append("-----------------------------")
        for i, lap in enumerate(lap_details):
            summary_parts.append(f"  Lap {i+1}:")
            summary_parts.append(f"    Heure de début : {lap.get('start_time', 'N/A')}")
            summary_parts.append(f"    Durée : {format_duration(lap.get('duration_seconds'))}")
            summary_parts.append(f"    Distance : {format_distance(lap.get('distance_meters'))}")
            # Vous pouvez ajouter d'autres détails de lap ici (FC moy, vitesse moy, etc.)
            summary_parts.append("") # Espace entre les laps

    # Section Erreurs et Avertissements
    if data.get('errors'):
        summary_parts.append("\n⚠️ Erreurs & Avertissements ⚠️")
        summary_parts.append("-----------------------------")
        for err_msg in data['errors']:
            summary_parts.append(f"  - {err_msg}")
        summary_parts.append("")

    return "\n".join(summary_parts)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400

    if file and file.filename.endswith('.fit'):
        try:
            # Lire le contenu du fichier en mémoire
            file_bytes = file.read()
            stream = Stream.from_byte_array(file_bytes)
            decoder = Decoder(stream)
            
            messages, errors = decoder.read(
                apply_scale_and_offset = True,
                convert_datetimes_to_dates = True,
                convert_types_to_strings = True,
                enable_crc_check = True,
                expand_sub_fields = True,
                expand_components = True,
                merge_heart_rates = True
            )

            # Logs de débogage pour inspecter les messages FIT
            app.logger.debug(f"Keys in FIT messages dictionary: {list(messages.keys()) if messages else 'No messages'}")
            if messages:
                app.logger.debug(f"Content of 'file_id_mesgs': {messages.get('file_id_mesgs')}")
                app.logger.debug(f"Content of 'activity_mesgs': {messages.get('activity_mesgs')}")
                app.logger.debug(f"Content of 'session_mesgs': {messages.get('session_mesgs')}")
                app.logger.debug(f"Content of 'user_profile_mesgs': {messages.get('user_profile_mesgs')}")
                app.logger.debug(f"Content of 'device_info_mesgs': {messages.get('device_info_mesgs')}")
                app.logger.debug(f"Content of 'time_in_zone_mesgs': {messages.get('time_in_zone_mesgs')}")
                app.logger.debug(f"Number of 'record_mesgs': {len(messages.get('record_mesgs', []))}")
                if messages.get('record_mesgs') and len(messages.get('record_mesgs')) > 0:
                    app.logger.debug(f"First 'record_mesg' content: {messages.get('record_mesgs')[0]}")

            if errors:
                app.logger.error(f"Erreurs de décodage FIT: {errors}")
                # Renvoyer une partie de l'erreur au client si pertinent
                # ou un message d'erreur générique
                # Pour l'instant, nous ne bloquons pas si des erreurs mineures existent
                # mais il est bon de les logger.

            # Traitement des données
            processed_data = process_fit_data(messages)
            summary_text = format_summary_text(processed_data)
            
            return jsonify({'summary': summary_text, 'errors': errors if errors else []})
        
        except Exception as e:
            app.logger.error(f"Erreur lors du traitement du fichier FIT: {e}")
            return jsonify({'error': f'Erreur lors du traitement du fichier: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Type de fichier invalide. Veuillez charger un fichier .fit'}), 400

if __name__ == '__main__':
    # S'assurer que le dossier d'upload existe au démarrage
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000, debug=True)
