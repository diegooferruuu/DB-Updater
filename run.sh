#!/bin/bash

# DBUpdater Startup Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Iniciando DBUpdater...${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: Archivo .env no encontrado${NC}"
    echo -e "${YELLOW}Por favor, copia .env.example a .env y configura tus credenciales:${NC}"
    echo "cp .env.example .env"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}🔌 Activando entorno virtual...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}📥 Instalando dependencias...${NC}"
pip install -r requirements.txt -q

# Run Streamlit
echo -e "${GREEN}✅ Iniciando aplicación Streamlit${NC}"
echo -e "${YELLOW}💻 La aplicación estará disponible en: http://localhost:8501${NC}"
echo ""

streamlit run src/app.py
