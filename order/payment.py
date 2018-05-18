
from abc import ABC, abstractmethod
from order.errors import UndefinedMethodError


class Payment(ABC):

    def __init__(self, provider):
        pass

    @abstractmethod
    def process_payment(self, order):
        raise UndefinedMethodError("process_payment() is not implemented")



class SMSPayment(Payment):

    def __init__(self, provider):
        self.provider = provider

    def process_payment(self, order):
        approved = self.provider.charge(order.user, order.total)
        if approved :
            print("SMS Payment approved ")
        else :
            print("SMS Payment not approved ")
        return approved