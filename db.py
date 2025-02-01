import os

from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# N:M metadata table
travel_route_destination = Table(
    'travel_route_destination',
    Base.metadata,
    Column(
        'travel_route_id', Integer,
        ForeignKey('travel_routes.id', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'destination_id', Integer,
        ForeignKey('destinations.id', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'order', Integer,
    )
)


class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    insurance_type = Column(String, nullable=False)
    tracking = Column(String, nullable=False)


class TravelRoute(Base):
    __tablename__ = 'travel_routes'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    comment = Column(String, nullable=False)
    date_of_start = Column(Date, nullable=False)
    subscription_plan_id = Column(Integer, ForeignKey('subscription_plans.id', ondelete='CASCADE'), nullable=False)
    subscription_plan = relationship('SubscriptionPlan', cascade='all, delete')
    destinations = relationship(
        'Destination',
        secondary=travel_route_destination,
        back_populates='travel_routes',
        cascade='all, delete'
    )


class Destination(Base):
    __tablename__ = 'destinations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    travel_routes = relationship(
        'TravelRoute',
        secondary=travel_route_destination,
        back_populates='destinations',
        cascade='all, delete'
    )


def create_destinations(session):
    destinations = [
        'La Corunya', 'Lugo', 'Pontevedra', 'Ourense', 'Leon', 'Asturias', 'Zamora', 'Salamanca', 'Caceres', 'Badajoz',
        'Huelva', 'Sevilla', 'Cadiz', 'Malaga', 'Cordoba', 'Ciudad Real', 'Toledo', 'Avila', 'Valladolid', 'Segovia',
        'Burgos', 'Palencia', 'Cantabria', 'Vizcaya', 'Guipuzcoa', 'Alava', 'La Rioja', 'Soria', 'Guadalajara',
        'Madrid',
        'Cuenca', 'Granada', 'Jaen', 'Almeria', 'Murcia', 'Albacete', 'Alicante', 'Valencia', 'Teruel', 'Castellon',
        'Zaragoza', 'Navarra', 'Lleida', 'Huesca', 'Girona', 'Barcelona', 'Tarragona', 'Menorca', 'Mallorca', 'Ibiza',
        'Cabrera', 'Formentera', 'Ceuta', 'La Palma', 'Melilla', 'Hierro', 'Gomera', 'Tenerife', 'Grancanaria',
        'Fuerteventura', 'Lanzarote'
    ]

    for name in destinations:
        destination = Destination(name=name)
        session.add(destination)


def create_subscription_plans(session):
    plans_data = [
        {"name": "Standard", "price": 10, "insurance_type": "1 month", "tracking": "Basic"},
        {"name": "Premium", "price": 15, "insurance_type": "6 months", "tracking": "24/7"},
        {"name": "Ultra", "price": 20, "insurance_type": "12 months", "tracking": "24/7"},
    ]

    for plan in plans_data:
        subscription_plan = SubscriptionPlan(**plan)
        session.add(subscription_plan)


def create_db():
    if not os.path.exists("travel_routes.db"):
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        create_subscription_plans(session)
        create_destinations(session)

        session.commit()
        session.close()

    else:
        Base.metadata.create_all(engine)


def create_travel(suscription_name, destinations, comment, email):
    Session = sessionmaker(bind=engine)
    session = Session()

    subscription_plan = session.query(SubscriptionPlan).filter_by(name=suscription_name).first()
    dests = session.query(Destination).filter(Destination.name.in_(destinations)).all()
    # print(subscription_plan.name)
    travel = TravelRoute(
        email=email,
        comment=comment,
        date_of_start=date.today(),
        subscription_plan=subscription_plan,
        destinations=dests
    )
    session.add(travel)
    session.commit()

    for order, destination in enumerate(dests, start=1):
        stmt = travel_route_destination.update().where(
            travel_route_destination.c.travel_route_id == travel.id,
            travel_route_destination.c.destination_id == destination.id
        ).values(order=order)
        session.execute(stmt)

    session.commit()
    session.close()


DATABASE_URL = "sqlite:///travel_routes.db"
engine = create_engine(DATABASE_URL)
create_db()
