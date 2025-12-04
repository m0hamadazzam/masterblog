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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
