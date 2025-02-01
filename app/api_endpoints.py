from flask import Blueprint, render_template, redirect, url_for, request, jsonify

from app.models import create_travel

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/save_travel_route', methods=['POST'])
def save_travel_route():
    data = request.get_json()
    print(data)
    create_travel(data['suscription_plan'], data['destinations'], data['comment_input'], data['email_input'])

    return jsonify("data")
