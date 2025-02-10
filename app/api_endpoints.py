from datetime import datetime, timedelta

from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_login import current_user
from flask_login import login_required

from app.models import create_travel, SubscriptionPlan, TravelRoute, db, User, Destination, travel_route_destination
from app.utils import calc_price, calc_distance

api_bp = Blueprint('api', __name__)


@api_bp.route('/save_travel_route', methods=['POST'])
@swag_from({
    'tags': ['Travel Management'],
    'summary': 'Save a Travel Route',
    'description': 'Create a new travel route based on the provided subscription plan and destinations.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'subscription_plan': {'type': 'string'},
                    'destinations': {'type': 'array', 'items': {'type': 'string'}},
                    'comment_input': {'type': 'string'},
                    'email_input': {'type': 'string'}
                },
                'required': ['subscription_plan', 'destinations']
            }
        }
    ],
    'responses': {
        200: {'description': 'Successfully saved travel route'},
        400: {'description': 'Bad request'},
        401: {'description': 'Authentication required for this action'}
    }
})
def save_travel_route():
    data = request.get_json()

    email = data.get('email_input')

    try:
        if current_user.is_authenticated:
            create_travel(data['subscription_plan'], data['destinations'], data['comment_input'],
                          user_id=current_user.id)
        elif email:
            create_travel(data['subscription_plan'], data['destinations'], data['comment_input'], email=email)
        else:
            return jsonify({"error": "Authentication required for this action"}), 401

    except Exception as e:
        return jsonify(str(e)), 400
    return jsonify('ok'), 200


@api_bp.route('/calculate_travel_route', methods=['GET'])
@swag_from({
    'tags': ['Travel Management'],
    'summary': 'Calculate Travel Route Details',
    'description': 'Get pricing and estimated delivery dates for various subscription plans based on destinations.',
    'parameters': [
        {
            'name': 'destinations',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Comma-separated list of destination names. Example: Madrid,Barcelona,Valencia'
        }
    ],
    'responses': {
        200: {
            'description': 'Successful response with travel details',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string', 'description': 'Name of the subscription plan'},
                        'price': {'type': 'integer', 'description': 'Price of the subscription plan'},
                        'estimated_date': {'type': 'string', 'description': 'Estimated delivery date'},
                        'insurance_type': {'type': 'string', 'description': 'Type of insurance provided'},
                        'tracking': {'type': 'string', 'description': 'Tracking details'}
                    }
                }
            }
        },
        400: {'description': 'Invalid request'}
    }
})
def calculate_travel_route():
    destinations = request.args.get('destinations')
    if not destinations:
        return jsonify({'error': 'Destinations parameter is required'}), 400

    destinations = destinations.split(',')
    if len(destinations) < 2:
        return jsonify({'error': 'At least 2 destinations are required'}), 400

    existing_destinations = [d.name for d in Destination.query.filter(Destination.name.in_(destinations)).all()]
    if len(existing_destinations) != len(destinations):
        return jsonify({'error': 'One or more destinations do not exist'}), 400

    plans = SubscriptionPlan.query.order_by(SubscriptionPlan.price).all()
    response = []
    for i, plan in enumerate(plans):
        amount_of_days = len(destinations) + i * 3
        estimated_date = (datetime.now() + timedelta(days=amount_of_days)).strftime('%B %d')
        response.append({
            'name': plan.name,
            'price': plan.price,
            'estimated_date': estimated_date,
            'insurance_type': plan.insurance_type,
            'tracking': plan.tracking
        })
    return jsonify(response)


@api_bp.route('/calculate_distance_price', methods=['GET'])
@swag_from({
    'tags': ['Pricing'],
    'summary': 'Calculate Price and Distance',
    'description': 'Calculate the total distance and pricing for a specific plan based on destinations.',
    'parameters': [
        {
            'name': 'destinations',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Comma-separated list of destination names. Example: Madrid,Barcelona,Valencia'
        },
        {
            'name': 'plan',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Name of the subscription plan (Standard | Premium | Ultra)'
        }
    ],
    'responses': {
        200: {'description': 'Successful calculation of price and distance'},
        400: {'description': 'Invalid request'}
    }
})
def calculate_distance_price():
    destinations = request.args.get('destinations')
    if not destinations:
        return jsonify({'error': 'Destinations parameter is required'}), 400

    destinations = destinations.split(',')
    if len(destinations) < 2:
        return jsonify({'error': 'At least 2 destinations are required'}), 400

    existing_destinations = [d.name for d in Destination.query.filter(Destination.name.in_(destinations)).all()]
    if len(existing_destinations) != len(destinations):
        return jsonify({'error': 'One or more destinations do not exist'}), 400

    plan_arg = request.args.get('plan')
    if not plan_arg:
        return jsonify({'error': 'Plan parameter is required'}), 400
    plan = SubscriptionPlan.query.filter_by(name=plan_arg).first()
    if not plan:
        return jsonify({'error': 'Plan not found'}), 400

    response = {
        'price': calc_price(destinations, plan.price),
        'distance': calc_distance(destinations)
    }
    return jsonify(response)


def query_routes(user_id):
    user = User.query.filter_by(id=user_id).first()
    res = (
        db.session
        .query(
            TravelRoute.id,
            SubscriptionPlan.name,
            TravelRoute.date_of_start,
            TravelRoute.date_of_end,
            SubscriptionPlan.price,
            Destination.name
        )
        .join(SubscriptionPlan, TravelRoute.subscription_plan_id == SubscriptionPlan.id)
        .join(travel_route_destination, TravelRoute.id == travel_route_destination.c.travel_route_id)
        .join(Destination, travel_route_destination.c.destination_id == Destination.id)
        .filter((TravelRoute.user_id == user_id) | (TravelRoute.guest_email == user.email))
        .order_by(travel_route_destination.c.order)
        .all())

    return res


@cross_origin()
@api_bp.route('/get_routes/<int:user_id>', methods=['GET'])
@login_required
@swag_from({
    'tags': ['Route Management'],
    'summary': 'Get all travel routes for a user',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the user'
        }
    ],
    'responses': {
        200: {
            'description': 'List of routes for the user',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'plan': {'type': 'string'},
                        'date_of_start': {'type': 'string'},
                        'date_of_end': {'type': 'string'},
                        'price': {'type': 'number'},
                        'distance': {'type': 'number'},
                        'destinations': {'type': 'array', 'items': {'type': 'string'}}
                    }
                }
            }
        },
        404: {
            'description': 'No routes found for the user'
        }
    }
})
def get_routes(user_id):
    res = query_routes(user_id)

    if not res:
        return jsonify({'error': 'No routes found for the user'}), 404

    res2 = []
    for r in res:
        route = next((item for item in res2 if item['id'] == r[0]), None)
        if route:
            route['destinations'].append(r[5])
        else:
            res2.append({
                'id': r[0],
                'plan': r[1],
                'date_of_start': r[2].strftime('%d/%m/%Y'),
                'date_of_end': r[3].strftime('%d/%m/%Y'),
                'price_km': r[4],
                'destinations': [r[5]],
            })

    for route in res2:
        route['price'] = calc_price(route['destinations'], route['price_km'])
        route['distance'] = calc_distance(route['destinations'])
        route.pop('price_km')

    return jsonify(res2)


@api_bp.route('/get_route_data/<int:user_id>', methods=['GET'])
@login_required
@swag_from({
    'tags': ['Route Analytics'],
    'summary': 'Get summarized route data for a user',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the user'
        }
    ],
    'responses': {
        200: {
            'description': 'Summary of route data for the user',
            'schema': {
                'type': 'object',
                'properties': {
                    'total_routes': {'type': 'integer'},
                    'in_progress': {'type': 'integer'},
                    'total_distance': {'type': 'number'},
                    'subscription_data': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    }
                }
            }
        },
        404: {'description': 'No routes found for the user'}
    }
})
def get_route_data(user_id):
    res = query_routes(user_id)

    if not res:
        return jsonify({'error': 'No routes found for the user'}), 404

    res2 = []
    for r in res:
        route = next((item for item in res2 if item['id'] == r[0]), None)
        if route:
            route['destinations'].append(r[5])
        else:
            res2.append({
                'id': r[0],
                'plan': r[1],
                'in_progress': r[2] <= datetime.now().date() <= r[3],
                'destinations': [r[5]],
            })

    for route in res2:
        route['distance'] = calc_distance(route['destinations'])

    res3 = {
        'total_routes': len(res2),
        'in_progress': sum(1 for e in res2 if e['in_progress']),
        'total_distance': sum(e['distance'] for e in res2),
        'subscription_data': {}
    }

    for route in res2:
        plan = route['plan']
        if plan in res3['subscription_data']:
            res3['subscription_data'][plan] += 1
        else:
            res3['subscription_data'][plan] = 1

    res3['subscription_data'] = dict(sorted(res3['subscription_data'].items(),
                                            key=lambda item: SubscriptionPlan.query.filter_by(name=item[0]).first().id))

    print(res3['subscription_data'])
    return jsonify(res3)
