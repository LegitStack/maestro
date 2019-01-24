"""
Settings from environment
"""
import os

from pathlib import Path
import dotenv
import yaml

dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True))


def get_config():
    ''' gets configuration out of the yaml file '''
    with open('config.yml') as config:
        return yaml.load(config)


def get_data_directory():
    ''' returns data directory from environment or yaml files '''
    data_path = Path(os.getenv('DATA_DIR'))
    if data_path is None:
        config = get_config()
    data_path = config['directories']['data']
