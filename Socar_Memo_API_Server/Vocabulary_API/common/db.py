from pymongo import MongoClient

_db_config = None


def init(app):
    global _db_config
    global close_connection

    _db_config = app.config["DATABASE"]
    close_connection = app.teardown_appcontext(close_connection)
    if get_db() == None:
        create_db()


def _db_connect():
    if _db_config is None:
        raise Exception("Call init first")  # or whatever error you want
    my_client = MongoClient(_db_config)
    return my_client


def create_db():
    client = _db_connect()
    client["Hackerton_Memo"]


def get_db():
    client = _db_connect()

    if "Hackerton_Memo" not in client.list_database_names():
        return None
    db = client.Hackerton_Memo
    # collection = db.mongoTest
    # results = collection.find()
    return db


def close_connection(client):
    if client != None:
        client.close()


def create_collection(collection_name: str):
    if collection_name in db.list_collection_names():
        return None

    db = get_db()
    db[collection_name]
