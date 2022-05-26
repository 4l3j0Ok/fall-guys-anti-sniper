# -*- coding: utf-8 -*-
import os


USER = os.getlogin()
UI_PATH = ".\\src\\ui\\home.ui"
ICON_PATH = ".\\src\\ui\\icon.png"
DATA_PATH = ".\\data.json"
PREV_GAMES_LIMIT = 5
LOG_FILE_PATH = "C:\\Users\\{}\\AppData\\LocalLow\\Mediatonic\\FallGuys_client\\Player.log".format(USER)
USERNAME_TARGET_STRING = "[UserInfo] Player Name: "
POSSIBLE_GAME_TARGET_STRING = "[GameStateMachine] Replacing FGClient.StateConnectToGame with FGClient.StateWaitingForGameToStart"
FOUND_GAME_TARGET_STRING = "[GameStateMachine] Replacing FGClient.StateWaitingForGameToStart with FGClient.StateGameLoading"
PLAYER_TARGET_STRING = "[CameraDirector] Adding Spectator target "
BREAK_TARGET_STRING = "[GameStateMachine] Replacing FGClient.StateGameLoading with FGClient.StateGameInProgress"
GAME_OVER_TARGET_STRING = "[FG_UnityInternetNetworkManager] FG_NetworkManager shutdown completed"
STRFTIME_FORMAT = "%d/%m/%Y - %H:%M:%S"
ABOUT_STRING = """
                Desarrollado por: Alejoide. \n
                Desarrollado con: Python, Qt, Redragon Aryaman.\n
                PD: Aitorek Bobo.
                """