import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeController:
    def __init__(self):
        # Usamos el enumerador directamente para obtener el objeto COM puro
        # Esto evita el error de 'AudioDevice' que estás teniendo
        device_enumerator = AudioUtilities.GetDeviceEnumerator()
        devices = device_enumerator.GetDefaultAudioEndpoint(0, 1)  # 0: eRender, 1: eMultimedia

        self.interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

        # Rango de volumen (usualmente -65.25 a 0.0)
        self.vol_range = self.volume.GetVolumeRange()
        self.min_vol = self.vol_range[0]
        self.max_vol = self.vol_range[1]

    def get_current_volume(self):
        # Retorna el volumen actual en escala 0.0 a 1.0 (multiplicado por 100 para %)
        return self.volume.GetMasterVolumeLevelScalar() * 100

    def set_volume(self, distance):
        # Mapeo de distancia (píxeles) a decibelios
        vol = np.interp(distance, [50, 300], [self.min_vol, self.max_vol])
        self.volume.SetMasterVolumeLevel(vol, None)
        # Retorna el porcentaje para la interfaz visual
        return np.interp(distance, [50, 300], [0, 100])

    def is_pinky_down(self, lm_list):
        # Gesto intencional requerido por el enunciado
        # El meñique (punto 20) está por debajo de su articulación (punto 18)
        if len(lm_list) >= 21:
            return lm_list[20][2] > lm_list[18][2]
        return False

    def set_mute(self, status):
        """
        Sets the mute state.
        status: True to mute, False to unmute.
        """
        self.volume.SetMute(status, None)

    def get_mute_status(self):
        """Returns the current mute status (0 for False, 1 for True)"""
        return self.volume.GetMute()