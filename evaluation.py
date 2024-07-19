from gpt_io import ChatGPT_IO
from LM_IO import LM_IOInterface
from display_utils import display_ml
import json
import numpy as np
import warnings
import re




class ModelEvaluator:
    def __init__(self, lm_io:LM_IOInterface=None):
        if lm_io is None:
            lm_io = ChatGPT_IO()
        self.lm_io = lm_io
        self.prepend_text = ""
        pass

    def prepare_question(self, instruction_list:list,dialogue_setup_list:list):
        test_message_list = []
        test_message_list.append(self.lm_io.generate_instruction_json(self.prepend_text))
        for instruction in instruction_list:
            test_message_list.append(self.lm_io.generate_instruction_json(instruction))
        for dialogue_setup in dialogue_setup_list:
            test_message_list.append(self.lm_io.generate_assistant_json(dialogue_setup))

        display_ml(test_message_list)

        return(test_message_list)
    

    def evaluate_model(self, test:dict):
        raise NotImplementedError()
    


class GradedModelEvaluator(ModelEvaluator):
    def grade_response(self,model_response:str, test):
        # consider the response
        # grade the response out of 10 based on the rubric

        rubric_instruction = "Grade the user's response according to the rubric. If the rubric doesn't specify, use a scale from 1 to 10. Only respond with a single number representing the grade.\n"
        rubric = test['rubric']
        parse_response_ml = [
            self.lm_io.generate_user_json(rubric_instruction),
            self.lm_io.generate_user_json(rubric),
            self.lm_io.generate_user_json("User's response:\n" + model_response)
            ]

        parse_response = self.lm_io.get_response(parse_response_ml)
        #now, use the response to determine which item the
        parse_response_text = parse_response.choices[0].message.content
        response_number_text = re.match(r'\d+', parse_response_text)
        if response_number_text is not None:
            response_grade = int(response_number_text[0])
        else:
            raise Exception("grade not completed successfully")

        return({'grade':response_grade,
                'statement':parse_response_text})

  
    def evaluate_model(self, test:dict):
        instruction = [test['test_instructions']]
        dialogue = []
        #first prepare the question
        test_message_list = self.prepare_question(instruction,dialogue)
        #get the response
        response = self.lm_io.get_response(test_message_list)
        vignette_raw_response = response.choices[0].message.content
        parsed_choice = self.grade_response(vignette_raw_response,test)
        return({
            'raw_response':vignette_raw_response,
            'grade': parsed_choice
            })
    

class HowToModelEvaluator(GradedModelEvaluator):
    def __init__(self, lm_io:LM_IOInterface=None):
        super.__init__(lm_io)
        self.prepend_text = ""
        pass    


class RolePlayModelEvaluator(ModelEvaluator):
    def __init__(self, lm_io:LM_IOInterface=None):
        super().__init__(lm_io)
        self.prepend_text = "Generally, keep responses brief, role-playing no more than 2-3 sentences at a time, unless it is particularly important to engage in a longer monologue.\n"
        pass    


    def parse_response_text(self,model_response:str, candidate_statements:list):

        np.random.shuffle(candidate_statements.copy())


        #generate the multichoice comparison text
        multichoice_comparison_text = "Please indicate which of the CANDIDATE STATEMENTS the SELECT STATEMENT most closely resembles. Only respond with a single number corresponding to the candidate statement selected. If the statement doesn't resemble any of the responses, respond with 0.\n"
        multichoice_comparison_text += "SELECT STATEMENT: " + model_response + "\n"
        for i,cs in enumerate(candidate_statements):
            multichoice_comparison_text += f"CANDIDATE STATEMENT {i+1}: " + cs['statement'] + "\n"

        
        parse_response_ml = [self.lm_io.generate_user_json(multichoice_comparison_text)]
        parse_response = self.lm_io.get_response(parse_response_ml)
        #now, use the response to determine which item the
        warnings.warn("this is untested, and we should probably run the parsing multiple times to ensure its accuracy")
        parse_response_text = parse_response.choices[0].message.content
        response_number_text = re.match(r'\d+', parse_response_text)
        if response_number_text is not None:
            response_number = int(response_number_text[0])

        response_index = response_number - 1

        if response_index>=0 and response_index<len(candidate_statements):
            parsed_choice = candidate_statements[response_index]
        else:
            parsed_choice = {'statement':'', 'status':'incorrect'}

        return(parsed_choice)

    def code_response(self, raw_response:str, contextual_test_json:dict):
        """
        Codes the free-text response from the model as one of the options
        This is necessary where we can't straightforwardly assess the log-probability of each of the responses.
        """
        #get the candidate from the test design in a shuffled order
        candidate_statements = [{'statement':t, 'status':'incorrect'} for t in contextual_test_json['dialogue_incorrect']]
        candidate_statements.append({'statement':contextual_test_json['dialogue_correct'], 'status':'correct'})
        choice = self.parse_response_text(raw_response,candidate_statements)
        return(choice)

    def evaluate_model(self, test:dict):
        instruction = [test['instruction']]
        dialogue = [test['vignette'], test['dialogue_setup']]
        #first prepare the question
        test_message_list = self.prepare_question(instruction,dialogue)
        #get the response
        response = self.lm_io.get_response(test_message_list)
        vignette_raw_response = response.choices[0].message.content
        parsed_choice = self.code_response(vignette_raw_response,test)
        return({
            'raw_response':vignette_raw_response,
            'parsed_choice': parsed_choice
            })
    
