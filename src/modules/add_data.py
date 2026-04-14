import streamlit as st
from datetime import datetime
from db_utils import get_db
from config import FIELD_DEFINITIONS, TABLE_NAME, CONTROL_ESTADO_OPTIONS, TIPO_ERROR_OPTIONS

def validate_field(field_name, value):
    """Validate a field using the validator if available"""
    if field_name not in FIELD_DEFINITIONS:
        return True, None
    
    field_config = FIELD_DEFINITIONS[field_name]
    
    # Check required
    if field_config.get('required', False):
        if value is None or str(value).strip() == '':
            return False, f"{field_name} es requerido"
    
    # Check validator
    if 'validator' in field_config:
        validator = field_config['validator']
        is_valid, error_msg = validator(value)
        if not is_valid:
            return False, error_msg
    
    return True, None


def render_add_data_page():
    """Render the form to add new data"""
    st.header("➕ Agregar Nuevo Registro")
    
    # Information about required fields
    st.info("ℹ️ Los campos marcados con * son requeridos")
    
    with st.form("add_record_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        form_data = {}
        field_errors = {}
        
        # Render form fields based on configuration
        with col1:
            for field_idx, (field_name, field_config) in enumerate(FIELD_DEFINITIONS.items()):
                # Skip id_file (auto-increment) and timestamp fields
                if field_name in ['id_file', 'creation_date', 'update_date']:
                    continue
                
                # Render only odd-indexed fields in first column
                if field_idx % 2 == 1:
                    error = render_field(field_name, field_config, form_data)
                    if error:
                        field_errors[field_name] = error
        
        with col2:
            for field_idx, (field_name, field_config) in enumerate(FIELD_DEFINITIONS.items()):
                # Skip id_file (auto-increment) and timestamp fields
                if field_name in ['id_file', 'creation_date', 'update_date']:
                    continue
                
                # Render only even-indexed fields in second column
                if field_idx % 2 == 0:
                    error = render_field(field_name, field_config, form_data)
                    if error:
                        field_errors[field_name] = error
        
        # Submit button
        submitted = st.form_submit_button("💾 Guardar Registro", use_container_width=True)
        
        if submitted:
            # Validate all fields
            validation_errors = {}
            
            for field_name, field_config in FIELD_DEFINITIONS.items():
                if field_name in ['id_file', 'creation_date', 'update_date']:
                    continue
                
                value = form_data.get(field_name)
                is_valid, error_msg = validate_field(field_name, value)
                
                if not is_valid:
                    validation_errors[field_name] = error_msg
            
            if validation_errors:
                st.error("❌ Errores de validación encontrados:")
                for field, error in validation_errors.items():
                    st.error(f"  • {field}: {error}")
            else:
                # Insert the record
                db = get_db()
                if db.connect():
                    success, result = db.insert_record(form_data)
                    db.disconnect()
                    
                    if success:
                        st.success(f"✅ Registro guardado exitosamente con ID: {result}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Error al guardar el registro: {result}")
                else:
                    st.error("❌ No se pudo conectar a la base de datos")


def render_field(field_name, field_config, form_data):
    """Render a single form field based on its configuration
    Returns error message if any validation error"""
    field_type = field_config.get('type', 'string')
    required = field_config.get('required', False)
    label = field_name.replace('_', ' ').title()
    
    if required:
        label += " *"
    
    error_message = None
    
    # Special handling for control_estado
    if field_name == 'control_estado':
        value = st.selectbox(label, options=[''] + CONTROL_ESTADO_OPTIONS, key=f"input_{field_name}")
        if value:
            form_data[field_name] = value
    
    # Special handling for tipo_error
    elif field_name == 'tipo_error':
        value = st.selectbox(label, options=[''] + TIPO_ERROR_OPTIONS, key=f"input_{field_name}")
        if value:
            form_data[field_name] = value
    
    elif field_type == 'integer':
        value = st.number_input(label, value=None, step=1, key=f"input_{field_name}")
        if value is not None:
            is_valid, error = validate_field(field_name, value)
            if not is_valid:
                st.error(f"❌ {error}")
                error_message = error
            form_data[field_name] = value
    
    elif field_type == 'datetime':
        value = st.date_input(label, value=None, key=f"input_{field_name}")
        if value is not None:
            form_data[field_name] = value
    
    elif field_type == 'string':
        value = st.text_input(label, key=f"input_{field_name}", help=f"Ingresa {label.lower()}")
        if value:
            is_valid, error = validate_field(field_name, value)
            if not is_valid:
                st.error(f"❌ {error}")
                error_message = error
            form_data[field_name] = value
    
    elif field_type == 'text':
        value = st.text_area(label, key=f"input_{field_name}", help=f"Ingresa {label.lower()}")
        if value:
            is_valid, error = validate_field(field_name, value)
            if not is_valid:
                st.error(f"❌ {error}")
                error_message = error
            form_data[field_name] = value
    
    return error_message


if __name__ == "__main__":
    render_add_data_page()
