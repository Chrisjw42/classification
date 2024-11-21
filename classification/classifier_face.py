import face_recognition
import logging

from classification.classifier import IndividualClassifier, Prediction, ClassPrediction, DUMMY_PREDICITON
from classification.constants import Classes, FileTypes

logger = logging.getLogger(__name__)

class FaceRecognitionClassifier(IndividualClassifier):
    def predict_file(self, file) -> Prediction:
        
        try:
            image = face_recognition.load_image_file(file)
        except Exception as e:
            # Use a broad except to ensure stability
            logger.error("Error reading file: %s.\nError: %s", file, e)
            # TODO: log these errors in somewhere for further inspection
            return DUMMY_PREDICITON
        
        # Run a facial recognition over the image
        face_locations = face_recognition.face_locations(image)

        # Exactly 0 face implies it is not a driver's license
        if len(face_locations) == 0:
            return Prediction(
                prediction_bank_statement = ClassPrediction(
                    class_ref = Classes.BANK_STATEMENT,
                    probability=0.2,
                    confidence=0.2,
                ),
                prediction_drivers_licence = ClassPrediction(
                    class_ref = Classes.DRIVERS_LICENCE,
                    probability=0.1,
                    # Stop short of 100% confidence, the facerecogniser is imperfect
                    confidence=0.8,
                ),
                prediction_invoice = ClassPrediction(
                    class_ref = Classes.INVOICE,
                    probability=0.2,
                    confidence=0.2,
                ),
            )
        # Exactly 1 face implies it is likely a drivers license
        elif len(face_locations) == 1:
            return Prediction(
                prediction_bank_statement = ClassPrediction(
                    class_ref = Classes.BANK_STATEMENT,
                    probability=0.2,
                    confidence=0.2,
                ),
                # Stop short of 100% confidence, the facerecogniser is imperfect
                prediction_drivers_licence = ClassPrediction(
                    class_ref = Classes.DRIVERS_LICENCE,
                    probability=0.9,
                    confidence=0.8,
                ),
                prediction_invoice = ClassPrediction(
                    class_ref = Classes.INVOICE,
                    probability=0.2,
                    confidence=0.2,
                ),
            )
        # >1 face implies it is possibly a driver's license, potentially an FP, or a logo appearing as a face
        elif len(face_locations) >1:
            return Prediction(
                prediction_bank_statement = ClassPrediction(
                    class_ref = Classes.BANK_STATEMENT,
                    probability=0.2,
                    confidence=0.2,
                ),
                # Stop short of 100% confidence, the facerecogniser is imperfect
                prediction_drivers_licence = ClassPrediction(
                    class_ref = Classes.DRIVERS_LICENCE,
                    probability=0.5,
                    confidence=0.5,
                ),
                prediction_invoice = ClassPrediction(
                    class_ref = Classes.INVOICE,
                    probability=0.2,
                    confidence=0.2,
                ),
            )


        return 
    
    @property
    def filetype_compatibility() -> list:
        return [FileTypes.jpg]
    


