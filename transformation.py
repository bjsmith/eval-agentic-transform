import json

from config import ATConfig
from gpt_io import ChatGPT_IO
from LM_IO import LM_IOInterface
from display_utils import display_ml
from display_utils import display_json

#if we want to write a class that has a 1:1 relationship with question, we'd call it QuestionTransformation

class QuestionTransformer:

    def __init__(self,transformation_task: str, lm_io_class:LM_IOInterface=ChatGPT_IO):
        self.lm_io = lm_io_class()
        self.transformation_task = transformation_task
        pass

    #take a question with type string input)
    def transform(self,question:str):
        message_list = []
        message_list.append(self.lm_io.generate_instruction_json(self.transformation_task))
        message_list.append(self.lm_io.generate_user_json(question))
        display_ml(message_list)

        response = self.lm_io.get_response(message_list,response_format="json")
        raw_content_response = response.choices[0].message.content

        if raw_content_response[0:7]=="```json":
            raw_content_response = raw_content_response[7:-3]


        #load the content into a json response
        try:
            contextual_test_json = json.loads(raw_content_response)
        #catch json decode error
        except json.JSONDecodeError as e:
            print("json decode error for json string:")
            print(raw_content_response)
            raise e

        return(contextual_test_json)


        