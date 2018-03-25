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
            future_to_url = {executor.submit(self.__getResponseText, domain.strip()): domain for domain in domains}
            for future in concurrent.futures.as_completed(future_to_url):
                pageURL = future_to_url[future]
                try:
                    resText = future.result()
                    outputCallback(self.config, pageURL, resText)
                except Exception as exc:
                    logging.exception("Error")

    def __getResponseText(self, domain):
        awsObj = AWIS(domain, self.actionName, self.responseGroup, self.accessKey, self.secretKey)
        resText = awsObj.getRequestResponse()
        res_dict = xmltodict.parse(str(resText))
        return res_dict