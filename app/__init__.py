from flask import Flask, jsonify
import sys

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status' : 'error', 'message' : "Page found, but we'll not show you"}), 404

@app.errorhandler(405)
def wrong_http(error):
    return jsonify({'status' : 'error', 'message' : 'wrong HTTP method used'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status' : 'error', 'message' : "Server is smoking hot!"}), 500


from app.blogs.controller import api as blogs_api
app.register_blueprint(blogs_api)
