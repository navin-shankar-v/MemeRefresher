import random
import requests
from flask import Flask, render_template

app = Flask(__name__)

def get_random_meme():
    """
    Fetches a list of posts from r/memes, filters out NSFW posts,
    and returns the URL of a random meme image.
    """
    reddit_url = "https://www.reddit.com/r/memes/hot.json?limit=50"
    headers = {"User-Agent": "meme-fetcher/0.1"}  # Reddit requires a User-Agent header
    try:
        response = requests.get(reddit_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching from Reddit:", e)
        return None

    data = response.json()
    posts = data.get("data", {}).get("children", [])

    # Filter out posts that are NSFW
    safe_posts = [post for post in posts if not post["data"].get("over_18", True)]

    if not safe_posts:
        return None

    meme = random.choice(safe_posts)
    # Usually the post's 'url' is a direct link to the image (if available)
    meme_url = meme["data"].get("url")
    return meme_url

@app.route("/")
def index():
    meme_url = get_random_meme()
    if not meme_url:
        meme_url = "https://via.placeholder.com/500?text=No+Meme+Available"
    return render_template("index.html", meme_url=meme_url)

if __name__ == "__main__":
    # Note: For production, do not use debug=True. Use a proper WSGI server.
    app.run(host="0.0.0.0", port=5000, debug=True)
