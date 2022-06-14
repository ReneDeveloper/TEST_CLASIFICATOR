class BasicAgent:
    def __init__(self, name_, type_):
        self.name = name_
        self.type = type_

    def execute_Task(self,taskObject_):
    	return False

    def describeme(self):
        print("Soy un Animal del tipo", type(self).__name__)
