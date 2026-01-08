import random
from string import ascii_letters, digits
import os



from flask import Flask, render_template, request, redirect
from redis import Redis
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

def redis_cli() -> Redis:
    return Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True
    )

cache = redis_cli()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('longurl')
    if not long_url:
        return "URL is missing", 400
    existing_code = cache.get(f"long:{long_url}")
    if existing_code:
        return render_template('index.html', short_url=f"http://127.0.0.1:5000/{existing_code}")
    else:
        new_code = generate_short_code()
        cache.set(f"short:{new_code}", long_url, ex=1800)
        cache.set(f"long:{long_url}", new_code, ex=1800)
        return render_template('index.html', short_url=f"http://127.0.0.1:5000/{new_code}")
                                   
def generate_short_code():
    characters = ascii_letters + digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/<short_code>')
def go_to_url(short_code):
    long_url = cache.get(f"short:{short_code}")

    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404
    
if __name__ == '__main__':
    app.run(debug=True)