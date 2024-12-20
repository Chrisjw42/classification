import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

import numpy as np


from classification import constants
from classification.constants import Classes


logger = logging.getLogger(__name__)


@dataclass
class Prediction:
    class_ref: Classes = field()
    probability: float = field()
    confidence: float = field()

    @property
    def positive_prediction_strength(self) -> float:
        """Return the 'positive prediction strength', the idea is that a very confident positive."""
        return self.probability * self.confidence

    def __dict__(self):
        return {
            "class_ref": self.class_ref,
            "probability": self.probability,
            "confidence": self.confidence,
        }

    def __repr__(self):
        return f"""
PREDICTION: {self.confidence} | {self.probability}
"""


@dataclass
class MulticlassPrediction:
    prediction_bank_statement: Prediction = field()
    prediction_drivers_licence: Prediction = field()
    prediction_invoice: Prediction = field()
    # TODO implement logic to force preds to sum to 1, so they can be treated as
    # a probability distribution

    @property
    def class_predictions(self):
        """Return the predictions as a list."""
        return [
            self.prediction_bank_statement,
            self.prediction_drivers_licence,
            self.prediction_invoice,
        ]

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


# Dummy prediction used in cases of uncertainty
UNCERTAIN_PREDICTION = MulticlassPrediction(
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

# TODO Upgrade filename classification to use Levenstein distance vs. keywords, hence addressing spelling mistakes
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


class IndividualClassifier(ABC):
    @property
    def filetype_compatibility() -> list:
        pass

    @abstractmethod
    def predict_file() -> MulticlassPrediction:
        pass

    # TODO extend to URL reading/classification, download the file to local and proceed with existing file processing
    # @abstractmethod
    # def predict_url():
    #     pass


class EnsembleClassifier:
    classifiers: List[IndividualClassifier] = field()

    def __init__(self, classifiers):
        self.classifiers = classifiers

    def _get_strongest_positive_pred(self, all_predictions) -> constants.Classes:
        """Across all predictions for all classifiers, return the strongest positive prediction."""
        preds_with_strength = [
            (pred.class_ref, pred.positive_prediction_strength)
            for pred in all_predictions
        ]
        # Sort by strength
        preds_with_strength.sort(key=lambda tuple: tuple[1])

        strongest_pred = preds_with_strength[-1]
        pred_class, pred_confidence = strongest_pred
        logger.info(
            f"Best prediction: {strongest_pred} with confidence: {pred_confidence}"
        )
        return pred_class

    def predict_file(self, file: str) -> constants.Classes:
        """For a single file, generate a class prediction"""
        # Have each classifier create a prediction
        classifier_predictions = [
            classifier.predict_file(file) for classifier in self.classifiers
        ]

        # Merge all individual class predictions into a single collection

        all_predictions = np.concatenate(
            [mcp.class_predictions for mcp in classifier_predictions]
        )

        strongest_pred = self._get_strongest_positive_pred(all_predictions)

        return strongest_pred
