from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from flask_login import login_required, current_user

lab9 = Blueprint('lab9', __name__)

PREMIUM_GIFTS = [0, 4, 7, 8]

IMAGE_FILES = [
    'lab9/1.png', 'lab9/2.png', 'lab9/3.png', 
    'lab9/4.jpg', 'lab9/5.jpg', 'lab9/6.jpg',
    'lab9/7.jpg', 'lab9/8.jpg', 'lab9/9.jpg', 
    'lab9/10.jpg'
]

POSITIONS = [
    {'left': 5, 'top': 5},
    {'left': 25, 'top': 15},
    {'left': 45, 'top': 5},
    {'left': 65, 'top': 20},
    {'left': 85, 'top': 10},
    {'left': 10, 'top': 40},
    {'left': 30, 'top': 50},
    {'left': 50, 'top': 40},
    {'left': 70, 'top': 55},
    {'left': 85, 'top': 45}
]

CONGRATS = [
    "Пусть в новом году мечты сбываются быстрее, чем падает снег!",
    "С Новым годом! Пусть каждый день будет как подарок.",
    "Пусть в этом году будет больше смеха и меньше метелей!",
    "С Новым годом! Пусть все невзгоды останутся в прошлом.",
    "Пусть в доме будет тепло, а в сердце – радость!",
    "Пусть в новом году будет меньше суеты и больше того, что действительно важно.",
    "С Новым годом! Пусть этот год будет продуктивным, гармоничным и без лишнего стресса.",
    "С наступающим! Желаю, чтобы твоя жизнь была ярче и интереснее, чем лента в соцсетях.",
    "Пусть в новом году твои проблемы будут как снежинки: тают сами по себе.",
    "С Новым годом! Пусть твой интернет не глючит, а жизнь идёт без «ошибок 404»."
]

GIFTS = [
    'lab9/gift1.jpg',
    'lab9/gift2.jpg', 
    'lab9/gift3.jpg',
    'lab9/gift4.jpg',
    'lab9/gift5.png',
    'lab9/gift6.jpg',
    'lab9/gift7.jpg',
    'lab9/gift8.jpg',
    'lab9/gift9.jpg',
    'lab9/gift10.jpg'
]


@lab9.route('/lab9/')
def lab():
    if 'opened_count' not in session:
        session['opened_count'] = 0
    if 'opened_gifts' not in session:
        session['opened_gifts'] = []
    if 'show_congrats' not in session:
        session['show_congrats'] = False
    if 'last_gift_data' not in session:
        session['last_gift_data'] = None
    
    opened_count = session['opened_count']
    opened_gifts = session['opened_gifts']
    remaining = 10 - len(opened_gifts)
    show_congrats = session['show_congrats']
    last_gift_data = session['last_gift_data']
    
    images = []
    for i, img in enumerate(IMAGE_FILES):
        is_opened = i in opened_gifts
        is_premium = i in PREMIUM_GIFTS
        is_available = not is_premium or (is_premium and current_user.is_authenticated)
        
        images.append({
            'path': img,
            'left': POSITIONS[i]['left'],
            'top': POSITIONS[i]['top'],
            'congrats': CONGRATS[i],
            'gift': GIFTS[i],
            'id': i,
            'opened': is_opened,
            'premium': is_premium,
            'available': is_available
        })
    
    return render_template('lab9/index.html', 
                         images=images,
                         opened_count=opened_count,
                         remaining=remaining,
                         current_user=current_user,
                         show_congrats=show_congrats,
                         last_gift_data=last_gift_data)


@lab9.route('/lab9/open_gift/<int:gift_id>', methods=['POST'])
def open_gift(gift_id):    
    if 'opened_count' not in session:
        session['opened_count'] = 0
    if 'opened_gifts' not in session:
        session['opened_gifts'] = []
    
    opened_gifts = session['opened_gifts']
    opened_count = session['opened_count']
    
    if opened_count >= 3:
        session['error'] = 'Вы уже открыли максимальное количество коробок (3)!'
        return redirect('/lab9/')
    
    if gift_id in PREMIUM_GIFTS and not current_user.is_authenticated:
        session['error'] = 'Этот подарок доступен только авторизованным пользователям!'
        return redirect('/lab9/')
    
    opened_gifts.append(gift_id)
    session['opened_gifts'] = opened_gifts
    session['opened_count'] = opened_count + 1
    
    session['last_gift_data'] = {
        'congrats': CONGRATS[gift_id],
        'gift_image': GIFTS[gift_id]
    }
    session['show_congrats'] = True
    
    return redirect('/lab9/')


@lab9.route('/lab9/close_congrats', methods=['POST'])
def close_congrats():
    session['show_congrats'] = False
    return redirect('/lab9/')


@lab9.route('/lab9/santa_refill', methods=['POST'])
@login_required
def santa_refill():
    session['opened_count'] = 0
    session['opened_gifts'] = []
    session['show_congrats'] = False
    session['last_gift_data'] = None
    session['message'] = 'Дед Мороз наполнил все коробки заново! Теперь вы можете открыть до 3 коробок.'
    
    return redirect('/lab9/')