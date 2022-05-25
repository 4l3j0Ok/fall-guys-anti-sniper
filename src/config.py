import os


USER = os.getlogin()
TESTING = False
UI_PATH = ".\\src\\ui\\home.ui"
BLACKLIST_PATH = ".\\blacklist.json"
PREV_GAME_LIST_PATH = ".\\prev_games.json"
PREV_GAMES_LIMIT = 10
LOG_FILE_PATH = "C:\\Users\\{}\\AppData\\LocalLow\\Mediatonic\\FallGuys_client\\Player.log".format(USER)
FOUND_GAME_TARGET_STRING = "[GameStateMachine] Replacing FGClient.StateConnectToGame with FGClient.StateWaitingForGameToStart"
PLAYER_TARGET_STRING = "[CameraDirector] Adding Spectator target "
BREAK_TARGET_STRING = "[GameStateMachine] Replacing FGClient.StateGameLoading with FGClient.StateGameInProgress"
GAME_OVER_TARGET_STRING = "[FG_UnityInternetNetworkManager] FG_NetworkManager shutdown completed"
STRFTIME_FORMAT = "%d/%m/%Y - %H:%M:%S"