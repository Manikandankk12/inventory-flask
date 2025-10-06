from app import app
from models import db, Product, Location, ProductMovement
from datetime import datetime, timedelta
import random

with app.app_context():
    db.create_all()

    # Create products
    products = [
        Product(product_id='P001', name='Product A'),
        Product(product_id='P002', name='Product B'),
        Product(product_id='P003', name='Product C'),
        Product(product_id='P004', name='Product D'),
    ]
    for p in products:
        if not Product.query.get(p.product_id):
            db.session.add(p)

    # Create locations
    locations = [
        Location(location_id='L001', name='Warehouse X'),
        Location(location_id='L002', name='Warehouse Y'),
        Location(location_id='L003', name='Warehouse Z'),
    ]
    for l in locations:
        if not Location.query.get(l.location_id):
            db.session.add(l)

    db.session.commit()

    # Generate ~20 movements (inbound, outbound, transfers)
    movements = []
    now = datetime.utcnow()
    movement_count = 20
    for i in range(1, movement_count + 1):
        pid = random.choice(['P001', 'P002', 'P003', 'P004'])
        # Randomly choose inbound, outbound, or transfer
        t = random.choice(['in', 'out', 'transfer'])
        qty = random.randint(1, 20)
        if t == 'in':
            m = ProductMovement(
                movement_id=f'M{i:03d}',
                timestamp=now - timedelta(hours=i),
                from_location=None,
                to_location=random.choice(['L001', 'L002', 'L003']),
                product_id=pid,
                qty=qty
            )
        elif t == 'out':
            m = ProductMovement(
                movement_id=f'M{i:03d}',
                timestamp=now - timedelta(hours=i),
                from_location=random.choice(['L001','L002','L003']),
                to_location=None,
                product_id=pid,
                qty=qty
            )
        else: # transfer
            fr = random.choice(['L001','L002','L003'])
            to = random.choice([l for l in ['L001','L002','L003'] if l!=fr])
            m = ProductMovement(
                movement_id=f'M{i:03d}',
                timestamp=now - timedelta(hours=i),
                from_location=fr,
                to_location=to,
                product_id=pid,
                qty=qty
            )
        if not ProductMovement.query.get(m.movement_id):
            db.session.add(m)

    db.session.commit()
    print("Seed data created.")
