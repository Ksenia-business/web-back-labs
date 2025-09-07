from flask import Flask, url_for, request, redirect
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
        </nav>
        
        <footer>
            <hr>
            <p>&copy Чепурнова Ксения Анатольевна, ФБИ-31, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''

@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="error.css")
    image_path = url_for("static", filename="404.jpg")
    
    return '''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <div class="error-container">
            <img src="''' + image_path + '''" class="404-image">
            <h1>404</h1>
            <h2>Страница не найдена</h2>
            <p>Запрашиваемая страница не существует или была перемещена.</p>
        </div>
    </body>
</html>
''', 404

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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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
        <a href="/">На главную</a>
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