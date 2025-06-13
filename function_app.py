import azure.functions as func
import logging
import os
import json
from azure.cosmos import CosmosClient, PartitionKey

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="logToCosmos")
def logToCosmos(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    url = os.environ["COSMOS_DB_URL"]
    key = os.environ["COSMOS_DB_KEY"]
    database_name = "demo-db"
    container_name = "demo-container"

    client = CosmosClient(url, credential=key)

    # Datenbank erstellen oder holen
    db = client.create_database_if_not_exists(id=database_name)

    # Container erstellen oder holen (ohne offer_throughput wegen Serverless!)
    container = db.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/id")
    )

    # Beispiel-Dokument
    item = {
        "id": "1",
        "name": "Youssef",
        "role": "Azure Demo",
        "verified": True
    }

    # Dokument einfügen
    container.upsert_item(item)

    # Alles ausgeben
    output = ""
    for item in container.read_all_items():
        output += json.dumps(item) + "\n"

    return func.HttpResponse(f"📦 Cosmos DB Inhalte:\n{output}", mimetype="text/plain")
