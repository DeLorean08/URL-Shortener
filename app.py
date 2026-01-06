from dotenv import load_dotenv
import random
from string import ascii_letters, digits


from flask import Flask, render_template, request, redirect
from redis import Redis

app_name = Flask(__name__)


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

def redis_cli() -> Redis:
    return Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True
    )

cache = get_redis_client()

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.args.get('longurl')
    if not long_url:
        return "URL is missing", 400
    existing_code = cache.set("long:{long_url}")
    if existing_code:
        return render_template('index.html', short_url=f"http://127.0.0.1:5000/{existing_code}")
    else:
        new_code = generate_short_code()()
        cache.set("short:{new_code}", new_code)
        cache.set("long:{long_url}", long_url)
        render_template('index.html', short_url=f"http://127.0.0.1:5000/{new_code}")
                                   
def generate_short_code():
    characters = ascii_letters + digits
    return random.sample(''.join(random.choice(characters) for _ in range(6)))

@app.route('/<short_code>')
def go_to_url(short_code):
    long_url = cache.get("short:{short_code}")

    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404
    
