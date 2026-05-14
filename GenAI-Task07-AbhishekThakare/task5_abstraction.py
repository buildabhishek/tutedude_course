# This program demonstrates abstraction using abstract base class

from abc import ABC, abstractmethod


class Payment(ABC):

    @abstractmethod
    def process_payment(self, amount):
        pass


class CreditCardPayment(Payment):

    def process_payment(self, amount):
        print("Credit Card Payment of", amount, "processed")


class UPIPayment(Payment):

    def process_payment(self, amount):
        print("UPI Payment of", amount, "processed")


payment1 = CreditCardPayment()
payment2 = UPIPayment()

payment1.process_payment(2500)
payment2.process_payment(1200)
