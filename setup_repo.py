import os
import urllib.request

INGEST_SCRIPT_URL = (
    "https://raw.githubusercontent.com/BexTuychiev/medium_stories/"
    "refs/heads/master/2024/9_september/3_neo4j_python/ingest_football_data.py"
)

GITIGNORE_CONTENT = """# Entornos virtuales
venv/
env/
.venv/

# Variables de entorno y credenciales (NUNCA subir a GitHub)
.env

# Archivos compilados de Python
__pycache__/
*.py[cod]
*$py.class

# Jupyter Notebooks
.ipynb_checkpoints/

# Datasets temporales
*.csv
"""

NEO4J_USERNAME="3c0dd928"
NEO4J_PASSWORD="x3isVAn1xSONM-i_28AjqahOLw_cUGXPpjBjib-i0sc"
NEO4J_URI="neo4j+s://Freeinstance.databases.neo4j.io"
NEO4J_CONNECTION_URI="neo4j+s://Freeinstance.databases.neo4j.io"




def writeFileIfNeeded(filePath, content, overwrite=False):
    if os.path.exists(filePath) and not overwrite:
        print(f"[OMITIDO] {filePath} ya existe (no se sobrescribió).")
        return
    with open(filePath, "w", encoding="utf-8") as fileObj:
        fileObj.write(content)
    print(f"[CREADO] {filePath}")


def downloadIngestScript(destPath="ingest_football_data.py"):
    if os.path.exists(destPath):
        print(f"[OMITIDO] {destPath} ya existe.")
        return
    try:
        print(f"Descargando {destPath} desde GitHub...")
        urllib.request.urlretrieve(INGEST_SCRIPT_URL, destPath)
        print(f"[DESCARGADO] {destPath}")
    except Exception as error:
        print(f"[ERROR] No se pudo descargar {destPath}: {error}")
        print(f"Puedes descargarlo manualmente desde: {INGEST_SCRIPT_URL}")


def main():
    print("=== Configurando archivos base del repositorio Neo4j ===\n")
    writeFileIfNeeded(".gitignore", GITIGNORE_CONTENT, overwrite=True)
    writeFileIfNeeded("requirements.txt", REQUIREMENTS_CONTENT, overwrite=True)
    writeFileIfNeeded(".env.example", ENV_TEMPLATE_CONTENT, overwrite=True)
    writeFileIfNeeded(".env", ENV_TEMPLATE_CONTENT, overwrite=False)
    downloadIngestScript()

    print("\n=== Siguientes pasos ===")
    print("1. Abre el archivo .env y coloca tus credenciales reales de Neo4j AuraDB.")
    print("2. Instala las dependencias: pip install -r requirements.txt")
    print("3. Carga los datos al grafo: python ingest_football_data.py")
    print("4. Ejecuta el análisis: python main.py")


if __name__ == "__main__":
    main()
