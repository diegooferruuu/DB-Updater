import streamlit as st
import pandas as pd
from datetime import datetime
from db_utils import get_db
from config import FIELD_DEFINITIONS, TABLE_NAME, FILTERABLE_COLUMNS, CONTROL_ESTADO_OPTIONS, TIPO_ERROR_OPTIONS

def render_view_edit_page():
    """Render the page to view and edit data"""
    st.header("📊 Visualizar y Editar Datos")
    
    # Initialize session state for hidden columns
    if 'hidden_columns' not in st.session_state:
        st.session_state.hidden_columns = []
    
    # Fetch data from database
    db = get_db()
    if db.connect():
        records = db.get_all_records()
        db.disconnect()
    else:
        st.error("❌ No se pudo conectar a la base de datos")
        return
    
    if not records:
        st.info("📭 No hay registros en la base de datos")
        return
    
    # Store original for filtering
    original_df = pd.DataFrame(records)
    df = original_df.copy()
    
    # Display total records
    st.metric("Total de Registros", len(df))
    
    # Advanced filters section
    with st.expander("🔍 Filtros Avanzados", expanded=False):
        st.subheader("Aplicar Filtros")
        
        filters = {}
        
        # Create filter inputs for each filterable column
        available_cols = [col for col in FILTERABLE_COLUMNS if col in df.columns]
        
        # Display filters in groups of 3 per row
        for batch_idx in range(0, len(available_cols), 3):
            batch_cols = available_cols[batch_idx:batch_idx+3]
            filter_cols = st.columns(3)
            
            for col_idx, col in enumerate(batch_cols):
                with filter_cols[col_idx]:
                    unique_values = df[col].dropna().unique()
                    
                    # For numerical columns, offer range filter
                    if len(unique_values) > 0 and (pd.api.types.is_numeric_dtype(df[col])):
                        min_val = df[col].min()
                        max_val = df[col].max()
                        
                        # Only show slider if min != max
                        if pd.notna(min_val) and pd.notna(max_val) and float(min_val) < float(max_val):
                            filter_range = st.slider(
                                f"Filtrar {col}",
                                float(min_val),
                                float(max_val),
                                (float(min_val), float(max_val)),
                                key=f"slider_{col}"
                            )
                            filters[col] = ('range', filter_range)
                        else:
                            # If all values are the same, show multiselect instead
                            selected_values = st.multiselect(
                                f"Filtrar {col}",
                                sorted(unique_values, key=str),
                                key=f"filter_{col}"
                            )
                            if selected_values:
                                filters[col] = ('value', selected_values)
                    else:
                        # For text columns, offer multi-select filter
                        selected_values = st.multiselect(
                            f"Filtrar {col}",
                            sorted(unique_values, key=str),
                            key=f"filter_{col}"
                        )
                        if selected_values:
                            filters[col] = ('value', selected_values)
        
        # Apply filters
        filtered_df = df.copy()
        for col, (filter_type, filter_value) in filters.items():
            if filter_type == 'range':
                filtered_df = filtered_df[
                    (filtered_df[col] >= filter_value[0]) & 
                    (filtered_df[col] <= filter_value[1])
                ]
            elif filter_type == 'value':
                filtered_df = filtered_df[filtered_df[col].isin(filter_value)]
        
        df = filtered_df
    
    # Search functionality
    st.subheader("🔎 Búsqueda Rápida")
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("Buscar por nombre o código:")
    
    # Filter data if search term is provided
    if search_term:
        df = df[
            (df['name'].astype(str).str.contains(search_term, case=False, na=False)) |
            (df['code'].astype(str).str.contains(search_term, case=False, na=False))
        ]
    
    st.write(f"**Mostrando {len(df)} registros** (de {len(original_df)} totales)")
    
    # Column visibility control
    with st.expander("👁️ Mostrar/Ocultar Columnas", expanded=False):
        col_options = st.columns(4)
        for idx, col in enumerate(df.columns):
            with col_options[idx % 4]:
                is_hidden = col in st.session_state.hidden_columns
                if st.checkbox(f"Mostrar {col}", value=not is_hidden, key=f"col_visibility_{col}"):
                    if col in st.session_state.hidden_columns:
                        st.session_state.hidden_columns.remove(col)
                else:
                    if col not in st.session_state.hidden_columns:
                        st.session_state.hidden_columns.append(col)
        
        if st.button("🔄 Mostrar Todas las Columnas"):
            st.session_state.hidden_columns = []
            st.rerun()
    
    # Remove hidden columns from view
    display_df = df.drop(columns=st.session_state.hidden_columns, errors='ignore')
    
    # Create editable data table
    st.subheader("📋 Tabla de Datos")
    st.write("💡 **Haz doble clic en cualquier celda para editar** (excepto ID y fechas)")
    
    # Display the dataframe with editor
    edited_df = st.data_editor(
        display_df,
        use_container_width=True,
        key="data_editor",
        disabled=['id_file', 'creation_date', 'update_date'],
    )
    
    # Merge back the hidden columns for full comparison
    edited_full_df = edited_df.copy()
    for col in st.session_state.hidden_columns:
        if col in df.columns:
            edited_full_df[col] = df[col]
    
    # Check for changes and save them
    if not edited_full_df.equals(df):
        st.warning("⚠️ Detectamos cambios. Por favor, revisa y guarda.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Guardar Cambios", use_container_width=True):
                save_changes(df, edited_full_df)
        
        with col2:
            if st.button("🔄 Descartar", use_container_width=True):
                st.rerun()
    
    # Delete record functionality
    # st.subheader("🗑️ Eliminar Registro")
    # col1, col2 = st.columns([3, 1])
    
    # with col1:
    #     selected_id = st.selectbox(
    #         "Selecciona un registro para eliminar:",
    #         options=df['id_file'].tolist(),
    #         format_func=lambda x: f"ID {x} - {df[df['id_file'] == x]['name'].values[0] if len(df[df['id_file'] == x]) > 0 else 'Unknown'}"
    #     )
    
    # with col2:
    #     st.write("")  # Spacer
    #     if st.button("🗑️ Eliminar", use_container_width=True):
    #         delete_record(selected_id)


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


def save_changes(original_df, edited_df):
    """Save changes made to the dataframe with validation"""
    db = get_db()
    
    if not db.connect():
        st.error("❌ No se pudo conectar a la base de datos")
        return
    
    try:
        validation_errors = {}
        successful_updates = 0
        
        # Find rows that were modified and validate
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            record_id = row['id_file']
            
            changed_fields = {}
            for col in edited_df.columns:
                if col not in ['id_file', 'creation_date', 'update_date']:
                    if str(original_row[col]) != str(row[col]):
                        # Validate the field
                        is_valid, error_msg = validate_field(col, row[col])
                        if not is_valid:
                            if record_id not in validation_errors:
                                validation_errors[record_id] = []
                            validation_errors[record_id].append(f"{col}: {error_msg}")
                        else:
                            changed_fields[col] = row[col]
            
            # Update if there are valid changes and no errors
            if changed_fields and record_id not in validation_errors:
                success, message = db.update_record(record_id, changed_fields)
                if success:
                    successful_updates += 1
                    st.success(f"✅ Registro {record_id} actualizado exitosamente")
                else:
                    st.error(f"❌ Error al actualizar registro {record_id}: {message}")
        
        # Display validation errors if any
        if validation_errors:
            st.error("⚠️ Errores de validación encontrados:")
            for record_id, errors in validation_errors.items():
                with st.expander(f"Registro {record_id}"):
                    for error in errors:
                        st.error(f"• {error}")
        
        db.disconnect()
        
        if successful_updates > 0 and not validation_errors:
            st.rerun()
        elif successful_updates > 0 and validation_errors:
            st.info(f"⚠️ {successful_updates} registros se actualizaron, pero hay errores en otros.")
    
    except Exception as e:
        st.error(f"❌ Error al guardar cambios: {str(e)}")
        db.disconnect()


def delete_record(record_id):
    """Delete a record from the database"""
    db = get_db()
    
    if not db.connect():
        st.error("❌ No se pudo conectar a la base de datos")
        return
    
    success, message = db.delete_record(record_id)
    db.disconnect()
    
    if success:
        st.success(f"✅ Registro {record_id} eliminado exitosamente")
        st.rerun()
    else:
        st.error(f"❌ Error al eliminar registro: {message}")


if __name__ == "__main__":
    render_view_edit_page()
