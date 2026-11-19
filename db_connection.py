import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase


class Neo4jConnection:
    """Administra la conexión y ejecución de consultas Cypher en Neo4j AuraDB."""

    def __init__(self):
        load_dotenv()
        self.neo4jUser = os.getenv("3c0dd928")
        self.neo4jPass = os.getenv("x3isVAn1xSONM-i_28AjqahOLw_cUGXPpjBjib-i0sc")
        self.neo4jUri = os.getenv("NEO4J_URI") or os.getenv("NEO4J_CONNECTION_URI")

        if not all([self.neo4jUser, self.neo4jPass, self.neo4jUri]):
            raise ValueError(
                "Faltan credenciales en el archivo .env. "
                "Verifica NEO4J_USERNAME, NEO4J_PASSWORD y NEO4J_URI."
            )

        if "TU_INSTANCIA_AQUI" in self.neo4jUri or "TU_PASSWORD_AQUI" in self.neo4jPass:
            raise ValueError(
                "Aún tienes los valores de ejemplo en .env. "
                "Reemplázalos con tus credenciales reales de Neo4j AuraDB."
            )

        self.driver = GraphDatabase.driver(
            self.neo4jUri,
            auth=(self.neo4jUser, self.neo4jPass),
        )

    def verifyConnection(self):
        self.driver.verify_connectivity()
        return True

    def executeToDataFrame(self, cypherQuery, params=None):
        """Ejecuta una consulta Cypher y devuelve los resultados como DataFrame de pandas."""
        records, _, _ = self.driver.execute_query(
            cypherQuery,
            parameters_=params or {},
        )
        dataRows = [record.data() for record in records]
        return pd.DataFrame(dataRows)

    def close(self):
        """Cierra el driver y libera recursos."""
        if self.driver:
            self.driver.close()

    def __enter__(self):
        return self

    def __exit__(self, excType, excVal, excTb):
        self.close()
