""" transaction_controller.py """
# pylint: disable=unused-argument
from io import StringIO
from datetime import datetime
import pandas as pd
from flask import Blueprint, jsonify, abort, request, g, Response
from server.config.logger import log
from server.config.authentication import authentication
from server.models.search_option_model import SearchOption
from server.models.person_model import Roles, MerchantRoles
from server.utilities.context_manager import open_transaction_context, ContextStatus
from server.repositories import transaction_repository


transaction_blueprint = Blueprint('transaction', __name__)

@transaction_blueprint.route('/merchants/<int:merchant_id>/transactions/search', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def search_transactions(merchant_id: int):
    fn = 'search_transactions'
    current_user = g.user

    with open_transaction_context(user=current_user, source='transactions') as context:
        context.propset(action='Search')
        search_option = SearchOption.map_from_query(request.args)

        if not search_option.search_term:
            context.propset(
                status=ContextStatus.ERROR,
                description='Empty search term',
                metadata={})
            return jsonify({}), 204

        transactions, total_count = transaction_repository.search_transactions(search_option, current_user)
        serialized_transactions = [tx.serialize() for tx in transactions]

        context.propset(
            status=ContextStatus.SUCCESS,
            description=f'{current_user.name} has searched for "{search_option.search_term}"',
            metadata={
                'page': search_option.page,
                'size': search_option.size,
                'project': search_option.project,
                'startdate': str(search_option.start_date),
                'enddate': str(search_option.end_date),
                'status': search_option.status,
                'query': search_option.search_term,
                'totalCount': total_count
            })
        log.info(f'{fn}: {current_user} searches for {search_option.search_term}')
        return jsonify({
            'transactions': serialized_transactions,
            'totalCount': total_count,
            'page': search_option.page,
            'size': search_option.size
        }), 200


@transaction_blueprint.route('/merchants/<int:merchant_id>/transactions/<transaction_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def get_merchant_transaction_by_id(merchant_id: str, transaction_id: str):
    merchant = g.merchant

    transaction = transaction_repository.find_transaction_by_external_transaction_id(transaction_id, merchant)
    if not transaction:
        abort(404, {'message': 'Transaction does not exist'})

    serialized_transaction = transaction.serialize()
    return jsonify(serialized_transaction), 200


@transaction_blueprint.route('/transactions/export', methods=['GET'])
def export_transactions():
    export_token = request.args.get('token')

    (is_success, current_user) = authentication.validate_export_token(export_token)
    if not is_success:
        abort(401, {'message': 'Unauthorized to export transactions'})

    if not current_user.is_allowed(MerchantRoles.MERCHANT_ADMIN):
        abort(403, {'message': 'You are not allowed to export transactions'})

    search_option = SearchOption.map_from_query(request.args)

    # The current export limit is 100 records only for search
    search_option.page = 1
    search_option.size = 100
    transactions, _ = transaction_repository.search_transactions(search_option, current_user)

    csv_content = build_csv(transactions)
    filename = 'transactions-{}.csv'.format(datetime.now().strftime('%Y-%m-%d'))

    response = Response(csv_content, 200)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'filename="{}"'.format(filename)
    return response

def build_csv(transactions: list) -> str:
    headers = [
        'transactionId',
        'referenceId',
        'xsrfKey',
        'projectName',
        'projectCategory',
        'merchantId',
        'merchantName',
        'billTotal',
        'billBase',
        'billFee',
        'billConverted',
        'paymentMethod',
        'transactionType',
        'paymentMode',
        'paymentType',
        'status',
        'customerName',
        'customerEmail',
        'customerPhone',
        'createdAt',
        'expiresAt'
    ]

    serialized_data = [t.serialize() for t in transactions]
    df = pd.DataFrame(serialized_data, columns=headers)

    # Uses buffer instead of file on to_csv
    # pandas has good built-in escape for exporting CSV
    buf = StringIO()
    df.to_csv(path_or_buf=buf, index=False)
    value = buf.getvalue()
    buf.close()
    return value
