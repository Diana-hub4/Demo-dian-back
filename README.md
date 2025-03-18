# Demo-dian-back

## ejecucion: 

### Crear entorno virtual
python -m venv venv

### Activar entorno
* En Windows:
venv\Scripts\activate


* En Linux/macOS:
source venv/bin/activate

## Instalar dependencias en entorno virtual
pip install -r requirements.txt


## Iniciar aplicacion 
uvicorn src.main:app --reload
