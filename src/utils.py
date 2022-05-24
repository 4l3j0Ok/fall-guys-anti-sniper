from config import *
import json
from datetime import datetime


def get_players(index, logger, player_target_string=PLAYER_TARGET_STRING, break_target_string=BREAK_TARGET_STRING):
	try:
		players_list = []
		finished = False
		logger.info("Voy a armar la lista de jugadores...")
		while True:
			with open(LOG_FILE_PATH, "r") as f:
				lines = f.readlines()
				new_index = len(lines) - index - 1
				for line in lines[new_index:]:
					if player_target_string in line:
						player = line.replace(line.split("_")[0] + "_", "").replace(" (" + line.split(" (")[1], "")
						if player in players_list:
							continue
						logger.info("Encontré el jugador '{}', lo guardo en la lista de jugadores.".format(player))
						players_list.append(player)
					if break_target_string in line:
						finished = True
						break
			if finished:
				logger.info("¡Lista de jugadores completada!")
				logger.debug(players_list)
				break
		return players_list
	except Exception as ex:
		logger.exception(ex)
		return []


def find_new_game(last_index, logger):
	with open(LOG_FILE_PATH, "r") as f:
		lines = f.readlines()
		for index, line in enumerate(reversed(lines)):
			if GAME_OVER_TARGET_STRING in line:
				return False, index
			elif FOUND_GAME_TARGET_STRING in line:
				if index != last_index:
					logger.debug("Encontré una nueva partida.")
					return True, index
	return False, index


def get_blacklist():
	try:
		with open(BLACKLIST_PATH, "r") as f:
			return json.load(f)
	except:
		with open(BLACKLIST_PATH, "w+") as f:
			return []


def save_to_blacklist(name, logger):
	try:
		blacklist = get_blacklist()
		with open(BLACKLIST_PATH, "w") as f:
			data = {}
			data["name"] = name
			data["saved_on"] = datetime.now().strftime(STRFTIME_FORMAT)
			blacklist.append(data)
			json.dump(blacklist, f)
			return True
	except Exception as ex:
		logger.exception(ex)
		return False

