from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date, datetime, timedelta

db = SQLAlchemy()

travel_route_destination = db.Table(
    'travel_route_destination',
    db.Column('travel_route_id', db.Integer, db.ForeignKey('travel_routes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('destination_id', db.Integer, db.ForeignKey('destinations.id', ondelete='CASCADE'), primary_key=True),
    db.Column('order', db.Integer)
)


class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    insurance_type = db.Column(db.String, nullable=False)
    tracking = db.Column(db.String, nullable=False)


class TravelRoute(db.Model):
    __tablename__ = 'travel_routes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    guest_email = db.Column(db.String, nullable=True)
    comment = db.Column(db.String, nullable=False)
    date_of_start = db.Column(db.Date, nullable=False)
    date_of_end = db.Column(db.Date, nullable=False)
    subscription_plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id', ondelete='CASCADE'),
                                     nullable=False)

    subscription_plan = db.relationship('SubscriptionPlan', cascade='all, delete')
    destinations = db.relationship('Destination', secondary=travel_route_destination, back_populates='travel_routes',
                                   cascade='all, delete')


class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    travel_routes = db.relationship('TravelRoute', secondary=travel_route_destination, back_populates='destinations',
                                    cascade='all, delete')


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=True)
    company_name = db.Column(db.String(20), nullable=True)


def create_travel(subscription_plan_name, destination_names, comment, email=None, user_id=None):
    subscription_plan = SubscriptionPlan.query.filter_by(name=subscription_plan_name).first()
    if not subscription_plan:
        raise ValueError(f"Subscription plan '{subscription_plan_name}' does not exist.")

    destination_dict = {destination.name: destination for destination in
                        Destination.query.filter(Destination.name.in_(destination_names)).all()}
    destinations = [destination_dict[name] for name in destination_names if name in destination_dict]

    if len(destinations) != len(destination_names):
        missing_destinations = set(destination_names) - {d.name for d in destinations}
        raise ValueError(f"Some destinations do not exist in the database: {missing_destinations}")

    plan_days_offset = {
        'Standard': 0,
        'Premium': 1,
        'Ultra': 2
    }.get(subscription_plan.name, 0)

    amount_of_days = len(destinations) + plan_days_offset * 3
    estimated_date = datetime.now() + timedelta(days=amount_of_days)

    travel_route = TravelRoute(
        user_id=user_id,
        guest_email=email if not user_id else None,
        comment=comment,
        date_of_start=date.today(),
        date_of_end=estimated_date,
        subscription_plan=subscription_plan,
        destinations=destinations
    )

    db.session.add(travel_route)
    db.session.commit()

    for order, destination in enumerate(destinations, start=1):
        stmt = travel_route_destination.update().where(
            travel_route_destination.c.travel_route_id == travel_route.id,
            travel_route_destination.c.destination_id == destination.id
        ).values(order=order)
        db.session.execute(stmt)

    db.session.commit()
