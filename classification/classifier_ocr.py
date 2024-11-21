import logging
from pathlib import Path
import re
import string
from typing import List
from PIL import Image

import pytesseract
from pypdf import PdfReader

from classification.classifier import (
    IndividualClassifier,
    MulticlassPrediction,
    Prediction,
    DUMMY_PREDICITON,
)
from classification.constants import Classes, FileTypes

logger = logging.getLogger(__name__)

# Define keywords we should expect to find in each document type
INVOICE_WORDS_HIGH = ["invoice"]
INVOICE_WORDS_MED = ["tax", "subtotal", "discount"]
DRIVERS_WORDS_HIGH = ["driving", "license", "driver"]
DRIVERS_WORDS_MED = ["manual", "automatic", "sex"]
BANK_STATEMENT_WORDS_HIGH = ["statement"]
BANK_STATEMENT_WORDS_MED = [
    "bank",
    "debit",
    "credit",
    "deposit",
    "payment",
    "purchase",
    "transfer",
]


def clean_string(text: str) -> List[str]:
    """
    Take a string (typically from OCR), clean the text, and return a list of words
    Most logic lifted from here: https://dataknowsall.com/blog/textcleaning.html
    """

    # Make lower
    text = text.lower()

    # Remove line breaks
    # Note: that this line can be augmented and used over
    # to replace any characters with nothing or a space
    text = re.sub(r"\n", " ", text)

    # Remove punctuation
    translator = str.maketrans(" ", " ", string.punctuation)
    text = text.translate(translator)

    text = text.split(" ")

    # Remove numbers
    return [re.sub(r"\w*\d\w*", "", w) for w in text]


class OCRClassifier(IndividualClassifier):
    def predict_file(self, file_path) -> MulticlassPrediction:
        try:
            text = self.extract_text(file_path)
        except Exception as e:
            # TODO: specific exception handling
            logger.error("Error reading file: %s.\nError: %s", file_path, e)
            # TODO: log these errors in somewhere for further inspection
            return DUMMY_PREDICITON

        words = clean_string(text)

        set(words) and set(BANK_STATEMENT_WORDS_MED)

        # assess if any of the keywords were observed in the document
        bank_statement_high_observed = (
            len(set(words).intersection(set(BANK_STATEMENT_WORDS_HIGH))) > 0
        )
        bank_statement_med_observed = (
            len(set(words).intersection(set(BANK_STATEMENT_WORDS_MED))) > 0
        )
        drivers_high_observed = (
            len(set(words).intersection(set(DRIVERS_WORDS_HIGH))) > 0
        )
        drivers_med_observed = len(set(words).intersection(set(DRIVERS_WORDS_MED))) > 0
        invoice_high_observed = (
            len(set(words).intersection(set(INVOICE_WORDS_HIGH))) > 0
        )
        invoice_med_observed = len(set(words).intersection(set(INVOICE_WORDS_MED))) > 0

        # TODO get a psuedo-probability by counting the percentage of words observed
        return MulticlassPrediction(
            prediction_bank_statement=Prediction(
                class_ref=Classes.BANK_STATEMENT,
                probability=(bank_statement_high_observed * 0.7)
                + (bank_statement_med_observed * 0.2),
                confidence=(bank_statement_high_observed * 0.7)
                + (bank_statement_med_observed * 0.2),
            ),
            prediction_drivers_licence=Prediction(
                class_ref=Classes.DRIVERS_LICENCE,
                probability=(drivers_high_observed * 0.7)
                + (drivers_med_observed * 0.2),
                confidence=(drivers_high_observed * 0.7) + (drivers_med_observed * 0.2),
            ),
            prediction_invoice=Prediction(
                class_ref=Classes.INVOICE,
                probability=(invoice_high_observed * 0.7)
                + (invoice_med_observed * 0.2),
                confidence=(invoice_high_observed * 0.7) + (invoice_med_observed * 0.2),
            ),
        )

    def extract_text(self, file_path: str):
        """Extract the raw text from the file, based on"""
        file_type = Path(file_path).suffix.lstrip(".")
        if file_type in [FileTypes.jpg.name, FileTypes.png.name]:
            print("IMG")
            text = pytesseract.image_to_string(Image.open(file_path))
        elif file_type == FileTypes.pdf.name:
            print("PDF")
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + " "
        else:
            return []
        return text

    @property
    def filetype_compatibility() -> list:
        #!TODO filter by type
        return [FileTypes.jpg, FileTypes.png, FileTypes.pdf]
