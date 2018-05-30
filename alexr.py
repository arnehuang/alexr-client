import json
import logging
import xmltodict
import concurrent.futures

from awis import AWIS

class Alexr:
    
    def __init__(self, config):
        self.config = config
        self.maxWorkers = config["MAX_WORKERS"]
        self.secretKey = config["AWS_SECRET_KEY"]
        self.accessKey = config["AWS_ACCESS_KEY"]
        self.actionName = config["ACTION_NAME"]
        self.responseGroup = config["ACTION_GROUP"][self.actionName]

    def startRequest(self, domains, outputCallback):
        if not domains:
            raise Exception("Input Domains Empty")
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:

            future_to_url = {executor.submit(self.__getResponseText, a_domain_input_dict['normed_url'].strip(), a_domain_input_dict['duplicate']): a_domain_input_dict for a_domain_input_dict in domains}
            # future_to_url = {executor.submit(self.__getResponseText, a_domain_input_dict.strip()): a_domain_input_dict for
            #                  a_domain_input_dict in domains}
            for future in concurrent.futures.as_completed(future_to_url):
                domain_input_dict = future_to_url[future]
                # print('domain_input_dict', domain_input_dict)
                try:
                    resText = future.result()
                    outputCallback(self.config, domain_input_dict, resText)
                except Exception as exc:
                    logging.exception("Error")

    def __getResponseText(self, domain, is_duplicate):
        if is_duplicate:
            return {'duplicate':True}
        else:
            awsObj = AWIS(domain, self.actionName, self.responseGroup, self.accessKey, self.secretKey)
            resText = awsObj.getRequestResponse()
            res_dict = xmltodict.parse(str(resText), dict_constructor=dict)
            return res_dict