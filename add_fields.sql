-- Agregar nuevos campos a la tabla file
-- Ejecutar esto si ya existe la tabla

-- Agregar campo responsable
ALTER TABLE file ADD COLUMN IF NOT EXISTS responsable VARCHAR(255);

-- Agregar campo estado de control (Activo, Inactivo, En Revisión, etc)
ALTER TABLE file ADD COLUMN IF NOT EXISTS control_estado VARCHAR(50);

-- Agregar campo tipo de error (para tracking de problemas)
ALTER TABLE file ADD COLUMN IF NOT EXISTS tipo_error VARCHAR(100);

-- Agregar campo display_name (nombre para mostrar)
ALTER TABLE file ADD COLUMN IF NOT EXISTS display_name VARCHAR(255);

-- Crear índices para mejor rendimiento en búsquedas
CREATE INDEX IF NOT EXISTS idx_file_responsable ON file(responsable);
CREATE INDEX IF NOT EXISTS idx_file_control_estado ON file(control_estado);
CREATE INDEX IF NOT EXISTS idx_file_tipo_error ON file(tipo_error);
CREATE INDEX IF NOT EXISTS idx_file_display_name ON file(display_name);

-- Verificar que se crearon las columnas
-- SELECT column_name FROM information_schema.columns WHERE table_name = 'file';
