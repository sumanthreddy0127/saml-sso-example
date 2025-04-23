# from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
# import json
# import os
#
#
# class CustomHandler(SimpleHTTPRequestHandler):
#     # def do_GET(self):
#     #     # Remove the leading slash and construct the file path
#     #     file_path = os.path.join('app', self.path.lstrip('/'))
#     #     # Ensure the file path is relative to the 'app' directory
#     #     try:
#     #         with open(file_path, 'rb') as file:
#     #             self.send_response(200)
#     #             self.send_header('Content-type', self.get_content_type(file_path))
#     #             self.end_headers()
#     #             self.wfile.write(file.read())
#     #     except FileNotFoundError:
#     #         self.send_error(404, f'File not found: {self.path}')
#
#     def do_GET(self):
#         # Serve files from the current directory (or a specific folder)
#         return super().do_GET()
#
#     def get_content_type(self, path):
#         if path.endswith('.html'):
#             return 'text/html'
#         elif path.endswith('.css'):
#             return 'text/css'
#         elif path.endswith('.js'):
#             return 'application/javascript'
#         elif path.endswith('.json'):
#             return 'application/json'
#         elif path.endswith('.png'):
#             return 'image/png'
#         elif path.endswith('.jpg') or path.endswith('.jpeg'):
#             return 'image/jpeg'
#         elif path.endswith('.gif'):
#             return 'image/gif'
#         else:
#             return 'application/octet-stream'  # Default for unknown types
#
#     def do_POST(self):
#         # Set CORS headers
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
#         self.send_header('Access-Control-Allow-Headers', 'Content-Type')
#
#         # Read the length of the data
#         content_length = int(self.headers['Content-Length'])
#
#         # Read the POST data
#         post_data = self.rfile.read(content_length).decode('utf-8')
#
#         # Print the posted data
#         print(f"Received POST data: {post_data}")
#
#         # Create a response
#         response = {
#             'message': 'Data received',
#             'data': post_data
#         }
#
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps(response).encode('utf-8'))
#
# def run(server_class=HTTPServer, handler_class=CustomHandler):
#     server_address = ('', 8086)  # Serve on all interfaces at port 8086
#     httpd = server_class(server_address, handler_class)
#     print('Starting server...')
#     httpd.serve_forever()
#
#
# if __name__ == '__main__':
#     run()
#
#
# from flask import Flask, request, jsonify
# import os
#
# app = Flask(__name__)
#
#
# @app.route('/', methods=['GET'])
# def serve_file():
#     # Serve files from the current directory or a specific folder
#     return "Welcome to the server! Use /upload to POST data."
#
#
# @app.route('/upload', methods=['POST'])
# def upload_data():
#     # Get the posted data
#     post_data = request.data.decode('utf-8')
#
#     # Print the posted data
#     print(f"Received POST data: {post_data}")
#
#     # Create a response
#     response = {
#         'message': 'Data received',
#         'data': post_data
#     }
#
#     return jsonify(response), 200
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8086)
import base64
import json

import xmltodict
from encodings.base64_codec import base64_decode

from flask import Flask, request, jsonify, send_from_directory, redirect

app = Flask(__name__, static_folder='/app')


@app.route('/', methods=['GET'])
def serve_file():
    return send_from_directory('/app', 'index.html')


@app.route('/saml-login', methods=['POST'])
def saml_login():
    # print(request.form)

    saml_response = request.form.get('SAMLResponse')
    if saml_response:
        try:
            decoded_response = base64.b64decode(saml_response).decode('utf-8')
            dict_data = xmltodict.parse(decoded_response)
            print(json.dumps(dict_data, indent=4))
        except Exception as e:
            print(f"Error decoding SAMLResponse: {e}")

    try:
        relay_state = request.form.get('RelayState')
        print("Relay State:", relay_state)
    except Exception as e:
        print(f"RelayState isn't available!")

    # post_data = request.data.decode('utf-8')
    return redirect('http://localhost/idp')


@app.route('/<path:filename>', methods=['GET'])
def serve_static_file(filename):
    return send_from_directory('/app', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)
