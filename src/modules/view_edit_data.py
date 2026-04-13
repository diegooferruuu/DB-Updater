import streamlit as st
import pandas as pd
from datetime import datetime
from db_utils import get_db
from config import FIELD_DEFINITIONS, TABLE_NAME

def render_view_edit_page():
    """Render the page to view and edit data"""
    st.header("📊 Visualizar y Editar Datos")
    
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
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Display total records
    st.metric("Total de Registros", len(df))
    
    # Search functionality
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Buscar por nombre o código:")
    
    # Filter data if search term is provided
    if search_term:
        df = df[
            (df['name'].astype(str).str.contains(search_term, case=False, na=False)) |
            (df['code'].astype(str).str.contains(search_term, case=False, na=False))
        ]
    
    st.write(f"Mostrando {len(df)} registros")
    
    # Create editable data table
    st.subheader("📋 Tabla de Datos")
    st.write("💡 **Haz doble clic en cualquier celda para editar** (excepto ID y fechas)")
    
    # Display the dataframe with editor
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        key="data_editor",
        disabled=['id_file', 'creation_date', 'update_date'],  # Disable specific columns
    )
    
    # Check for changes and save them
    if not edited_df.equals(df):
        st.warning("⚠️ Detectamos cambios. Por favor, revisa y guarda.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Guardar Cambios", use_container_width=True):
                save_changes(df, edited_df)
        
        with col2:
            if st.button("🔄 Descartar", use_container_width=True):
                st.rerun()
    
    # Delete record functionality
    st.subheader("🗑️ Eliminar Registro")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_id = st.selectbox(
            "Selecciona un registro para eliminar:",
            options=df['id_file'].tolist(),
            format_func=lambda x: f"ID {x} - {df[df['id_file'] == x]['name'].values[0] if len(df[df['id_file'] == x]) > 0 else 'Unknown'}"
        )
    
    with col2:
        st.write("")  # Spacer
        if st.button("🗑️ Eliminar", use_container_width=True):
            delete_record(selected_id)


def save_changes(original_df, edited_df):
    """Save changes made to the dataframe"""
    db = get_db()
    
    if not db.connect():
        st.error("❌ No se pudo conectar a la base de datos")
        return
    
    try:
        # Find rows that were modified
        for idx, row in edited_df.iterrows():
            original_row = original_df.iloc[idx]
            record_id = row['id_file']
            
            # Check if any value changed (excluding id_file and dates)
            changed_fields = {}
            for col in edited_df.columns:
                if col not in ['id_file', 'creation_date', 'update_date']:
                    if str(original_row[col]) != str(row[col]):
                        changed_fields[col] = row[col]
            
            # Update if there are changes
            if changed_fields:
                success, message = db.update_record(record_id, changed_fields)
                if success:
                    st.success(f"✅ Registro {record_id} actualizado exitosamente")
                else:
                    st.error(f"❌ Error al actualizar registro {record_id}: {message}")
        
        db.disconnect()
        st.rerun()
    
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
