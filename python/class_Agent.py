from class_BasicAgent import BasicAgent
class Agent(BasicAgent):


    def __init__(self, name_, type_):
        self.name = name_
        self.type = type_


    def __init__(self, parameters_):
        
        self.parameters = parameters_
        #self.name = parameters_['name']
        #self.type = parameters_['type']
        self.LOG_ACTIVE = parameters_['LOG_ACTIVE']

        super().__init__(parameters_['name'], parameters_['type'])
        if self.LOG_ACTIVE:
            print("Agent.__init__():" + str(parameters_))

parameters_ = {}
parameters_['LOG_ACTIVE'] = True
parameters_['name'] = 'test_agent'
parameters_['type'] = 'bottle'


myAgent = Agent(parameters_)

myAgent.describeme()





