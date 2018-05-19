
from abc import ABC, abstractmethod
from order.errors import UndefinedMethodError
import urllib, json

class SMSPayProvider(ABC):

    @abstractmethod
    def charge(self,customer, amount):
        raise UndefinedMethodError("charge() is not implemented")
    


class AirtelMoneyProviderMock(SMSPayProvider):
    api_url = "https://api.airtelmoney.com/gabon/"
    def charge(self, customer, amount):
        approved = False
        if (amount > 0) and (customer is not None):
            content_type = 'Content-Type'
            value = 'application/json'
            postdata = {
                'customer': customer.userprofile.telefon,
                'amount': amount
            }
            request =  urllib.request.Request(AirtelMoneyProviderMock.api_url)
            request.add_header(content_type, value)
            jsondata = json.dumps(postdata).encode('utf-8')
            request.add_header('Content-Length', len(jsondata))
            #response = urllib.request.urlopen(request, jsondata)
            approved = True
        return approved


class PaypalProviderMock(SMSPayProvider):
    api_url = "https://api.paypal.com/v1/"
    def charge(self, customer, amount):
        approved = False
        if (amount > 0) and (customer is not None):
            content_type = 'Content-Type'
            value = 'application/json'
            postdata = {
                'customer': customer.email,
                'amount': amount
            }
            request =  urllib.request.Request(PaypalProviderMock.api_url)
            request.add_header(content_type, value)
            jsondata = json.dumps(postdata).encode('utf-8')
            request.add_header('Content-Length', len(jsondata))
            #response = urllib.request.urlopen(request, jsondata)
            approved = True
        return approved