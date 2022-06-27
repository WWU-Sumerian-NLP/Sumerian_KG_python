from json import dumps
from flask import (
    Flask,
    g, 
    request,
    Response
)

from neo4j import(
    GraphDatabase,
    basic_auth
)

app = Flask(__name__, static_url_path="/static/")

url = "bolt://localhost:7687"
username = "neo4j"
password = "password"
neo4j_version = "4.4.5"
database = "neo4j"
port = "8080"

driver = GraphDatabase.driver(url, auth=basic_auth(username, password))

def get_db():
    if not hasattr(g, "neo4j_db"):
        if neo4j_version.startswith("4"):
            g.neo4j_db = driver.session(database=database)
        else:
            g.neo4j_db = driver.session()
    return g.neo4j_db 

@app.route("/")
def get_index():
    return app.send_static_file("index.html")

def serialize_person(person):
    return {
        "id": person["id"],
        "name": person["name"]
    }

def serialize_animal(animal):
    print(animal[2] == None)
    return {
        "person": animal[0],
        "del": animal[1],
        "name": animal[2]
    }

@app.route("/graph")
def get_graph():
    def work(tx):
        return list(tx.run(
            "MATCH (a:Animal)<-[:deliveredBy]-(p:Person) Return p.name as personName, collect(a.name) as animalName"
        ))
    db = get_db()
    results = db.read_transaction(work)
    # print(results)
    nodes = []
    rels = []
    i = 0
    for record in results: 
        nodes.append({"person": record["personName"], "label": "person"})
        target = i 
        i += 1
        for name in record["animalName"]:
            animal = {"name": name, "label": "animal"}
        try: 
            source = nodes.index(animal) #find duplicates
        except ValueError:
            nodes.append(animal)
            source = i 
            i += 1
        rels.append({"source": source, "target": target})
    return Response(dumps({"nodes": nodes, "links": rels}),
                    mimetype="application/json")

    
@app.route("/search")
def get_search():
    def work(tx, q_):
        return list(tx.run(
            "MATCH(person:Person) WHERE toLower(person.name) CONTAINS toLower($name) Return person LIMIT 1",
            {"name": q_}
        ))
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        db = get_db()
        results = db.read_transaction(work, q)
        return Response(
            dumps([serialize_person(record["person"]) for record in results]),
            mimetype="application/json"
        )

@app.route("/person/<personName>")
def get_person(personName):
    def work(tx, personName_):
        return tx.run(
            "MATCH(person:Person {name:$personName})"
            "OPTIONAL MATCH (person)<-[r]-(animal:Animal)"
            "RETURN person.name as personName, COLLECT([person.name, HEAD(SPLIT(TOLOWER(TYPE(r)), '_')), animal.name]) as cast",
            {"personName": personName_}
        ).single()
    
    db = get_db()
    result = db.read_transaction(work, personName)
    print(result)
    return Response(dumps({"personName": result["personName"],
                    "animals": [serialize_animal(animal)
                                for animal in result["cast"] if animal[2] != None]}),
                    mimetype="application/json")


if __name__ == "__main__":
    app.run(port=port)

    