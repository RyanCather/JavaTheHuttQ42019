from app import app, db
from app.forms import RegistrationForm, OrderForm, ProductRegistrationForm, LoginForm, ProductOrderForm, \
    ResetPasswordForm, EditUserForm
from app.models import Order, Product, User
from flask import render_template, redirect, flash, request, url_for, Markup
from flask_login import logout_user, current_user, login_required, login_user
from sqlalchemy import text
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/static/productimages'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", user=current_user), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html", user=current_user), 500


# Main Routes

@app.route('/')
@app.route('/index')
def main_page():
    # Useful for determining file structure formats....
    # print(os.name)
    # print(platform.system())
    return render_template('index.html', title='Home', user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@app.route('/user')
@login_required
def user_details():
    return render_template("user.html", title="User Details", user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main_page'))
    return render_template('login.html', title='Sign In', form=form, user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_administrator="Regular")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, user=current_user)


@app.route('/report/listallusers')
def display_users():
    sql = text('select username, id from user')
    result = db.engine.execute(sql)
    users = []
    html_output = Markup(
        "<div class=\"container-fluid table table-hover text-centered\"><div class = \"row\"><div class=\"col-sm-3 font-weight-bold\">ID</div><div class=\"col-sm-3 font-weight-bold\">User Name</div><div class=\"col-sm-3 font-weight-bold\">Reset Password</div><div class=\"col-sm-3 font-weight-bold\">Edit User Details</div></div>")
    for row in result:
        users.append(row)
    print(users)
    user_counter = 1
    for index, user in enumerate(users):

        if (index % 2 == 0):
            html_output = Markup(
                "{}<div class = \"row cell1\"><div class=\"col-sm-3\">{}</div> <div class=\"col-sm-3\">{}</div><div class=\"col-sm-3\"><a href=\"/reset_password/{}\">Reset Password</a></div> <div class=\"col-sm-3\"><a href=\"/edit_user/{}\">Edit User Details</a></div></div>".format(
                    html_output, user_counter, user[0], user[1], user[1]))
        else:
            html_output = Markup(
                "{}<div class = \"row cell2\"><div class=\"col-sm-3\">{}</div> <div class=\"col-sm-3\">{}</div><div class=\"col-sm-3\"><a href=\"/reset_password/{}\">Reset Password</a></div><div class=\"col-sm-3\"><a href=\"/edit_user/{}\">Edit User Details</a></div></div>".format(
                    html_output, user_counter, user[0], user[1], user[1]))
        user_counter = user_counter + 1

    html_output = Markup("{}</tbody></table>".format(html_output))
    print(html_output)

    return render_template('reportresult.html', Title='List of Users', data=html_output, user=current_user)


'''
@app.route('/order')
def order_products():

    products = text('select productname, quantity from product')
    result = db.engine.execute(products)
    html_output = Markup("<table class='table'><thead><tr><th>Product name</th><th>Quantity</th></tr></thead><tbody>")
    for row in result:
        product_name = row[0]
        product_quantity = row[1]
        html_output = Markup("{}<tr><td>{}:</td><td>{}</td></tr>".format(html_output, product_name, product_quantity))

    html_output = Markup("{}</tbody></table>".format(html_output))
    print(html_output)

    return render_template('reportresult.html', Title='Stock Level', data=html_output, user=current_user)

'''


@app.route('/report/stocklevels')
def display_stock():
    products = text('select * from product')
    result = db.engine.execute(products)
    html_output = Markup(
        "<div class=\"container-fluid table table-hover text-centered\"><div class = \"row\"><div class=\"col-sm-4\">Product name</div><div class=\"col-sm-4\">Quantity</div><div class=\"col-sm-4\">Image</div></div>")
    for index, row in enumerate(result):
        product_name = row[1]
        quantity = row[5]
        image = row[6]
        if index % 2 == 0:
            print(index)
            html_output = Markup(
                "{}<div class = \"row cell1\"><div class=\"col-sm-4\">{}</div> <div class=\"col-sm-4\">{}</div><div class=\"col-sm-4\"><img src=\"/static/productimages/{}\" class=\"img-fluid\" width=200 height=200></img></div></div>".format(
                    html_output, product_name, quantity, image))
        else:
            html_output = Markup(
                "{}<div class = \"row cell2\"><div class=\"col-sm-4\">{}</div> <div class=\"col-sm-4\">{}</div><div class=\"col-sm-4\"><img src=\"/static/productimages/{}\" class=\"img-fluid\" width=200 height=200></img></div></div>".format(
                    html_output, product_name, quantity, image))
    html_output = Markup("{}</div>".format(html_output))
    print(html_output)

    return render_template('reportresult.html', Title='Stock Level', data=html_output, user=current_user)


@app.route('/productorder', methods=['GET', 'POST'])
@login_required
def productorder():
    form = ProductOrderForm()
    if form.validate_on_submit():
        print("submit")
        selected_products = request.form.getlist("Products")
        print(selected_products)

        for product_order in selected_products:
            new_order = Order(current_user.id, product_order)
            db.session.add(new_order)
            flash("Ordered Product: {}".format(new_order.productID))

        print("commit")
        db.session.commit()
        if len(selected_products) > 0:
            flash("Products ordered")
        else:
            flash("Nothing selected. Please select at least one product to complete an order.")
        return redirect(url_for('main_page'))

    # THIS IS NEEDED AFTER THE IF STATEMENTS. I DON'T KNOW WHY. ANWAR TELLS ME AND IT IS SO.
    # I KNOW WHY NOW.
    # ON "POST", THIS CODE IS NOT REACHED DUE TO THE RETURN IN THE IF STATEMENT.
    products = text('select * from product')
    result = db.engine.execute(products)

    return render_template('order.html', Title='Order Product', products=result, user=current_user, form=form)


'''
    
 #Old version of order
    
    form = OrderForm()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if form.validate_on_submit():
        new_order = Order(current_user.id, form.productID.data,datetime.today() )

        if not Product.query.filter_by(productID=form.productID.data).first() == None:
            print(new_order)
            db.session.add(new_order)

            db.session.commit()
            return redirect(url_for('main_page'))
        else:
            flash("No Product Found")
    return render_template('productorder.html', title='Order Products', form=form, user=current_user)
'''


@app.route('/productregister', methods=['GET', 'POST'])
@login_required
def productregister():
    form = ProductRegistrationForm()
    if form.validate_on_submit():
        prod_image = form.image.data
        filename = secure_filename(prod_image.filename)

        # Get the file extension of the file.
        file_ext = filename.split(".")[1]
        print(filename.split("."))
        print(file_ext)

        print(prod_image, filename)

        prod_image.save(os.path.join('./app/static/productimages', filename))

        product = Product(productname=form.product_name.data, description=form.description.data,
                          purchasePrice=form.purchase_price.data, sellingPrice=form.selling_price.data,
                          quantity=form.quantity.data, image=filename)
        db.session.add(product)
        db.session.commit()

        flash('You registered a product!')
        return redirect(url_for('login'))
    return render_template('productregister.html', title='Product Registration', form=form, user=current_user)


@app.route('/test/<data>', methods=['GET'])
def test_route(data):
    print(data)
    return render_template('index.html', title=data, user=current_user)

@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        print("Resetting Password:{}".format(form.new_password.data))
        user = User.query.filter_by(username=current_user.username).first()
        user.set_password(form.new_password.data)
        db.session.commit()
        print("done")
        flash('Your password has been reset')
        return redirect(url_for('main_page'))
    return render_template('reset-password.html', title='Reset Password', form=form, user=current_user)


@app.route('/reset_password/<userid>', methods=['GET', 'POST'])
@login_required
def reset_user_password(userid):
    form = ResetPasswordForm()
    user = User.query.filter_by(id=userid).first()
    if form.validate_on_submit():
        print("Resetting Password:{}".format(form.new_password.data))

        user.set_password(form.new_password.data)
        db.session.commit()
        print("done")
        flash('Password has been reset for user {}'.format(user.username))
        return redirect(url_for('main_page'))

    return render_template('reset-password.html', title='Reset Password', form=form, user=user)

@app.route('/edit_user/<userid>', methods=['GET', 'POST'])
@login_required
def edit_User(userid):
    form = EditUserForm()
    user = User.query.filter_by(id=userid).first()
    if form.validate_on_submit():
        user.update_details(form.username.data, form.name.data, form.email.data)
        db.session.commit()
        print("User Updated : {}".format(user))
        flash("User Reset")
        return redirect(url_for('main_page'))

    form.username.data = user.username
    form.email.data = user.email
    form.name.data = user.name
    return render_template('edit-user.html', title='Reset Password', form=form, user=user)


