# Python and the Web

## Overview
- Web servers with Flask
- Web clients using the requests module
- Web scraping with BeautifulSoup and Scrapy
- HTML parsing with lxml
- Testing web applications with Selenium
- Web development best practices

---

## Web Development with Python

## The Python Web Ecosystem
- Python is widely used for web development
- Server-side applications and APIs
- Client and automation tools
- Full-stack frameworks
- Microservices and serverless applications
- Data processing and analysis

```txt
Common Python Web Technology Stack:
- Web Framework: Flask, Django, FastAPI
- HTTP Client: requests, httpx, aiohttp
- Database: SQLAlchemy, psycopg2, PyMongo
- Templates: Jinja2, Mako
- Task Queue: Celery, RQ
- Web Server: Gunicorn, uWSGI, Daphne
- Containerization: Docker, Kubernetes
```

---

## Web Servers with Flask

## Introduction to Flask
- Lightweight web framework
- "Micro" framework (minimalist core)
- Highly extensible
- Easy to learn and use
- Great for APIs, small to medium applications
- Widely used in production

```python
# Installing Flask
# pip install flask

from flask import Flask

# Create application instance
app = Flask(__name__)

# Define a route
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
```

---

## Web Servers with Flask

## Flask Routing
- Map URLs to view functions
- Route parameters
- HTTP methods (GET, POST, etc.)
- URL building with `url_for()`
- Error handling

```python
from flask import Flask, url_for

app = Flask(__name__)

# Basic route
@app.route('/')
def index():
    return 'Index Page'

# Route with parameter
@app.route('/user/<username>')
def show_user(username):
    return f'User: {username}'

# Route with typed parameter
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post: {post_id}'

# Multiple HTTP methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        return 'Login form submitted'
    else:
        # Show login form
        return 'Please log in'
```

---

## Web Servers with Flask

## Flask Request Handling
- Access request data
- Form handling
- File uploads
- JSON payloads
- Headers and cookies

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/form', methods=['POST'])
def handle_form():
    # Access form data
    name = request.form.get('name')
    email = request.form.get('email')
    return f'Received: {name} ({email})'

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle file upload
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    # Save the file
    file.save('/path/to/uploads/' + file.filename)
    return f'Uploaded: {file.filename}'

@app.route('/api/data', methods=['POST'])
def api_data():
    # Handle JSON data
    data = request.get_json()
    return jsonify({'received': data})
```

---

## Web Servers with Flask

## Flask Responses
- Return strings, dictionaries, tuples
- HTML, JSON, files, streams
- Custom status codes
- Headers and cookies
- Redirects

```python
from flask import Flask, jsonify, send_file, make_response, redirect, url_for

app = Flask(__name__)

@app.route('/text')
def text_response():
    return 'Plain text response'

@app.route('/api/user/<id>')
def user_api(id):
    user = {'id': id, 'name': 'John Doe', 'email': 'john@example.com'}
    return jsonify(user)

@app.route('/download')
def download_file():
    return send_file('static/file.pdf', as_attachment=True)

@app.route('/custom_header')
def custom_header():
    resp = make_response('Response with custom header')
    resp.headers['X-Custom-Header'] = 'Custom Value'
    return resp

@app.route('/set_cookie')
def set_cookie():
    resp = make_response('Cookie set')
    resp.set_cookie('user_id', '12345')
    return resp

@app.route('/redirect')
def redirect_example():
    return redirect(url_for('text_response'))
```

---

## Web Servers with Flask

## Templating with Jinja2
- HTML templates with dynamic content
- Template inheritance
- Variable substitution
- Filters and custom filters
- Control structures

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/greet/<name>')
def greet(name):
    return render_template('greeting.html', name=name)

@app.route('/users')
def user_list():
    users = [
        {'name': 'Alice', 'email': 'alice@example.com'},
        {'name': 'Bob', 'email': 'bob@example.com'},
        {'name': 'Charlie', 'email': 'charlie@example.com'}
    ]
    return render_template('users.html', users=users)
```

```html
<!-- templates/greeting.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Greeting</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
    <p>Welcome to our website.</p>
</body>
</html>
```

---

## Web Servers with Flask

## Flask Application Structure
- Organizing routes and views
- Blueprints for modular applications
- Application factory pattern
- Configuration management
- Project structure best practices

```txt
flask_app/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── models.py            # Database models
│   ├── static/              # Static files (CSS, JS)
│   ├── templates/           # Jinja2 templates
│   └── views/               # Route definitions
│       ├── __init__.py
│       ├── auth.py          # Authentication blueprint
│       └── main.py          # Main blueprint
├── requirements.txt         # Dependencies
├── run.py                   # Application entry point
└── tests/                   # Test suite
    ├── __init__.py
    ├── test_auth.py
    └── test_main.py
```

```python
# app/__init__.py (Application Factory)
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(f'app.config.{config_name.capitalize()}Config')

    # Register blueprints
    from app.views.main import main_bp
    from app.views.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
```

---

## Web Servers with Flask

## Database Integration
- SQLAlchemy ORM
- Flask-SQLAlchemy extension
- Database migrations
- Model definitions
- Query building and execution

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.title}>'

# Create tables
with app.app_context():
    db.create_all()
```

---

## Web Servers with Flask

## Flask Authentication
- User authentication
- Password hashing
- Session management
- Login and registration forms
- Flask-Login extension

```python
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Welcome, {current_user.username}!'
```

---

## Web Servers with Flask

## RESTful APIs with Flask
- API design principles
- Resource-based routing
- JSON responses
- Status codes
- Authentication and authorization
- API documentation

```python
from flask import Flask, jsonify, request, abort
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Sample data
users = {
    'admin': 'password123'
}

items = [
    {'id': 1, 'name': 'Item 1', 'price': 10.99},
    {'id': 2, 'name': 'Item 2', 'price': 24.99},
]

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        abort(404)
    return jsonify({'item': item})

@app.route('/api/items', methods=['POST'])
@auth.login_required
def create_item():
    if not request.json or 'name' not in request.json:
        abort(400)
    item = {
        'id': items[-1]['id'] + 1 if items else 1,
        'name': request.json['name'],
        'price': request.json.get('price', 0)
    }
    items.append(item)
    return jsonify({'item': item}), 201
```

---

## Web Servers with Flask

## Flask Extensions Ecosystem
- Common extensions for Flask
- Authentication, authorization
- Forms and validation
- Database integration
- REST APIs
- Admin interfaces

```python
# Flask-WTF for forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

# Flask-Migrate for database migrations
from flask_migrate import Migrate
migrate = Migrate(app, db)

# Flask-RESTful for APIs
from flask_restful import Resource, Api
api = Api(app)

class ItemResource(Resource):
    def get(self, item_id):
        # Get item logic
        pass

api.add_resource(ItemResource, '/api/items/<int:item_id>')

# Flask-Admin for admin interface
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
```

---

## Web Servers with Flask

## Deploying Flask Applications
- Development vs. production environments
- WSGI servers (Gunicorn, uWSGI)
- Reverse proxies (Nginx, Apache)
- Containerization with Docker
- Cloud platforms (Heroku, AWS, GCP)
- Environment variables and secrets

```bash
# Installation for production
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"

# Example Docker setup
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP=app
ENV FLASK_ENV=production

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
```

```nginx
# Nginx config snippet
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Web Clients with Requests

## Introduction to Requests
- HTTP client library for Python
- Simple and intuitive API
- Handles complex HTTP operations
- SSL/TLS verification
- Session and cookie management
- Most popular HTTP library for Python

```python
# Installing Requests
# pip install requests

import requests

# Basic GET request
response = requests.get('https://api.github.com/users/python')

# Check status code
print(f"Status: {response.status_code}")  # 200

# Response content
print(f"Content type: {response.headers['content-type']}")
print(f"Encoding: {response.encoding}")

# Parse JSON response
data = response.json()
print(f"User: {data['login']}")
print(f"Followers: {data['followers']}")

# Text response
print(response.text[:100])  # Print first 100 chars
```

---

## Web Clients with Requests

## HTTP Methods with Requests
- GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD
- Query parameters
- Request body (form data, JSON)
- Custom headers
- Timeout settings
- Streaming responses

```python
import requests

# GET with parameters
params = {'q': 'python', 'sort': 'stars'}
response = requests.get('https://api.github.com/search/repositories', params=params)
print(f"URL: {response.url}")

# POST with form data
form_data = {'username': 'user', 'password': 'pass'}
response = requests.post('https://httpbin.org/post', data=form_data)

# POST with JSON
json_data = {'name': 'John', 'age': 30}
response = requests.post('https://httpbin.org/post', json=json_data)

# PUT request
response = requests.put('https://httpbin.org/put', data={'key': 'value'})

# DELETE request
response = requests.delete('https://httpbin.org/delete')

# Custom headers
headers = {'User-Agent': 'MyApp/1.0', 'Authorization': 'token abc123'}
response = requests.get('https://api.github.com/user', headers=headers)

# Timeout
response = requests.get('https://httpbin.org/delay/2', timeout=5)
```

---

## Web Clients with Requests

## Working with Sessions
- Persistent connections
- Cookie persistence
- Default headers
- Reduce overhead for multiple requests
- Better performance for API clients

```python
import requests

# Create a session
session = requests.Session()

# Set default headers for all requests in this session
session.headers.update({
    'User-Agent': 'MyAppClient/1.0',
    'Accept': 'application/json'
})

# Add cookies to session
session.cookies.update({'session_token': 'abc123'})

# Authentication is persisted across requests
session.auth = ('username', 'password')

# First request
response = session.get('https://httpbin.org/cookies')
print(response.json())  # Shows cookies

# Second request (uses same session, cookies, headers)
response = session.get('https://httpbin.org/headers')
print(response.json())  # Shows headers

# POST request in same session
response = session.post('https://httpbin.org/post', json={'key': 'value'})
print(response.json())

# Close the session when done
session.close()
```

---

## Web Clients with Requests

## Error Handling and Exceptions
- Handle different HTTP status codes
- Catch connection errors
- Implement retries
- Timeouts
- Response validation

```python
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

def make_request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)

            # Raise an exception for 4XX/5XX responses
            response.raise_for_status()

            # If successful, return the response
            return response

        except HTTPError as e:
            # Handle HTTP errors (400-599)
            print(f"HTTP error occurred: {e}")
            if response.status_code >= 500 and attempt < max_retries - 1:
                print(f"Server error, retrying ({attempt+1}/{max_retries})")
                continue
            else:
                raise

        except ConnectionError:
            print(f"Connection error, retrying ({attempt+1}/{max_retries})")
            if attempt < max_retries - 1:
                continue
            else:
                raise

        except Timeout:
            print(f"Request timed out, retrying ({attempt+1}/{max_retries})")
            if attempt < max_retries - 1:
                continue
            else:
                raise

        except RequestException as e:
            # Catch any other requests-related exceptions
            print(f"Error during request: {e}")
            raise

try:
    response = make_request_with_retry('https://httpbin.org/status/503')
    print(f"Success: {response.status_code}")
except Exception as e:
    print(f"Failed after retries: {e}")
```

---

## Web Clients with Requests

## Working with Authentication
- Basic authentication
- Digest authentication
- Token-based authentication
- OAuth
- Custom authentication classes

```python
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

# Basic Authentication
response = requests.get(
    'https://httpbin.org/basic-auth/user/pass',
    auth=HTTPBasicAuth('user', 'pass')
)
print(f"Basic Auth: {response.status_code}")

# Simpler syntax for Basic Auth
response = requests.get(
    'https://httpbin.org/basic-auth/user/pass',
    auth=('user', 'pass')  # Shorthand for HTTPBasicAuth
)

# Digest Authentication
response = requests.get(
    'https://httpbin.org/digest-auth/auth/user/pass',
    auth=HTTPDigestAuth('user', 'pass')
)
print(f"Digest Auth: {response.status_code}")

# Token Authentication (common for APIs)
headers = {'Authorization': 'Bearer my-token-string'}
response = requests.get('https://api.example.org/data', headers=headers)

# OAuth 2.0 Example (using requests-oauthlib)
from requests_oauthlib import OAuth2Session

client_id = 'your-client-id'
authorization_base_url = 'https://example.com/oauth/authorize'
token_url = 'https://example.com/oauth/token'

oauth = OAuth2Session(client_id)
authorization_url, state = oauth.authorization_url(authorization_base_url)

print(f"Please go to {authorization_url} and authorize access")
redirect_response = input("Enter the full callback URL: ")

token = oauth.fetch_token(
    token_url,
    authorization_response=redirect_response,
    client_secret='your-client-secret'
)

# Make requests with the OAuth session
response = oauth.get('https://example.com/api/data')
```

---

## Web Clients with Requests

## File Uploads and Downloads
- Upload files to servers
- Download files and save locally
- Progress monitoring
- Streaming large files
- Resumable downloads
- Content type handling

```python
import requests
import os
from tqdm import tqdm  # For progress bars

# File Upload
files = {'file': open('document.pdf', 'rb')}
response = requests.post('https://httpbin.org/post', files=files)
print(f"Upload response: {response.status_code}")

# Make sure to close the file
files['file'].close()

# Safer upload using context manager
with open('document.pdf', 'rb') as f:
    response = requests.post('https://httpbin.org/post', files={'file': f})
    print(f"Upload response: {response.status_code}")

# Download small file
response = requests.get('https://example.com/files/sample.pdf')
with open('sample.pdf', 'wb') as f:
    f.write(response.content)

# Download large file with streaming and progress bar
url = 'https://example.com/files/large_file.zip'
response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))
block_size = 1024  # 1 KB

with open('large_file.zip', 'wb') as f:
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        f.write(data)
    progress_bar.close()
```

---

## Web Clients with Requests

## Advanced Requests Features
- Custom adapters
- Transport adapters
- Connection pooling
- SSL/TLS verification
- Proxies
- Event hooks

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure retries with backoff strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
    status_forcelist=[429, 500, 502, 503, 504],  # Retry on these statuses
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Only retry safe methods
)

# Create an adapter with the retry strategy
adapter = HTTPAdapter(max_retries=retry_strategy)

# Use the adapter for all http:// and https:// requests
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)

# Using a proxy
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080',
}
response = session.get('https://example.org', proxies=proxies)

# Disable SSL verification (not recommended for production)
response = session.get('https://example.org', verify=False)

# Custom cert verification
response = session.get('https://example.org', verify='/path/to/certfile')

# Event hooks
def print_url(r, *args, **kwargs):
    print(f"Request URL: {r.url}")

session.hooks['response'] = [print_url]
response = session.get('https://httpbin.org/get')
```

---

## Web Scraping with BeautifulSoup

## Introduction to Web Scraping
- Extract data from websites
- Parse HTML and XML
- Navigate web document structure
- Extract specific elements, attributes, text
- Legal and ethical considerations

```python
# Installing BeautifulSoup
# pip install beautifulsoup4 requests

import requests
from bs4 import BeautifulSoup

# Fetch a web page
url = 'https://quotes.toscrape.com/'
response = requests.get(url)
html_content = response.text

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Overview of the page
print(soup.title.text)  # Get page title
print(soup.find('h1').text)  # Find the first h1 tag

# Extract all quotes
quotes = []
for quote in soup.find_all('div', class_='quote'):
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    quotes.append({'text': text, 'author': author})

# Print the first few quotes
for quote in quotes[:3]:
    print(f'"{quote["text"]}" - {quote["author"]}')
```

---

## Web Scraping with BeautifulSoup

## Navigating the DOM
- Find elements by tag name, class, id
- CSS selectors
- Element attributes
- Parent, child, sibling navigation
- Filtering and searching

```python
from bs4 import BeautifulSoup

# Sample HTML
html = """
<html>
<head><title>Sample Page</title></head>
<body>
    <div id="main" class="container">
        <h1>Welcome to the Page</h1>
        <p class="intro">This is an introduction.</p>
        <div class="content">
            <p>First paragraph in content.</p>
            <p>Second paragraph in content.</p>
        </div>
        <ul id="items">
            <li class="item">Item 1</li>
            <li class="item highlighted">Item 2</li>
            <li class="item">Item 3</li>
        </ul>
    </div>
    <div class="footer">
        <p>Footer text</p>
    </div>
</body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# Find by tag
title = soup.title
print(f"Title tag: {title}")
print(f"Title text: {title.text}")

# Find by ID
main_div = soup.find(id='main')
print(f"Main div: {main_div.name}")

# Find by class
intro = soup.find(class_='intro')
print(f"Intro text: {intro.text}")

# Find all matching elements
all_paragraphs = soup.find_all('p')
print(f"Number of paragraphs: {len(all_paragraphs)}")

# CSS selector
highlighted_item = soup.select('li.highlighted')
print(f"Highlighted item: {highlighted_item[0].text}")

# Navigating the tree
content_div = soup.find(class_='content')
parent = content_div.parent
siblings = content_div.find_next_siblings()
children = content_div.findChildren('p')

print(f"Parent tag: {parent.name}")
print(f"Number of siblings: {len(siblings)}")
print(f"Number of children: {len(children)}")
```

---

## Web Scraping with BeautifulSoup

## Extracting Data
- Get text content
- Get attributes
- Extract links and URLs
- Extract tables
- Extract forms
- Clean and process data

```python
from bs4 import BeautifulSoup
import requests

# Fetch a page with a table
url = 'https://en.wikipedia.org/wiki/List_of_programming_languages'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all links
links = []
for link in soup.find_all('a'):
    href = link.get('href')
    text = link.text.strip()
    if href and text and href.startswith('/wiki/') and ':' not in href:
        links.append({
            'url': f"https://en.wikipedia.org{href}",
            'text': text
        })

print(f"Found {len(links)} links")
for link in links[:5]:
    print(f"{link['text']}: {link['url']}")

# Extract table data
tables = soup.find_all('table', class_='wikitable')
if tables:
    table = tables[0]  # Take the first table
    rows = []

    # Extract table headers
    headers = [th.text.strip() for th in table.find_all('th')]

    # Extract table rows
    for row in table.find_all('tr')[1:]:  # Skip header row
        cells = [cell.text.strip() for cell in row.find_all('td')]
        if cells:  # Skip empty rows
            rows.append(dict(zip(headers, cells)))

    print(f"\nExtracted {len(rows)} rows from table")
    for row in rows[:3]:
        print(row)
```

---

## Web Scraping with BeautifulSoup

## Common Scraping Challenges
- Dynamic content (JavaScript)
- Authentication
- Rate limiting
- CAPTCHA
- Anti-scraping measures
- Handling malformed HTML

```python
import requests
from bs4 import BeautifulSoup
import time
import random

# Define headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def scrape_with_retry(url, max_retries=3):
    """Scrape a URL with retry logic and random delays."""
    for attempt in range(max_retries):
        try:
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))

            # Make the request with headers
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Parse even if malformed HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup

        except requests.exceptions.RequestException as e:
            print(f"Error on attempt {attempt+1}: {e}")
            if attempt == max_retries - 1:
                raise

            # Wait longer between retries
            time.sleep(random.uniform(5, 10))

    return None

# Handle sites with login required
def scrape_authenticated_page(login_url, target_url, username, password):
    with requests.Session() as session:
        # Set headers
        session.headers.update(headers)

        # Get the login page to retrieve any CSRF token
        login_page = session.get(login_url)
        login_soup = BeautifulSoup(login_page.text, 'html.parser')

        # Find CSRF token (implementation depends on the site)
        csrf_token = login_soup.find('input', {'name': 'csrf_token'})['value']

        # Prepare login data
        login_data = {
            'username': username,
            'password': password,
            'csrf_token': csrf_token
        }

        # Perform login
        session.post(login_url, data=login_data)

        # Now scrape the authenticated page
        response = session.get(target_url)
        return BeautifulSoup(response.text, 'html.parser')
```

---

## Web Scraping with BeautifulSoup

## Web Scraping Ethics and Best Practices
- Respect robots.txt
- Implement rate limiting
- Identify your scraper (User-Agent)
- Cache results to avoid unnecessary requests
- Check terms of service
- Consider API alternatives

```python
import requests
from bs4 import BeautifulSoup
import time
import os
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

class EthicalScraper:
    def __init__(self, base_url, user_agent="EthicalBot/1.0"):
        self.base_url = base_url
        self.user_agent = user_agent
        self.headers = {'User-Agent': user_agent}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.rate_limit = 1  # Seconds between requests
        self.last_request = 0
        self.cache_dir = "cache"

        # Create cache directory if it doesn't exist
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        # Check robots.txt
        self.robot_parser = RobotFileParser()
        parsed_url = urlparse(base_url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        self.robot_parser.set_url(robots_url)
        self.robot_parser.read()

    def can_fetch(self, url):
        """Check if robots.txt allows scraping this URL"""
        return self.robot_parser.can_fetch(self.user_agent, url)

    def get_page(self, url):
        """Get a page respecting rate limits and robots.txt"""
        # Check if allowed by robots.txt
        if not self.can_fetch(url):
            print(f"Robots.txt disallows scraping: {url}")
            return None

        # Check cache first
        cache_file = os.path.join(self.cache_dir,
                                urlparse(url).path.replace('/', '_') or 'index')

        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return BeautifulSoup(f.read(), 'html.parser')

        # Respect rate limiting
        elapsed = time.time() - self.last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)

        # Make the request
        self.last_request = time.time()
        response = self.session.get(url)

        # Cache the result
        if response.status_code == 200:
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(response.text)

        return BeautifulSoup(response.text, 'html.parser')

# Usage
scraper = EthicalScraper("https://quotes.toscrape.com")
soup = scraper.get_page("https://quotes.toscrape.com")
if soup:
    quotes = soup.find_all('div', class_='quote')
    print(f"Found {len(quotes)} quotes")
```

---

## Web Scraping with Scrapy

## Introduction to Scrapy
- Full-featured web scraping framework
- High-level, organized architecture
- Asynchronous networking
- Built-in middleware and extensions
- Export data in various formats
- Ideal for large-scale scraping

```python
# Installing Scrapy
# pip install scrapy

# Creating a new Scrapy project
# scrapy startproject quotescraper

# Structure of a Scrapy project
"""
quotescraper/
├── scrapy.cfg            # Deploy configuration file
└── quotescraper/         # Project's Python module
    ├── __init__.py
    ├── items.py          # Project items definition
    ├── middlewares.py    # Project middlewares
    ├── pipelines.py      # Project pipelines
    ├── settings.py       # Project settings
    └── spiders/          # Directory for spiders
        └── __init__.py
"""

# Creating a simple spider
"""
# quotescraper/spiders/quotes_spider.py
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
"""

# Running the spider
# scrapy crawl quotes -o quotes.json
```

---

## Web Scraping with Scrapy

## Scrapy Selectors
- CSS selectors
- XPath selectors
- Element extraction
- Attribute extraction
- Nested selectors
- Text extraction

```python
import scrapy

class ProductSpider(scrapy.Spider):
    name = "products"
    start_urls = ['https://example.com/products']

    def parse(self, response):
        # CSS selectors
        products = response.css('div.product')
        for product in products:
            name = product.css('h2.title::text').get()
            price = product.css('span.price::text').get()
            url = product.css('a.product-link::attr(href)').get()

            yield {
                'name': name,
                'price': price,
                'url': url
            }

        # XPath selectors
        products = response.xpath('//div[@class="product"]')
        for product in products:
            name = product.xpath('./h2[@class="title"]/text()').get()
            price = product.xpath('./span[@class="price"]/text()').get()
            url = product.xpath('./a[@class="product-link"]/@href').get()

            yield {
                'name': name,
                'price': price,
                'url': url
            }

        # Combining selectors
        for product in response.css('div.product'):
            # Get description using XPath within a CSS-selected element
            description = product.css('div.details').xpath('./p/text()').get()
            # Extract all images
            images = product.css('img::attr(src)').getall()

            yield {
                'description': description,
                'images': images
            }
```

---

## Web Scraping with Scrapy

## Spider Types and Crawling Strategies
- Basic Spider
- CrawlSpider for following links
- SitemapSpider for sitemap parsing
- XMLFeedSpider for XML/RSS
- CSVFeedSpider for CSV data
- Handling pagination and infinite scroll

```python
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# Basic Spider
class SimpleSpider(scrapy.Spider):
    name = "simple"
    start_urls = ["https://example.com"]

    def parse(self, response):
        yield {"url": response.url, "title": response.css("title::text").get()}

# CrawlSpider with Rules
class ArticleSpider(CrawlSpider):
    name = "articles"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/articles"]

    rules = (
        # Extract links matching '/article/' and parse them with parse_article
        Rule(LinkExtractor(allow=r'/article/\d+/'), callback='parse_article'),

        # Extract links matching '/category/' and follow them
        Rule(LinkExtractor(allow=r'/category/'), follow=True),

        # Deny admin pages
        Rule(LinkExtractor(deny=r'/admin/')),
    )

    def parse_article(self, response):
        yield {
            'url': response.url,
            'title': response.css('h1::text').get(),
            'content': response.css('div.content p::text').getall(),
            'date': response.css('span.date::text').get(),
        }

# SitemapSpider
from scrapy.spiders import SitemapSpider

class SitemapProductSpider(SitemapSpider):
    name = "sitemap_products"
    sitemap_urls = ['https://example.com/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product'),
    ]

    def parse_product(self, response):
        yield {
            'url': response.url,
            'name': response.css('h1.product-title::text').get(),
            'price': response.css('span.price::text').get(),
        }
```

---

## Web Scraping with Scrapy

## Items and Item Pipelines
- Define structured data with Item classes
- Process extracted data with Pipelines
- Clean and validate data
- Store to databases or files
- Deduplication and filtering
- Image and file downloading

```python
# Define items in items.py
import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    in_stock = scrapy.Field()
    brand = scrapy.Field()

# Define a spider that yields items
class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = ["https://example.com/products"]

    def parse(self, response):
        for product in response.css('div.product'):
            item = ProductItem()
            item['name'] = product.css('h2::text').get()
            item['price'] = product.css('span.price::text').get()
            item['description'] = product.css('div.description::text').get()
            item['url'] = response.urljoin(product.css('a::attr(href)').get())
            item['image_urls'] = [
                response.urljoin(url) for url in
                product.css('img::attr(src)').getall()
            ]
            item['in_stock'] = 'In Stock' in product.css('div.stock::text').get('')
            item['brand'] = product.css('span.brand::text').get()

            yield item

# Define pipelines in pipelines.py
import re
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from .models import Product, db_connect

class PriceCleanerPipeline:
    def process_item(self, item, spider):
        # Extract numeric price
        if 'price' in item:
            price_str = item['price']
            # Remove currency symbol and commas
            price_match = re.search(r'[\d,]+\.\d+', price_str)
            if price_match:
                item['price'] = float(price_match.group().replace(',', ''))
        return item

class DuplicatesPipeline:
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem(f"Duplicate item found: {item['url']}")
        self.urls_seen.add(item['url'])
        return item

class DatabaseStorePipeline:
    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        product = Product()
        product.name = item['name']
        product.price = item['price']
        # Set other attributes

        try:
            session.add(product)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
```

---

## Web Scraping with Scrapy

## Middlewares and Settings
- Request and response processing
- User-agent rotation
- Proxy management
- Rate limiting
- Cookie handling
- Error handling and retries

```python
# Middleware example in middlewares.py
import random
from scrapy import signals

class RandomUserAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        self.user_agents = getattr(spider, 'user_agents', [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ])

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)
        return None

class ProxyMiddleware:
    def process_request(self, request, spider):
        proxy = getattr(spider, 'proxy', None)
        if proxy:
            request.meta['proxy'] = proxy
        return None

# Settings configuration in settings.py
"""
# Enable middleware
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.RandomUserAgentMiddleware': 543,
    'myproject.middlewares.ProxyMiddleware': 544,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'myproject.pipelines.PriceCleanerPipeline': 300,
    'myproject.pipelines.DuplicatesPipeline': 400,
    'myproject.pipelines.DatabaseStorePipeline': 500,
}

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Configure delay between requests
DOWNLOAD_DELAY = 1.5  # 1.5 seconds between requests

# Enable cookies
COOKIES_ENABLED = True

# Configure retry behavior
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

# Enable caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # 24 hours
HTTPCACHE_DIR = 'httpcache'
"""
```

---

## HTML Parsing with lxml

## Introduction to lxml
- Fast XML and HTML parser
- XPath and CSS selector support
- Compliant with web standards
- Handles malformed HTML
- Memory-efficient parsing
- Used by BeautifulSoup and Scrapy internally

```python
# Installing lxml
# pip install lxml

from lxml import etree, html
import requests

# Parsing HTML from a string
html_string = "<html><body><h1>Title</h1><p>Paragraph</p></body></html>"
tree = html.fromstring(html_string)

# Parsing HTML from a URL
response = requests.get('https://example.com')
tree = html.fromstring(response.content)

# XPath selectors
title = tree.xpath('//h1/text()')[0]
paragraphs = tree.xpath('//p/text()')
links = tree.xpath('//a/@href')

print(f"Title: {title}")
print(f"Paragraphs: {paragraphs}")
print(f"Links: {links}")

# CSS selectors (using cssselect)
title = tree.cssselect('h1')[0].text
paragraphs = [p.text for p in tree.cssselect('p')]
links = [a.get('href') for a in tree.cssselect('a')]

print(f"Title (CSS): {title}")
print(f"Paragraphs (CSS): {paragraphs}")
print(f"Links (CSS): {links}")
```

---

## HTML Parsing with lxml

## Working with XML
- Parse and create XML documents
- XML namespaces
- Validation against schemas
- Transform XML with XSLT
- Efficient XML processing

```python
from lxml import etree
import io

# Create an XML document
root = etree.Element("root")
child1 = etree.SubElement(root, "child")
child1.text = "Child 1 content"
child1.set("attribute", "value")

child2 = etree.SubElement(root, "child")
child2.text = "Child 2 content"

# XML to string
xml_string = etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')
print(xml_string)

# Parse XML
parsed = etree.fromstring(xml_string.encode('utf-8'))
children = parsed.findall(".//child")
print(f"Number of children: {len(children)}")

# Working with namespaces
ns_xml = """
<root xmlns="http://example.com/ns">
  <child>Child in namespace</child>
</root>
"""
ns_root = etree.fromstring(ns_xml.encode('utf-8'))

# Namespace aware lookup
ns = {"e": "http://example.com/ns"}
ns_child = ns_root.find(".//e:child", namespaces=ns)
print(f"Child with namespace: {ns_child.text}")

# XML validation with schema
schema_text = """
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="child" minOccurs="0" maxOccurs="unbounded">
          <xs:complexType>
            <xs:simpleContent>
              <xs:extension base="xs:string">
                <xs:attribute name="attribute" type="xs:string"/>
              </xs:extension>
            </xs:simpleContent>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""

schema_root = etree.parse(io.BytesIO(schema_text.encode('utf-8')))
schema = etree.XMLSchema(schema_root)
valid = schema.validate(root)
print(f"Validation result: {valid}")
```

---

## HTML Parsing with lxml

## HTML Cleaning and Transformation
- Sanitize HTML
- Remove unwanted tags
- Fix malformed HTML
- HTML to plain text conversion
- HTML manipulation

```python
from lxml import html
from lxml.html import clean

# HTML with potentially harmful content
dirty_html = """
<html>
<head>
    <script>alert('XSS attack!');</script>
    <style>body { background: red; }</style>
</head>
<body>
    <h1>Article Title</h1>
    <p>This is a safe paragraph.</p>
    <a href="javascript:alert('XSS');">Dangerous Link</a>
    <iframe src="http://attacker.com"></iframe>
    <div onclick="alert('click')">Click me</div>
    <p>Another safe paragraph.</p>
</body>
</html>
"""

# Parse the HTML
doc = html.fromstring(dirty_html)

# Create a cleaner
cleaner = clean.Cleaner(
    scripts=True,           # Remove script tags
    javascript=True,        # Remove JavaScript (onclick, etc.)
    comments=True,          # Remove comments
    style=True,             # Remove style tags
    links=False,            # Keep links but remove JavaScript links
    meta=True,              # Remove meta tags
    page_structure=False,   # Keep HTML, body, etc.
    processing_instructions=True,
    embedded=True,          # Remove iframe, object, etc.
    frames=True,            # Remove frames
    forms=False,            # Keep forms
    annoying_tags=True,     # Remove blink, marquee
    remove_tags=["div"],    # Remove specific tags
    kill_tags=["iframe"],   # Remove tags and their content
    allow_tags=["h1", "p", "a"],  # Whitelist of allowed tags
    remove_unknown_tags=True,
    safe_attrs_only=True    # Only allow safe attributes
)

# Clean the document
cleaned_doc = cleaner.clean_html(doc)
cleaned_html = html.tostring(cleaned_doc, pretty_print=True).decode('utf-8')
print(cleaned_html)

# Extract plain text
plain_text = cleaned_doc.text_content()
print(plain_text)

# Extract specific element text
title = cleaned_doc.xpath("//h1/text()")[0]
paragraphs = cleaned_doc.xpath("//p/text()")
print(f"Title: {title}")
print(f"Paragraphs: {paragraphs}")

# Modify HTML
for para in cleaned_doc.xpath("//p"):
    para.attrib["class"] = "paragraph"
    para.text = para.text + " [Modified]"

modified_html = html.tostring(cleaned_doc, pretty_print=True).decode('utf-8')
print(modified_html)
```

---

## HTML Parsing with lxml

## Performance Optimization
- Efficient DOM traversal
- Memory management
- Incremental parsing
- Selective node access
- Benchmark comparison

```python
import time
import memory_profiler
from lxml import etree, html
from bs4 import BeautifulSoup
import requests

# Fetch a large HTML page
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_population'
response = requests.get(url)
html_content = response.content

def benchmark_lxml():
    # Parse with lxml
    start_time = time.time()
    tree = html.fromstring(html_content)

    # Extract all table rows
    rows = tree.xpath('//table[contains(@class, "wikitable")]/tbody/tr')

    # Extract data from the first 20 rows
    data = []
    for row in rows[:20]:
        cells = row.xpath('./td')
        if cells:
            row_data = [cell.text_content().strip() for cell in cells]
            data.append(row_data)

    elapsed = time.time() - start_time
    return elapsed, len(data)

def benchmark_beautifulsoup():
    # Parse with BeautifulSoup
    start_time = time.time()
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all table rows
    rows = soup.select('table.wikitable tbody tr')

    # Extract data from the first 20 rows
    data = []
    for row in rows[:20]:
        cells = row.select('td')
        if cells:
            row_data = [cell.text.strip() for cell in cells]
            data.append(row_data)

    elapsed = time.time() - start_time
    return elapsed, len(data)

def benchmark_beautifulsoup_lxml():
    # Parse with BeautifulSoup using lxml parser
    start_time = time.time()
    soup = BeautifulSoup(html_content, 'lxml')

    # Extract all table rows
    rows = soup.select('table.wikitable tbody tr')

    # Extract data from the first 20 rows
    data = []
    for row in rows[:20]:
        cells = row.select('td')
        if cells:
            row_data = [cell.text.strip() for cell in cells]
            data.append(row_data)

    elapsed = time.time() - start_time
    return elapsed, len(data)

# Run benchmarks
lxml_time, lxml_count = benchmark_lxml()
bs_time, bs_count = benchmark_beautifulsoup()
bs_lxml_time, bs_lxml_count = benchmark_beautifulsoup_lxml()

print(f"lxml: {lxml_time:.4f}s for {lxml_count} rows")
print(f"BeautifulSoup (html.parser): {bs_time:.4f}s for {bs_count} rows")
print(f"BeautifulSoup (lxml): {bs_lxml_time:.4f}s for {bs_lxml_count} rows")
print(f"lxml is {bs_time/lxml_time:.2f}x faster than BeautifulSoup (html.parser)")
print(f"lxml is {bs_lxml_time/lxml_time:.2f}x faster than BeautifulSoup (lxml)")
```

---

## Testing Web Applications with Selenium

## Introduction to Selenium
- Automate browser interactions
- Simulate user behavior
- Test web applications
- Extract data from JavaScript-rendered pages
- Support for multiple browsers
- Execute JavaScript

```python
# Installing Selenium
# pip install selenium
# Download webdriver for your browser (e.g., ChromeDriver)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Initialize the driver
service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Navigate to a page
    driver.get("https://example.com")

    # Get page information
    title = driver.title
    current_url = driver.current_url

    print(f"Title: {title}")
    print(f"URL: {current_url}")

    # Find elements
    heading = driver.find_element(By.TAG_NAME, "h1")
    paragraph = driver.find_element(By.TAG_NAME, "p")

    print(f"Heading: {heading.text}")
    print(f"Paragraph: {paragraph.text}")

    # Take a screenshot
    driver.save_screenshot("example.png")

finally:
    # Always quit the driver
    driver.quit()
```

---

## Testing Web Applications with Selenium

## Selenium Element Selection
- Find elements by ID, class, tag, CSS, XPath
- Work with single or multiple elements
- Element properties and attributes
- Element state (visible, enabled)
- Wait for elements to appear

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service)

try:
    # Navigate to a page
    driver.get("https://www.python.org")

    # Find element by ID
    element_by_id = driver.find_element(By.ID, "documentation")
    print(f"By ID: {element_by_id.text}")

    # Find element by class name
    element_by_class = driver.find_element(By.CLASS_NAME, "widget-title")
    print(f"By class: {element_by_class.text}")

    # Find element by tag name
    element_by_tag = driver.find_element(By.TAG_NAME, "h1")
    print(f"By tag: {element_by_tag.text}")

    # Find element by CSS selector
    element_by_css = driver.find_element(By.CSS_SELECTOR, "#site-map > div.row > div:nth-child(1) > h2")
    print(f"By CSS: {element_by_css.text}")

    # Find element by XPath
    element_by_xpath = driver.find_element(By.XPATH, "//div[@class='introduction']/p[1]")
    print(f"By XPath: {element_by_xpath.text}")

    # Find elements (plural) - returns a list
    elements = driver.find_elements(By.CSS_SELECTOR, "#site-map a")
    print(f"Found {len(elements)} links")
    for i, element in enumerate(elements[:5]):
        print(f"Link {i+1}: {element.text} - {element.get_attribute('href')}")

    # Element properties
    print(f"Is displayed: {element_by_id.is_displayed()}")
    print(f"Is enabled: {element_by_id.is_enabled()}")
    print(f"Tag name: {element_by_id.tag_name}")
    print(f"Size: {element_by_id.size}")
    print(f"Location: {element_by_id.location}")

    # Wait for element
    wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
    element = wait.until(
        EC.presence_of_element_located((By.ID, "success-stories"))
    )
    print(f"Found after waiting: {element.text}")

finally:
    driver.quit()
```

---

## Testing Web Applications with Selenium

## Interacting with Pages
- Click elements
- Enter text
- Submit forms
- Select dropdowns
- Handle alerts
- Scroll and move
- Drag and drop

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service)

try:
    # Navigate to a form page
    driver.get("https://www.example.com/form")

    # Click a button
    button = driver.find_element(By.ID, "submit-button")
    button.click()

    # Enter text in a field
    text_field = driver.find_element(By.NAME, "username")
    text_field.clear()  # Clear existing text
    text_field.send_keys("testuser")

    # Enter text and press Enter
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("selenium python")
    search_box.send_keys(Keys.RETURN)

    # Work with select dropdowns
    select_element = driver.find_element(By.ID, "dropdown")
    select = Select(select_element)

    # Select by visible text
    select.select_by_visible_text("Option 1")

    # Select by value attribute
    select.select_by_value("option2")

    # Select by index
    select.select_by_index(2)

    # Get selected option
    selected_option = select.first_selected_option
    print(f"Selected: {selected_option.text}")

    # Handle alerts
    driver.find_element(By.ID, "alert-button").click()

    # Wait for alert to appear
    WebDriverWait(driver, 5).until(EC.alert_is_present())

    # Switch to the alert
    alert = driver.switch_to.alert
    print(f"Alert text: {alert.text}")

    # Accept the alert (click OK)
    alert.accept()

    # For dismiss (cancel), use:
    # alert.dismiss()

    # Scroll page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Scroll to a specific element
    element = driver.find_element(By.ID, "footer")
    driver.execute_script("arguments[0].scrollIntoView();", element)

    # Mouse hover
    menu = driver.find_element(By.ID, "menu")
    ActionChains(driver).move_to_element(menu).perform()

    # Drag and drop
    source = driver.find_element(By.ID, "draggable")
    target = driver.find_element(By.ID, "droppable")
    ActionChains(driver).drag_and_drop(source, target).perform()

finally:
    driver.quit()
```

---

## Testing Web Applications with Selenium

## Working with Windows and Frames
- Switch between browser windows
- Work with iframes
- Handle popups
- Navigate browser history
- Cookies and local storage

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service)

try:
    # Navigate to a page
    driver.get("https://www.example.com")

    # Open a new window/tab
    driver.execute_script("window.open('https://www.python.org', '_blank');")

    # Get all window handles
    handles = driver.window_handles
    print(f"Number of windows: {len(handles)}")

    # Switch to the new window
    driver.switch_to.window(handles[1])
    print(f"New window title: {driver.title}")

    # Switch back to the original window
    driver.switch_to.window(handles[0])
    print(f"Original window title: {driver.title}")

    # Navigate to a page with frames
    driver.get("https://www.example.com/frames")

    # Switch to frame by index
    driver.switch_to.frame(0)

    # Switch to frame by name or ID
    driver.switch_to.frame("frame-name")

    # Switch to frame by element
    frame_element = driver.find_element(By.CSS_SELECTOR, "iframe.content")
    driver.switch_to.frame(frame_element)

    # Work inside the frame
    element_in_frame = driver.find_element(By.ID, "inside-frame")
    print(f"Element in frame: {element_in_frame.text}")

    # Switch back to the main content
    driver.switch_to.default_content()

    # Browser navigation
    driver.get("https://www.example.com/page1")
    driver.get("https://www.example.com/page2")

    # Go back
    driver.back()
    print(f"After back: {driver.title}")

    # Go forward
    driver.forward()
    print(f"After forward: {driver.title}")

    # Refresh page
    driver.refresh()

    # Working with cookies
    driver.add_cookie({"name": "test_cookie", "value": "test_value"})

    cookie = driver.get_cookie("test_cookie")
    print(f"Cookie: {cookie}")

    all_cookies = driver.get_cookies()
    print(f"Number of cookies: {len(all_cookies)}")

    driver.delete_cookie("test_cookie")
    driver.delete_all_cookies()

    # Local storage
    driver.execute_script("localStorage.setItem('key', 'value');")
    value = driver.execute_script("return localStorage.getItem('key');")
    print(f"Local storage value: {value}")

finally:
    driver.quit()
```

---

## Testing Web Applications with Selenium

## Selenium for Web Testing
- Test case organization
- Assertions
- Page Object Model
- Test suites
- Integration with test frameworks
- Reports and screenshots

```python
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Page Object for login page
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login")
        self.error_message = (By.ID, "error-message")

    def load(self):
        self.driver.get("https://example.com/login")

    def enter_username(self, username):
        self.driver.find_element(*self.username_input).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

# Page Object for dashboard page
class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.welcome_message = (By.ID, "welcome")
        self.logout_button = (By.ID, "logout")

    def get_welcome_message(self):
        return self.driver.find_element(*self.welcome_message).text

    def is_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.welcome_message)
            )
            return True
        except:
            return False

    def logout(self):
        self.driver.find_element(*self.logout_button).click()

# Test cases using unittest
class LoginTests(unittest.TestCase):
    def setUp(self):
        service = Service('/path/to/chromedriver')
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

    def tearDown(self):
        if hasattr(self, '_outcome') and hasattr(self._outcome, 'errors'):
            # If the test failed, take a screenshot
            for method, error in self._outcome.errors:
                if error:
                    self.driver.save_screenshot(f"error_{self._testMethodName}.png")
        self.driver.quit()

    def test_valid_login(self):
        self.login_page.load()
        self.login_page.login("validuser", "validpass")

        # Assert that we're on the dashboard
        self.assertTrue(self.dashboard_page.is_loaded(), "Dashboard page did not load")

        # Assert welcome message
        welcome_text = self.dashboard_page.get_welcome_message()
        self.assertIn("Welcome", welcome_text)

    def test_invalid_login(self):
        self.login_page.load()
        self.login_page.login("invaliduser", "invalidpass")

        # Assert error message
        error_text = self.login_page.get_error_message()
        self.assertEqual("Invalid username or password", error_text)

if __name__ == "__main__":
    unittest.main()
```

---

## Testing Web Applications with Selenium

## Selenium in CI/CD Pipelines
- Integration with CI systems
- Headless browser testing
- Cross-browser testing
- Parallel test execution
- Test results reporting
- Docker integration

```python
# Example of headless Chrome configuration for CI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def get_driver_for_ci():
    chrome_options = Options()

    # Headless mode
    chrome_options.add_argument("--headless")

    # Disable GPU (good for CI environments)
    chrome_options.add_argument("--disable-gpu")

    # Set window size
    chrome_options.add_argument("--window-size=1920,1080")

    # Disable sandbox for CI environments
    chrome_options.add_argument("--no-sandbox")

    # Disable dev-shm usage (for Docker)
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Create the driver
    service = Service('/usr/bin/chromedriver')  # Adjust path for CI
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

# Example GitHub Actions workflow for Selenium testing
"""
# .github/workflows/selenium-tests.yml
name: Selenium Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install Chrome
      run: |
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable

    - name: Install ChromeDriver
      run: |
        CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1)
        CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
        wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
        unzip chromedriver_linux64.zip
        sudo mv chromedriver /usr/bin/chromedriver
        sudo chmod +x /usr/bin/chromedriver

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install pytest-html

    - name: Run tests
      run: |
        pytest tests/ --html=report.html --self-contained-html

    - name: Upload test report
      uses: actions/upload-artifact@v2
      with:
        name: test-report
        path: report.html
"""
```

---

## Summary

## Key Takeaways
- Flask provides a lightweight framework for web servers
- Requests simplifies HTTP client operations
- BeautifulSoup and Scrapy excel at web scraping
- lxml offers powerful HTML/XML processing
- Selenium enables browser automation and testing
- Python has a rich ecosystem for web development
- Each tool has specific strengths and use cases

---

## Resources

## Further Reading
- Flask documentation: flask.palletsprojects.com
- Requests documentation: docs.python-requests.org
- BeautifulSoup documentation: www.crummy.com/software/BeautifulSoup/bs4/doc/
- Scrapy documentation: docs.scrapy.org
- lxml documentation: lxml.de
- Selenium documentation: www.selenium.dev/documentation/
- "Web Scraping with Python" by Ryan Mitchell
- "Flask Web Development" by Miguel Grinberg
