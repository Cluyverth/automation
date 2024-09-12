import configparser
from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()   

def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config_file = Path(__file__).parent / 'config.ini'
    config.read(config_file)
    return config

def get_db_config(service_name: str) -> Dict[str, Optional[str]]:
    config = load_config()
    db_config = config[service_name]
    return{
        'server': db_config.get('server'),
        'database': db_config.get('database')
    }
    
def get_env_variable(var_name: str) -> Optional[str]:
    return os.getenv(var_name)