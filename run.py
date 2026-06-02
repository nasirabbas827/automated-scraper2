from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
import requests
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "YOUR_OWN_API_KEY"

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            cellNo TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

init_db()

import time
import random
import requests
from flask import render_template, request, flash, redirect, url_for, session
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Download necessary NLTK data if not already available
# nltk.download('punkt')
# nltk.download('stopwords')

import time
import random
import requests
from flask import render_template, request, flash, redirect, url_for, session
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter



import matplotlib.pyplot as plt
import io
import base64
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
from bs4 import BeautifulSoup
import time
import random

# Function to generate focus keywords visualization using Matplotlib
def generate_focus_keywords_visualization(focused_keywords):
    # Unzip the list of keywords and their frequencies
    keywords, counts = zip(*focused_keywords)  # Unpack the list of tuples

    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(keywords, counts, color='skyblue')
    ax.set_xlabel('Frequency')
    ax.set_title('Top Focus Keywords')

    # Save the figure to a BytesIO object
    img_stream = io.BytesIO()
    plt.tight_layout()  # Adjust layout for better fit
    plt.savefig(img_stream, format='png')  # Save as PNG to in-memory stream
    img_stream.seek(0)  # Rewind to the start of the stream

    # Encode image as base64
    img_data = base64.b64encode(img_stream.getvalue()).decode('utf-8')
    plt.close(fig)  # Close the plot to free memory
    return img_data

# Scrape gig data and extract focus keywords
def scrape_data(keyword):
    url = f"https://www.fiverr.com/search/gigs?query={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return [], None

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = []
    seen_titles = set()

    for gig in soup.find_all('div', class_='basic-gig-card')[:3]:  # Limiting to results for now
        username_tag = gig.find('a', class_='text-bold')
        title_tag = gig.find('p', role='heading', class_='f2YMuU6 tbody-5 text-normal')
        seller_rank_tag = gig.find('p', class_='z58z872')
        rating_tag = gig.find('strong', class_='rating-score')
        price_tag = gig.find('span', class_='text-bold co-grey-1200')
        image_tag = gig.find('img', class_='box-image-ratio')
        url_tag = gig.find('a', {'aria-label': 'Go to gig'})

        username = username_tag.text.strip() if username_tag else 'No username'
        title = title_tag.text.strip() if title_tag else 'No title'
        seller_rank = seller_rank_tag.text.strip() if seller_rank_tag else 'No rank'
        rating = rating_tag.text.strip() if rating_tag else 'No rating'
        price = price_tag.text.strip() if price_tag else 'No price'
        image_url = image_tag['src'] if image_tag else ''
        gig_url = 'https://www.fiverr.com' + url_tag['href'] if url_tag else 'No URL'

        # Scraping gig details
        time.sleep(random.uniform(2, 5))  # Adding sleep to avoid bot detection
        gig_details = get_automated_description(gig_url)

        if title not in seen_titles:
            listings.append({
                'username': username,
                'title': title,
                'seller_rank': seller_rank,
                'rating': rating,
                'price': price,
                'image_url': image_url,
                'gig_url': gig_url,
                'gig_description': gig_details['description'] if gig_details else 'No description available'
            })
            seen_titles.add(title)

    # Process all titles and descriptions to extract focused keywords
    focused_keywords = extract_focused_keywords(listings)
    
    # Generate the visualization image
    img_data = generate_focus_keywords_visualization(focused_keywords)
    
    return listings, focused_keywords, img_data

# Function to extract focused keywords from gig listings
def extract_focused_keywords(listings):
    stop_words = set(stopwords.words('english'))
    all_text = []
    
    # Combine all titles and descriptions into one list
    for listing in listings:
        all_text.append(listing['title'])
        all_text.append(listing['gig_description'])
    
    # Tokenize and remove stopwords
    words = []
    for text in all_text:
        tokens = word_tokenize(text.lower())
        filtered_words = [word for word in tokens if word.isalnum() and word not in stop_words]
        words.extend(filtered_words)
    
    # Count the frequency of each word
    word_counts = Counter(words)
    
    # Get the most common words (focus keywords)
    focused_keywords = word_counts.most_common(10)  # Show top most frequent keywords
    
    return focused_keywords  # Return as a list of tuples (keyword, count)

@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = ''
    listings = []
    focused_keywords = []
    img_data = None
    
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        listings, focused_keywords, img_data = scrape_data(keyword)
        session['listings'] = listings  # Store the listings in session
        session['focused_keywords'] = focused_keywords  # Store the focused keywords in session
        session['img_data'] = img_data  # Store the image data in session

    return render_template('search.html', keyword=keyword, listings=listings, focused_keywords=focused_keywords, img_data=img_data)


def get_automated_description(gig_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(gig_url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

    if response.status_code != 200:
        print("Failed to retrieve page. Status code:", response.status_code)
        return None

    time.sleep(random.uniform(2, 5))  # Sleep to avoid bot detection

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting gig details
    gig_title = soup.find('h1', class_='_1axk4v3k zle7n01g8 zle7n01ge zle7n01dq zle7n01dw zle7n08 zle7n02 zle7n0og')
    gig_description = soup.find('div', class_='gig-description')

    # Return the gig title and description
    gig_details = {
        'title': gig_title.text.strip() if gig_title else 'No Title Available',
        'description': gig_description.text.strip() if gig_description else 'No Description Available',
        'url': gig_url
    }

    return gig_details


import time
import random
import requests
from flask import render_template, request, flash, redirect, url_for
from bs4 import BeautifulSoup

@app.route('/view_gig')
def view_gig():
    gig_url = request.args.get('gig_url')  # Get gig URL from query parameter
    gig_details = get_description(gig_url)
    if gig_details:
        return render_template('view_gig.html', gig=gig_details)
    else:
        flash("Failed to retrieve gig details.", "error")
        return redirect(url_for('search'))  # Redirect back to search if failed

def get_description(gig_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(gig_url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

    if response.status_code != 200:
        print("Failed to retrieve page. Status code:", response.status_code)
        return None

    time.sleep(random.uniform(2, 5))  # To avoid detection as a bot

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting gig details
    gig_title = soup.find('h1', class_='_1axk4v3k zle7n01g8 zle7n01ge zle7n01dq zle7n01dw zle7n08 zle7n02 zle7n0og')
    gig_image = soup.find('img', class_='profile-pict-img')
    public_name = soup.find('div', class_='FS8RhT9 tbody-4 text-bold')
    level = soup.find('p', class_='zle7n02')
    rating = soup.find('strong', class_='_1axk4v3k zle7n01f9 zle7n01cr zle7n08 zle7n02 zle7n0r3')
    total_ratings = soup.find('span', class_='_1axk4v3k zle7n024y zle7n01f9 zle7n01cr zle7n06 zle7n02 zle7n0d')
    seller_statistics = soup.find('div', class_='stats-desc')
    gig_description = soup.find('div', class_='gig-description')

    # Extracting all feedbacks
    feedback_elements = soup.find_all('div', class_='reliable-review-description review-description')

    # Extract and clean data for feedbacks (get only the first 5)
    feedback_list = [feedback.text.strip() for feedback in feedback_elements[:5]] if feedback_elements else ['No Feedbacks Available']

    # Extract and clean other data
    gig_details = {
        'title': gig_title.text.strip() if gig_title else 'No Title Available',
        'image': gig_image['src'] if gig_image else 'No Image Available',
        'public_name': public_name.text.strip() if public_name else 'No Name Available',
        'level': level.text.strip() if level else 'No Level Available',
        'rating': rating.text.strip() if rating else 'No Rating Available',
        'total_ratings': total_ratings.text.strip() if total_ratings else 'No Total Ratings Available',
        'seller_statistics': seller_statistics.text.strip() if seller_statistics else 'No Seller Stats Available',
        'description': gig_description.text.strip() if gig_description else 'No Description Available',
        'feedbacks': feedback_list,  # List of feedbacks
        'url': gig_url
    }

    return gig_details


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = ""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cellNo = request.form['cellNo']
        password = request.form['password']

        if not name or not email or not cellNo or not password:
            error_message = "All fields are required!"
            return redirect(url_for('register', error=error_message))

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (name, email, cellNo, password) VALUES (?, ?, ?, ?)',
                         (name, email, cellNo, password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            error_message = 'Email already registered!'
        finally:
            conn.close()

    return render_template('register.html', error=error_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            error_message = 'Invalid email or password!'

    return render_template('login.html', error=error_message)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
