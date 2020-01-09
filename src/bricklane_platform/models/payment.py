from decimal import Decimal
from dateutil.parser import parse

from bricklane_platform.models.bank import Bank
from bricklane_platform.models.card import Card
from bricklane_platform.config import PAYMENT_FEE_RATE


class Payment(object):

    source = None
    customer_id = None
    date = None
    amount = None
    fee = None
    card_id = None
    bank_account_id = None

    def __init__(self, data=None):

        if not data:
            return

        self.source = data["source"]
        self.customer_id = int(data["customer_id"])
        self.date = parse(data["date"])

        total_amount = Decimal(data["amount"])
        self.fee = total_amount * PAYMENT_FEE_RATE
        self.amount = total_amount - self.fee

        if self.source == "card":
            card = Card()
            card.card_id = int(data["card_id"])
            card.status = data["card_status"]
            self.card = card
        elif self.source == "bank":
            bank = Bank()
            bank.bank_account_id = int(data["bank_account_id"])
            self.bank = bank

    def is_successful(self):
        """
        Check if a payment was successful.    

        All bank payments are assumed to be successful.
        """
        if self.source == "bank":
            is_successful = True
        elif self.source == "card":
            is_successful = (self.card.status == "processed")
        else:
            is_successful = False

        return is_successful
