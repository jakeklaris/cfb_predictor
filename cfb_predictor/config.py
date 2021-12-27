import pathlib

APPLICATION_ROOT = '/'

# File Upload to var/uploads/
CFB_PREDICTOR_ROOT = pathlib.Path(__file__).resolve().parent.parent
RANKINGS_FOLDER = CFB_PREDICTOR_ROOT/'cfb_predictor'/'static'/'SP+Data'