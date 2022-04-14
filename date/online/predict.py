from date.utils import utils
from date.models.pipeline import Pipeline

pipeline = Pipeline()

def predict(date):
	result =  pipeline.predict(date)
	return result
        