from flask import Blueprint, request, render_template, make_response, redirect
import datetime
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')

    if not name:
        name = "Аноним"

    if not age:
        age = "не указан"

    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    
    if user == '':
        errors['user'] = 'Заполните поле!'
    
    if age == '':
        errors['age'] = 'Заполните поле возраста!'
    
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fontsize = request.args.get('fontsize')
    fontstyle = request.args.get('fontstyle')

    if color is not None or bgcolor is not None or fontsize is not None or fontstyle is not None:
        resp = make_response(redirect('/lab3/settings'))
        if color is not None:
            resp.set_cookie('color', color)
        if bgcolor is not None:
            resp.set_cookie('bgcolor', bgcolor)
        if fontsize is not None:
            resp.set_cookie('fontsize', fontsize)
        if fontstyle is not None:
            resp.set_cookie('fontstyle', fontstyle)
        return resp
    
    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fontsize = request.cookies.get('fontsize')
    fontstyle = request.cookies.get('fontstyle')

    resp = make_response(render_template(
        'lab3/settings.html',
        color=color,
        bgcolor=bgcolor,
        fontsize=fontsize,
        fontstyle=fontstyle
    ))
    return resp


@lab3.route('/lab3/reset_settings')
def reset_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('bgcolor', '', expires=0)
    resp.set_cookie('fontsize', '', expires=0)
    resp.set_cookie('fontstyle', '', expires=0)
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    form_submitted = request.args.get('submitted')

    if form_submitted:
        if not fio:
            errors['fio'] = 'Заполните поле ФИО'
        if not shelf:
            errors['shelf'] = 'Выберите полку'
        if not age:
            errors['age'] = 'Заполните возраст'
        elif age:
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 120:
                    errors['age'] = 'Возраст должен быть от 1 до 120 лет'
            except ValueError:
                errors['age'] = 'Возраст должен быть числом'
        if not departure:
            errors['departure'] = 'Заполните пункт выезда'
        if not destination:
            errors['destination'] = 'Заполните пункт назначения'
        if not date:
            errors['date'] = 'Выберите дату поездки'

    if errors:
        return render_template('lab3/ticket_form.html', 
                             errors=errors,
                             fio=fio or '',
                             shelf=shelf or '',
                             bedding=bedding,
                             baggage=baggage,
                             age=age or '',
                             departure=departure or '',
                             destination=destination or '',
                             date=date or '',
                             insurance=insurance)

    if form_submitted and not errors:
        age_int = int(age)
        if age_int < 18:
            base_price = 700 
            ticket_type = "Детский билет"
        else:
            base_price = 1000  
            ticket_type = "Взрослый билет"

        total_price = base_price

        if shelf in ['lower', 'lower_side']:
            total_price += 100  
        
        if bedding == 'on':
            total_price += 75 
        
        if baggage == 'on':
            total_price += 250  
        
        if insurance == 'on':
            total_price += 150 

        return render_template('lab3/ticket_result.html',
                             fio=fio,
                             shelf=shelf,
                             bedding=bedding,
                             baggage=baggage,
                             age=age,
                             departure=departure,
                             destination=destination,
                             date=date,
                             insurance=insurance,
                             ticket_type=ticket_type,
                             total_price=total_price)

    return render_template('lab3/ticket_form.html', 
                         errors={},
                         fio='',
                         shelf='',
                         bedding='',
                         baggage='',
                         age='',
                         departure='',
                         destination='',
                         date='',
                         insurance='')


products = [
    {"id": 1, "name": "iPhone 14", "price": 43890, "brand": "Apple", "color": "Black", "storage": "128GB"},
    {"id": 2, "name": "Samsung Galaxy S23", "price": 42990, "brand": "Samsung", "color": "White", "storage": "256GB"},
    {"id": 3, "name": "Google Pixel 7", "price": 27990, "brand": "Google", "color": "Gray", "storage": "128GB"},
    {"id": 4, "name": "OnePlus 11", "price": 37382, "brand": "OnePlus", "color": "Green", "storage": "256GB"},
    {"id": 5, "name": "Xiaomi 13", "price": 12899, "brand": "Xiaomi", "color": "Blue", "storage": "128GB"},
    {"id": 6, "name": "iPhone 14 Pro", "price": 84990, "brand": "Apple", "color": "Silver", "storage": "256GB"},
    {"id": 7, "name": "Samsung Galaxy Z Flip5", "price": 44669, "brand": "Samsung", "color": "Purple", "storage": "256GB"},
    {"id": 8, "name": "Google Pixel 7a", "price": 31990, "brand": "Google", "color": "Coral", "storage": "128GB"},
    {"id": 9, "name": "OnePlus Nord 3", "price": 37470, "brand": "OnePlus", "color": "Black", "storage": "128GB"},
    {"id": 10, "name": "Xiaomi Redmi Note 12", "price": 45999, "brand": "Xiaomi", "color": "White", "storage": "256GB"},
    {"id": 11, "name": "iPhone 13", "price": 49999, "brand": "Apple", "color": "Pink", "storage": "128GB"},
    {"id": 12, "name": "Samsung Galaxy A54", "price": 40739, "brand": "Samsung", "color": "Black", "storage": "128GB"},
    {"id": 13, "name": "Google Pixel 6a", "price": 28905, "brand": "Google", "color": "Green", "storage": "128GB"},
    {"id": 14, "name": "OnePlus 10T", "price": 37724, "brand": "OnePlus", "color": "Silver", "storage": "256GB"},
    {"id": 15, "name": "Xiaomi Poco F5", "price": 24662, "brand": "Xiaomi", "color": "Blue", "storage": "128GB"},
    {"id": 16, "name": "iPhone 15 Pro Max", "price": 171999, "brand": "Apple", "color": "Titanium", "storage": "512GB"},
    {"id": 17, "name": "Samsung Galaxy S23 Ultra", "price": 121990, "brand": "Samsung", "color": "Black", "storage": "512GB"},
    {"id": 18, "name": "Google Pixel 8 Pro", "price": 73499, "brand": "Google", "color": "Obsidian", "storage": "256GB"},
    {"id": 19, "name": "OnePlus Open", "price": 69990, "brand": "OnePlus", "color": "Black", "storage": "512GB"},
    {"id": 20, "name": "Xiaomi 13 Ultra", "price": 13299, "brand": "Xiaomi", "color": "Green", "storage": "512GB"}
]


@lab3.route('/lab3/products')
def products_search():
    min_price_all = min(product['price'] for product in products)
    max_price_all = max(product['price'] for product in products)
    
    min_price_cookie = request.cookies.get('min_price', '')
    max_price_cookie = request.cookies.get('max_price', '')
    
    min_price_form = request.args.get('min_price', '')
    max_price_form = request.args.get('max_price', '')
    
    min_price = min_price_form if min_price_form != '' else min_price_cookie
    max_price = max_price_form if max_price_form != '' else max_price_cookie
    
    if request.args.get('reset'):
        min_price = ''
        max_price = ''
    
    filtered_products = products
    
    if min_price != '' or max_price != '':
        try:
            min_val = float(min_price) if min_price != '' else min_price_all
            max_val = float(max_price) if max_price != '' else max_price_all
            
            if min_val > max_val:
                min_val, max_val = max_val, min_val
                min_price, max_price = str(min_val), str(max_val)
            
            filtered_products = [
                product for product in products
                if min_val <= product['price'] <= max_val
            ]
            
        except ValueError:
            filtered_products = products
    
    response = make_response(render_template(
        'lab3/products.html',
        products=filtered_products,
        min_price=min_price,
        max_price=max_price,
        min_price_all=min_price_all,
        max_price_all=max_price_all,
        products_count=len(filtered_products),
        total_products=len(products)
    ))
    
    if not request.args.get('reset'):
        if min_price != '':
            response.set_cookie('min_price', min_price, max_age=30*24*60*60)
        if max_price != '':
            response.set_cookie('max_price', max_price, max_age=30*24*60*60)
    else:
        response.set_cookie('min_price', '', expires=0)
        response.set_cookie('max_price', '', expires=0)
    
    return response