import pytest

from classification.classifier import Prediction
from classification.classifier_face import FaceRecognitionClassifier
from classification.constants import Classes


def test_basic_instantiation():
    """Ensure the basic structure of the classes is hooked up as expected."""

    Prediction(
        # Dummy prediction
        predictions={
            Classes.BANK_STATEMENT: 0.5, 
            Classes.DRIVERS_LICENCE: 0.5, 
            Classes.INVOICE: 0.5
        },
        confidences={
            Classes.BANK_STATEMENT: 0.5, 
            Classes.DRIVERS_LICENCE: 0.5, 
            Classes.INVOICE: 0.5
        },
    )

    FaceRecognitionClassifier()
    