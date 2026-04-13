import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'datax_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
}

# Table name
TABLE_NAME = 'file'

# App Configuration
APP_TITLE = "DBUpdater - Data Management System"
APP_DESCRIPTION = "Manage your database with ease"

# Field definitions for the database
FIELD_DEFINITIONS = {
    'id_file': {'type': 'integer', 'primary_key': True, 'editable': False},
    'id_source': {'type': 'integer', 'required': True},
    'name': {'type': 'string', 'required': True},
    'code': {'type': 'string', 'required': False},
    'main_url': {'type': 'string', 'required': False},
    'path': {'type': 'string', 'required': False},
    'type': {'type': 'string', 'required': False},
    'specific_url': {'type': 'string', 'required': False},
    'alternate_url': {'type': 'string', 'required': False},
    'navigation_path': {'type': 'string', 'required': False},
    'publication_frequency': {'type': 'string', 'required': False},
    'priority': {'type': 'integer', 'required': False},
    'state': {'type': 'string', 'required': False},
    'creation_date': {'type': 'datetime', 'required': False, 'editable': False},
    'update_date': {'type': 'datetime', 'required': False, 'editable': False},
    'observations': {'type': 'string', 'required': False},
    'updated_to': {'type': 'string', 'required': False},
    'last_file_path': {'type': 'string', 'required': False},
    'last_file_url': {'type': 'string', 'required': False},
    'schedule_interval': {'type': 'string', 'required': False},
    'publication_date': {'type': 'string', 'required': False},
    'key_words': {'type': 'string', 'required': False},
    'section_path': {'type': 'string', 'required': False},
    'short_name': {'type': 'string', 'required': False},
    'download_type': {'type': 'string', 'required': False},
}
