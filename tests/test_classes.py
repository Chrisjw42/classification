from classification.classifier import ClassPrediction, Prediction
from classification.classifier_face import FaceRecognitionClassifier
from classification.constants import Classes


def test_basic_instantiation():
    """Ensure the basic structure of the classes is hooked up as expected."""

    Prediction(
        # Dummy prediction
        prediction_bank_statement = ClassPrediction(
            class_ref = Classes.BANK_STATEMENT,
            probability=0.5,
            confidence=0.,
        ),
        prediction_drivers_licence = ClassPrediction(
            class_ref = Classes.DRIVERS_LICENCE,
            probability=0.5,
            confidence=0.,
        ),
        prediction_invoice = ClassPrediction(
            class_ref = Classes.INVOICE,
            probability=0.5,
            confidence=0.,
        ),
    )

    FaceRecognitionClassifier()
    