from flask import Flask, jsonify
from ImageProcessor import ImageProcessor
from validate_email import validate_email

app = Flask(__name__)

pathImage = "/home/gazandic/linebot/memegenerator/";

@app.route("/email/<string:url>",methods=['GET'])
def get_email(url):
    if len(url) == 0:
        abort(404)
    ip = ImageProcessor()
    s = ip.process_image(pathImage+url)
    is_valid = validate_email(s)
    if is_valid :
        return jsonify({'result':s})
    else :
        return jsonify({'result':"fail"})


@app.route("/telephone/<string:url>",methods=['GET'])
def get_telephone(url):
    if len(url) == 0:
        abort(404)
    ip = ImageProcessor()
    s = ip.process_image(pathImage+url)
    print(s)
    return jsonify({"result":s})

if __name__ == "__main__":
    app.run()
