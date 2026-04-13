# DBUpdater - Data Management System

Una aplicación web simple y eficiente para gestionar datos en una base de datos PostgreSQL usando Python y Streamlit.

## 🎯 Características

- **Agregar Datos**: Formulario interactivo para insertar nuevos registros
- **Ver Datos**: Tabla con todos los registros de la base de datos
- **Editar Datos**: Edición en línea con doble clic en las celdas
- **Eliminar Datos**: Opción para eliminar registros
- **Búsqueda**: Filtrado rápido por nombre o código
- **Validación**: Validación de campos requeridos

## 🛠️ Instalación

### Requisitos Previos
- Python 3.8+
- PostgreSQL
- pip

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
cd /Users/diegoferrufino/Documents/Datax/Software/DBUpdater
```

2. **Crear un entorno virtual** (opcional pero recomendado)
```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales de PostgreSQL:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
```

5. **Crear la tabla en PostgreSQL**

Ejecuta el siguiente comando en pgAdmin o psql:

```sql
CREATE TABLE file (
    id_file SERIAL PRIMARY KEY,
    id_source INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(100),
    main_url TEXT,
    path TEXT,
    type VARCHAR(50),
    specific_url TEXT,
    alternate_url TEXT,
    navigation_path TEXT,
    publication_frequency VARCHAR(50),
    priority INTEGER,
    state VARCHAR(50),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observations TEXT,
    updated_to VARCHAR(100),
    last_file_path TEXT,
    last_file_url TEXT,
    schedule_interval VARCHAR(100),
    publication_date VARCHAR(100),
    key_words TEXT,
    section_path TEXT,
    short_name VARCHAR(100),
    download_type VARCHAR(50)
);
```

## 🚀 Uso

### Ejecutar la aplicación

```bash
streamlit run src/app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
DBUpdater/
├── src/
│   ├── app.py                 # Aplicación principal
│   ├── config.py              # Configuración
│   ├── db_utils.py            # Utilidades de base de datos
│   └── pages/
│       ├── add_data.py        # Página de agregar datos
│       └── view_edit_data.py  # Página de ver y editar datos
├── requirements.txt           # Dependencias
├── .env.example              # Ejemplo de variables de entorno
├── .env                      # Variables de entorno (no versionar)
├── .gitignore               # Archivos a ignorar en git
└── README.md                # Este archivo
```

## 🔧 Configuración

### Campos de la Base de Datos

La aplicación maneja los siguientes campos:

- `id_file` - ID único (auto-increment)
- `id_source` - ID de fuente (requerido)
- `name` - Nombre del archivo (requerido)
- `code` - Código
- `main_url` - URL principal
- `path` - Ruta
- `type` - Tipo
- `specific_url` - URL específica
- `alternate_url` - URL alternativa
- `navigation_path` - Ruta de navegación
- `publication_frequency` - Frecuencia de publicación
- `priority` - Prioridad
- `state` - Estado
- `creation_date` - Fecha de creación (auto-generada)
- `update_date` - Fecha de actualización (auto-generada)
- `observations` - Observaciones
- `updated_to` - Actualizado a
- `last_file_path` - Última ruta de archivo
- `last_file_url` - Última URL de archivo
- `schedule_interval` - Intervalo de programación
- `publication_date` - Fecha de publicación
- `key_words` - Palabras clave
- `section_path` - Ruta de sección
- `short_name` - Nombre corto
- `download_type` - Tipo de descarga

## 📝 Notas

- Los campos `creation_date` y `update_date` se generan automáticamente
- La edición en línea requiere hacer doble clic en la celda
- Los campos `id_file`, `creation_date` y `update_date` no son editables
- La búsqueda es insensible a mayúsculas/minúsculas

## ⚠️ Troubleshooting

### Error de conexión a la base de datos
- Verifica que PostgreSQL esté corriendo
- Comprueba las credenciales en el archivo `.env`
- Asegúrate de que la base de datos existe

### Error de tabla no encontrada
- Ejecuta el script SQL para crear la tabla (ver sección de Instalación)

### Error al editar datos
- Verifica que tengas permisos de escritura en la base de datos
- Revisa los registros en el servidor PostgreSQL

## 📄 Licencia

Este proyecto es de uso privado.

## 👨‍💻 Autor

Desarrollado para gestión de datos en DBUpdater
# DB-Updater
