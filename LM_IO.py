
class LMResponseException(Exception):
    def __init__(self):
        super.__init__()
        pass
    
class LM_IOInterface:
    def __init__(self):
        self.initialize_llm_connection(self)

    def initialize_llm_connection(self):
        raise NotImplementedError