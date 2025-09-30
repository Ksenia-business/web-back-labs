from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
            </ul>
        </nav>
        
        <footer>
            <hr>
            <p>&copy Чепурнова Ксения Анатольевна, ФБИ-31, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Лабораторная 1</h1>
        </header>
        
        <nav>
            <h1>Лабораторная работа 1</h1>
            <p>
                Flask — фреймворк для создания веб-приложений на языке
                программирования Python, использующий набор инструментов
                Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                называемых микрофреймворков — минималистичных каркасов
                веб-приложений, сознательно предоставляющих лишь самые ба
                зовые возможности.
            </p>
            <a href="/">На главную</a>

            <h2>Список роутов</h2>
            <ul>
                <li><a href="/lab1/web">/lab1/web</a> - Веб-сервер на Flask</li>
                <li><a href="/lab1/author">/lab1/author</a> - Информация об авторе</li>
                <li><a href="/lab1/image">/lab1/image</a> - Изображение дуба</li>
                <li><a href="/lab1/counter">/lab1/counter</a> - Счетчик посещений</li>
                <li><a href="/lab1/clean_counter">/lab1/clean_counter</a> - Очистка счетчика</li>
                <li><a href="/lab1/info">/lab1/info</a> - Перенаправление на автора</li>
                <li><a href="/lab1/created">/lab1/created</a> - Страница создания (201)</li>
                <li><a href="/lab1/error">/lab1/error</a> - Вызов ошибки сервера (505)</li>
                <li><a href="/400">/400</a> - Ошибка 400. Bad Request</li>
                <li><a href="/401">/401</a> - Ошибка 401. Unauthorized</li>
                <li><a href="/402">/402</a> - Ошибка 402. Payment Required</li>
                <li><a href="/403">/403</a> - Ошибка 403. Forbidden</li>
                <li><a href="/405">/405</a> - Ошибка 405. Method Not Allowed</li>
                <li><a href="/418">/418</a> - Ошибка 418. I'm a teapot</li>
            </ul>
        </nav>
        
        <footer>
            <hr>
            <p>&copy Чепурнова Ксения Анатольевна, ФБИ-31, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''

access_log = []

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    
    log_entry = {
        'ip': client_ip,
        'date': access_date,
        'url': requested_url
    }
    access_log.append(log_entry)
    
    css_path = url_for("static", filename="error.css")
    image_path = url_for("static", filename="404.jpg")
    
    html_template = '''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <div class="container">
            <div class="error-section">
                <h1 style="font-family: Comic Sans MS", cursive; color: #C41E3A;">404 - Страница не найдена</h1>
                <p style="margin-top: 20px; color: #474A51; font-size: 30px; font-family: Comic Sans MS", cursive;">У нас что-то происходит, но мы пока сами не знаем что &#128556;.</p>
                <p style="color: #474A51; font-family: Comic Sans MS", cursive;">Поэтому лучше перейти на другую страницу.</p>
                <img src="''' + image_path + '''" alt="404 Error" class="error-image">

                <div class="error-info">
                    <p><strong>Ваш IP-адрес:</strong> ''' + client_ip + '''</p>
                    <p><strong>Дата доступа:</strong> ''' + access_date + '''</p>
                    <p><strong>Запрошенный URL:</strong> ''' + requested_url + '''</p>
                </div>                
                <a href="/" class="btn-home">Вернуться на главную страницу</a>
            </div>
            
            <div class="log-section">
                <h2>Журнал посещений</h2>
                <p>История всех обращений к несуществующим страницам:</p>
                
                <table class="log-table">
                    <thead>
                        <tr>
                            <th>IP-адрес</th>
                            <th>Дата и время</th>
                            <th>Запрошенный URL</th>
                        </tr>
                    </thead>
                    <tbody>
'''
    for entry in reversed(access_log):  
        html_template += f'''
                        <tr>
                            <td>{entry['ip']}</td>
                            <td>{entry['date']}</td>
                            <td>{entry['url']}</td>
                        </tr>
'''
    
    html_template += '''
                    </tbody>
                </table>
                
                <p style="margin-top: 20px; color: #666; font-size: 14px;">
                    Всего записей в журнале: ''' + str(len(access_log)) + '''
                </p>
            </div>
        </div>
    </body>
</html>
'''
    
    return html_template, 404

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Чепурнова Ксения Анатольевна"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
           <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/lab1/web">web</a>
           </body>
        </html>"""

@app.route("/lab1/image")
def image():
    image_path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    html_content = '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <div class="container">
            <h1>Дуб</h1>
            <img src="''' + image_path + '''" alt="Дуб" class="oak-image">
            <p class="description">«Сегодняшний огромный дуб — просто вчерашний жёлудь, настоявший на своём» (Дэвид Айк)</p>
        </div>
    </body>
</html>
'''

    return html_content, 200, {
            'Content-Language': 'ru',  
            'X-Image-Type': 'nature',
            'X-Author-Name': 'Chepurnova Ksenia'
        }

count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP адрес: ''' + client_ip + '''<br>
        <hr>
        <a href="/lab1/clean_counter">Очистить счетчик</a>
    </body>
</html>
'''

@app.route("/lab1/clean_counter")
def clean_counter():
    global count
    count = 0

    return '''
<!doctype html>
<html>
    <body>
        <h2>Счетчик очищен</h2>
        Текущее значение счетчика: ''' + str(count) + '''
        <hr>
        <a href="/lab1/counter">Вернуться к счетчику</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.route("/400")
def bad_request():
    return '''
<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может или не будет обрабатывать запрос из-за чего-то, что воспринимается как ошибка клиента (например, неправильный синтаксис, формат или маршрутизация запроса).</p>
        <a href="/lab1">Назад</a>
    </body>
</html>
''', 400

@app.route("/401")
def unauthorized():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Хотя стандарт HTTP определяет этот ответ как «неавторизованный», семантически он означает «неаутентифицированный». Это значит, что клиент должен аутентифицировать себя, чтобы получить запрошенный ответ.</p>
        <a href="/lab1">Назад</a>
    </body>
</html>
''', 401

@app.route("/402")
def payment_required():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Этот код ответа зарезервирован для использования в будущем. Первоначальной целью создания этого кода было использование его для цифровых платежных систем, однако он используется очень редко и стандартного соглашения не существует.</p>
        <a href="/lab1">Назад</a>
    </body>
</html>
''', 402

@app.route("/403")
def forbidden():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Клиент не имеет прав доступа к контенту, то есть он неавторизован, поэтому сервер отказывается предоставить запрошенный ресурс. В отличие от 401 Unauthorized, личность клиента известна серверу.</p>
        <a href="/lab1">Назад</a>
    </body>
</html>
''', 403

@app.route("/405")
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод запроса известен серверу, но не поддерживается целевым ресурсом. Например, API может не разрешать вызов DELETE для удаления ресурса.</p>
        <a href="/lab1">Назад</a>
    </body>
</html>
''', 405

@app.route("/418")
def teapot():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>«Шуточный» ответ: сервер отклоняет попытку заварить кофе в чайнике.</p>
        <a href="/lab1">Назад</a>
    </body>
</html>
''', 418

@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for("static", filename="error500.css")
    image_path = url_for("static", filename="error500.png")

    
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <div class="error-container">
            <h1>500</h1>
            <h2>Внутренняя ошибка сервера</h2>
            <p>Произошла непредвиденная ошибка на сервере. Пожалуйста, попробуйте позже.</p>
            <img src="''' + image_path + '''" class="error500-image">
        </div>
    </body>
</html>
''', 500

@app.route("/lab1/error")
def cause_error():
    result = 50 / 0
    return "Этот код никогда не выполнится"


@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

# Список цветов теперь с ценами
flower_list = [
    {'name': 'роза', 'price': 150},
    {'name': 'тюльпан', 'price': 80},
    {'name': 'незабудка', 'price': 50},
    {'name': 'ромашка', 'price': 40}
]

@app.route('/lab2/flowers/<int:flower_id>')
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

@app.route('/lab2/flowers/')
def all_flowers():
    return render_template('flowers.html',
                         flower_list=flower_list,
                         total_flowers=len(flower_list))

@app.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return render_template('clear_flowers.html')

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append({'name': name, 'price': 100})
    return render_template('add_flower.html',
                         flower_name=name,
                         flower_list=flower_list,
                         total_flowers=len(flower_list))

@app.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        deleted_flower = flower_list.pop(flower_id)
        return redirect('/lab2/flowers/')

@app.route('/lab2/add_flower/')
def add_flower_empty():
    return render_template('add_flower_error.html'), 400

@app.route('/lab2/add_flower_form/', methods=['POST'])
def add_flower_form():
    name = request.form.get('name')
    price = int(request.form.get('price', 100))
    
    if name:
        flower_list.append({'name': name, 'price': price})
        return redirect('/lab2/flowers/')
    else:
        return render_template('add_flower_error.html'), 400

@app.route('/lab2/example')
def example():
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
        ]
    return render_template('example.html',
                           name="Ксения Чепурнова",
                           group="ФБИ-31",
                           course="3 курс",
                           lab_num=2,
                           fruits=fruits)
    
@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/3/4')
def calculate_operations():
    a = 3
    b = 4
    return render_template('calc.html', a=a, b=b)

@app.route('/lab2/calc/')
def default_calc():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calculate_operations_any(a, b):
    return render_template('calc.html', a=a, b=b)

@app.route('/lab2/calc/<int:a>')
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

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

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

@app.route('/lab2/cars')
def show_cars():
    return render_template('cars.html', cars=cars)