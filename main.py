from db_connection import Neo4jConnection
from queries import (
    getGraphOverview,
    getLateMinuteGoals,
    getMatchesByTournament,
    getOwnGoalLeaders,
    getPenaltyScorers,
    getTopScorers,
    getTournamentTopScorers,
)


def printSection(title, dataFrame):
    print(f"\n{'=' * 55}")
    print(f" {title}")
    print(f"{'=' * 55}")
    if dataFrame.empty:
        print("Sin resultados (verifica si ya ejecutaste ingest_football_data.py).")
    else:
        print(dataFrame.to_string(index=False))


def main():
    try:
        with Neo4jConnection() as dbConn:
            dbConn.verifyConnection()
            print("¡Conexión exitosa a Neo4j AuraDB!")

            nodesDf, relsDf = getGraphOverview(dbConn)
            printSection("Resumen de Nodos en el Grafo", nodesDf)
            printSection("Resumen de Relaciones en el Grafo", relsDf)

            topScorersDf = getTopScorers(dbConn, limit=10)
            printSection("Top 10 Goleadores Históricos", topScorersDf)

            worldCupScorersDf = getTournamentTopScorers(
                dbConn, tournamentName="FIFA World Cup", limit=10
            )
            printSection("Top 10 Goleadores en FIFA World Cup", worldCupScorersDf)

            lateGoalsDf = getLateMinuteGoals(dbConn, minuteThreshold=90, limit=10)
            printSection("Top 10 Goleadores en el Minuto 90+", lateGoalsDf)

            penaltyDf = getPenaltyScorers(dbConn, limit=10)
            printSection("Top 10 Goleadores de Penal", penaltyDf)

            ownGoalsDf = getOwnGoalLeaders(dbConn, limit=5)
            printSection("Top 5 Autogoles", ownGoalsDf)

            tournamentsDf = getMatchesByTournament(dbConn, limit=10)
            printSection("Top 10 Torneos con Más Partidos", tournamentsDf)

    except Exception as error:
        print(f"\n[ERROR] {error}")


if __name__ == "__main__":
    main()
