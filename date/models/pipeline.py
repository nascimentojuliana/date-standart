from date.models.rules import Rules

class Pipeline():

	def __init__(self):
	
		self.rules = Rules()


	def predict(self,date):

		entities = self.rules.process_entities(date)

		return entities
