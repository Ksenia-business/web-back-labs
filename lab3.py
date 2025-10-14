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