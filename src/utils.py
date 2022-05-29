# -*- coding: utf-8 -*-
import json
import csv
import time
from itertools import zip_longest
from datetime import datetime
from config import *
from logger import logger


def find_new_game(index_list, cached_line, playing=False):
	try:
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
						logger.info("Juego terminado.")
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
	except Exception as ex:
		logger.exception(ex)
		return False, index_list, cached_line, playing


def get_username():
	with open(LOG_FILE_PATH, "r") as f:
		username = None
		lines = f.readlines()
		for line in lines:
			if USERNAME_TARGET_STRING in line:
				logger.info("Último nombre del jugador obtenido!")
				username = line.split(USERNAME_TARGET_STRING)[1].replace("\n", "")
				data = get_data()
				logger.debug("Guardando el nombre en data.json")
				logger.debug(username)
				data["username"] = username
				save_data(data)
				break
		return username


def get_players(index, username):
	try:
		players_list = []
		finished = False
		logger.info("Voy a armar la lista de jugadores...")
		while True:
			time.sleep(3)
			with open(LOG_FILE_PATH, "r") as f:
				lines = f.readlines()
				for line in lines[index:]:
					if PLAYER_TARGET_STRING in line:
						player = line.replace(line.split("_")[0] + "_", "").replace(" (" + line.split(" (")[1], "")
						if player == username:
							continue
						if player in players_list:
							continue
						logger.info("Encontré el jugador '{}', lo guardo en la lista de jugadores.".format(player))
						players_list.append(player)
					if BREAK_TARGET_STRING in line:
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
	with open(LOG_FILE_PATH, "r") as f:
		data = get_data()
		lines = f.readlines()
		players_list = []
		for line in lines[:index]:
			if PLAYER_TARGET_STRING in line:
				player = line.replace(line.split("_")[0] + "_", "").replace(" (" + line.split(" (")[1], "")
				if player == username:
					continue
				if player in players_list:
					continue
				players_list.append(player)
			if BREAK_TARGET_STRING in line:
				data["prev_games_players"] = data.get("prev_games_players", [])
				if len(data["prev_games_players"]) == PREV_GAMES_LIMIT:
					data["prev_games_players"].pop(0)
				logger.info("Guardando la lista anterior de jugadores...")
				data["prev_games_players"].append([player for player in players_list])
				save_data(data)
				players_list = []
	logger.info("Terminé de llenar la lista de jugadores previos.")


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
			if player in blacklist:
				logger.info("ENCONTRÉ UN SNIPER: {}".format(player))
				snipers_data["snipers"].append(player)
				continue
			for prev_players in prev_games:
				if player in prev_players:
					if player not in snipers_data["suspects"]:
						logger.info("ENCONTRÉ UN POSIBLE SNIPER: {}".format(player))
						snipers_data["suspects"].append(player)
						continue
		logger.debug(snipers_data)
		return snipers_data
	except Exception as ex:
		logger.exception(ex)
		return {}


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


def save_to_blacklist(player):
	data = get_data()
	data["blacklist"] = data.get("blacklist", [])
	data["blacklist"].append(player)
	save_data(data)


def clear_blacklist(player=None):
	data = get_data()
	if data.get("blacklist"):
		if not player:
			logger.warning("Voy a limpiar la blacklist entera.")
			del(data["blacklist"])
		else:
			logger.warning("Voy a sacar a '{}' de la blacklist.".format(player))
			if player in data["blacklist"]:
				data["blacklist"].remove(player)
		save_data(data)


def export_as_csv(blacklist, players, suspects, snipers):
	filepath = ".\\fall_guys_anti_sniper_" + datetime.today().strftime("%d-%m-%Y_%H.%M.%S") + ".csv"
	header = ["Lista negra", "Jugadores en la partida", "Posibles snipers", "Snipers"]
	lists = [blacklist, players, suspects, snipers]
	with open(filepath, "w", newline="") as f:
		writer = csv.writer(f)
		writer.writerow(header)
		for values in zip_longest(*lists):
			writer.writerow(values)
	return filepath
