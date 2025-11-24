from flask import Blueprint, request, render_template, redirect, session, current_app
from os import path
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor

lab6 = Blueprint('lab6', __name__)

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

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        conn, cur = db_connect()
        cur.execute('SELECT * FROM offices ORDER BY number')
        
        if current_app.config['DB_TYPE'] == 'postgres':
            offices = cur.fetchall()
            offices_list = []
            for office in offices:
                offices_list.append({
                    'number': office['number'],
                    'tenant': office['tenant'],
                    'price': office['price']
                })
        else:
            offices = cur.fetchall()
            offices_list = []
            for office in offices:
                offices_list.append({
                    'number': office['number'],
                    'tenant': office['tenant'],
                    'price': office['price']
                })
        
        cur.close()
        conn.close()
        
        return {
            'jsonrpc': '2.0',
            'result': offices_list,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('SELECT * FROM offices WHERE number = %s', (office_number,))
        else:
            cur.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
        
        office = cur.fetchone()
        
        if not office:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Invalid office number'
                },
                'id': id
            }
        
        tenant = office['tenant']
        if tenant:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('UPDATE offices SET tenant = %s WHERE number = %s', (login, office_number))
        else:
            cur.execute('UPDATE offices SET tenant = ? WHERE number = ?', (login, office_number))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    if data['method'] == 'cancellation':
        office_number = data['params']
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('SELECT * FROM offices WHERE number = %s', (office_number,))
        else:
            cur.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
        
        office = cur.fetchone()
        
        if not office:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32602,
                    'message': 'Invalid office number'
                },
                'id': id
            }
        
        tenant = office['tenant']
        
        if not tenant:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office is not booked'
                },
                'id': id
            }
        
        if tenant != login:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Cannot cancel someone else booking'
                },
                'id': id
            }
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute('UPDATE offices SET tenant = %s WHERE number = %s', ('', office_number))
        else:
            cur.execute('UPDATE offices SET tenant = ? WHERE number = ?', ('', office_number))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }