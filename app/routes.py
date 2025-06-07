from flask import render_template, request, current_app, jsonify
from app import app
from collections import Counter
from app.models import TimelinePost
from playhouse.shortcuts import model_to_dict
from app.helper import load_country_coordinates, read_visited_csv

@app.route('/')
def index():
    userinfo = current_app.config['USERINFO']
    return render_template('index.html',
                           title='Home',
                           name=userinfo['name'],
                           shortIntro=userinfo['shortIntro'],
                           longIntro=userinfo['longIntro'],
                           work=userinfo['work'],
                           skills=userinfo['skills'],
                           education=userinfo['education'],
                           email=userinfo['email'],
                           facebook=userinfo['facebook'],
                           instagram=userinfo['instagram'],
                           github=userinfo['github'],
                           linkedin=userinfo['linkedin'],
                           twitter=userinfo['twitter'],
                           profilepic='./static/images/profile_pic.jpg')

@app.route('/projects')
def projects():
    userinfo = current_app.config['USERINFO']
    return render_template('projects.html',
                           title='Projects',
                           project_rows=userinfo['project_rows'],
                           email=userinfo['email'],
                           facebook=userinfo['facebook'],
                           instagram=userinfo['instagram'],
                           github=userinfo['github'],
                           linkedin=userinfo['linkedin'],
                           twitter=userinfo['twitter'])

@app.route('/hobbies')
def hobbies():
    userinfo = current_app.config['USERINFO']
    all_places = load_country_coordinates()
    visited_raw = read_visited_csv()
    visited_places = []
    country_list = []
    for entry in visited_raw:
        country = entry["country"]
        if country in all_places:
            place = all_places[country]
            visited_places.append({
                "country": country,
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "alpha3": place["alpha3"],
                "visited_date": entry["visited_date"],
                "notes": entry["notes"]
            })
            country_list.append(country)
    # Count visits per country
    country_counts = Counter(country_list)
    country_names = list(country_counts.keys())
    country_visits = list(country_counts.values())
    return render_template('hobbies.html',
                           title='Hobbies',
                           hobbies=userinfo['hobbies'],
                           visited=visited_places,
                           country_names=country_names,
                           country_visits=country_visits,
                           email=userinfo['email'],
                           facebook=userinfo['facebook'],
                           instagram=userinfo['instagram'],
                           github=userinfo['github'],
                           linkedin=userinfo['linkedin'],
                           twitter=userinfo['twitter'])

@app.route('/timeline')
def timeline():
    userinfo = current_app.config['USERINFO']
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    post_dicts = [model_to_dict(post) for post in posts]
    return render_template('timeline.html',
                           title='Timeline',
                           posts=post_dicts,
                           email=userinfo['email'],
                           facebook=userinfo['facebook'],
                           instagram=userinfo['instagram'],
                           github=userinfo['github'],
                           linkedin=userinfo['linkedin'],
                           twitter=userinfo['twitter'])

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name:
        return "Invalid name", 400
    elif not email or "@" not in email:
        return "Invalid email", 400
    elif not content:
        return "Invalid content", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return jsonify({'timeline_posts': [model_to_dict(p) for p in posts]})
