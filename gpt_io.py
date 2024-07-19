from LM_IO import *
from config import ATConfig
import openai


class ChatGPT_IO(LM_IOInterface):

    def __init__(self,model_version:str=None) -> None:
        self.version = model_version
        self.initialize_llm_connection()


    def initialize_llm_connection(self):
        #load the API key from the YAML file "athentication.yml", under the item "openaikey"
        # use the yaml package

        config = ATConfig.get_config()

        openai.api_key = config['openaikey']
        if self.version is None:
            self.version = config['openai_model_version']

    def get_response(self, all_messages,response_format=None):
        print("getting response")

        if response_format is None:
            api_response = openai.chat.completions.create(
                model=self.version,
                messages=all_messages
                )
        elif response_format=="json":
            api_response = openai.chat.completions.create(
                model=self.version,
                messages=all_messages,
                response_format={"type":"json_object"}
                )
        else:
            raise Exception("response format " + response_format + " not supported")
        return(api_response)
    
    def generate_instruction_json(self, instruction):
        return({"role": "system", "content": instruction})
    
    def generate_user_json(self, user_input):
        return({"role": "user", "content": user_input})
    
    def generate_assistant_json(self, user_input):
        return({"role": "assistant", "content": user_input})
    

        

    

    
