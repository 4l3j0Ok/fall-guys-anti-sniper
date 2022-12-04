# -*- coding: utf-8 -*-
import json
import csv
from itertools import zip_longest
import config as cfg
from logger import logger
import requests
import shutil


def find_new_game(index_list, cached_line, playing=False):
	try:
		with open(cfg.LOG_FILE_PATH, "r", encoding="utf8") as f:
			lines = f.readlines()
			if not playing:
				for index, line in enumerate(lines):
					if cfg.POSSIBLE_GAME_TARGET_STRING in line:
						if index not in index_list:
							index_list.append(index)
							logger.debug("Encontré el FOUND_GAME_TARGET_STRING")
							logger.debug("Total de juegos encontrados hasta ahora: {}".format(len(index_list) - 1))
							return False, index_list, cached_line, playing
			for index, line in enumerate(reversed(lines[index_list[-1]:])):
				if playing:
					if cfg.GAME_OVER_TARGET_STRING in line:
						logger.info("Juego terminado.")
						return False, index_list, "", False
				else:
					if cfg.GAME_OVER_TARGET_STRING in line:
						return False, index_list, "", False
					if not cached_line:
						if cfg.POSSIBLE_GAME_TARGET_STRING in line:
							logger.info("POSIBLE PARTIDA ENCONTRADA!")
							return False, index_list, line, False
					else:
						if cfg.FOUND_GAME_TARGET_STRING in line:
							logger.info("PARTIDA ENCONTRADA!")
							return True, index_list, "", True
			return False, index_list, cached_line, playing
	except Exception as ex:
		logger.exception(ex)
		return False, index_list, cached_line, playing


def get_username():
	try:
		with open(cfg.LOG_FILE_PATH, "r", encoding="utf8") as f:
			username = None
			lines = f.readlines()
			for line in lines:
				if cfg.USERNAME_TARGET_STRING in line:
					logger.info("Último nombre del jugador obtenido!")
					username = line.split(cfg.USERNAME_TARGET_STRING)[1].replace("\n", "")
					data = get_data()
					logger.debug("Guardando el nombre en data.json")
					logger.debug(username)
					data["username"] = username
					save_data(data)
					break
			return username
	except Exception as ex:
		logger.exception(ex)
		return None


def get_username_by_data():
	data = get_data()
	return data.get("username")

def get_players(index, username):
	try:
		players_list = []
		finished = False
		logger.info("Voy a armar la lista de jugadores...")
		while True:
			with open(cfg.LOG_FILE_PATH, "r", encoding="utf8") as f:
				lines = f.readlines()
				for line in lines[index:]:
					if cfg.PLAYER_TARGET_STRING in line:
						player = line.replace(line.split("...")[0] + "...", "").replace(" (" + line.split(" (")[1], "")
						if player == username:
							continue
						if player in players_list:
							continue
						logger.info("Encontré el jugador '{}', lo guardo en la lista de jugadores.".format(player))
						players_list.append(player)
					if cfg.BREAK_TARGET_STRING in line:
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


def update_prev_games_players(index, username):
	try:
		with open(cfg.LOG_FILE_PATH, "r", encoding="utf8") as f:
			data = get_data()
			lines = f.readlines()
			players_list = []
			for line in lines[:index]:
				if cfg.PLAYER_TARGET_STRING in line:
					player = line.replace(line.split("...")[0] + "...", "").replace(" (" + line.split(" (")[1], "")
					if player == username:
						continue
					if player in players_list:
						continue
					players_list.append(player)
				if cfg.BREAK_TARGET_STRING in line:
					data["prev_games_players"] = data.get("prev_games_players", [])
					if len(data["prev_games_players"]) == cfg.PREV_GAMES_LIMIT:
						data["prev_games_players"].pop(0)
					logger.info("Guardando la lista anterior de jugadores...")
					data["prev_games_players"].append([player for player in players_list])
					save_data(data)
					players_list = []
		logger.info("Terminé de llenar la lista de jugadores previos.")
		return True
	except Exception as ex:
		logger.exception(ex)
		return False


def get_snipers(players_list):
	try:
		logger.info("Buscando snipers...")
		data = get_data()
		blacklist = data.get("blacklist", [])
		snipers_data = {}
		snipers_data["suspects"] = []
		snipers_data["snipers"] = []
		prev_games = data.get("prev_games_players", [])
		username = data.get("username")
		for player in players_list:
			if player == username:
				continue
			if blacklist:
				if cfg.EVIL_MEDIATONIC:
					if not cfg.CASE_SENSITIVE:
						if player.lower() in [p.lower()[-3:] for p in blacklist]:
							logger.info("ENCONTRÉ UN SNIPER: {}".format(player))
							for i, p in enumerate(blacklist):
								if player == p.lower()[-3:]:
									snipers_data["snipers"].append(blacklist[i])
									continue
					else:
						if player in [p for p in blacklist]:
							logger.info("ENCONTRÉ UN SNIPER: {}".format(player))
							for i, p in enumerate(blacklist):
								if player == p:
									snipers_data["snipers"].append(blacklist[i])
									continue
				else:
					if not cfg.CASE_SENSITIVE:
						if player.lower() in [p.lower() for p in blacklist]:
							logger.info("ENCONTRÉ UN SNIPER: {}".format(player))
							snipers_data["snipers"].append(player)
							continue
					else:
						if player in [p for p in blacklist]:
							logger.info("ENCONTRÉ UN SNIPER: {}".format(player))
							snipers_data["snipers"].append(player)
							continue
			if not cfg.EVIL_MEDIATONIC:
				if prev_games:
					for prev_players in prev_games:
						if not cfg.CASE_SENSITIVE:
							if player.lower() in [p.lower() for p in prev_players]:
								if player not in snipers_data["suspects"]:
									logger.info("ENCONTRÉ UN POSIBLE SNIPER: {}".format(player))
									snipers_data["suspects"].append(player)
									continue
						else:
							if player in [p for p in prev_players]:
								if player not in snipers_data["suspects"]:
									logger.info("ENCONTRÉ UN POSIBLE SNIPER: {}".format(player))
									snipers_data["suspects"].append(player)
									continue
		logger.debug(snipers_data)
		return snipers_data
	except Exception as ex:
		logger.exception(ex)
		return {}


def get_data(key=None, default=None):
	try:
		with open(cfg.DATA_PATH, "r") as f:
			data = json.load(f)
			if key:
				return data.get(key, default)
			return data
	except Exception:
		with open(cfg.DATA_PATH, "w+") as f:
			if default != None:
				return default
			return {}


def save_data(data):
	try:
		with open(cfg.DATA_PATH, "w", encoding="utf8") as f:
			json.dump(data, f)
			return True
	except Exception as ex:
		logger.exception(ex)
		return False


def save_to_blacklist(players):
	try:
		data = get_data()
		data["blacklist"] = data.get("blacklist", [])
		if isinstance(players, str):
			players = str(players).replace("\n", "")
			if players not in data["blacklist"]:
				data["blacklist"].append(players)
		elif isinstance(players, list):
			for player in players:
				player = str(player).replace("\n", "")
				if player not in data["blacklist"]:
					data["blacklist"].append(player)
		success = save_data(data)
		if not success:
			logger.error("Hubo un error al guardar en la blacklist.")
			return False, []
		return True, data["blacklist"]
	except Exception as ex:
		logger.exception(ex)
		return False, []


def clear_blacklist(player=None):
	try:
		data = get_data()
		if data.get("blacklist"):
			if not player:
				logger.warning("Voy a limpiar la blacklist entera.")
				del(data["blacklist"])
			else:
				logger.warning("Voy a sacar a '{}' de la blacklist.".format(player))
				if player in data["blacklist"]:
					data["blacklist"].remove(player)
			success = save_data(data)
			if not success:
				logger.error("Hubo un error al limpiar la blacklist.")
				return False
			return True
	except Exception as ex:
		logger.exception(ex)
		return False


def export_as_csv(filepath, blacklist, players, suspects, snipers):
	try:
		header = ["Lista negra", "Jugadores en la partida", "Posibles snipers", "Snipers"]
		lists = [blacklist, players, suspects, snipers]
		with open(filepath, "w", newline="") as f:
			writer = csv.writer(f)
			writer.writerow(header)
			for values in zip_longest(*lists):
				writer.writerow(values)
		return True, filepath
	except Exception as ex:
		logger.exception(ex)
		return False, ""


def export_blacklist(filepath, blacklist):
	try:
		with open(filepath, "w+") as f:
			for player in blacklist:
				logger.info("Voy a exportar esta blacklist: {}".format(blacklist))
				f.write(player + "\n")
		return True
	except Exception as ex:
		logger.exception(ex)
		return False


def import_blacklist(filepath):
	try:
		with open(filepath, "r", encoding="utf8") as f:
			players = f.readlines()
			logger.info("Voy a importar esta blacklist: {}".format(players))
			success, blacklist = save_to_blacklist(players)
			if not success:
				return False, []
		return True, blacklist
	except Exception as ex:
		logger.exception(ex)
		return False, []


def check_new_release():
	try:
		logger.info("Chequeando si hay nuevos releases.")
		try:
			response = requests.get(cfg.GITHUB_API_URL, timeout=5).json()
		except requests.Timeout as exw:
			logger.exception(exw)
			return False
		except requests.ConnectionError as exw:
			logger.exception(exw)
			return False
		if response.get("tag_name"):
			latest_version = float(response.get("tag_name").replace("v", ""))
			if latest_version > cfg.APP_VERSION:
				return True
		logger.info("No encontré nuevos releases.")
		return False
	except Exception as ex:
		logger.exception(ex)
		return False


def get_latest_version():
	try:
		response = requests.get(cfg.GITHUB_API_URL).json()
	except requests.Timeout as exw:
		logger.exception(exw)
		return False, cfg.ERR_CONNECTION
	except requests.ConnectionError as exw:
		logger.exception(exw)
		return False, cfg.ERR_CONNECTION
	if response.get("tag_name"):
		return True, response["tag_name"]
	return False, cfg.ERR_TAG_NAME


def clear_log():
	try:
		dest = cfg.APP_LOG_FILE_PATH.replace(".log", "_old.log")
		shutil.copy(cfg.APP_LOG_FILE_PATH, dest)
		open(cfg.APP_LOG_FILE_PATH, "w+").close()
		logger.debug("Log vaciado con éxito.")
		logger.info("Log antiguo guardado en {}.".format(dest))
	except Exception as ex:
		logger.exception(ex)

# TODO
# def prevalidate():
# 	try:
# 		logfile = open(LOG_FILE_PATH, "r", encoding="utf8")
# 		logger.info("Encontré el archivo log del juego.")
# 	except Exception as ex:
# 		logger.exception(ex)
