from config import *


def get_last_instance_index(file_path, logger, index_target_string=INDEX_TARGET_STRING):
	try:
		with open(file_path, "r") as f:
			lines = f.readlines()
			for index, line in enumerate(reversed(lines)):
				if index_target_string in line:
					return index
			return None
	except Exception as ex:
		logger.exception(ex)
		return None


def get_players(file_path, logger, index=None, player_target_string=PLAYER_TARGET_STRING, break_target_string=BREAK_TARGET_STRING):
	try:
		players_list = []
		finished = False
		logger.info("Voy a armar la lista de jugadores...")
		while True:
			with open(file_path, "r") as f:
				lines = f.readlines()
				new_index = len(lines) - index - 1
				for line in lines[new_index:]:
					if player_target_string in line:
						logger.info("Encontré el PLAYER_TARGET_STRING")
						player = line.split("_")[1].split(" (")[0].replace(" ", "_")
						if player in players_list:
							continue
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
