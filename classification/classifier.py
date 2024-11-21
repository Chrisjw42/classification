from abc import ABC, abstractmethod
from dataclasses import dataclass, field


from classification.constants import Classes, FileTypes

from werkzeug.datastructures import FileStorage


@dataclass
class ClassPrediction():
    class_ref: Classes = field()  # TODO nullable=False
    probability: float = field()
    confidence: float = field()

@dataclass
class Prediction():
    prediction_bank_statement: ClassPrediction = field()
    prediction_drivers_licence: ClassPrediction = field()
    prediction_invoice: ClassPrediction = field()
    # TODO implement logic to force preds to sum to 1, so they can be treated as
    # a probability distribution

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

def classify_file(file: FileStorage):
    filename = file.filename.lower()
    # file_bytes = file.read()

    if "drivers_license" in filename:
        return "drivers_licence"

    if "bank_statement" in filename:
        return "bank_statement"

    if "invoice" in filename:
        return "invoice"

    return "unknown file"


class Classifier(ABC):
    @property
    def filetype_compatibility() -> list:
        pass


    @abstractmethod
    def predict_file() -> Prediction:
        pass

    # @abstractmethod
    # def predict_url():
    #     pass
    


