from config import *
import json
from datetime import datetime


def find_new_game(index_list, cached_line):
	with open(LOG_FILE_PATH, "r") as f:
		lines = f.readlines()
		for index, line in enumerate((lines)):
			if FOUND_GAME_TARGET_STRING in line:
				if index not in index_list:
					index_list.append(index)
					return False, index_list, cached_line
		for index, line in enumerate(reversed(lines[index_list[-1]:])):
			if GAME_OVER_TARGET_STRING in line:
					return False, index_list, cached_line
			elif FOUND_GAME_TARGET_STRING in line:
				if line != cached_line:
					print("NUEVA PARTIDA")
					return True, index_list, line
		return False, index_list, cached_line

def get_players(index, logger, player_target_string=PLAYER_TARGET_STRING, break_target_string=BREAK_TARGET_STRING):
	try:
		players_list = []
		finished = False
		logger.info("Voy a armar la lista de jugadores...")
		while True:
			with open(LOG_FILE_PATH, "r") as f:
				lines = f.readlines()
				for line in lines[index:]:
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


def get_previous_game_players():
	try:
		with open(PREV_GAME_LIST_PATH, "r") as f:
			return json.load(f)
	except:
		with open(PREV_GAME_LIST_PATH, "w+") as f:
			return []


def save_previous_game_players(players_list, logger):
	try:
		if not players_list:
			return True
		previous_list = get_previous_game_players()
		if len(previous_list) == PREV_GAMES_LIMIT:
			previous_list.pop(-1)
		logger.info("Guardando la lista anterior de jugadores...")
		with open(PREV_GAME_LIST_PATH, "w") as f:
			previous_list.append([player for player in players_list])
			json.dump(previous_list, f)
			return True
	except Exception as ex:
		logger.exception(ex)
		return False
