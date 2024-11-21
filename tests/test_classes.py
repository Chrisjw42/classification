from classification.classifier import Prediction, MulticlassPrediction
from classification.classifier_face import FaceRecognitionClassifier
from classification.classifier_ocr import OCRClassifier
from classification.constants import Classes


def test_basic_instantiation():
    """Ensure the basic structure of the classes is hooked up as expected."""

    MulticlassPrediction(
        # Dummy prediction
        prediction_bank_statement=Prediction(
            class_ref=Classes.BANK_STATEMENT,
            probability=0.5,
            confidence=0.0,
        ),
        prediction_drivers_licence=Prediction(
            class_ref=Classes.DRIVERS_LICENCE,
            probability=0.5,
            confidence=0.0,
        ),
        prediction_invoice=Prediction(
            class_ref=Classes.INVOICE,
            probability=0.5,
            confidence=0.0,
        ),
    )

    FaceRecognitionClassifier()

    OCRClassifier()
