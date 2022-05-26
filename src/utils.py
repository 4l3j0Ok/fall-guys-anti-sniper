from config import *
import json
from datetime import datetime


def find_new_game(index_list, cached_line, logger, playing=False):
	with open(LOG_FILE_PATH, "r") as f:
		lines = f.readlines()
		if not playing:
			for index, line in enumerate(lines):
				if POSSIBLE_GAME_TARGET_STRING in line:
					if index not in index_list:
						index_list.append(index)
						logger.debug("Encontré el FOUND_GAME_TARGET_STRING")
						logger.debug("Total de juegos encontrados hasta ahora: {}".format(len(index_list) - 1))
						return False, index_list, cached_line, playing
		for index, line in enumerate(reversed(lines[index_list[-1]:])):
			if playing:
				if GAME_OVER_TARGET_STRING in line:
					logger.info("Juego terminado")
					return False, index_list, "", False
			else:
				if GAME_OVER_TARGET_STRING in line:
					return False, index_list, "", False
				if not cached_line:
					if POSSIBLE_GAME_TARGET_STRING in line:
						logger.info("POSIBLE PARTIDA ENCONTRADA!")
						return False, index_list, line, False
				else:
					if FOUND_GAME_TARGET_STRING in line:
						logger.info("PARTIDA ENCONTRADA!")
						return True, index_list, "", True
		return False, index_list, cached_line, playing


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


def get_data():
	try:
		with open(DATA_PATH, "r") as f:
			return json.load(f)
	except:
		with open(DATA_PATH, "w+") as f:
			return {}


def save_data(data):
	with open(DATA_PATH, "w") as f:
		json.dump(data, f)


def save_to_blacklist(name):
	data = get_data()
	data.get("blacklist", []).append(name)
	save_data(data)


def save_previous_game_players(players_list, logger):
	data = get_data()
	data["prev_games_players"] = data.get("prev_games_players", [])
	if len(data["prev_games_players"]) == PREV_GAMES_LIMIT:
		data["prev_games_players"].pop(-1)
	logger.info("Guardando la lista anterior de jugadores...")
	data["prev_games_players"].append([player for player in players_list])
	save_data(data)
