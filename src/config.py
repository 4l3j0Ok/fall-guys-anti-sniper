import os


USER = os.getlogin()
TESTING = False
UI_PATH = ".\\src\\ui\\home.ui"
LOG_FILE_PATH = "C:\\Users\\{}\\AppData\\LocalLow\\Mediatonic\\FallGuys_client\\Player.log".format(USER)
TEST_FILE = "test.txt"
FOUND_GAME_TARGET_STRING = "[GameStateMachine] Replacing FGClient.StateWaitingForGameToStart with FGClient.StateGameLoading"
PLAYER_TARGET_STRING = "[CameraDirector] Adding Spectator target "
BREAK_TARGET_STRING = "[CameraDirector].UseIntroCameras"
GAME_OVER_TARGET_STRING = "[FG_UnityInternetNetworkManager] FG_NetworkManager shutdown completed"