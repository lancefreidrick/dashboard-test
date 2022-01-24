""" project_controller.py """
# pylint: disable=unused-argument
from flask import Blueprint, abort, jsonify, g, request

from server.config.logger import log
from server.config.authentication import authentication
from server.models.person_model import Roles, MerchantRoles
from server.models.search_option_model import SearchOption
from server.models.project_model import Project
from server.repositories import merchant_repository, project_repository

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route('/merchants/<int:merchant_id>/projects', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def get_projects(merchant_id: int):
    current_user = g.user
    merchant = merchant_repository.find_merchant_by_id(merchant_id)
    if not merchant:
        abort(404, {'message': 'Merchant does not exist'})

    # if not merchant.can_manage_projects:
    #     abort(403, {'message': 'You are not allowed to get projects'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to get projects'})

    search_option = SearchOption.map_from_query(request.args)
    merchant_projects, total_count = project_repository.get_merchant_projects(
        merchant=merchant,
        search_option=search_option)
    serialize_merchant_projects = [p.serialize() for p in merchant_projects]
    return jsonify({
        'projects': serialize_merchant_projects,
        'totalCount': total_count,
    }), 200


@project_blueprint.route('/merchants/<int:merchant_id>/projects/<int:project_id>', methods=['GET'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_AGENT)
def find_project_by_id(merchant_id: int, project_id: int):
    current_user = g.user
    fn = 'find_project_by_id'

    merchant = g.merchant
    if not current_user.is_internal() and not merchant.can_manage_projects:
        abort(403, {'message': 'You are not allowed to get this project'})

    project = project_repository.find_merchant_project_by_project_id(
        merchant=merchant,
        project_id=project_id)
    if not project:
        log.error(f'{fn}: Project does not exist')
        abort(404, {'message': 'Project does not exist'})

    if not project.is_enabled:
        log.error(f'{fn}: Project has been already removed from the list')
        abort(404, {'message': 'Project does not exist'})

    serialize_merchant_project = project.serialize()
    return jsonify(serialize_merchant_project), 200


@project_blueprint.route('/merchants/<int:merchant_id>/projects', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_STAFF)
def create_project(merchant_id: int):
    current_user = g.user
    fn = 'create_project'

    merchant = g.merchant
    if not current_user.is_internal() and not merchant.can_manage_projects:
        abort(403, {'message': 'You are not allowed to create a project'})

    is_valid, validated_data = Project.validate_submitted_info(request.get_json())
    if not is_valid:
        log.error(f'{fn}: Validation error on project {validated_data}')
        abort(400, {
            'message': 'Submitted project has form validation errors',
            'fields': validated_data.messages
        })

    project = Project()
    project.name = validated_data.get('name')
    project.category = validated_data.get('category')
    project.description = validated_data.get('description')
    project.project_key = project.generate_key(merchant.merchant_code)

    project_id, is_created, message = project_repository.create_merchant_project(
        merchant=merchant,
        project=project)
    if not is_created:
        log.error(f'{fn}: Project was not saved: {message}')
        abort(400, {'message': 'Submitted project has not been created. Please try again later.'})

    return jsonify({
        'projectId': project_id,
        'key': project.project_key,
        'message': 'Project has been created'
    }), 201


@project_blueprint.route('/merchants/<int:merchant_id>/projects/<int:project_id>', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def update_project(merchant_id: int, project_id: int):
    current_user = g.user
    fn = 'update_project'

    merchant = g.merchant
    if not current_user.is_internal() and not merchant.can_manage_projects:
        abort(403, {'message': 'You are not allowed to update the project'})

    project = project_repository.find_merchant_project_by_project_id(
        merchant=merchant,
        project_id=project_id)
    if not project:
        log.error(f'{fn}: Project does not exist')
        abort(404, {'message': 'Project does not exist'})

    if not project.is_enabled:
        log.error(f'{fn}: Project has been already removed from the list')
        abort(404, {'message': 'Project does not exist'})

    is_valid, validated_data = Project.validate_submitted_info(request.get_json())
    if not is_valid:
        log.error(f'{fn}: Validation error on project {validated_data}')
        abort(400, {
            'message': 'Submitted project has form validation errors',
            'fields': validated_data.messages
        })

    project.name = validated_data.get('name')
    project.category = validated_data.get('category')
    project.project_key = project.generate_key(merchant.merchant_code)
    project.description = validated_data.get('description')

    is_updated, message = project_repository.update_merchant_project(
        merchant=merchant,
        project=project)
    if not is_updated:
        log.error(f'{fn}: Project was not saved: {message}')
        abort(400, {'message': 'Submitted project has not been saved. Please try again later.'})

    return jsonify({
        'key': project.project_key,
        'message': 'Project has been updated'
    }), 200


@project_blueprint.route('/merchants/<int:merchant_id>/projects/<int:project_id>/publish', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def publish_project(merchant_id: int, project_id: int):
    fn = 'publish_project'

    current_user = g.user
    merchant = g.merchant
    if not current_user.is_internal() and not merchant.can_manage_projects:
        abort(403, {'message': 'You are not allowed to publish the project'})

    project = project_repository.find_merchant_project_by_project_id(
        merchant=merchant,
        project_id=project_id)
    if not project:
        log.error(f'{fn}: Project does not exist')
        abort(404, {'message': 'Project does not exist'})

    if not project.is_enabled:
        log.error(f'{fn}: Project has been already removed from the list')
        abort(404, {'message': 'Project does not exist'})

    if project.is_active:
        log.error(f'{fn}: Project is already published')
        abort(400, {'message': 'Project has already been published'})

    is_published, message = project_repository.publish_merchant_project(merchant, project)
    if not is_published:
        log.error(f'{fn}: Project was not published: {message}')
        abort(400, {'message': 'Project was not published'})

    log.info(f'{fn}: Project {project} was published for {merchant} by {current_user}')
    return jsonify({ 'message': 'Project has been published' }), 200


@project_blueprint.route('/merchants/<int:merchant_id>/projects/<int:project_id>/disable', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def disable_project(merchant_id: int, project_id: int):
    fn = 'disable_project'

    current_user = g.user
    merchant = g.merchant
    if not current_user.is_internal() and not merchant.can_manage_projects:
        abort(403, {'message': 'You are not allowed to disable the project'})

    if not current_user.is_internal() and merchant.merchant_code not in current_user.scopes:
        abort(403, {'message': 'You are not allowed to disable the project'})

    project = project_repository.find_merchant_project_by_project_id(
        merchant=merchant,
        project_id=project_id)
    if not project:
        log.error(f'{fn}: Project does not exist')
        abort(404, {'message': 'Project does not exist'})

    if not project.is_enabled:
        log.error(f'{fn}: Project has been already removed from the list')
        abort(404, {'message': 'Project does not exist'})

    if not project.is_active:
        log.error(f'{fn}: Project is already disabled')
        abort(400, {'message': 'Project has already been disabled'})

    is_disabled, message = project_repository.disable_merchant_project(merchant, project)
    if not is_disabled:
        log.error(f'{fn}: Project was not disabled: {message}')
        abort(400, {'message': 'Project was not disabled'})

    log.info(f'{fn}: Project {project} was disabled for {merchant} by {current_user}')
    return jsonify(), 204


@project_blueprint.route('/merchants/<int:merchant_id>/projects/<int:project_id>', methods=['DELETE'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def delete_project(merchant_id: int, project_id: int):
    fn = 'delete_project'

    current_user = g.user
    merchant = g.merchant
    if not current_user.is_internal() and not merchant.can_manage_projects:
        abort(403, {'message': 'You are not allowed to delete the project'})

    project = project_repository.find_merchant_project_by_project_id(
        merchant=merchant,
        project_id=project_id)
    if not project:
        log.error(f'{fn}: Project does not exist')
        abort(404, {'message': 'Project does not exist'})

    if not project.is_enabled:
        log.error(f'{fn}: Project is disabled')
        abort(404, {'message': 'Project does not exist'})

    is_removed, message = project_repository.delete_merchant_project(merchant, project)
    if not is_removed:
        log.error(f'{fn}: Project was not deleted: {message}')
        if message == 'Project has existing transactions':
            abort(400, {'message': 'Project has already existing transactions.'})
        else:
            abort(400, {'message': 'Project was not deleted from the list.'})

    log.info(f'{fn}: Project {project} was deleted for {merchant} by {current_user}')
    return jsonify(), 204


@project_blueprint.route('/merchants/<int:merchant_id>/projects/<int:project_id>/metadata', methods=['POST'])
@authentication.jwt_required
@authentication.min_access_merchant_role(Roles.USER, MerchantRoles.MERCHANT_ADMIN)
def update_project_metadata(merchant_id: int, project_id: int):
    fn = 'update_project_metadata'

    merchant = g.merchant
    if not merchant.can_manage_projects:
        abort(403, {'message': 'You are not allowed to update the project metadata'})

    project = project_repository.find_merchant_project_by_project_id(
        merchant=merchant,
        project_id=project_id)
    if not project:
        log.error(f'{fn}: Project does not exist')
        abort(404, {'message': 'Project does not exist'})

    if not project.is_enabled:
        log.error(f'{fn}: Project is disabled')
        abort(404, {'message': 'Project does not exist'})

    is_valid, validated_content = Project.validate_metadata_fields(request.get_json())
    if not is_valid:
        log.error(f'{fn}: Project metadata has invalid schema {validated_content}')
        abort(400, {
            'message': 'Submitted project has form validation errors',
            'fields': validated_content.messages
        })

    project.project_fields = project.project_fields or {}
    project.project_fields['fields'] = validated_content

    is_updated, message = project_repository.update_merchant_project_metadata(project)
    if not is_updated:
        log.error(f'{fn}: Project metadata was not updated: {message}')
        abort(400, {'message': 'Project metadata was not updated'})

    log.info(f'{fn}: Project metadata has been updated ({message})')
    return jsonify({'message': 'Project metadata has been updated'}), 200
