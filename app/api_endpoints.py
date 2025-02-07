from datetime import datetime, timedelta

from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from flask_login import login_required

from app.models import create_travel, SubscriptionPlan, TravelRoute, db, User, Destination, travel_route_destination
from app.utils import calc_price, calc_distance

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/save_travel_route', methods=['POST'])
def save_travel_route():
    data = request.get_json()

    email = data.get('email_input')
    if email:
        create_travel(data['suscription_plan'], data['destinations'], data['comment_input'], email=email)
    else:
        create_travel(data['suscription_plan'], data['destinations'], data['comment_input'], user_id=current_user.id)
    return jsonify("data")


@api_bp.route('/api/calculate_travel_route', methods=['GET'])
def calculate_travel_route():
    destinations = request.args.get('destinations')
    destinations = destinations.split(',')
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


@api_bp.route('/api/calculate_distance_price', methods=['GET'])
def calculate_distance_price():
    destinations = request.args.get('destinations')
    destinations = destinations.split(',')
    plan_arg = request.args.get('plan')
    plan = SubscriptionPlan.query.filter_by(name=plan_arg).first()

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
        .all())

    # print(res)
    return res


@api_bp.route('/api/get_routes/<int:user_id>', methods=['GET'])
# @login_required
def get_routes(user_id):
    res = query_routes(user_id)

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

    # print(res2)
    return jsonify(res2)


@api_bp.route('/api/get_route_data/<int:user_id>', methods=['GET'])
# @login_required
def get_route_data(user_id):
    res = query_routes(user_id)

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
        'suscription_data': {}
    }

    for route in res2:
        plan = route['plan']
        if plan in res3['suscription_data']:
            res3['suscription_data'][plan] += 1
        else:
            res3['suscription_data'][plan] = 1
    print(res3)

    return jsonify(res3)
