# -*- coding: utf-8 -*-
import os


# APP CONFIG
APP_NAME = "Fall Guys Anti Sniper"
APP_VERSION = 1.7
STRFTIME_FORMAT = "%d/%m/%Y - %H:%M:%S"


# PATHS
LOCALAPPDATA = os.environ.get("LOCALAPPDATA")
LOG_FILE_PATH = "{}Low\\Mediatonic\\FallGuys_client\\Player.log".format(LOCALAPPDATA)
APP_LOG_FILE_PATH = ".\\application.log"
DATA_PATH = ".\\data.json"


# APP MISC CONFIG
PREV_GAMES_LIMIT = 5
USERNAME_TARGET_STRING = "[UserInfo] Player Name: "
POSSIBLE_GAME_TARGET_STRING = "[GameStateMachine] Replacing FGClient.StateConnectToGame with FGClient.StateConnectionAuthentication"
FOUND_GAME_TARGET_STRING = "[GameStateMachine] Replacing FGClient.StateConnectionAuthentication with FGClient.StateGameLoading"
PLAYER_TARGET_STRING = "[CameraDirector] Adding Spectator target "
BREAK_TARGET_STRING = "[GameStateMachine] Replacing FGClient.StateGameLoading with FGClient.StateGameInProgress"
GAME_OVER_TARGET_STRING = "[FG_UnityInternetNetworkManager] FG_NetworkManager shutdown completed"
ABOUT_STRING = "Desarrollado por: Alejoide.\nDesarrollado con: Python, Qt, Redragon Aryaman.\n\nPD: Aitorek Bobo."
GITHUB_API_URL = "https://api.github.com/repos/4l3j0Ok/fall-guys-anti-sniper/releases/latest"
GITHUB_RELEASE_DOWNLOAD_URL = "https://github.com/4l3j0Ok/fall-guys-anti-sniper/releases/download/{}/FGAntiSniper.zip"
LATEST_RELEASE_URL = "https://github.com/4l3j0Ok/fall-guys-anti-sniper/releases/latest"


# EXCEPTION STRINGS
ERR_CONNECTION = "Ocurrió un error al intentar conectar con GitHub."
ERR_TAG_NAME = "Ocurrió un error al descargar la última versión."
ERR_UPDATER_EXCEPTION = "Ocurrió un error al actualizar la aplicación."
ERR_LATEST_VERSION_EXISTS = "La ultima versión ya se encuentra descargada."