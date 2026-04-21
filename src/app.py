import streamlit as st
from modules import add_data, view_edit_data
from config import APP_TITLE, APP_DESCRIPTION

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    h1 {
        color: #1f77b4;
    }
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🗂️ Menú de Navegación")
    page = st.radio(
        "Selecciona una sección:",
        ["📊 Ver y Editar Datos"], #"➕ Agregar Datos", 
        key="page_selector"
    )
    
    st.divider()
    
    st.markdown("""
    ### ℹ️ Información
    - **Aplicación**: DBUpdater
    - **Base de Datos**: PostgreSQL
    - **Tecnología**: Streamlit
    """)

# Main content
st.title(APP_TITLE)
st.write(APP_DESCRIPTION)

st.divider()

# Route to the selected page

if page == "📊 Ver y Editar Datos":
    view_edit_data.render_view_edit_page()
# elif page == "➕ Agregar Datos":
#     add_data.render_add_data_page()
