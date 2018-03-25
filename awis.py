import os
import sys
import hmac 
import base64
import hashlib
import datetime
import requests 
import logging

class AWIS:

    methodHttp = 'GET'
    serviceName = 'awis'
    serviceURL = '/api'
    algorithm = 'AWS4-HMAC-SHA256'
    serviceEndPoint = 'awis.us-west-1.amazonaws.com'
    serviceRegion = 'us-west-1'
    signed_headers = 'host;x-amz-date'

    def __init__(self, domain, actionName, responseGroup, awsAccessKey, awsSecretKey):
        timeStampObj = datetime.datetime.utcnow()
        self.awsAccessKey = awsAccessKey
        self.awsSecretKey = awsSecretKey
        self.responseGroup = responseGroup
        self.serviceBaseURL = 'https://' + self.serviceEndPoint + self.serviceURL
        self.amzDate = timeStampObj.strftime('%Y%m%dT%H%M%SZ')
        self.datestamp = timeStampObj.strftime('%Y%m%d')
        self.payload_hash = hashlib.sha256(''.encode('utf-8')).hexdigest()       
        self.requestParameters = 'Action={0}&ResponseGroup={1}&Url={2}'.format(actionName, responseGroup, domain)

    def getCanonicalHeader(self):
        return 'host:' + self.serviceEndPoint + '\n' + 'x-amz-date:' + self.amzDate + '\n'


    def getCanonicalRequest(self):
        return self.methodHttp + '\n' + self.serviceURL + '\n' + self.requestParameters + '\n' + self.getCanonicalHeader() + '\n' + self.signed_headers + '\n' + self.payload_hash

    
    def getCredentialScope(self):
        return self.datestamp + '/' + self.serviceRegion + '/' + self.serviceName + '/' + 'aws4_request'


    def getStringToSign(self):
        canonicalReq = self.getCanonicalRequest()
        return self.algorithm + '\n' +  self.amzDate + '\n' +  self.getCredentialScope() + '\n' +  hashlib.sha256(canonicalReq.encode('utf-8')).hexdigest()

    def getSign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def getSignatureKey(self, key, dateStamp, regionName, serviceName):
        kDate = self.getSign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = self.getSign(kDate, regionName)
        kService = self.getSign(kRegion, serviceName)
        kSigning = self.getSign(kService, 'aws4_request')
        return kSigning

    def getSigningKey(self):
        return self.getSignatureKey(self.awsSecretKey, self.datestamp, self.serviceRegion, self.serviceName)

    def getAbsSignature(self):
        signing_key = self.getSigningKey()
        return hmac.new(signing_key, self.getStringToSign().encode('utf-8'), hashlib.sha256).hexdigest()

    def getAuthorization(self):
        return self.algorithm + ' ' + 'Credential=' + self.awsAccessKey + '/' + self.getCredentialScope() + ', ' +  'SignedHeaders=' + self.signed_headers + ', ' + 'Signature=' + self.getAbsSignature()
    
    def getHeaders(self):
        return {'x-amz-date': self.amzDate, 'Authorization': self.getAuthorization()}

    def getRequestResponse(self):
        headers = self.getHeaders()
        logging.info(headers)
        requestURL = self.serviceBaseURL + '?' + self.requestParameters
        logging.info(requestURL)
        reqObj = requests.get(requestURL, headers=headers)
        return reqObj.text


