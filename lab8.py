from flask import Blueprint, request, render_template, redirect, session, current_app
from os import path
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=current_user.login if current_user.is_authenticated else None)


@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') == 'on'

    if not login_form or not login_form.strip():
        return render_template('/lab8/login.html',
                               error='Логин не может быть пустым')

    if not password_form or not password_form.strip():
        return render_template('/lab8/login.html',
                               error='Пароль не может быть пустым')

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = remember_me)
            return redirect('/lab8/')
    
    return render_template('/lab8/login.html',
                           error = 'Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not login_form.strip():
        return render_template('lab8/register.html',
                               error='Имя пользователя не может быть пустым')

    if not password_form or not password_form.strip():
        return render_template('lab8/register.html',
                               error='Пароль не может быть пустым')

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/articles')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not title.strip():
        return render_template('lab8/create_article.html',
                               error='Название статьи не может быть пустым')
    
    if not article_text or not article_text.strip():
        return render_template('lab8/create_article.html',
                               error='Текст статьи не может быть пустым')
    
    new_article = articles(
        title=title.strip(),
        article_text=article_text.strip(),
        is_public=is_public,
        login_id=current_user.id,
        is_favorite=False,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles')


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        return redirect('/lab8/articles')
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not title.strip():
        return render_template('lab8/edit_article.html', 
                               article=article,
                               error='Название статьи не может быть пустым')
    
    if not article_text or not article_text.strip():
        return render_template('lab8/edit_article.html', 
                               article=article,
                               error='Текст статьи не может быть пустым')
    
    article.title = title.strip()
    article.article_text = article_text.strip()
    article.is_public = is_public
    
    db.session.commit()
    return redirect('/lab8/articles')


