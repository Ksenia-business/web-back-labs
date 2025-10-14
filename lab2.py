from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {'name': 'роза', 'price': 150},
    {'name': 'тюльпан', 'price': 80},
    {'name': 'незабудка', 'price': 50},
    {'name': 'ромашка', 'price': 40}
]


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower = flower_list[flower_id]
        return render_template('flower_detail.html',
                             flower_name=flower['name'],
                             flower_price=flower['price'],
                             flower_id=flower_id,
                             total_flowers=len(flower_list))


@lab2.route('/lab2/flowers/')
def all_flowers():
    return render_template('lab2/flowers.html',
                         flower_list=flower_list,
                         total_flowers=len(flower_list))


@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return render_template('lab2/clear_flowers.html')


@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append({'name': name, 'price': 100})
    return render_template('add_flower.html',
                         flower_name=name,
                         flower_list=flower_list,
                         total_flowers=len(flower_list))


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        deleted_flower = flower_list.pop(flower_id)
        return redirect('/lab2/flowers/')


@lab2.route('/lab2/add_flower/')
def add_flower_empty():
    return render_template('lab2/add_flower_error.html'), 400


@lab2.route('/lab2/add_flower_form/', methods=['POST'])
def add_flower_form():
    name = request.form.get('name')
    price = int(request.form.get('price', 100))
    
    if name:
        flower_list.append({'name': name, 'price': price})
        return redirect('/lab2/flowers/')
    else:
        return render_template('lab2/add_flower_error.html'), 400


@lab2.route('/lab2/example')
def example():
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
        ]
    return render_template('lab2/example.html',
                           name="Ксения Чепурнова",
                           group="ФБИ-31",
                           course="3 курс",
                           lab_num=2,
                           fruits=fruits)
    

@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase = phrase)


@lab2.route('/lab2/calc/3/4')
def calculate_operations():
    a = 3
    b = 4
    return render_template('lab2/calc.html', a=a, b=b)


@lab2.route('/lab2/calc/')
def default_calc():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calculate_operations_any(a, b):
    return render_template('lab2/calc.html', a=a, b=b)


@lab2.route('/lab2/calc/<int:a>')
def calc_with_one_default(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
    {
        'author': 'Фёдор Достоевский',
        'title': 'Преступление и наказание',
        'genre': 'Роман',
        'pages': 672
    },
    {
        'author': 'Лев Толстой',
        'title': 'Война и мир',
        'genre': 'Роман-эпопея',
        'pages': 1220
    },
    {
        'author': 'Михаил Булгаков',
        'title': 'Мастер и Маргарита',
        'genre': 'Роман',
        'pages': 480
    },
    {
        'author': 'Антон Чехов',
        'title': 'Рассказы',
        'genre': 'Рассказы',
        'pages': 320
    },
    {
        'author': 'Александр Пушкин',
        'title': 'Евгений Онегин',
        'genre': 'Роман в стихах',
        'pages': 384
    },
    {
        'author': 'Николай Гоголь',
        'title': 'Мёртвые души',
        'genre': 'Поэма',
        'pages': 352
    },
    {
        'author': 'Иван Тургенев',
        'title': 'Отцы и дети',
        'genre': 'Роман',
        'pages': 288
    },
    {
        'author': 'Александр Грибоедов',
        'title': 'Горе от ума',
        'genre': 'Комедия',
        'pages': 160
    },
    {
        'author': 'Михаил Лермонтов',
        'title': 'Герой нашего времени',
        'genre': 'Роман',
        'pages': 224
    },
    {
        'author': 'Иван Гончаров',
        'title': 'Обломов',
        'genre': 'Роман',
        'pages': 640
    },
    {
        'author': 'Александр Островский',
        'title': 'Гроза',
        'genre': 'Драма',
        'pages': 416
    },
    {
        'author': 'Николай Лесков',
        'title': 'Левша',
        'genre': 'Повесть',
        'pages': 144
    }
]


@lab2.route('/lab2/books')
def show_books():
    return render_template('lab2/books.html', books=books)

cars = [
    {
        'name': 'Toyota Camry',
        'image': 'toyota_camry.jpeg',
        'description': 'Надёжный седан бизнес-класса с комфортным салоном и экономичным двигателем.'
    },
    {
        'name': 'BMW 5 Series',
        'image': 'bmw_5.jpg',
        'description': 'Немецкий премиум-седан с отличной динамикой и передовыми технологиями.'
    },
    {
        'name': 'Mercedes-Benz E-Class',
        'image': 'mercedes_e.jpg',
        'description': 'Роскошный бизнес-седан с элегантным дизайном и высоким уровнем комфорта.'
    },
    {
        'name': 'Audi A6',
        'image': 'audi_a6.jpg',
        'description': 'Стильный премиум-седан с полным приводом Quattro и современной электроникой.'
    },
    {
        'name': 'Honda Civic',
        'image': 'honda_civic.jpg',
        'description': 'Популярный компактный седан с надёжной конструкцией и спортивным характером.'
    },
    {
        'name': 'Ford Mustang',
        'image': 'ford_mustang.jpg',
        'description': 'Легендарный американский маслкар с мощным двигателем V8 и агрессивным дизайном.'
    },
    {
        'name': 'Chevrolet Camaro',
        'image': 'chevrolet_camaro.jpeg',
        'description': 'Спортивный купе с ярким дизайном и выдающимися динамическими характеристиками.'
    },
    {
        'name': 'Volkswagen Golf',
        'image': 'vw_golf.jpg',
        'description': 'Культовый хетчбек, сочетающий практичность, комфорт и отличную управляемость.'
    },
    {
        'name': 'Hyundai Tucson',
        'image': 'hyundai_tucson.jpg',
        'description': 'Современный кроссовер с смелым дизайном и богатым оснащением по доступной цене.'
    },
    {
        'name': 'Kia Sportage',
        'image': 'kia_sportage.jpeg',
        'description': 'Стильный компактный кроссовер с просторным салоном и длинной гарантией.'
    },
    {
        'name': 'Nissan Qashqai',
        'image': 'nissan_qashqai.jpg',
        'description': 'Популярный городской кроссовер, создавший новый сегмент компактных SUV.'
    },
    {
        'name': 'Mazda CX-5',
        'image': 'mazda_cx5.jpg',
        'description': 'Элегантный кроссовер с прекрасной управляемостью и качественной отделкой.'
    },
    {
        'name': 'Lexus RX',
        'image': 'lexus_rx.jpg',
        'description': 'Роскошный премиум-кроссовер с бесшумным ходом и высочайшим качеством сборки.'
    },
    {
        'name': 'Porsche 911',
        'image': 'porsche_911.jpg',
        'description': 'Легендарный спортивный автомобиль с задним расположением двигателя и уникальным дизайном.'
    },
    {
        'name': 'Jeep Wrangler',
        'image': 'jeep_wrangler.jpeg',
        'description': 'Внедорожник-легенда с рамной конструкцией и съёмными дверями для настоящих приключений.'
    },
    {
        'name': 'Land Rover Defender',
        'image': 'land_rover_defender.jpg',
        'description': 'Современная интерпретация классического внедорожника с флагманскими внедорожными качествами.'
    },
    {
        'name': 'Tesla Model 3',
        'image': 'tesla_model3.jpg',
        'description': 'Электрический седан с минималистичным дизайном и передовыми технологиями автопилота.'
    },
    {
        'name': 'Volvo XC90',
        'image': 'volvo_xc90.jpg',
        'description': 'Скандинавский флагманский SUV с emphasis на безопасности и экологичности.'
    },
    {
        'name': 'Subaru Outback',
        'image': 'subaru_outback.jpg',
        'description': 'Универсал повышенной проходимости с полным приводом Symmetrical AWD и надёжной конструкцией.'
    },
    {
        'name': 'Renault Duster',
        'image': 'renault_duster.jpg',
        'description': 'Доступный компактный внедорожник с хорошей геометрией проходимости и практичным салоном.'
    },
    {
        'name': 'Lada Vesta',
        'image': 'lada_vesta.jpg',
        'description': 'Российский седан с современным дизайном, предлагающий отличное соотношение цены и качества.'
    },
    {
        'name': 'Skoda Octavia',
        'image': 'skoda_octavia.jpg',
        'description': 'Практичный лифтбек с огромным багажником и немецким качеством по доступной цене.'
    }
]


@lab2.route('/lab2/cars')
def show_cars():
    return render_template('lab2/cars.html', cars=cars)