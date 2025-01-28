from pymongo import MongoClient

def get_mongo_connection():
    """
    Estabelece uma conexão com o MongoDB local e retorna a coleção 'movies'.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["movie_catalog"]
    return db["movies"]
