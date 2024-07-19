import pandas as pd
import json

class EvalDesignSuite:

    def __init__(self) -> None:
        pass


class QuestionTransformationTest:
    """
    Designed to store information about a single Question*TransformationTask mapping with all of the transfomred questions and responses.
    """

    def __init__(self,orig_question:str,transform_instructions:str) -> None:
        self.question = self.get_question_dict(orig_question)
        self.transformation_task = self.get_transformation_task_dict(transform_instructions)
        pass

    def get_question_dict(self,question_text:str):
        return({'q_text':question_text})
    
    def get_transformation_task_dict(self, transform_instructions):
        return({'trans_task':transform_instructions})


    def get_json_for_question_mapping(self,contextual_test_json:dict, vignette_raw_response:str,parsed_choice:dict):

        tranformation_test = {
            'response_raw_text':vignette_raw_response,
            'parsed_choice_text': parsed_choice['statement'],
            'choice_status': parsed_choice['choice_status']    
        }
        question_transformation = {
            'transformation':contextual_test_json,
            'tranformation_tests':[tranformation_test]
        }
        question_map = {
            'question_orig':self.question,
            'transformation_instructions':self.transformation_task,
            'question_transformations':[question_transformation]
        }
        return(question_map)
    
    def flatten_question_map_to_df(self,question_map:dict,qm_i=None):
        """
        Takes a question_map dictionary and flattens it into a pandas dataframe row.
        """
        

        row_list = []
        #for qm_i, qm in enumerate(question_list):
        qm = question_map
        for qt_i, qt in enumerate(qm['question_transformations']):
            for tt_i, tt in enumerate(qt['tranformation_tests']):
                #now create the pandas row, storing all the important data including the indices
                row = {}
                if qm_i is not None:
                    row['question_map_i'] = qm_i
                #should maybe be storing the questions as a dataframe to give them proper IDs but lets' not worry for now.
                #I don't want to design a whole in-memory database for this.    
                row['question_orig'] = qm['question_orig']['q_text']
                row['trans_task'] = qm['transformation_instructions']['trans_task']
                #iterate through each key in contextual_test_json and add that key to the row
                row['transformation_i'] = qt_i
                for k,v in qt['transformation'].items():
                    row['transformation_'+k] = v

                row['test_i']=tt_i
                row['response_raw_text'] = tt['response_raw_text']
                row['parsed_choice_text'] = tt['parsed_choice_text']
                row['choice_status'] = tt['choice_status']
                #add the row to the list of rows
                row_list.append(row)
        #convert the row_list into a pandas dataframe with one row for each output combination
        df = pd.DataFrame(row_list)
        return(df)








#question_list = [question_map]

        pass