from flask import Blueprint, request, render_template, make_response, redirect, session
import datetime
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['GET', 'POST'])
def div():
    if request.method == 'GET':
        return render_template('lab4/div_form.html')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    if x2 == 0:
        return render_template('lab4/div.html', error='Деление на ноль невозможно!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Ноль в нулевой степени не определен!')
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0
max_trees = 12

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=max_trees)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
                tree_count -= 1
    elif operation == 'plant':
        if tree_count < max_trees:
            tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'М'},
    {'login': 'bob', 'password': '555', 'name': 'Роберт Джонсон', 'gender': 'М'},
    {'login': 'maria', 'password': '941', 'name': 'Мария Зайцева', 'gender': 'Ж'},
    {'login': 'sarah', 'password': '861', 'name': 'Сара Коннор', 'gender': 'Ж'},
    {'login': 'mike', 'password': '40865', 'name': 'Михаил Боярский', 'gender': 'М'},
    {'login': 'david', 'password': 'david99', 'name': 'Манукян Давид Ашотович', 'gender': 'М'},
    {'login': 'mia', 'password': '56789', 'name': 'Мия Бойко', 'gender': 'Ж'},
    {'login': 'liam', 'password': '740', 'name': 'Лиам Нисон', 'gender': 'М'},
    {'login': 'sophia', 'password': '94230', 'name': 'Софи Лорен', 'gender': 'Ж'},
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']    
            user_name = session.get('user_name', '')
        else:
            authorized = False
            login = ''
            user_name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, user_name=user_name)
    
    login_input = request.form.get('login', '')
    password = request.form.get('password', '')

    if not login_input:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login_input)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login_input)

    for user in users:
        if login_input == user['login'] and password == user['password']:
            session['login'] = login_input
            session['user_name'] = user['name']
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login_value=login_input)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('user_name', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    temperature = None
    message = ''
    snowflakes = 0
    error = ''
    
    if request.method == 'POST':
        temp_input = request.form.get('temperature')
        
        if not temp_input:
            error = 'Ошибка: не задана температура'
        else:
            try:
                temperature = int(temp_input)
                
                if temperature < -12:
                    error = 'Не удалось установить температуру — слишком низкое значение'
                elif temperature > -1:
                    error = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= temperature <= -9:
                    message = f'Установлена температура: {temperature}°С'
                    snowflakes = 3
                elif -8 <= temperature <= -5:
                    message = f'Установлена температура: {temperature}°С'
                    snowflakes = 2
                elif -4 <= temperature <= -1:
                    message = f'Установлена температура: {temperature}°С'
                    snowflakes = 1
                    
            except ValueError:
                error = 'Ошибка: введите целое число'
    
    return render_template('lab4/fridge.html', temperature=temperature, message=message, snowflakes=snowflakes, error=error)


grain_prices = {
    'barley': 12000,  
    'oats': 8500,    
    'wheat': 9000,   
    'rye': 15000      
}

grain_names = {
    'barley': 'ячмень',
    'oats': 'овёс', 
    'wheat': 'пшеница',
    'rye': 'рожь'
}

@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    if request.method == 'GET':
        return render_template('lab4/grain_order.html')
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    errors = []
    
    if not grain_type:
        errors.append('Не выбрано зерно')
    
    if not weight:
        errors.append('Не указан вес')
    else:
        try:
            weight = float(weight)
            if weight <= 0:
                errors.append('Вес должен быть положительным числом')
            elif weight > 100:
                errors.append('Такого объёма сейчас нет в наличии')
        except ValueError:
            errors.append('Вес должен быть числом')
    
    if errors:
        return render_template('lab4/grain_order.html', 
                             errors=errors,
                             selected_grain=grain_type,
                             entered_weight=weight if isinstance(weight, str) else '')
    
    price_per_ton = grain_prices[grain_type]
    total_cost = weight * price_per_ton
    
    discount_applied = False
    discount_amount = 0
    
    if weight > 10:
        discount_amount = total_cost * 0.1
        total_cost -= discount_amount
        discount_applied = True
    
    def format_number(num):
        return f"{num:,.0f}".replace(",", " ")
    
    grain_name = grain_names[grain_type]
    
    success_message = f'Заказ успешно сформирован.<br>Вы заказали {grain_name}.<br>Вес: {weight} т.<br>Сумма к оплате: {format_number(total_cost)} руб.'
    
    if discount_applied:
        success_message += f'<br>Применена скидка 10% за большой объём.<br>Размер скидки: {format_number(discount_amount)} руб.'
    
    return render_template('lab4/grain_order.html',
                         success_message=success_message,
                         selected_grain=grain_type,
                         entered_weight=weight)