from IPython.display import Markdown, display

def display_ml(message_list):
    for i, message in enumerate(message_list):
        display(Markdown("### Message " + str(i+1)))
        #iterate through each kv pair in the json and print
        display_json(message)        

def display_json(json_dict):
    for key, value in json_dict.items():
        display(Markdown("**" +key+"**"+ ": "+ value))
        
