from classification.classifier_face import FaceRecognitionClassifier

def test_facial_recognition():
    """Simple unit test to ensure the facial recognition is working on a known case."""

    classifier = FaceRecognitionClassifier()

    res = classifier.predict_file("/Users/chriswilliams/repo/classification/files/drivers_licence_2.jpg")

    print(res)

    # The classifier should be very confident that this example is a driver's licence
    assert res.prediction_drivers_licence.probability   > res.prediction_bank_statement.probability
    assert res.prediction_drivers_licence.confidence    > res.prediction_bank_statement.confidence
    assert res.prediction_drivers_licence.probability   > res.prediction_invoice.probability
    assert res.prediction_drivers_licence.confidence    > res.prediction_invoice.confidence
