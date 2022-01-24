"""reports_controller.py"""
# pylint: disable=unused-argument
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, abort, g
import pytz

from server.config.authentication import authentication
from server.repositories import reports_repository, merchant_repository
from server.models.person_model import Roles, MerchantRoles
from server.models.search_option_model import SearchOption
from server.utilities import garnish


tzone = 'Asia/Manila'
reports_blueprint = Blueprint('reports', __name__)


@reports_blueprint.route('/reports/<int:merchant_id>/revenue', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
@garnish.require_query_params(['startday', 'endday'])
def get_revenue_summary_by_date_range(merchant_id: int):
    search_option = SearchOption.map_from_query(request.args)
    merchant = g.merchant

    start_date, end_date = search_option.localize_start_date(tzone), search_option.localize_end_date(tzone)
    allowed_start_date = localize_date(datetime.now() - timedelta(days=90), tzone)
    allowed_end_date = localize_date(datetime.now() + (timedelta(days=1) - timedelta(milliseconds=1)), tzone)

    if not start_date:
        start_date = localize_date(datetime.now() - timedelta(days=7), tzone)
    if not end_date:
        end_date = localize_date(datetime.now(), tzone)
    if start_date < allowed_start_date or end_date > allowed_end_date:
        start_date = localize_date(datetime.now() - timedelta(days=7), tzone)
        end_date = localize_date(datetime.now(), tzone)
    end_date = end_date + (timedelta(days=1) - timedelta(milliseconds=1))

    revenues = reports_repository.get_revenue_summary(merchant, start_date, end_date)
    mapped_revenues = [{
        'transactionDate': r['transaction_date'].isoformat(),
        'totalBaseCurrency': r['total_base_currency'],
        'totalBaseAmount': float(r['total_base_amount']),
        'totalChargedCurrency': r['total_charged_currency'],
        'totalChargedAmount': float(r['total_charged_amount']),
        'totalTransactionCount': r['transaction_count']
    } for r in revenues]
    transaction_dates = [m['transactionDate'] for m in mapped_revenues]

    # append unavailable data
    while start_date < end_date:
        key_date = get_key_date(start_date)
        if key_date not in transaction_dates:
            mapped_revenues.append({
                'transactionDate': key_date,
                'totalBaseCurrency': mapped_revenues[0]['totalBaseCurrency']\
                    if mapped_revenues and mapped_revenues[0] else 'PHP',
                'totalBaseAmount': 0,
                'totalChargedCurrency': mapped_revenues[0]['totalChargedCurrency']\
                    if mapped_revenues and mapped_revenues[0] else 'PHP',
                'totalChargedAmount': 0,
                'totalTransactionCount': 0
            })

        start_date = start_date + timedelta(days=1)

    return jsonify({
        'revenues': mapped_revenues,
        'totalCount': len(mapped_revenues)
    }), 200


@reports_blueprint.route('/reports/<int:merchant_id>/payments', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
@garnish.require_query_params(['startday', 'endday'])
def get_transactions_by_date_range(merchant_id: int):
    search_option = SearchOption.map_from_query(request.args)
    merchant = g.merchant

    start_date, end_date = search_option.localize_start_date(tzone), search_option.localize_end_date(tzone)
    if not start_date:
        start_date = localize_date(datetime.now() - timedelta(days=7), tzone)
    if not end_date:
        end_date = localize_date(datetime.now(), tzone)
    end_date = end_date + (timedelta(days=1) - timedelta(milliseconds=1))

    payments = reports_repository.get_project_payment_type_summary(merchant, start_date, end_date)
    payment_types = list({p['paymentType'] for p in payments})
    pre_mapped_payments = {}
    mapped_payments = []

    for p in payments:
        project_name = p['projectName']
        payment_type = p['paymentType']
        amount = p['baseAmount']
        currency = p['baseCurrency']
        if project_name in pre_mapped_payments:
            pre_mapped_payments[project_name][payment_type] = amount
        else:
            pre_mapped_payments[project_name] = {payment_type: amount, 'currency': currency}

    for key in pre_mapped_payments:
        payment = pre_mapped_payments[key]
        payment['projectName'] = key
        for pt in payment_types:
            if pt not in payment:
                payment[pt] = 0
        mapped_payments.append(payment)

    return jsonify({
        'payments': mapped_payments,
        'paymentTypes': payment_types
    }), 200


@reports_blueprint.route('/reports/<int:merchant_id>/total-payments-by-type', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def get_merchant_total_payments_by_type(merchant_id: int):
    merchant = g.merchant

    payment_type_group = reports_repository.get_total_payments_by_type(merchant)
    return jsonify(payment_type_group), 200


@reports_blueprint.route('/reports/<int:merchant_id>/payments-by-project-payment-type', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
@garnish.require_query_params(['startday', 'endday'])
def get_payments_by_project_payment_type(merchant_id: int):
    current_user = g.user
    merchant = g.merchant
    search_option = SearchOption.map_from_query(request.args)

    start_date, end_date = search_option.localize_start_date(tzone), search_option.localize_end_date(tzone)
    if not start_date:
        start_date = localize_date(datetime.now() - timedelta(days=7), tzone)
    if not end_date:
        end_date = localize_date(datetime.now(), tzone)
    end_date = end_date + timedelta(days=1)

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get the data'})

    payment_data = reports_repository.get_paid_payments_by_project_report(
        merchant=merchant,
        start_date=start_date,
        end_date=end_date)

    # Set key for the view loop
    payload = []
    for row in payment_data:
        item = dict(row)
        item['key'] = f"{row['project']}-{row['source']}-{row['paymentType']}"
        payload.append(item)

    return jsonify(payload), 200

@reports_blueprint.route('/reports/summary-payments-by-project-payment-type', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.USER, MerchantRoles.NO_ACCESS)
def get_summary_payments_by_project_payment_type():
    missing_params = [k for k in ['merchant', 'startday', 'endday'] if k not in request.args.keys()]
    if len(missing_params) == 1:
        if('startday' in missing_params or 'endday' in missing_params):
            abort(400, {'message': 'Please select a valid report date'})
        else:
            abort(400, {'message': 'Please select a valid {}'.format(missing_params[0])})
    if len(missing_params) > 1:
        if(('startday' in missing_params or 'endday' in missing_params) and 'merchant' in missing_params):
            abort(400, {'message': 'Please select a valid merchant and report date'})
        elif('startday' in missing_params or 'endday' in missing_params and 'merchant' not in missing_params):
            abort(400, {'message': 'Please select a valid report date'})
        else:
            abort(400, {'message': 'Please select a valid merchant'})

    current_user = g.user
    search_option = SearchOption.map_from_query(request.args)
    merchant = merchant_repository.find_merchant_by_code(search_option.merchant_code)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    # start_date, end_date = search_option.start_date, search_option.end_date
    # if not start_date:
    #     start_date = datetime.now() - timedelta(days=7)
    # if not end_date:
    #     end_date = datetime.now()
    # end_date = end_date + timedelta(days=1)

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get the data'})

    payment_data = reports_repository.get_summary_payments_by_payment_type(
        merchant=merchant,
        search_option=search_option
        )

    # Set key for the view loop
    payload = []
    for row in payment_data:
        item = dict(row)
        item['key'] = f"{row['project']}-{row['category']}"
        payload.append(item)

    return jsonify(payload), 200


@reports_blueprint.route('/reports/<int:merchant_id>/payment-method-issuers', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
@garnish.require_query_params(['startday', 'endday'])
def get_payment_method_issuers(merchant_id: int):
    current_user = g.user
    merchant = g.merchant
    search_option = SearchOption.map_from_query(request.args)

    start_date, end_date = search_option.localize_start_date(tzone), search_option.localize_end_date(tzone)
    if not start_date:
        start_date = localize_date(datetime.now() - timedelta(days=7), tzone)
    if not end_date:
        end_date = localize_date(datetime.now(), tzone)
    end_date = end_date + timedelta(days=1)

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get data'})

    payment_data = reports_repository.get_payment_method_reports(
        merchant=merchant,
        start_date=start_date,
        end_date=end_date)

    stats_data = reports_repository.get_payment_statistics(
        merchant=merchant,
        start_date=start_date,
        end_date=end_date)

    # Set key for the view loop
    payload = []
    for row in payment_data:
        item = dict(row)
        item['key'] = f"{row['method']}-{row['origin']}-{row['provider']}"
        payload.append(item)

    return jsonify({
        'issuers': payload,
        'stats': stats_data
    }), 200

@reports_blueprint.route('/reports/payment-method-issuers-admin', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_role(Roles.SYSADMIN, MerchantRoles.NO_ACCESS)
def get_payment_method_issuers_admin():
    missing_params = [k for k in ['merchant', 'startday', 'endday'] if k not in request.args.keys()]
    if len(missing_params) == 1:
        print(missing_params)
        if('startday' in missing_params or 'endday' in missing_params):
            abort(400, {'message': 'Please select a valid report date'})
        else:
            abort(400, {'message': 'Please select a valid {}'.format(missing_params[0])})
    if len(missing_params) > 1:
        if(('startday' in missing_params or 'endday' in missing_params) and 'merchant' in missing_params):
            abort(400, {'message': 'Please select a valid merchant and report date'})
        elif('startday' in missing_params or 'endday' in missing_params and 'merchant' not in missing_params):
            abort(400, {'message': 'Please select a valid report date'})
        else:
            abort(400, {'message': 'Please select a valid merchant'})


    current_user = g.user
    search_option = SearchOption.map_from_query(request.args)
    merchant = merchant_repository.find_merchant_by_code(search_option.merchant_code)


    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    start_date, end_date = search_option.start_date, search_option.end_date
    if not start_date:
        start_date = datetime.now() - timedelta(days=7)
    if not end_date:
        end_date = datetime.now()
    end_date = end_date + timedelta(days=1)

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get data'})

    payment_data = reports_repository.get_payment_method_reports_admin(
        merchant=merchant,
        start_date=start_date,
        end_date=end_date)

    stats_data = reports_repository.get_payment_statistics(
        merchant=merchant,
        start_date=start_date,
        end_date=end_date)

    # Set key for the view loop
    payload = []
    for row in payment_data:
        item = dict(row)
        item['key'] = f"{row['method']}-{row['origin']}-{row['provider']}"
        payload.append(item)

    return jsonify({
        'issuers': payload,
        'stats': stats_data
    }), 200


####################################################
####################################################

def get_key_date(dt: datetime):
    return str(dt.year)\
        + '-' + (str(dt.month) if dt.month > 9 else ('0' + str(dt.month)))\
        + '-' + (str(dt.day) if dt.day > 9 else ('0' + str(dt.day)))


def localize_date(dt: datetime, t_zone='Asia/Manila'):
    return pytz.timezone(t_zone).localize(dt, is_dst=None)
