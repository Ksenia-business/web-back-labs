from flask import Blueprint, request, render_template, current_app, jsonify, abort
from os import path
from datetime import datetime
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
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


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    
    try:
        cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id")
        films_db = cur.fetchall()
        
        films_list = []
        if current_app.config['DB_TYPE'] == 'postgres':
            for film in films_db:
                films_list.append({
                    'id': film['id'],
                    'title': film['title'],
                    'title_ru': film['title_ru'],
                    'year': film['year'],
                    'description': film['description']
                })
        else:
            for film in films_db:
                films_list.append({
                    'id': film['id'],
                    'title': film['title'],
                    'title_ru': film['title_ru'],
                    'year': film['year'],
                    'description': film['description']
                })
        
        return jsonify(films_list)
    except Exception as e:
        print(f"Ошибка при получении фильмов: {e}")
        return jsonify([])
    finally:
        conn.close()


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?", (id,))
        
        film = cur.fetchone()
        
        if not film:
            abort(404, description="Фильм с таким ID не найден")
        
        if current_app.config['DB_TYPE'] == 'postgres':
            film_dict = {
                'id': film['id'],
                'title': film['title'],
                'title_ru': film['title_ru'],
                'year': film['year'],
                'description': film['description']
            }
        else:
            film_dict = {
                'id': film['id'],
                'title': film['title'],
                'title_ru': film['title_ru'],
                'year': film['year'],
                'description': film['description']
            }
        
        return jsonify(film_dict)
    finally:
        conn.close()


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        
        film = cur.fetchone()
        
        if not film:
            abort(404, description="Фильм с таким ID не найден")
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM films WHERE id = %s", (id,))
        else:
            cur.execute("DELETE FROM films WHERE id = ?", (id,))
        
        conn.commit()
        return '', 204
    except Exception as e:
        conn.rollback()
        abort(500, description=f"Ошибка при удалении фильма: {e}")
    finally:
        conn.close()


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    errors = {}
    
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание не может быть пустым'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    title_ru = film.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Русское название не может быть пустым'

    title = film.get('title', '').strip()
    if not title and not title_ru:
        errors['title'] = 'Оригинальное название не может быть пустым, если русское название тоже пустое'
    elif not title and title_ru:
        film['title'] = title_ru

    try:
        year_str = film.get('year', '')
        if not year_str:
            errors['year'] = 'Год не может быть пустым'
        else:
            year = int(year_str)
            current_year = datetime.now().year
            if year < 1895 or year > current_year:
                errors['year'] = f'Год должен быть от 1895 до {current_year}'
            else:
                film['year'] = year
    except (ValueError, TypeError):
        errors['year'] = 'Год должен быть числом'
    
    if errors:
        return jsonify(errors), 400
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        
        existing_film = cur.fetchone()
        
        if not existing_film:
            abort(404, description="Фильм с таким ID не найден")
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE films 
                SET title = %s, title_ru = %s, year = %s, description = %s 
                WHERE id = %s
                RETURNING id, title, title_ru, year, description
            """, (film['title'], film['title_ru'], film['year'], film['description'], id))
            
            updated_film = cur.fetchone()
            film_dict = {
                'id': updated_film['id'],
                'title': updated_film['title'],
                'title_ru': updated_film['title_ru'],
                'year': updated_film['year'],
                'description': updated_film['description']
            }
        else:
            cur.execute("""
                UPDATE films 
                SET title = ?, title_ru = ?, year = ?, description = ? 
                WHERE id = ?
            """, (film['title'], film['title_ru'], film['year'], film['description'], id))
            
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?", (id,))
            updated_film = cur.fetchone()
            film_dict = {
                'id': updated_film['id'],
                'title': updated_film['title'],
                'title_ru': updated_film['title_ru'],
                'year': updated_film['year'],
                'description': updated_film['description']
            }
        
        conn.commit()
        return jsonify(film_dict)
    except Exception as e:
        conn.rollback()
        abort(500, description=f"Ошибка при обновлении фильма: {e}")
    finally:
        conn.close()


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    errors = {}
    
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание не может быть пустым'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    title_ru = film.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Русское название не может быть пустым'
    
    title = film.get('title', '').strip()
    if not title and not title_ru:
        errors['title'] = 'Оригинальное название не может быть пустым, если русское название тоже пустое'
    elif not title and title_ru:
        film['title'] = title_ru 
    
    try:
        year_str = film.get('year', '')
        if not year_str:
            errors['year'] = 'Год не может быть пустым'
        else:
            year = int(year_str)
            current_year = datetime.now().year
            if year < 1895 or year > current_year:
                errors['year'] = f'Год должен быть от 1895 до {current_year}'
            else:
                film['year'] = year 
    except (ValueError, TypeError):
        errors['year'] = 'Год должен быть числом'
    
    if errors:
        return jsonify(errors), 400
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description) 
                VALUES (%s, %s, %s, %s) 
                RETURNING id
            """, (film['title'], film['title_ru'], film['year'], film['description']))
            
            new_id = cur.fetchone()['id']
        else:
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description) 
                VALUES (?, ?, ?, ?)
            """, (film['title'], film['title_ru'], film['year'], film['description']))
            
            new_id = cur.lastrowid
        
        conn.commit()
        return jsonify({"id": new_id}), 201
    except Exception as e:
        conn.rollback()
        abort(500, description=f"Ошибка при добавлении фильма: {e}")
    finally:
        conn.close()