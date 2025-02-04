from datetime import datetime, timedelta

from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from flask_login import login_required

from app.models import create_travel, SubscriptionPlan, TravelRoute, db, User, Destination, travel_route_destination

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
    destinations = request.args.getlist('destinations')
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
    destinations = request.args.getlist('destinations')
    plan_arg = request.args.get('plan')
    plan = SubscriptionPlan.query.filter_by(name=plan_arg).first()

    response = {
        'price': plan.price * len(destinations),
        'distance': len(destinations) * 100
    }
    return jsonify(response)


@api_bp.route('/api/get_routes/<int:user_id>', methods=['GET'])
# @login_required
def get_routes(user_id):
    user = User.query.filter_by(id=user_id).first()
    res = (db.session.query(TravelRoute.id, SubscriptionPlan.name, Destination.name)
           .join(SubscriptionPlan, TravelRoute.subscription_plan_id == SubscriptionPlan.id)
           .join(travel_route_destination, TravelRoute.id == travel_route_destination.c.travel_route_id)
           .join(Destination, travel_route_destination.c.destination_id == Destination.id)
           .filter((TravelRoute.user_id == user_id) | (TravelRoute.guest_email == user.email))
           .all())

    print(res)
    res2 = {}
    for r in res:
        if r[0] in res2:
            res2[r[0]]['destinations'].append(r[2])
        else:
            res2[r[0]] = {
                'plan': r[1],
                'destinations': [r[2]]
            }

    print(res2)
    return jsonify(res2)
