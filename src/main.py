from logger import logger
import utils
import config


#TODO Graphic interface (Tkinter/PyQt5)
#TODO Send windows notification if sniper detected https://www.youtube.com/watch?v=p1w-FZclhXs


if __name__ == "__main__":
	file_path = config.LOG_FILE_PATH if not config.TESTING else config.TEST_FILE
	last_instance_index = utils.get_last_instance_index(file_path, logger)
	players_list = utils.get_players(file_path, logger, index=last_instance_index)