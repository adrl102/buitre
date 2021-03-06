from flask import Blueprint, request, jsonify, g

from ..api import GetOpportunityService, CreateOpportunityService, ListOpportunitiesService, authenticate_user, get_request

from ..utils.exceptions import OpportunityNotFoundException

opportunity_api = Blueprint('opportunity_api', __name__)


@opportunity_api.route('/<int:opportunity_id>', methods=['GET'])
def get_opportunity(opportunity_id):
    response = {}
    response_code = 200

    try:
        response = GetOpportunityService.call({
            'opportunity_id': opportunity_id
        })
    except OpportunityNotFoundException as e:
        response['message'] = e.message
        response_code = 404

    return jsonify(response), response_code


@opportunity_api.route('/create', methods=['POST'])
@authenticate_user
def create_opportunity():
    rq = get_request(request)
    response = {}
    response_code = 200

    tags = rq.get('tags').split(',')
    pictures = rq.get('pictures').split(',')

    args = {
        'user_id': g.user_id,
        'name': rq.get('name'),
        'description': rq.get('description'),
        'address': rq.get('address'),
        'latitude': rq.get('latitude'),
        'longitude': rq.get('longitude'),
        'pictures': pictures,
        'tags': tags
    }

    try:
        CreateOpportunityService.call(args)
        response['message'] = "success"
    except Exception as e:
        response['message'] = e.message
        response_code = 500

    return jsonify(response), response_code


@opportunity_api.route('/search', methods=['GET'])
def search_opportunities():
    response = {}
    response_code = 200

    keywords = request.args.get('keywords')
    page = request.args.get('page')

    args = {
        'keywords': keywords,
        'page': int(page)
    }

    #try:
    opportunities = []
    db_opportunities = ListOpportunitiesService.call(args)
    for db_opportunity in db_opportunities:
        opportunity = {
            'id': db_opportunity['id'],
            'name': db_opportunity['name'],
            'distance': "5km",
            'picture': db_opportunity['main_picture'],
            'score': db_opportunity['score']
        }
        opportunities.append(opportunity)
    response['opportunities'] = opportunities
    # except Exception as e:
    #     response_code = 500
    #     response['message'] = e.__repr__()

    return jsonify(response), response_code
