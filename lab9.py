from flask import Blueprint, render_template, jsonify, request, session

lab9 = Blueprint('lab9', __name__)

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

def initialize_session():
    if 'opened_count' not in session:
        session['opened_count'] = 0
    if 'opened_gifts' not in session:
        session['opened_gifts'] = []

def calculate_remaining():
    return 10 - len(session.get('opened_gifts', []))

def get_images_data():
    opened_gifts = session.get('opened_gifts', [])
    
    images = []
    for i, img in enumerate(IMAGE_FILES):
        is_opened = i in opened_gifts
        images.append({
            'path': img,
            'left': POSITIONS[i]['left'],
            'top': POSITIONS[i]['top'],
            'congrats': CONGRATS[i],
            'gift': GIFTS[i],
            'id': i,
            'opened': is_opened  
        })
    return images

def validate_gift_id(gift_id_str):
    try:
        gift_id = int(gift_id_str) if gift_id_str is not None else None
    except (ValueError, TypeError):
        return None, 'Некорректный ID'
    
    if gift_id is None or gift_id < 0 or gift_id >= len(IMAGE_FILES):
        return None, 'Некорректный ID'
    
    return gift_id, None

def can_open_gift(gift_id):
    opened_gifts = session.get('opened_gifts', [])
    opened_count = session.get('opened_count', 0)
    
    if gift_id in opened_gifts:
        return False, 'Подарок уже открыт'
    
    if opened_count >= 3:
        return False, 'Вы уже открыли 3 коробки'
    
    return True, None


@lab9.route('/lab9/')
def lab():
    initialize_session()
    
    opened_count = session['opened_count']
    remaining = calculate_remaining()
    images = get_images_data()
    
    return render_template('lab9/index.html', 
                         images=images,
                         opened_count=opened_count,
                         remaining=remaining)


@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    data = request.get_json()
    gift_id_str = data.get('gift_id')
    
    gift_id, error = validate_gift_id(gift_id_str)
    if error:
        return jsonify({'success': False, 'error': error})
    
    can_open, error = can_open_gift(gift_id)
    if not can_open:
        return jsonify({'success': False, 'error': error})
    
    opened_gifts = session.get('opened_gifts', [])
    opened_count = session.get('opened_count', 0)
    
    opened_gifts.append(gift_id)
    session['opened_gifts'] = opened_gifts
    session['opened_count'] = opened_count + 1
    
    remaining = calculate_remaining()
    
    return jsonify({
        'success': True, 
        'gift_id': gift_id,
        'opened_count': opened_count + 1,
        'remaining': remaining,
        'congrats': CONGRATS[gift_id],
        'gift_image': GIFTS[gift_id]
    })


@lab9.route('/lab9/reset_count', methods=['POST'])
def reset_count():
    session['opened_count'] = 0
    session['opened_gifts'] = []
    
    return jsonify({
        'success': True, 
        'message': 'Счетчик сброшен. Теперь вы можете открыть до 3 коробок.'
    })