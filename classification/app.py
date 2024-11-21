from flask import Flask, request, jsonify

from classification import constants
from classification.classifier import EnsembleClassifier
from classification.classifier_face import FaceRecognitionClassifier
from classification.classifier_ocr import OCRClassifier
from werkzeug.datastructures import FileStorage


app = Flask(__name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in [
        ft.name for ft in constants.FileTypes
    ]


def classify_file(file: FileStorage):
    ensemble = EnsembleClassifier(
        classifiers=[
            # TODO add different classifiers
            FaceRecognitionClassifier(),
            OCRClassifier(),
        ]
    )
    return ensemble.predict_file(file)


@app.route("/classify_file", methods=["POST"])
def classify_file_route():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    file_class = classify_file(file)
    return jsonify({"file_class": file_class}), 200


if __name__ == "__main__":
    app.run(debug=True)
