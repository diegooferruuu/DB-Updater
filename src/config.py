import os
from dotenv import load_dotenv
import re
from urllib.parse import urlparse

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
APP_TITLE = "Datax DBUpdater"
APP_DESCRIPTION = "Manage File Table"

# Validation Functions
def validate_url(url):
    """Validate URL format"""
    if not url or url.strip() == '':
        return True, None
    try:
        result = urlparse(str(url))
        is_valid = all([result.scheme, result.netloc])
        return is_valid, None if is_valid else "Invalid URL format"
    except:
        return False, "Invalid URL format"

def validate_integer(value):
    """Validate integer value"""
    if value is None or value == '':
        return True, None
    try:
        int(value)
        return True, None
    except:
        return False, "Must be a number"

def validate_path(path):
    """Validate path format"""
    if not path or path.strip() == '':
        return True, None
    # Basic path validation (can be enhanced)
    if path.startswith('/') or path.startswith('.'):
        return True, None
    return False, "Path should start with / or ."

def validate_email(email):
    """Validate email format"""
    if not email or email.strip() == '':
        return True, None
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(pattern, str(email)))
    return is_valid, None if is_valid else "Invalid email format"

# Field definitions for the database
FIELD_DEFINITIONS = {
    'id_file': {'type': 'integer', 'primary_key': True, 'editable': False, 'filterable': False},
    'id_source': {'type': 'integer', 'required': True, 'validator': validate_integer, 'filterable': False},
    'name': {'type': 'string', 'required': True, 'filterable': True},
    'code': {'type': 'string', 'required': False, 'filterable': True},
    'main_url': {'type': 'string', 'required': False, 'validator': validate_url, 'filterable': True},
    'path': {'type': 'string', 'required': False, 'validator': validate_path, 'filterable': False},
    'type': {'type': 'string', 'required': False, 'filterable': True},
    'specific_url': {'type': 'string', 'required': False, 'validator': validate_url, 'filterable': False},
    'alternate_url': {'type': 'string', 'required': False, 'validator': validate_url, 'filterable': False},
    'navigation_path': {'type': 'string', 'required': False, 'validator': validate_path, 'filterable': False},
    'publication_frequency': {'type': 'string', 'required': False, 'filterable': True},
    'priority': {'type': 'integer', 'required': False, 'validator': validate_integer, 'filterable': True},
    'state': {'type': 'string', 'required': False, 'filterable': True},
    'creation_date': {'type': 'datetime', 'required': False, 'editable': False, 'filterable': True},
    'update_date': {'type': 'datetime', 'required': False, 'editable': False, 'filterable': True},
    'observations': {'type': 'string', 'required': False, 'filterable': True},
    'updated_to': {'type': 'string', 'required': False, 'filterable': True},
    'last_file_path': {'type': 'string', 'required': False, 'filterable': False},
    'last_file_url': {'type': 'string', 'required': False, 'filterable': False},
    'schedule_interval': {'type': 'string', 'required': False, 'filterable': True},
    'publication_date': {'type': 'string', 'required': False, 'filterable': True},
    'key_words': {'type': 'string', 'required': False, 'filterable': True},
    'section_path': {'type': 'string', 'required': False, 'filterable': False},
    'short_name': {'type': 'string', 'required': False, 'filterable': True},
    'download_type': {'type': 'string', 'required': False, 'filterable': True},
    'responsable': {'type': 'string', 'required': False, 'filterable': True},
    'control_estado': {'type': 'string', 'required': False, 'filterable': True},
    'tipo_error': {'type': 'string', 'required': False, 'filterable': True},
    'display_name': {'type': 'string', 'required': False, 'filterable': True},
}

# Fields that require validation
FIELDS_WITH_VALIDATION = [
    'id_source', 'name', 'type', 'alternate_url', 'navigation_path', 
    'publication_frequency', 'priority', 'state', 'observations', 'key_words', 'section_path'
]

# Control Estado options
CONTROL_ESTADO_OPTIONS = ['Activo', 'Inactivo', 'En Revisión', 'Archivado']

# Tipo Error options
TIPO_ERROR_OPTIONS = ['Datos Incompletos', 'URL Inválida', 'Path Incorrecto', 'Otro']

# Columns to hide by default in view
HIDDEN_COLUMNS_DEFAULT = []

# All filterable columns
FILTERABLE_COLUMNS = [key for key, value in FIELD_DEFINITIONS.items() if (value.get('filterable', False))]
