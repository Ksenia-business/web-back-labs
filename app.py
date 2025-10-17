from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4

import datetime
app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)


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
                <li><a href="/lab3">Третья лабораторная</a></li>
                <li><a href="/lab4">Четвертая лабораторная</a></li>
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
    
    css_path = url_for("static", filename="lab1/error.css")
    image_path = url_for("static", filename="lab1/404.jpg")
    
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
    css_path = url_for("static", filename="lab1/error500.css")
    image_path = url_for("static", filename="lab1/error500.png")

    
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
