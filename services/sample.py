import json
import pprint

def processOutput(meta, pageURL, resDict):
    try:
        pprint.pprint(resDict)

        quried_url = pageURL.strip()

        status = resDict["aws:UrlInfoResponse"]["aws:Response"]["aws:ResponseStatus"]["aws:StatusCode"]  # 'Success'
        request_info = resDict["aws:UrlInfoResponse"]["aws:Response"]["aws:UrlInfoResult"]["aws:Alexa"]['aws:Request']

        _traffic_data = resDict["aws:UrlInfoResponse"]["aws:Response"]["aws:UrlInfoResult"]["aws:Alexa"]['aws:TrafficData']



        subdomains = _traffic_data['aws:ContributingSubdomains']
        returned_url = _traffic_data['aws:DataUrl']
        rank = _traffic_data['aws:Rank']
        usage_statistics = _traffic_data['aws:UsageStatistics']

        print("queried_url", quried_url)
        print('request_info', request_info)
        print('status', status)
        print('subdomains', subdomains)
        print('returned_url', returned_url)
        print('rank', rank)
        print('usage_statistics', usage_statistics)



        with open("output.txt", "a") as outputObj:
            jsonStr = json.dumps(str({"queried_url": quried_url,
                                      "rank": rank,
                                      "request_info": request_info,
                                      "status": status,
                                      "subdomains": subdomains,
                                      "returned_url": returned_url,
                                      "usage_statistics": usage_statistics,
                                      "domain_id":'s',
                                      }))
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


    
