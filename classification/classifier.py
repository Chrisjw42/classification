from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

import numpy as np


from classification.constants import Classes, FileTypes

from werkzeug.datastructures import FileStorage


@dataclass
class ClassPrediction():
    class_ref: Classes = field()  # TODO nullable=False
    probability: float = field()
    confidence: float = field()
    
    def __dict__(self):
        return {
            "class_ref": self.class_ref,
            "probability": self.probability,
            "confidence": self.confidence,
        }
    def __repr__(self):
        return f"""
PREDICTION: {self.class_ref}: {self.confidence} | {self.probability}
"""

@dataclass
class Prediction():
    prediction_bank_statement: ClassPrediction = field()
    prediction_drivers_licence: ClassPrediction = field()
    prediction_invoice: ClassPrediction = field()
    # TODO implement logic to force preds to sum to 1, so they can be treated as
    # a probability distribution

    # Store the preds as a list
    class_predictions = [
        prediction_bank_statement,
        prediction_drivers_licence,
        prediction_invoice,
    ]
    

    def estimate_class(self):
        "Starting with the highest confidence level, work backwards to see if we have any confident predictions"
        for confidence_level in np.linspace(1.0, 0.5, 6):

            predictions_confident = [p for p in self.class_predictions if p.confidence >= confidence_level]
            if len(predictions_confident) == 0:
                continue
            if len(predictions_confident) == 1:
                continue


    def __dict__(self):
        return {
            "prediction_bank_statement": dict(self.prediction_bank_statement),
            "prediction_drivers_licence": dict(self.prediction_drivers_licence),
            "prediction_invoice": dict(self.prediction_invoice),
        }
    
    def __repr__(self):
        return f"""MULTICLASS PREDICTION:
bank_statement: {self.prediction_bank_statement.confidence} | {self.prediction_bank_statement.probability}
drivers_licence: {self.prediction_drivers_licence.confidence} | {self.prediction_drivers_licence.probability}
invoice: {self.prediction_invoice.confidence} | {self.prediction_invoice.probability}
"""





# Dummy prediction used in error cases
DUMMY_PREDICITON = Prediction(
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

# TODO Upgrade filename classification to Levenstein distance
# def classify_file(file: FileStorage):
#     filename = file.filename.lower()
#     # file_bytes = file.read()

#     if "drivers_license" in filename:
#         return "drivers_licence"

#     if "bank_statement" in filename:
#         return "bank_statement"

#     if "invoice" in filename:
#         return "invoice"

#     return "unknown file"


def classify_file(file: FileStorage):
    return DUMMY_PREDICITON


class IndividualClassifier(ABC):
    @property
    def filetype_compatibility() -> list:
        pass


    @abstractmethod
    def predict_file() -> Prediction:
        pass

    # TODO extend to URL reading/classification
    # @abstractmethod
    # def predict_url():
    #     pass
    

class EnsembleClassifier():
    classifiers: List[IndividualClassifier] = field()

    def __init__(self, classifiers):
        self.classifiers = classifiers

    
    def get_most_confident(self):
        return

    def predict_file(self, file):
        # Have each classifier create a prediction
        classifier_predictions = [
            classifier.predict_file(file)
            for classifier
            in self.classifiers
        ]

        # Merge all individual class predictions into a single collection

        all_predictions = np.concatenate(
            [pred.class_predictions for pred in classifier_predictions]
        )




        return classifier_predictions



