# Alexr Client
 Impressively Fast Multithreaded Python Implementation of AWS Alexa Website Analytics Service 

### Alexr Client Can

* Gather information about web sites, including historical web traffic data, related links and more.
* Access historical web traffic data for web sites to analyze growth and understand the effects of specific events on web site traffic
* Access the list of sites linking to any given site


## Necessary Required Permission To Access AWIS

Inorder to get start using with AWIS Service API you needs to give AWIS access permission to you AWS IAM Role. Access permission provided below

    {
     "Version": "2012-10-17",
     "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "awis:GET"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    } 
    
### A Four Step Setup

* Create a services class within service/new_service.py
* Write two functions - loadInput and processOutput passing necessary params and callback functions.
* Update the Config Json
* Run the Main

### Deep Dive Alexr Components 

* Service Module
* Config Json

#### Service Module

* Services module was built to decouple the input and output source of the service. 
* A major advantage that the Services module gives is that one can pass required requests in batches highly useful if one is polling the request input periodically from various sources.

Getting started with Sample.py is pretty simple. If you take a look at the services/sample.py module the implementation is pretty straight forward.

There are two methods:

* `loadInput`
* `processOutput`

Services module contains a method named `loadInput` - that takes in two parameters: `meta` object and a `callback` function. 

    def loadInput(meta, callback):
        outputObj = open("output.txt", "w")
        with open("input.txt", "r") as inpObj:
            domains = inpObj.readlines()
            callback(domains, outputCallback=processOutput)

* `meta` object lets you add or remove config that could be passed around easily through the service for post processing work.
* `Callback` function is the function that will run the Alexr service. Callback function needs to be passed the domains list or set. Which will serve as the input list.

`One can use the Services module for instantiating DB connections as well` 

The output processing is handled by the `processOutput` function

Here the response dictionary is parsed and appended to a file output.txt which was instantiated in the loadInput method.

    def processOutput(meta, pageURL, resDict):
        try:
            rank = resDict["aws:UrlInfoResponse"]["aws:Response"]["aws:UrlInfoResult"]["aws:Alexa"]["aws:TrafficData"]["aws:Rank"]
            with open("output.txt", "a") as outputObj:
                jsonStr = json.dumps(str({"page": pageURL.strip(), "rank": rank}))
                outputObj.write(jsonStr)
                outputObj.write("\n")
                outputObj.flush()
        except Exception as exp:
            raise


#### Config Json

Config Json is the heart of the system. Provided is the sample config json.

    {
        "MAX_WORKERS": 100,
        "CUSTOM_SERVICE": "sample.py",
        "AWS_ACCESS_KEY": "",
        "AWS_SECRET_KEY": "",
        "ACTION_NAME": "SitesLinkingIn",
        "ACTION_GROUP": {
            "UrlInfo": "",
            "TrafficHistory": "History",
            "SitesLinkingIn": "SitesLinkingIn",
            "CategoryBrowser": ""
        }
    }

There are only few parameters that you've to fill other than AWS Access and Secret Key. So, in order for one to use a CUSTOM_SERVICE one has to include the class name of the service in this key pair. Only then it will be instantiated.

`ACTION_NAME` and `ACTION_GROUP` determines the API Url to be used to get the specific information. Available below are the various web analytics attributes that one can get for each action name and action group.


    "TrafficHistory": "History"

    "SitesLinkingIn": "SitesLinkingIn",

    "UrlInfo" : {
        "Categories", 
        "Rank", 
        "RankByCountry", 
        "UsageStats", 
        "AdultContent", 
        "Speed", 
        "Language", 
        "OwnedDomains", 
        "LinksInCount", 
        "SiteData"
    }

    "CategoryBrowser": {
        "Categories", 
        "RelatedCategories", 
        "LanguageCategories", 
        "LetterBars"
    }

So to get specific information one just has to map the Action name to its group and pass it in the Config Json file. Eg

    ACTION_NAME: UrlInfo
    ACTION_GROUP: Rank

> Note: Multiple action group cannot be passed. Issue being fixed

