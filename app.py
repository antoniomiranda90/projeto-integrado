from flask import Flask, jsonify, request 
from mongo_client import get_mongo_connection 
from omdb_client import fetch_movie 
 
app = Flask(__name__) 
movies_collection = get_mongo_connection() 
 
@app.route("/movies", methods=["GET"])
def get_movies():
    movies = list(movies_collection.find({}, {"_id": 0})) 
    return jsonify(movies) 
 
@app.route("/movies", methods=["POST"])
def add_movie(): 
    """ 
    Adiciona um novo filme ao MongoDB usando a OMDb API. 
    """ 
    data = request.get_json() 
    title = data.get("title") 
    if not title: 
        return jsonify({"error": "O campo 'title' é obrigatório."}), 400 
 
    movie = fetch_movie(title) 
    if not movie: 
        return jsonify({"error": "Filme não encontrado na OMDb API."}), 404 
 
    movies_collection.insert_one(movie) 
    return jsonify({"message": "Filme adicionado com sucesso!", "movie": movie}) 

@app.route("/all-movies", methods=["GET"])

def get_all_movies():
    """
    Retorna todos os filmes adicionados ao banco de dados.
    """
    movies = list(movies_collection.find({}, {"_id": 0}))
    return jsonify({"total_movies": len(movies), "movies": movies})

@app.route("/group-stats", methods=["GET"])
def get_group_stats():
    """
    Exibe estatísticas dos filmes do grupo.
    """
    total_movies = movies_collection.count_documents({})
    avg_rating = movies_collection.aggregate([
    {"$group": {"_id": None, "average": {"$avg": {"$toDouble":
    "$imdb_rating"}}}}])
    avg_rating = next(avg_rating, {}).get("average", 0)
    return jsonify({"total_movies": total_movies, "average_rating": round(avg_rating, 2)})

if __name__ == "__main__": 
    app.run(host='127.0.0.1', port=9000, debug=True)