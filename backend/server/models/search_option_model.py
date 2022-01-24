import traceback
import re
from datetime import timedelta
from dateutil import parser as dtp
import pytz


class SearchOption:
    def __init__(self):
        self.search_term = None
        self.project = None
        self.project_name = None
        self.project_category = None
        self.payment_type = None
        self.status = None
        self.page = 1
        self.size = 10
        self.settlement_status = None
        self.settlement_reference_id = None
        self.show_incomplete = None
        self.invoice_id = None
        self.merchant_id = None
        self.merchant_code = None
        self.system_role = None
        self.merchant_role = None
        self.is_enabled = None
        self.payment_method = None
        # There are instances that you have to check dates as None
        #   instead having the default of today
        self.start_date = None
        self.end_date = None
        self.reporting_date = None
        self.due_date = None

    def skip(self):
        return (self.page - 1) * self.size

    def localize_start_date(self, tzone='Asia/Manila'):
        if not self.start_date:
            return None
        return pytz.timezone(tzone).localize(self.start_date, is_dst=None)

    def localize_end_date(self, tzone='Asia/Manila'):
        if not self.end_date:
            return None
        return pytz.timezone(tzone).localize(self.end_date, is_dst=None)

    def reporting_date_at_four(self, tzone='Asia/Manila'):
        if not self.reporting_date:
            return None, None

        base = self.reporting_date
        # e.g. August 10 is (August 9, 4:01pm - August 10, 4:00pm)
        start_date = pytz.timezone(tzone).\
            localize(base - timedelta(hours=8, minutes=1), is_dst=None)
        end_date = pytz.timezone(tzone).\
            localize(base + timedelta(hours=16, milliseconds=9999), is_dst=None)
        return start_date, end_date

    def due_date_range(self, tzone='Asia/Manila'):
        if not self.due_date:
            return None, None

        start_date = pytz.timezone(tzone)\
            .localize(self.due_date, is_dst=None)
        end_date = pytz.timezone(tzone)\
            .localize(self.due_date + timedelta(days=1), is_dst=None)
        return start_date, end_date

    @property
    def custom_field(self):
        if not self.search_term:
            return None
        #   search format is "cf-{customFieldName}:{customeFieldValue}"
        finds = re.findall('cf-[a-zA-Z0-9]+:[a-zA-Z0-9]+', self.search_term)
        if not finds:
            return None

        # placeholder for all the project fields
        project_field_list = []
        project_field_dict = {}

        # creates dictionary matching the mongodb query
        for find in finds:
            project_field_dict["$elemMatch"] = {
                'name' : re.search('cf-(.*):', find).group(1),
                "value": re.search(':(.*)', find).group(1)}
            project_field_list.append(project_field_dict)

        all_project_field_dict = {"$all":project_field_list}
        return all_project_field_dict

    @property
    def reference_id(self):
        if not self.search_term:
            return None

        matches = re.match('^QW-[EPSI]-[A-Z0-9]+$', self.search_term)
        if not matches:
            return None

        return matches.string

    @property
    def transaction_id(self):
        if not self.search_term:
            return None

        matches = re.match('^[A-Z0-9]{16}$', self.search_term)
        if not matches:
            return None

        return matches.string

    @property
    def email(self):
        if not self.search_term:
            return None

        matches = re.match('^(?=.{5,70}$)[^\\s@]+@[^\\s@]+\\.[^\\s@]+$', self.search_term)
        if not matches:
            return None

        return matches.string

    @property
    def last_term(self):
        #this will be the query for the customer name
        if not self.search_term:
            return None
        finds = re.findall('cf-[a-zA-Z0-9]+:[a-zA-Z0-9]+', self.search_term)
        final_query = self.search_term
        for find in finds:
            final_query = final_query.replace(find, '').strip()

        return final_query

    @staticmethod
    def map_from_query(query: dict):
        """
        Maps the request query values into SearchOption
        :param query: Dictionary object of request args
        """
        search_option = SearchOption()
        try:
            search_option.search_term = query.get('query')
            search_option.merchant_id = int(query.get('mid') or 0) or None
            search_option.merchant_code = query.get('merchant')
            search_option.system_role = query.get('systemRole')\
                if query.get('systemRole') is not None else None
            search_option.merchant_role = int(query.get('merchantRole'))\
                if query.get('merchantRole') is not None else None
            search_option.is_enabled = query.get('deactivated') != 'true'
            search_option.project = int(query.get('project')) if query.get('project') else None
            search_option.project_name = query.get('projectName') or None
            search_option.project_category = query.get('projectCategory') or None
            search_option.payment_type = query.get('paymentType')
            search_option.status = query.get('status')
            search_option.page = int(query.get('page') or 1)
            search_option.size = int(query.get('size') or 10)
            search_option.start_date = dtp.parse(query.get('startday'))\
                if query.get('startday') is not None else None
            search_option.end_date = dtp.parse(query.get('endday'))\
                if query.get('endday') is not None else None
            search_option.reporting_date = dtp.parse(query.get('reportdate'))\
                if query.get('reportdate') is not None else None
            search_option.due_date = dtp.parse(query.get('duedate'))\
                if query.get('duedate') is not None else None
            search_option.settlement_status = query.get('settlementstatus')
            search_option.settlement_reference_id = query.get('settlementrefid')
            search_option.show_incomplete = 1 if query.get('showinc') == 'true' else None
            search_option.invoice_id = query.get('invoiceId')
            search_option.payment_method = query.get('paymentMethod')
        except ValueError:
            traceback.print_exc()
        return search_option
