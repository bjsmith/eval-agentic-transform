from yaml import load
from yaml.loader import SafeLoader
from socket import gethostname
class ATConfig:

    config = None

    def get_config(force_reload=False):


        if force_reload or ATConfig.config is None:
            #add some code about getting keys in production here if you need a production env
            # is_prod = os.environ.get('IS_HEROKU', None)=='True'
            # if is_prod==True:
            #     print("loading config from heroku")
            
            #     #get all keys in the environment with os.environ
            #     all_environ = dict(os.environ)
            #     prod_environ = {k.replace("PROD_",""):v for k,v in all_environ.items() if k.startswith("PROD_")}
            #     #attempt to convert each value to json, if it fails, just use the string
            #     for k,v in prod_environ.items():
            #         try:
            #             prod_environ[k] = json.loads(v)
            #         except ValueError:
            #             pass
                
            #     ATConfig.config = prod_environ
            #     return ATConfig.config

            with open('config.yml') as f:
                    all_yaml = load(f, Loader=SafeLoader)
                    if gethostname() in all_yaml.keys():
                        ATConfig.config = all_yaml[gethostname()]
                    else:
                        ATConfig.config = all_yaml['default']
        
        return ATConfig.config
