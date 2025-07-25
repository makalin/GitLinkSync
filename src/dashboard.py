from flask import Flask, render_template_string
from src import db, analytics

app = Flask(__name__)

@app.route('/')
def index():
    links = db.get_links()
    stats = {
        'total': analytics.get_total_links(),
        'followed': analytics.get_followed_count(),
        'unfollowed': analytics.get_unfollowed_count(),
        'rate': analytics.get_follow_back_rate(),
    }
    return render_template_string('''
    <h1>GitLinkSync Dashboard</h1>
    <h2>Stats</h2>
    <ul>
      <li>Total links: {{ stats.total }}</li>
      <li>Followed: {{ stats.followed }}</li>
      <li>Unfollowed: {{ stats.unfollowed }}</li>
      <li>Follow-back rate: {{ stats.rate }}%</li>
    </ul>
    <h2>Links</h2>
    <table border="1">
      <tr><th>URL</th><th>Followed</th></tr>
      {% for url, followed in links %}
        <tr><td>{{ url }}</td><td>{{ 'Yes' if followed else 'No' }}</td></tr>
      {% endfor %}
    </table>
    ''', links=links, stats=stats)

if __name__ == "__main__":
    app.run(debug=True) 