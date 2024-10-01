"""Default variables used in the post-processing"""
import numpy 


# Default binning strategy
BIN_CENTER, BIN_OFFSET = numpy.linspace(0, 100, 21), 2.5


UNCERTAINTY_EXPRESSIONS = [
  "almost certain",
  "highly likely",
  "very likely",
  "probable",
  "likely",
  "somewhat likely",
  "somewhat unlikely",
  "uncertain",
  "possible",
  "unlikely",
  "not likely",
  "doubtful",
  "very unlikely",
  "highly unlikely"
]


MAPPING_2_CANONIC = {
    "top-k": {
        "model": 'model',
        'uncertainty_expression': "uncertainty_expression",
        "number_1": "numerical_response", 
        'name': "speaker_name", 
        'gender': "speaker_gender", 
        'template': "template", 
        'statement_id': "statement_id", 
        "statement_type": "statement_type", 
        "statement_uuid": "statement_uuid",
        'statement': "statement",
    },
    "full-prob": {
        "completion__model": 'model',
        'uncertainty_expression': "uncertainty_expression",
        "completion__suffix": "numerical_response",
        'name': "speaker_name", 
        'gender': "speaker_gender", 
        'template': "template", 
        'statement_id': "statement_id", 
        "statement_type": "statement_type", 
        "statement_uuid": "statement_uuid",
        'statement': "statement",
    },
    "sampling-based": {
        "model": 'model',
        'uncertainty_expression': "uncertainty_expression",
        "response_first_number": "numerical_response", 
        'name': "speaker_name", 
        'gender': "speaker_gender", 
        'template': "template", 
        'statement_id': "statement_id", 
        "statement_type": "statement_type", 
        "statement_uuid": "statement_uuid",
        'statement': "statement",
    }
}