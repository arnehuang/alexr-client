import os
import json
import logging
import services  

from importlib.machinery import SourceFileLoader
from alexr import Alexr

logging.basicConfig(filename='service.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s')

config = json.loads(open("config.json").read())

customServiceModule = config["CUSTOM_SERVICE"]

logging.info("Basic config load completed")

customServiceModule = SourceFileLoader(services.__name__, os.path.join("services", customServiceModule)).load_module()

if __name__ == "__main__":
    alexrObj = Alexr(config)
    services.loadInput(config, alexrObj.startRequest)