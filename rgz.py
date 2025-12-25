from flask import Blueprint, request, render_template, redirect, session, current_app, jsonify, flash
from os import path
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor
from datetime import datetime, date, time
import hashlib
import os

rgz = Blueprint('rgz', __name__)

_sqlite_initialized = False

def init_sqlite_database_once():
    """Инициализация SQLite базы только один раз при запуске"""
    global _sqlite_initialized
    
    if _sqlite_initialized:
        return
    
    if current_app.config.get('DB_TYPE') != 'postgres':
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        
        if not os.path.exists(db_path):
            print(f"Создание новой SQLite базы данных: {db_path}")
        
        init_conn = sqlite3.connect(db_path)
        init_cur = init_conn.cursor()
        
        init_cur.execute('''
            CREATE TABLE IF NOT EXISTS users_kino (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        init_cur.execute('''
            CREATE TABLE IF NOT EXISTS sessions_kino (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_title VARCHAR(200) NOT NULL,
                session_date DATE NOT NULL,
                session_time TIME NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        init_cur.execute('''
            CREATE TABLE IF NOT EXISTS bookings_kino (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                seat_number INTEGER NOT NULL,
                booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(session_id, seat_number)
            )
        ''')
        
        init_cur.execute("SELECT COUNT(*) FROM users_kino")
        user_count = init_cur.fetchone()[0]
        
        if user_count == 0:
            print("👤 Добавляем тестовых пользователей в SQLite...")
            
            admin_password = hashlib.sha256('admin'.encode()).hexdigest()
            init_cur.execute('''
                INSERT INTO users_kino (username, password, full_name, is_admin) 
                VALUES (?, ?, ?, ?)
            ''', ('admin', admin_password, 'Администратор', 1))
            
            user_password = hashlib.sha256('user123'.encode()).hexdigest()
            init_cur.execute('''
                INSERT INTO users_kino (username, password, full_name, is_admin) 
                VALUES (?, ?, ?, ?)
            ''', ('user', user_password, 'Тестовый Пользователь', 0))
            
            today = date.today()
            
            test_sessions = [
                ('Матрица', today, '19:00:00'),
                ('Аватар', today, '21:30:00'),
                ('Интерстеллар', today, '16:30:00'),
                ('Начало', today, '18:00:00'),
                ('Пираты Карибского моря', today, '20:30:00'),
                ('Гарри Поттер', today, '17:30:00'),
                ('Властелин колец', today, '20:00:00'),
                ('Титаник', today, '18:30:00'),
                ('Крепкий орешек', today, '21:00:00'),
                ('Назад в будущее', today, '16:00:00')
            ]
            
            for movie, date_obj, time_str in test_sessions:
                init_cur.execute('''
                    INSERT INTO sessions_kino (movie_title, session_date, session_time)
                    VALUES (?, ?, ?)
                ''', (movie, date_obj.isoformat(), time_str))
            
            print(f"✅ Добавлено {len(test_sessions)} тестовых сеансов")
        
        init_conn.commit()
        init_cur.close()
        init_conn.close()
        
        _sqlite_initialized = True
        print("✅ SQLite база данных инициализирована")

def db_connect():
    if current_app.config.get('DB_TYPE') != 'postgres':
        init_sqlite_database_once()
    
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='ksenia_chepurnova_knowledge_base',
            user='ksenia_chepurnova_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def get_query_placeholder():
    if current_app.config.get('DB_TYPE') == 'postgres':
        return '%s'
    else:
        return '?'

def execute_query(query, params=None):
    conn, cur = db_connect()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        return conn, cur
    except Exception as e:
        cur.close()
        conn.close()
        raise e

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password(stored_password, provided_password):
    if stored_password == hashlib.sha256(provided_password.encode('utf-8')).hexdigest():
        return True
    
    if stored_password == provided_password:
        return True
    
    salts = ['', 'my_salt_string', 'salt', 'admin']
    for salt in salts:
        if stored_password == hashlib.sha256((provided_password + salt).encode('utf-8')).hexdigest():
            return True
    
    return False

def is_admin():
    return session.get('is_admin', False)

def is_past_session(session_date, session_time):
    today = date.today()
    now_time = datetime.now().time()
    
    if isinstance(session_date, str):
        session_date = date.fromisoformat(session_date)
    if isinstance(session_time, str):
        session_time = time.fromisoformat(session_time)
    
    if session_date < today:
        return True
    elif session_date == today and session_time < now_time:
        return True
    return False


@rgz.route('/rgz/')
def main():
    conn, cur = db_connect()
    
    try:
        cur.execute('SELECT * FROM sessions_kino ORDER BY session_date, session_time')
        sessions = cur.fetchall()
        
        sessions_list = []
        for sess in sessions:
            session_dict = dict(sess)
            session_dict['is_past'] = is_past_session(session_dict['session_date'], session_dict['session_time'])
            sessions_list.append(session_dict)
        
        cur.close()
        conn.close()
        
        return render_template('rgz/index.html', sessions=sessions_list, 
                             logged_in='login' in session,
                             is_admin=is_admin())
                             
    except Exception as e:
        print(f"Ошибка в main: {e}")
        cur.close()
        conn.close()
        return render_template('rgz/index.html', sessions=[], 
                             logged_in='login' in session,
                             is_admin=is_admin())


@rgz.route('/rgz/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    
    if not username or not password or not full_name:
        flash('Все поля обязательны для заполнения', 'error')
        return redirect('/rgz/register/')
    
    import string
    allowed_chars = string.ascii_letters + string.digits
    if not all(c in allowed_chars for c in username):
        flash('Логин должен содержать только латинские буквы и цифры', 'error')
        return redirect('/rgz/register/')
    
    allowed_chars = string.ascii_letters + string.digits + string.punctuation
    if not all(c in allowed_chars for c in password):
        flash('Пароль содержит недопустимые символы', 'error')
        return redirect('/rgz/register/')
    
    conn, cur = db_connect()
    
    try:
        placeholder = get_query_placeholder()
        cur.execute(f'SELECT id FROM users_kino WHERE username = {placeholder}', (username,))
        
        if cur.fetchone():
            flash('Пользователь с таким логином уже существует', 'error')
            return redirect('/rgz/register/')
        
        hashed_pw = hash_password(password)
        cur.execute(f'INSERT INTO users_kino (username, password, full_name) VALUES ({placeholder}, {placeholder}, {placeholder})',
                    (username, hashed_pw, full_name))
        
        conn.commit()
        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        
    except Exception as e:
        flash(f'Ошибка при регистрации: {str(e)}', 'error')
        print(f"Ошибка регистрации: {e}")
        
    finally:
        cur.close()
        conn.close()
    
    return redirect('/rgz/')


@rgz.route('/rgz/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn, cur = db_connect()
    
    try:
        placeholder = get_query_placeholder()
        cur.execute(f'SELECT * FROM users_kino WHERE username = {placeholder}', (username,))
        user = cur.fetchone()
        
        if user and check_password(user['password'], password):
            session['login'] = user['username']
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            session['is_admin'] = bool(user['is_admin'])
            
            cur.close()
            conn.close()
            
            return redirect('/rgz/')
        else:
            flash('Неверный логин или пароль', 'error')
            
    except Exception as e:
        flash(f'Ошибка при входе: {str(e)}', 'error')
        print(f"Ошибка входа: {e}")
        
    finally:
        cur.close()
        conn.close()
        
    return redirect('/rgz/login/')


@rgz.route('/rgz/logout/')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect('/rgz/')


@rgz.route('/rgz/delete_account/')
def delete_account():
    if 'user_id' not in session:
        return redirect('/rgz/login/')
    
    user_id = session['user_id']
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('DELETE FROM bookings_kino WHERE user_id = %s', (user_id,))
            cur.execute('DELETE FROM users_kino WHERE id = %s', (user_id,))
        else:
            cur.execute('DELETE FROM bookings_kino WHERE user_id = ?', (user_id,))
            cur.execute('DELETE FROM users_kino WHERE id = ?', (user_id,))
        
        conn.commit()
        session.clear()
        flash('Ваш аккаунт был удален', 'info')
        
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка при удалении аккаунта: {str(e)}', 'error')
        
    finally:
        cur.close()
        conn.close()
    
    return redirect('/rgz/')


@rgz.route('/rgz/session/<int:session_id>/')
def view_session(session_id):
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему для просмотра сеансов', 'error')
        return redirect('/rgz/login/')
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('SELECT * FROM sessions_kino WHERE id = %s', (session_id,))
        else:
            cur.execute('SELECT * FROM sessions_kino WHERE id = ?', (session_id,))
        
        session_data = cur.fetchone()
        
        if not session_data:
            flash('Сеанс не найден', 'error')
            cur.close()
            conn.close()
            return redirect('/rgz/')
        
        session_dict = dict(session_data)
        
        is_past = is_past_session(session_dict['session_date'], session_dict['session_time'])
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('''
                SELECT b.seat_number, u.full_name, u.id as user_id 
                FROM bookings_kino b 
                JOIN users_kino u ON b.user_id = u.id 
                WHERE b.session_id = %s
                ORDER BY b.seat_number
            ''', (session_id,))
        else:
            cur.execute('''
                SELECT b.seat_number, u.full_name, u.id as user_id 
                FROM bookings_kino b 
                JOIN users_kino u ON b.user_id = u.id 
                WHERE b.session_id = ?
                ORDER BY b.seat_number
            ''', (session_id,))
        
        bookings = cur.fetchall()
        
        booked_seats = {}
        for booking in bookings:
            booked_seats[booking['seat_number']] = {
                'user_name': booking['full_name'],
                'user_id': booking['user_id']
            }
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('SELECT COUNT(*) as count FROM bookings_kino WHERE session_id = %s AND user_id = %s',
                       (session_id, session['user_id']))
        else:
            cur.execute('SELECT COUNT(*) as count FROM bookings_kino WHERE session_id = ? AND user_id = ?',
                       (session_id, session['user_id']))
        
        result = cur.fetchone()
        user_bookings_count = result['count'] if result else 0
        
        session_dict['user_id'] = session['user_id']
        
        cur.close()
        conn.close()
        
        return render_template('rgz/session.html',
                             session=session_dict,
                             booked_seats=booked_seats,
                             is_past=is_past,
                             user_bookings_count=user_bookings_count,
                             seats=range(1, 31))
                             
    except Exception as e:
        flash(f'Ошибка загрузки сеанса: {str(e)}', 'error')
        cur.close()
        conn.close()
        return redirect('/rgz/')


@rgz.route('/rgz/admin/')
def admin_panel():
    if not is_admin():
        flash('Доступ запрещен. Требуются права администратора', 'error')
        return redirect('/rgz/')
    
    conn, cur = db_connect()
    
    try:
        cur.execute('SELECT * FROM sessions_kino ORDER BY session_date, session_time')
        sessions = cur.fetchall()
        
        cur.execute('SELECT id, username, full_name, created_at FROM users_kino ORDER BY id')
        users = cur.fetchall()
        
        cur.execute('''
            SELECT b.id, b.session_id, b.seat_number, u.username, s.movie_title
            FROM bookings_kino b
            JOIN users_kino u ON b.user_id = u.id
            JOIN sessions_kino s ON b.session_id = s.id
            ORDER BY b.booked_at DESC
        ''')
        bookings = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return render_template('rgz/admin.html',
                             sessions=list(sessions),
                             users=list(users),
                             bookings=list(bookings))
                             
    except Exception as e:
        flash(f'Ошибка загрузки панели администратора: {str(e)}', 'error')
        cur.close()
        conn.close()
        return redirect('/rgz/')


@rgz.route('/rgz/admin/create_session/', methods=['POST'])
def create_session():
    if not is_admin():
        flash('Доступ запрещен', 'error')
        return redirect('/rgz/')
    
    movie_title = request.form.get('movie_title')
    session_date = request.form.get('session_date')
    session_time = request.form.get('session_time')
    
    if not all([movie_title, session_date, session_time]):
        flash('Все поля обязательны для заполнения', 'error')
        return redirect('/rgz/admin/')
    
    conn, cur = db_connect()
    
    try:
        cur.execute('''
            INSERT INTO sessions_kino (movie_title, session_date, session_time)
            VALUES (?, ?, ?)
        ''', (movie_title, session_date, session_time))
        
        conn.commit()
        flash('Сеанс успешно создан', 'success')
        
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка при создании сеанса: {str(e)}', 'error')
        
    finally:
        cur.close()
        conn.close()
    
    return redirect('/rgz/admin/')


@rgz.route('/rgz/admin/delete_session/<int:session_id>/')
def delete_session(session_id):
    if not is_admin():
        flash('Доступ запрещен', 'error')
        return redirect('/rgz/')
    
    conn, cur = db_connect()
    
    try:
        cur.execute('DELETE FROM sessions_kino WHERE id = ?', (session_id,))
        conn.commit()
        flash('Сеанс удален', 'success')
        
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка при удалении сеанса: {str(e)}', 'error')
        
    finally:
        cur.close()
        conn.close()
    
    return redirect('/rgz/admin/')


@rgz.route('/rgz/admin/cancel_booking/<int:booking_id>/')
def cancel_booking_admin(booking_id):
    if not is_admin():
        flash('Доступ запрещен', 'error')
        return redirect('/rgz/')
    
    conn, cur = db_connect()
    
    cur.execute('DELETE FROM bookings_kino WHERE id = ?', (booking_id,))
    conn.commit()
    flash('Бронь отменена', 'success')

    cur.close()
    conn.close()
    
    return redirect('/rgz/admin/')


@rgz.route('/rgz/json-rpc-api/', methods=['POST'])
def api():
    data = request.get_json()
    method = data.get('method')
    request_id = data.get('id', 1)
    
    if method == 'book_seat':
        if 'user_id' not in session:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {'code': 1, 'message': 'Требуется авторизация'},
                'id': request_id
            })
        
        params = data.get('params', {})
        session_id = params.get('session_id')
        seat_number = params.get('seat_number')
        
        conn, cur = db_connect()
        
        try:
            cur.execute('SELECT * FROM sessions_kino WHERE id = ?', (session_id,))
            
            session_data = cur.fetchone()
            if not session_data:
                cur.close()
                conn.close()
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {'code': -32602, 'message': 'Сеанс не найден'},
                    'id': request_id
                })
            
            if is_past_session(session_data['session_date'], session_data['session_time']):
                cur.close()
                conn.close()
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {'code': 2, 'message': 'Нельзя бронировать места на прошедший сеанс'},
                    'id': request_id
                })
            
            cur.execute('''
                SELECT b.*, u.full_name, u.id as user_id 
                FROM bookings_kino b 
                JOIN users_kino u ON b.user_id = u.id 
                WHERE b.session_id = ? AND b.seat_number = ?
            ''', (session_id, seat_number))
            
            existing_booking = cur.fetchone()
            if existing_booking:
                cur.close()
                conn.close()
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {'code': 3, 'message': f'Место уже занято пользователем {existing_booking["full_name"]}'},
                    'id': request_id
                })
            
            cur.execute('SELECT COUNT(*) as count FROM bookings_kino WHERE session_id = ? AND user_id = ?',
                      (session_id, session['user_id']))
            
            result = cur.fetchone()
            user_bookings_count = result['count'] if result else 0
            
            if user_bookings_count >= 5:
                cur.close()
                conn.close()
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {'code': 4, 'message': 'Нельзя забронировать более 5 мест на один сеанс'},
                    'id': request_id
                })
            
            cur.execute('''
                INSERT INTO bookings_kino (session_id, user_id, seat_number, booked_at)
                VALUES (?, ?, ?, datetime("now"))
            ''', (session_id, session['user_id'], seat_number))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return jsonify({
                'jsonrpc': '2.0',
                'result': {
                    'message': 'Место успешно забронировано',
                    'seat_number': seat_number,
                    'user_name': session.get('full_name', 'Вы'),
                    'remaining_slots': 4 - user_bookings_count
                },
                'id': request_id
            })
            
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({
                'jsonrpc': '2.0',
                'error': {'code': -32000, 'message': f'Ошибка сервера: {str(e)}'},
                'id': request_id
            })
    
    elif method == 'cancel_booking':
        if 'user_id' not in session:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {'code': 1, 'message': 'Требуется авторизация'},
                'id': request_id
            })
        
        params = data.get('params', {})
        session_id = params.get('session_id')
        seat_number = params.get('seat_number')
        
        conn, cur = db_connect()
        
        try:
            cur.execute('''
                SELECT b.*, u.full_name, u.id as user_id 
                FROM bookings_kino b 
                JOIN users_kino u ON b.user_id = u.id 
                WHERE b.session_id = ? AND b.seat_number = ?
            ''', (session_id, seat_number))
            
            existing_booking = cur.fetchone()
            
            if not existing_booking:
                cur.close()
                conn.close()
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {'code': 3, 'message': 'Бронь не найдена'},
                    'id': request_id
                })
            
            if existing_booking['user_id'] != session['user_id']:
                cur.close()
                conn.close()
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {'code': 5, 'message': f'Вы не можете отменить бронь другого пользователя ({existing_booking["full_name"]})'},
                    'id': request_id
                })
            
            cur.execute('DELETE FROM bookings_kino WHERE session_id = ? AND seat_number = ?',
                      (session_id, seat_number))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return jsonify({
                'jsonrpc': '2.0',
                'result': {
                    'message': 'Бронь успешно отменена',
                    'seat_number': seat_number
                },
                'id': request_id
            })
            
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({
                'jsonrpc': '2.0',
                'error': {'code': -32000, 'message': f'Ошибка сервера: {str(e)}'},
                'id': request_id
            })
    
    return jsonify({
        'jsonrpc': '2.0',
        'error': {'code': -32601, 'message': 'Метод не найден'},
        'id': request_id
    })