import os
import pytest

from classification import constants
from classification.classifier import EnsembleClassifier
from classification.classifier_face import FaceRecognitionClassifier
from classification.classifier_ocr import OCRClassifier


def test_facial_recognition():
    """Simple unit test to ensure the facial recognition is working on a known case."""

    classifier = FaceRecognitionClassifier()

    # TODO update this to a relative path
    res = classifier.predict_file(
        "/Users/chriswilliams/repo/classification/files/drivers_licence_2.jpg"
    )
    # The classifier should be very confident that this example is a driver's licence
    assert (
        res.prediction_drivers_licence.probability
        > res.prediction_bank_statement.probability
    )
    assert (
        res.prediction_drivers_licence.confidence
        > res.prediction_bank_statement.confidence
    )
    assert (
        res.prediction_drivers_licence.probability > res.prediction_invoice.probability
    )
    assert res.prediction_drivers_licence.confidence > res.prediction_invoice.confidence


@pytest.mark.parametrize(
    "file_name, expected_class",
    [
        ("bank_statement_1.pdf", constants.Classes.BANK_STATEMENT),
        ("bank_statement_2.pdf", constants.Classes.BANK_STATEMENT),
        ("bank_statement_3.pdf", constants.Classes.BANK_STATEMENT.BANK_STATEMENT),
        ("drivers_license_1.jpg", constants.Classes.DRIVERS_LICENCE),
        ("drivers_licence_2.jpg", constants.Classes.DRIVERS_LICENCE),
        ("drivers_license_3.jpg", constants.Classes.DRIVERS_LICENCE),
        ("invoice_1.pdf", constants.Classes.INVOICE),
        ("invoice_2.pdf", constants.Classes.INVOICE),
        ("invoice_2.pdf", constants.Classes.INVOICE),
        ("additional-bank-statement-2.pdf", constants.Classes.BANK_STATEMENT),
        ("additional-bank-statement-1.pdf", constants.Classes.BANK_STATEMENT),
        ("additional-drivers-license-1.jpg", constants.Classes.DRIVERS_LICENCE),
        ("additional-drivers-license-1.jpg", constants.Classes.DRIVERS_LICENCE),
        ("additional-invoice-1.png", constants.Classes.INVOICE),
        ("additional-invoice-2.png", constants.Classes.INVOICE),
        # New filetype
        (
            "sample-modern-drivers-license-front-600nw-1977258998.webp",
            constants.Classes.DRIVERS_LICENCE,
        ),
    ],
)
def test_ensemble_logic(file_name, expected_class):
    ensemble = EnsembleClassifier(
        classifiers=[
            FaceRecognitionClassifier(),
            OCRClassifier(),
        ]
    )

    file_path = f"{os.getcwd()}/files/{file_name}"
    res = ensemble.predict_file(file_path)

    assert res == expected_class
