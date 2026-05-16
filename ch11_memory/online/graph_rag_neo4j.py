"""
graph_rag_neo4j.py — Knowledge Graph RAG with Neo4j.

Vector search answers "what is semantically similar?" — it cannot answer
"who funds the project Bob works on?" without the relationship chain being
encoded somewhere in the embedding. Knowledge graphs store that chain
explicitly, and a single Cypher query traverses it in milliseconds.

This script:
1. Connects to a local Neo4j instance
2. Ingests a small org-chart dataset (people, projects, orgs)
3. Queries it with multi-hop Cypher — the kind of question that breaks
   flat vector search

Prerequisites:
    docker run -p 7474:7474 -p 7687:7687 \
        -e NEO4J_AUTH=neo4j/password neo4j:latest

    pip install langchain-community neo4j

Usage:
    python graph_rag_neo4j.py
"""

from langchain_community.graphs import Neo4jGraph

NEO4J_URL = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"


def connect() -> Neo4jGraph:
    return Neo4jGraph(url=NEO4J_URL, username=NEO4J_USER, password=NEO4J_PASSWORD)


def ingest(graph: Neo4jGraph):
    """Load a minimal org-chart into the graph."""
    graph.query("MATCH (n) DETACH DELETE n")  # Clear previous runs

    graph.query("""
    CREATE
      (alice:Person {name: "Alice", role: "VP Engineering"}),
      (bob:Person   {name: "Bob",   role: "Engineer"}),
      (carol:Person {name: "Carol", role: "Engineer"}),
      (atlas:Project    {name: "Atlas",    status: "active"}),
      (nexus:Project    {name: "Nexus",    status: "archived"}),
      (acme:Organization  {name: "Acme Corp",  type: "funder"}),
      (horizon:Organization {name: "Horizon VC", type: "funder"}),

      (alice)-[:MANAGES]->(bob),
      (alice)-[:MANAGES]->(carol),
      (bob)-[:WORKS_ON]->(atlas),
      (carol)-[:WORKS_ON]->(nexus),
      (acme)-[:FUNDS]->(atlas),
      (horizon)-[:FUNDS]->(nexus)
    """)
    print("Graph ingested: 3 people, 2 projects, 2 orgs\n")


def get_entity_context(graph: Neo4jGraph, entity_name: str) -> list[dict]:
    """Return all nodes within 2 hops of a named entity."""
    return graph.query(
        """
        MATCH (e {name: $name})-[r*1..2]-(connected)
        RETURN e.name AS source,
               [rel IN r | type(rel)] AS relationship_path,
               connected.name AS target,
               labels(connected)[0] AS target_type
        LIMIT 25
        """,
        params={"name": entity_name},
    )


def who_funds_project_of(graph: Neo4jGraph, person_name: str) -> list[dict]:
    """
    Answer: "Which organization funds the project that <person> works on?"

    A vector search would return paragraphs about funding and projects.
    This Cypher query answers it exactly in one traversal.
    """
    return graph.query(
        """
        MATCH (p:Person {name: $name})-[:WORKS_ON]->(proj:Project)
              <-[:FUNDS]-(org:Organization)
        RETURN p.name AS person, proj.name AS project, org.name AS funder
        """,
        params={"name": person_name},
    )


def main():
    print("Connecting to Neo4j...")
    graph = connect()

    print("Ingesting org-chart data...")
    ingest(graph)

    print("Query 1: What is within 2 hops of Bob?")
    context = get_entity_context(graph, "Bob")
    for row in context:
        path = " → ".join(row["relationship_path"])
        print(f"  {row['source']} --[{path}]--> {row['target']} ({row['target_type']})")

    print("\nQuery 2: Who funds the project Bob works on?")
    funding = who_funds_project_of(graph, "Bob")
    for row in funding:
        print(f"  {row['person']} → {row['project']} ← funded by {row['funder']}")

    print("\nQuery 3: Same question for Carol")
    funding = who_funds_project_of(graph, "Carol")
    for row in funding:
        print(f"  {row['person']} → {row['project']} ← funded by {row['funder']}")

    print(
        "\nThese answers require traversing two relationship hops. "
        "A vector search over the same data would return paragraphs "
        "about funding in general — not the specific funder."
    )


if __name__ == "__main__":
    main()
