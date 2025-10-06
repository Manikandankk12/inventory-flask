from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Product, Location, ProductMovement
from forms import ProductForm, LocationForm, MovementForm
from sqlalchemy import func, and_

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me-for-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

# ----- Products -----
@app.route('/products')
def products_list():
    products = Product.query.order_by(Product.product_id).all()
    return render_template('products/list.html', products=products)

@app.route('/products/new', methods=['GET','POST'])
def product_create():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(product_id=form.product_id.data, name=form.name.data)
        db.session.add(p)
        db.session.commit()
        flash('Product created', 'success')
        return redirect(url_for('products_list'))
    return render_template('products/form.html', form=form, title="Create Product")

@app.route('/products/<string:product_id>/edit', methods=['GET','POST'])
def product_edit(product_id):
    p = Product.query.get_or_404(product_id)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        p.name = form.name.data
        db.session.commit()
        flash('Product updated', 'success')
        return redirect(url_for('products_list'))
    return render_template('products/form.html', form=form, title="Edit Product")

@app.route('/products/<string:product_id>')
def product_view(product_id):
    p = Product.query.get_or_404(product_id)
    movements = ProductMovement.query.filter_by(product_id=product_id).order_by(ProductMovement.timestamp.desc()).all()
    return render_template('products/view.html', product=p, movements=movements)

# ----- Locations -----
@app.route('/locations')
def locations_list():
    locations = Location.query.order_by(Location.location_id).all()
    return render_template('locations/list.html', locations=locations)

@app.route('/locations/new', methods=['GET','POST'])
def location_create():
    form = LocationForm()
    if form.validate_on_submit():
        l = Location(location_id=form.location_id.data, name=form.name.data)
        db.session.add(l)
        db.session.commit()
        flash('Location created', 'success')
        return redirect(url_for('locations_list'))
    return render_template('locations/form.html', form=form, title="Create Location")

@app.route('/locations/<string:location_id>/edit', methods=['GET','POST'])
def location_edit(location_id):
    l = Location.query.get_or_404(location_id)
    form = LocationForm(obj=l)
    if form.validate_on_submit():
        l.name = form.name.data
        db.session.commit()
        flash('Location updated', 'success')
        return redirect(url_for('locations_list'))
    return render_template('locations/form.html', form=form, title="Edit Location")

# ----- Movements -----
@app.route('/movements')
def movements_list():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements/list.html', movements=movements)

@app.route('/movements/new', methods=['GET','POST'])
def movement_create():
    form = MovementForm()
    form.product_id.choices = [(p.product_id, f"{p.product_id} - {p.name}") for p in Product.query.order_by(Product.product_id)]
    locs = [(None, '---')]
    locs += [(l.location_id, f"{l.location_id} - {l.name}") for l in Location.query.order_by(Location.location_id)]
    form.from_location.choices = [(l[0], l[1]) for l in locs]
    form.to_location.choices = [(l[0], l[1]) for l in locs]

    if form.validate_on_submit():
        m = ProductMovement(
            movement_id=form.movement_id.data,
            timestamp=form.timestamp.data or datetime.utcnow(),
            from_location=form.from_location.data or None,
            to_location=form.to_location.data or None,
            product_id=form.product_id.data,
            qty=form.qty.data
        )
        db.session.add(m)
        db.session.commit()
        flash('Movement recorded', 'success')
        return redirect(url_for('movements_list'))
    return render_template('movements/form.html', form=form, title="Record Movement")

# ----- Reports -----
@app.route('/reports/balances')
def report_balances():
    # Compute balances by product & location
    # Approach:
    # - For each location and product, sum qty where to_location==loc (IN) minus sum qty where from_location==loc (OUT)
    products = Product.query.order_by(Product.product_id).all()
    locations = Location.query.order_by(Location.location_id).all()

    # We compute a list of (product, location, qty)
    rows = []
    for p in products:
        for loc in locations:
            loc_id = loc.location_id
            in_sum = db.session.query(func.coalesce(func.sum(ProductMovement.qty), 0)).filter(
                ProductMovement.product_id==p.product_id,
                ProductMovement.to_location==loc_id
            ).scalar()
            out_sum = db.session.query(func.coalesce(func.sum(ProductMovement.qty), 0)).filter(
                ProductMovement.product_id==p.product_id,
                ProductMovement.from_location==loc_id
            ).scalar()
            balance = (in_sum or 0) - (out_sum or 0)
            if balance != 0:
                rows.append({'product': p, 'location': loc, 'qty': balance})
    return render_template('reports/balances.html', rows=rows, products=products, locations=locations)

if __name__ == '__main__':
    app.run(debug=True)
