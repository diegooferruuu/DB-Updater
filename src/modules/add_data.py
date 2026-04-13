import streamlit as st
from datetime import datetime
from db_utils import get_db
from config import FIELD_DEFINITIONS, TABLE_NAME

def render_add_data_page():
    """Render the form to add new data"""
    st.header("➕ Agregar Nuevo Registro")
    
    with st.form("add_record_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        form_data = {}
        
        # Render form fields based on configuration
        with col1:
            for field_idx, (field_name, field_config) in enumerate(FIELD_DEFINITIONS.items()):
                # Skip id_file (auto-increment) and timestamp fields
                if field_name in ['id_file', 'creation_date', 'update_date']:
                    continue
                
                # Render only odd-indexed fields in first column
                if field_idx % 2 == 1:
                    render_field(field_name, field_config, form_data)
        
        with col2:
            for field_idx, (field_name, field_config) in enumerate(FIELD_DEFINITIONS.items()):
                # Skip id_file (auto-increment) and timestamp fields
                if field_name in ['id_file', 'creation_date', 'update_date']:
                    continue
                
                # Render only even-indexed fields in second column
                if field_idx % 2 == 0:
                    render_field(field_name, field_config, form_data)
        
        # Submit button
        submitted = st.form_submit_button("💾 Guardar Registro", use_container_width=True)
        
        if submitted:
            # Validate required fields
            required_fields = {k: v for k, v in FIELD_DEFINITIONS.items() 
                             if v.get('required', False) and k not in ['id_file', 'creation_date', 'update_date']}
            
            missing_fields = []
            for field in required_fields:
                if field not in form_data or form_data[field] == '' or form_data[field] is None:
                    missing_fields.append(field)
            
            if missing_fields:
                st.error(f"❌ Campos requeridos faltantes: {', '.join(missing_fields)}")
            else:
                # Insert the record
                db = get_db()
                if db.connect():
                    success, result = db.insert_record(form_data)
                    db.disconnect()
                    
                    if success:
                        st.success(f"✅ Registro guardado exitosamente con ID: {result}")
                        st.rerun()
                    else:
                        st.error(f"❌ Error al guardar el registro: {result}")
                else:
                    st.error("❌ No se pudo conectar a la base de datos")


def render_field(field_name, field_config, form_data):
    """Render a single form field based on its configuration"""
    field_type = field_config.get('type', 'string')
    required = field_config.get('required', False)
    label = field_name.replace('_', ' ').title()
    
    if required:
        label += " *"
    
    if field_type == 'integer':
        value = st.number_input(label, value=None, step=1, key=f"input_{field_name}")
        if value is not None:
            form_data[field_name] = value
    
    elif field_type == 'datetime':
        value = st.date_input(label, value=None, key=f"input_{field_name}")
        if value is not None:
            form_data[field_name] = value
    
    elif field_type == 'string':
        value = st.text_input(label, key=f"input_{field_name}")
        if value:
            form_data[field_name] = value
    
    elif field_type == 'text':
        value = st.text_area(label, key=f"input_{field_name}")
        if value:
            form_data[field_name] = value


if __name__ == "__main__":
    render_add_data_page()
