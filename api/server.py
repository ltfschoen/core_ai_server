#!flask/bin/python
from __future__ import print_function
import sys
from flask import Flask, jsonify, request, make_response, abort

# Python 3.6+ - CORS to allow all domains
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from PIL import Image
from io import BytesIO
import base64

import site

def get_main_path():
    test_path = sys.path[0] # sys.path[0] is current path in 'examples' subdirectory
    split_on_char = "/"
    return split_on_char.join(test_path.split(split_on_char)[:-1])
main_path = get_main_path()
# site.addsitedir(main_path+'/examples')
# print ("Imported subfolder: %s" % (main_path+'/examples') )

"""
RESTful web service endpoints using Flask.
"""
app = Flask(__name__)

@app.route('/api/v1.0/image', methods=["POST"])
def post_image():
    """
    Examples:
        curl -F "data=@images/core_tray_6.jpg" http://127.0.0.1:5000/api/v1.0/image

        Note: Server responds to above with: `Image is: <PIL.JpegImagePlugin.JpegImageFile image mode=L size=1134x2016 at 0x10BAAEA20>`
    """
    if request.method == 'POST':
        # assert 'file' in request.files

        # Reference: https://stackoverflow.com/questions/8552675/form-sending-error-flask
        # print("request is: ", request)
        # print("request args are: ", request.args)
        print("request form is: ", dict(request.form)) # request form is:  ImmutableMultiDict([('data:image/png;base64,iVB
        print("base64 data is: ", dict(request.form).popitem()[0])
        # data = request.files['data']
        data = dict(request.form).popitem()[0] # since request.form appears to be a hash where base64 image is the key of the hash
        img = Image.open(BytesIO(base64.b64decode(data)))
        print("Image is: ", img)
        return 'Success!'
    else:
        print("POST request required to this endpoint")

# Python 2.7 - CORS to allow all domains
# Reference: https://stackoverflow.com/questions/22181384/javascript-no-access-control-allow-origin-header-is-present-on-the-requested
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, use_debugger=False, use_reloader=False)
