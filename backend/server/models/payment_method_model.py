""" server.models.payment_method_model.py """
from datetime import datetime

class PaymentMethod:
    def __init__(self):
        self.payment_method_id: int = None
        self.payment_method_name: str = None
        self.payment_method_processor: str = None
        self.payment_method_type: str = None
        self.status: str = None
        self.provider: str = None
        self.expiry: str = None
        self.origin: str = None
        self.issuer: str = None
        self.tokenized_account_number: str = None
        self.tokenized_routing_number: str = None
        self.tokenized_card_number: str = None
        self.given_name: str = None
        self.family_name: str = None
        self.full_name: str = None
        self.email_address: str = None
        self.customer_country_name: str = None
        self.customer_postal_code: str = None
        self.billing_address_one: str = None
        self.billing_address_two: str = None
        self.billing_address_three: str = None
        self.billing_state: str = None
        self.billing_country_name: str = None
        self.billing_country_alpha2_code: str = None
        self.billing_country_alpha3_code: str = None
        self.billing_country_numeric_code: str = None
        self.billing_postal_code: str = None
        self.payment_method_processor_id: str = None
        self.payment_method_metadata: dict = None
        self.is_primary: bool = False
        self.is_enabled: bool = False
        self.created_at: datetime = None
        self.updated_at: datetime = None

    def payment_method_expiry(self):
        if self.expiry and self.expiry.startswith('tok_'):
            return '--/--'
        return self.expiry

    def payment_method_full_name(self):
        if self.full_name:
            return self.full_name
        elif self.given_name and self.family_name:
            return f'{self.family_name}, {self.given_name}'
        return None

    def billing_address(self):
        if self.payment_method_name == 'ach':
            return f'{self.billing_state}, {self.billing_country_name}, {self.billing_postal_code}'
        elif self.payment_method_name == 'cc':
            if self.billing_address_one and self.billing_address_two and self.billing_state:
                return f'{self.billing_address_one}, \
                        {self.billing_address_two}, \
                        {self.billing_state}, \
                        {self.billing_country_name}'
            return self.billing_country_name
        return None

    def processor_id(self):
        if self.payment_method_name == 'pp':
            return self.payment_method_processor_id
        return None

    def card_last_four(self):
        """
        Return the last four if it has 16 characters
        """
        if self.tokenized_card_number and len(self.tokenized_card_number) == 16:
            return self.tokenized_card_number[-4:]
        elif self.tokenized_card_number and self.payment_method_name == 'directdebit':
            return self.tokenized_card_number[-4:]
        return '****'

    def __str__(self):
        return f'PaymentMethod: {self.payment_method_id}, '\
            f'{self.payment_method_name}, {self.payment_method_type}, '\
            f'{self.status}, {self.payment_method_processor}'

    def __repr__(self):
        return f'PaymentMethod({self.payment_method_id},{self.payment_method_name},{self.payment_method_type})'

    @staticmethod
    def map_from_row(data: dict):
        method = PaymentMethod()
        method.payment_method_id = data.get('payment_method_id')
        method.payment_method_name = data.get('payment_method_name')
        method.payment_method_processor = data.get('payment_method_processor')
        method.payment_method_type = data.get('payment_method_type')
        method.status = data.get('payment_method_status')
        method.provider = data.get('payment_method_provider')
        method.expiry = data.get('payment_method_expiry')
        method.origin = data.get('payment_method_origin')
        method.issuer = data.get('payment_method_issuer')
        method.origin = data.get('payment_method_origin')

        method.tokenized_account_number = data.get('tokenized_account_number')
        method.tokenized_routing_number = data.get('tokenized_routing_number')
        method.tokenized_card_number = data.get('tokenized_card_number')

        method.given_name = data.get('payment_method_given_name')
        method.family_name = data.get('payment_method_family_name')
        method.full_name = data.get('payment_method_full_name')
        method.email_address = data.get('payment_method_email_address')
        method.customer_country_name = data.get('customer_country_name')
        method.customer_postal_code = data.get('customer_postal_code')

        method.billing_address_one = data.get('billing_address_one')
        method.billing_address_two = data.get('billing_address_two')
        method.billing_address_three = data.get('billing_address_three')
        method.billing_state = data.get('billing_state')
        method.billing_country_name = data.get('billing_country_name')
        method.billing_country_alpha2_code = data.get('billing_country_alpha2_code')
        method.billing_country_alpha3_code = data.get('billing_country_alpha3_code')
        method.billing_country_numeric_code = data.get('billing_country_numeric_code')
        method.billing_postal_code = data.get('billing_postal_code')

        method.payment_method_processor_id = data.get('payment_method_processor_id')
        method.payment_method_metadata = data.get('payment_method_metadata')
        method.is_primary = data.get('is_primary')
        method.is_enabled = data.get('is_enabled')
        method.created_at = data.get('payment_method_created_at')
        method.updated_at = data.get('payment_method_updated_at')

        return method
