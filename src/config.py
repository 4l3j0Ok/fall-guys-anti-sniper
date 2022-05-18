import os

USER = os.getlogin()
TESTING = False
LOG_FILE_PATH = "C:\\Users\\{}\\AppData\\LocalLow\\Mediatonic\\FallGuys_client\\Player.log".format(USER)
TEST_FILE = "C:\\Users\\{}\\Desktop\\test.txt".format(USER)
INDEX_TARGET_STRING = "[StateMatchmaking] Found game on"
PLAYER_TARGET_STRING = "[CameraDirector] Adding Spectator target "
BREAK_TARGET_STRING = "[CameraDirector].UseIntroCameras"
GAME_OVER_TARGET_STRING = "[GameSession] Changing state from Playing to GameOver"