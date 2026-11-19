def getGraphOverview(dbConn):
    """Devuelve el conteo de nodos por etiqueta y relaciones por tipo."""
    nodesQuery = """
    MATCH (n)
    UNWIND labels(n) AS nodeLabel
    RETURN nodeLabel, count(*) AS totalNodes
    ORDER BY totalNodes DESC
    """
    relsQuery = """
    MATCH ()-[r]->()
    RETURN type(r) AS relationshipType, count(*) AS totalRelationships
    ORDER BY totalRelationships DESC
    """
    nodesDf = dbConn.executeToDataFrame(nodesQuery)
    relsDf = dbConn.executeToDataFrame(relsQuery)
    return nodesDf, relsDf


def getTopScorers(dbConn, limit=10):
    """Top goleadores históricos en todos los partidos."""
    query = """
    MATCH (p:Player)-[s:SCORED_IN]->(m:Match)
    WHERE coalesce(s.own_goal, false) = false
    RETURN p.name AS playerName, count(s) AS totalGoals
    ORDER BY totalGoals DESC
    LIMIT $limit
    """
    return dbConn.executeToDataFrame(query, {"limit": limit})


def getTournamentTopScorers(dbConn, tournamentName="FIFA World Cup", limit=10):
    """Top goleadores filtrados por un torneo específico."""
    query = """
    MATCH (p:Player)-[s:SCORED_IN]->(m:Match)-[:PART_OF]->(t:Tournament {name: $tournamentName})
    WHERE coalesce(s.own_goal, false) = false
    RETURN p.name AS playerName, t.name AS tournament, count(s) AS totalGoals
    ORDER BY totalGoals DESC
    LIMIT $limit
    """
    return dbConn.executeToDataFrame(
        query,
        {"tournamentName": tournamentName, "limit": limit},
    )


def getLateMinuteGoals(dbConn, minuteThreshold=90, limit=10):
    """Jugadores con más goles anotados a partir de un minuto específico."""
    query = """
    MATCH (p:Player)-[s:SCORED_IN]->(m:Match)
    WHERE s.minute >= $minuteThreshold AND coalesce(s.own_goal, false) = false
    RETURN p.name AS playerName, count(s) AS lateGoals
    ORDER BY lateGoals DESC
    LIMIT $limit
    """
    return dbConn.executeToDataFrame(
        query,
        {"minuteThreshold": minuteThreshold, "limit": limit},
    )


def getPenaltyScorers(dbConn, limit=10):
    """Jugadores con más goles anotados de penal."""
    query = """
    MATCH (p:Player)-[s:SCORED_IN {penalty: true}]->(m:Match)
    RETURN p.name AS playerName, count(s) AS penaltyGoals
    ORDER BY penaltyGoals DESC
    LIMIT $limit
    """
    return dbConn.executeToDataFrame(query, {"limit": limit})


def getOwnGoalLeaders(dbConn, limit=10):
    """Jugadores con más autogoles registrados."""
    query = """
    MATCH (p:Player)-[s:SCORED_IN {own_goal: true}]->(m:Match)
    RETURN p.name AS playerName, count(s) AS ownGoals
    ORDER BY ownGoals DESC
    LIMIT $limit
    """
    return dbConn.executeToDataFrame(query, {"limit": limit})


def getMatchesByTournament(dbConn, limit=10):
    """Torneos con mayor cantidad de partidos registrados."""
    query = """
    MATCH (m:Match)-[:PART_OF]->(t:Tournament)
    RETURN t.name AS tournamentName, count(m) AS totalMatches
    ORDER BY totalMatches DESC
    LIMIT $limit
    """
    return dbConn.executeToDataFrame(query, {"limit": limit})
