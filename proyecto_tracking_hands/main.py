import cv2
import time
import math
import numpy as np
from datetime import datetime

# Importaciones de arquitectura MVC/DAO
from HandTrackingModule import HandDetector
from VolumeHandControl import VolumeController
from dao.mongodb_dao import MongoDBDAO


def main():
    # --- 1. CONFIGURACIÓN INICIAL ---
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detection_con=0.8, max_hands=1)
    vol_ctrl = VolumeController()
    dao = MongoDBDAO()

    # Registro de inicio de sesión en MongoDB Atlas
    session_data = {
        "user": "Estudiante_Monlau",
        "start_time": datetime.now(),
        "status": "active"
    }
    dao.save_session(session_data)

    # Variables de estado visual
    vol_bar = 400
    vol_per = vol_ctrl.get_current_volume()

    # Paleta Cyber Neon
    COLOR_CYAN = (255, 255, 0)  # Volumen Activo
    COLOR_MAGENTA = (255, 0, 255)  # Detalle / Pinza
    COLOR_RED = (0, 0, 255)  # MUTE
    COLOR_GRAY = (80, 80, 80)  # Bloqueado / Idle

    print("--- Sistema Gestual con Modo Mute Iniciado ---")

    while True:
        success, img = cap.read()
        if not success: break

        img = detector.find_hands(img)
        lm_list = detector.find_position(img)

        # Estado por defecto
        ui_color = COLOR_GRAY
        mode_text = "MODO: BLOQUEADO"

        if len(lm_list) != 0:
            # --- 2. LÓGICA MUTE (PUÑO CERRADO) ---
            # Comprobamos si las puntas (8,12,16,20) están por debajo de sus articulaciones (6,10,14,18)
            is_fist = (lm_list[8][2] > lm_list[6][2] and
                       lm_list[12][2] > lm_list[10][2] and
                       lm_list[16][2] > lm_list[14][2] and
                       lm_list[20][2] > lm_list[18][2])

            if is_fist:
                ui_color = COLOR_RED
                mode_text = "MODO: MUTE (SILENCIO)"

                if not vol_ctrl.get_mute_status():
                    vol_ctrl.set_mute(True)
                    # Persistencia del evento de silencio
                    dao.save_volume_event({
                        "session_id": session_data.get("_id"),
                        "timestamp": datetime.now(),
                        "action": "mute_on",
                        "reason": "gesture_fist"
                    })
            else:
                # Si no hay puño, quitamos el silencio si estaba puesto
                if vol_ctrl.get_mute_status():
                    vol_ctrl.set_mute(False)

                # --- 3. LÓGICA VOLUMEN (MEÑIQUE BAJADO) ---
                is_vol_active = vol_ctrl.is_pinky_down(lm_list)

                if is_vol_active:
                    ui_color = COLOR_CYAN
                    mode_text = "MODO: AJUSTE VOLUMEN"

                    # Distancia entre Pulgar (4) e Índice (8)
                    x1, y1 = lm_list[4][1], lm_list[4][2]
                    x2, y2 = lm_list[8][1], lm_list[8][2]
                    distance = math.hypot(x2 - x1, y2 - y1)

                    # Aplicar volumen y actualizar UI
                    old_v = vol_ctrl.get_current_volume()
                    vol_per = vol_ctrl.set_volume(distance)
                    vol_bar = np.interp(distance, [50, 250], [400, 150])

                    # Persistencia en Atlas si el cambio es real
                    if abs(vol_per - old_v) > 3:
                        dao.save_volume_event({
                            "session_id": session_data.get("_id"),
                            "timestamp": datetime.now(),
                            "type": "volume_change",
                            "level": int(vol_per)
                        })

                    # Feedback visual de la "pinza"
                    cv2.line(img, (x1, y1), (x2, y2), COLOR_MAGENTA, 3)
                else:
                    # Modo Idle: Actualizamos la barra según el volumen real del sistema
                    real_v = vol_ctrl.get_current_volume()
                    vol_per = real_v
                    vol_bar = np.interp(real_v, [0, 100], [400, 150])

        # --- 4. RENDERIZADO DE INTERFAZ ---

        # Barra de volumen lateral
        cv2.rectangle(img, (50, 150), (85, 400), (40, 40, 40), cv2.FILLED)
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), ui_color, cv2.FILLED)
        cv2.rectangle(img, (50, 150), (85, 400), (200, 200, 200), 2)
        cv2.putText(img, f'{int(vol_per)}%', (45, 450), cv2.FONT_HERSHEY_DUPLEX, 1, ui_color, 2)

        # Panel superior de Estado
        cv2.rectangle(img, (0, 0), (400, 110), (20, 20, 20), cv2.FILLED)
        cv2.putText(img, mode_text, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1.5, ui_color, 2)

        # Indicador DB (Requisito)
        db_color = (0, 255, 0) if dao.connection_ok else (0, 0, 255)
        db_txt = "CONEXION ATLAS: OK" if dao.connection_ok else "CONEXION ATLAS: --"
        cv2.putText(img, db_txt, (20, 80), cv2.FONT_HERSHEY_PLAIN, 1.2, db_color, 1)

        cv2.imshow("Cyber Volume Control - Monlau Edition", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- 5. CIERRE ---
    dao.db.sessions.update_one(
        {"_id": session_data.get("_id")},
        {"$set": {"end_time": datetime.now(), "status": "closed"}}
    )
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()