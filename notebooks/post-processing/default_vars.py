"""Default variables used in the analysis"""
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
