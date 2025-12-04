from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def post_posts():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no post submitted"}), 400

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "title and content must be submitted"}), 400

    if len(POSTS) == 0:
        new_id = 1
    else:
        new_id = max(post["id"] for post in POSTS) + 1

    post = {
        "id": new_id,
        "title": title,
        "content": content
    }

    POSTS.append(post)
    return jsonify(post), 201

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = next((post for post in POSTS if post["id"] == id), None)
    print(post)

    if not post:
        return jsonify({"error": "post with id {} not found".format(id)}), 404
    POSTS.remove(post)

    return jsonify({"message": "Post with id {} has been deleted successfully.".format(id)}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "no update data provided"}), 400

    post = next((post for post in POSTS if post["id"] == id), None)
    if not post:
        return jsonify({"error": "post with id {} not found".format(id)}), 404

    if "title" in data:
        post["title"] = data["title"]
    if "content" in data:
        post["content"] = data["content"]

    return jsonify(post), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get("title", "").lower()
    content = request.args.get("content", "").lower()
    search_results = []

    for post in POSTS:
        found = False
        if title:
            if title in post["title"].lower():
                found = True
        if content:
            if content in post["content"].lower():
                found = True
        if found:
            search_results.append(post)

    return jsonify(search_results), 200





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
