import json

def processOutput(meta, pageURL, resDict):
    try:
        rank = resDict["aws:UrlInfoResponse"]["aws:Response"]["aws:UrlInfoResult"]["aws:Alexa"]["aws:TrafficData"]
        with open("output.txt", "a") as outputObj:
            jsonStr = json.dumps(str({"page": pageURL.strip(), "rank": rank}))
            outputObj.write(jsonStr)
            outputObj.write("\n")
            outputObj.flush()
    except Exception as exp:
        raise

def loadInput(meta, callback):
    outputObj = open("output.txt", "w")
    with open("input.txt", "r") as inpObj:
        domains = inpObj.readlines()
        callback(domains, outputCallback=processOutput)


    
