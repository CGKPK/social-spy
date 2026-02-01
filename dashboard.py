"""
Dashboard Generator
====================
Generates a beautiful HTML dashboard with charts and visualizations.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict


def generate_dashboard(data: Dict, output_path: str = "dashboard.html"):
    """
    Generate an HTML dashboard from social media data.

    Args:
        data: Dictionary containing posts and stats
        output_path: Path to save the HTML file
    """
    posts = data.get("posts", [])
    stats = data.get("stats", {})
    last_updated = data.get("last_updated", datetime.now().isoformat())

    # Calculate additional metrics
    platform_data = stats.get("by_platform", {})

    # Get recent posts (last 7 days)
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    recent_posts = [
        p for p in posts
        if p.get("published", p.get("fetched_at", "")) >= week_ago
    ]

    # Posts by day (last 7 days)
    posts_by_day = defaultdict(int)
    for post in posts:
        date_str = post.get("published", post.get("fetched_at", ""))[:10]
        if date_str:
            posts_by_day[date_str] += 1

    # Sort and get last 7 days
    sorted_days = sorted(posts_by_day.items(), reverse=True)[:7]
    sorted_days.reverse()

    # Top posts by engagement
    def get_engagement(post):
        return (
            post.get("likes", 0) +
            post.get("comments", 0) * 2 +
            post.get("shares", post.get("retweets", 0)) * 3 +
            (post.get("views", 0) // 1000 if post.get("views") else 0)
        )

    top_posts = sorted(posts, key=get_engagement, reverse=True)[:10]

    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #e4e4e4;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
        }}

        h1 {{
            font-size: 2.5rem;
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}

        .last-updated {{
            color: #888;
            font-size: 0.9rem;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-card .icon {{
            font-size: 2rem;
            margin-bottom: 10px;
        }}

        .stat-card .value {{
            font-size: 2rem;
            font-weight: bold;
            color: #fff;
        }}

        .stat-card .label {{
            color: #888;
            font-size: 0.9rem;
            margin-top: 5px;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .chart-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .chart-card h3 {{
            margin-bottom: 20px;
            color: #fff;
        }}

        .posts-section {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 30px;
        }}

        .posts-section h2 {{
            margin-bottom: 20px;
            color: #fff;
        }}

        .post-list {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .post-card {{
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: background 0.3s ease;
        }}

        .post-card:hover {{
            background: rgba(255, 255, 255, 0.08);
        }}

        .post-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}

        .platform-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }}

        .platform-youtube {{ background: #ff0000; color: white; }}
        .platform-twitter {{ background: #1da1f2; color: white; }}
        .platform-facebook {{ background: #1877f2; color: white; }}
        .platform-instagram {{ background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: white; }}
        .platform-linkedin {{ background: #0077b5; color: white; }}
        .platform-manual {{ background: #6c757d; color: white; }}

        .post-author {{
            color: #667eea;
            font-weight: 500;
        }}

        .post-date {{
            color: #666;
            font-size: 0.85rem;
            margin-left: auto;
        }}

        .post-text {{
            color: #ccc;
            line-height: 1.6;
            margin-bottom: 15px;
        }}

        .post-metrics {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}

        .metric {{
            display: flex;
            align-items: center;
            gap: 5px;
            color: #888;
            font-size: 0.9rem;
        }}

        .post-link {{
            color: #667eea;
            text-decoration: none;
            font-size: 0.9rem;
            margin-left: auto;
        }}

        .post-link:hover {{
            text-decoration: underline;
        }}

        .filters {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: transparent;
            color: #ccc;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .filter-btn:hover, .filter-btn.active {{
            background: #667eea;
            border-color: #667eea;
            color: white;
        }}

        .no-data {{
            text-align: center;
            padding: 40px;
            color: #666;
        }}

        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Social Media Dashboard</h1>
            <p class="last-updated">Last updated: {format_date(last_updated)}</p>
        </header>

        <!-- Stats Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="icon">📝</div>
                <div class="value">{stats.get('total_posts', len(posts))}</div>
                <div class="label">Total Posts</div>
            </div>
            <div class="stat-card">
                <div class="icon">❤️</div>
                <div class="value">{format_number(stats.get('total_likes', 0))}</div>
                <div class="label">Total Likes</div>
            </div>
            <div class="stat-card">
                <div class="icon">💬</div>
                <div class="value">{format_number(stats.get('total_comments', 0))}</div>
                <div class="label">Total Comments</div>
            </div>
            <div class="stat-card">
                <div class="icon">🔄</div>
                <div class="value">{format_number(stats.get('total_shares', 0))}</div>
                <div class="label">Total Shares</div>
            </div>
            <div class="stat-card">
                <div class="icon">📈</div>
                <div class="value">{len(recent_posts)}</div>
                <div class="label">Posts This Week</div>
            </div>
        </div>

        <!-- Charts -->
        <div class="charts-grid">
            <div class="chart-card">
                <h3>Posts by Platform</h3>
                <canvas id="platformChart"></canvas>
            </div>
            <div class="chart-card">
                <h3>Activity Over Time</h3>
                <canvas id="activityChart"></canvas>
            </div>
        </div>

        <!-- Recent Posts -->
        <div class="posts-section">
            <h2>📰 Recent Posts</h2>
            <div class="filters">
                <button class="filter-btn active" onclick="filterPosts('all')">All</button>
                <button class="filter-btn" onclick="filterPosts('youtube')">YouTube</button>
                <button class="filter-btn" onclick="filterPosts('twitter')">Twitter/X</button>
                <button class="filter-btn" onclick="filterPosts('facebook')">Facebook</button>
                <button class="filter-btn" onclick="filterPosts('instagram')">Instagram</button>
                <button class="filter-btn" onclick="filterPosts('linkedin')">LinkedIn</button>
            </div>
            <div class="post-list" id="postList">
                {generate_post_cards(posts[:50])}
            </div>
        </div>

        <!-- Top Performing Posts -->
        <div class="posts-section">
            <h2>🏆 Top Performing Posts</h2>
            <div class="post-list">
                {generate_post_cards(top_posts)}
            </div>
        </div>
    </div>

    <script>
        // Platform distribution chart
        const platformCtx = document.getElementById('platformChart').getContext('2d');
        new Chart(platformCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(list(platform_data.keys()))},
                datasets: [{{
                    data: {json.dumps(list(platform_data.values()))},
                    backgroundColor: [
                        '#ff0000',  // YouTube
                        '#1da1f2',  // Twitter
                        '#1877f2',  // Facebook
                        '#e4405f',  // Instagram
                        '#0077b5',  // LinkedIn
                        '#6c757d',  // Other
                    ],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{ color: '#ccc' }}
                    }}
                }}
            }}
        }});

        // Activity over time chart
        const activityCtx = document.getElementById('activityChart').getContext('2d');
        new Chart(activityCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps([d[0] for d in sorted_days])},
                datasets: [{{
                    label: 'Posts',
                    data: {json.dumps([d[1] for d in sorted_days])},
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{ color: 'rgba(255,255,255,0.1)' }},
                        ticks: {{ color: '#888' }}
                    }},
                    x: {{
                        grid: {{ display: false }},
                        ticks: {{ color: '#888' }}
                    }}
                }}
            }}
        }});

        // Filter functionality
        function filterPosts(platform) {{
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            const posts = document.querySelectorAll('.post-card');
            posts.forEach(post => {{
                if (platform === 'all' || post.dataset.platform === platform) {{
                    post.style.display = 'block';
                }} else {{
                    post.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


def generate_post_cards(posts: List[Dict]) -> str:
    """Generate HTML for post cards."""
    if not posts:
        return '<div class="no-data">No posts found. Run the listener to fetch posts.</div>'

    cards = []
    for post in posts:
        platform = post.get("platform", "other")
        text = post.get("text", post.get("title", ""))[:300]
        if len(post.get("text", post.get("title", ""))) > 300:
            text += "..."

        author = post.get("author", post.get("author_username", "Unknown"))
        date = format_date(post.get("published", post.get("fetched_at", "")))
        url = post.get("url", "")

        # Metrics
        likes = post.get("likes", 0)
        comments = post.get("comments", post.get("replies", 0))
        shares = post.get("shares", post.get("retweets", 0))
        views = post.get("views", 0)

        metrics_html = ""
        if likes:
            metrics_html += f'<span class="metric">❤️ {format_number(likes)}</span>'
        if comments:
            metrics_html += f'<span class="metric">💬 {format_number(comments)}</span>'
        if shares:
            metrics_html += f'<span class="metric">🔄 {format_number(shares)}</span>'
        if views:
            metrics_html += f'<span class="metric">👁️ {format_number(views)}</span>'

        link_html = f'<a href="{url}" target="_blank" class="post-link">View →</a>' if url else ""

        card = f'''
        <div class="post-card" data-platform="{platform}">
            <div class="post-header">
                <span class="platform-badge platform-{platform}">{platform.upper()}</span>
                <span class="post-author">@{author}</span>
                <span class="post-date">{date}</span>
            </div>
            <p class="post-text">{escape_html(text)}</p>
            <div class="post-metrics">
                {metrics_html}
                {link_html}
            </div>
        </div>'''
        cards.append(card)

    return "\n".join(cards)


def format_date(date_str: str) -> str:
    """Format a date string for display."""
    if not date_str:
        return "Unknown"
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y %H:%M")
    except (ValueError, TypeError):
        return date_str[:16] if len(date_str) > 16 else date_str


def format_number(num: int) -> str:
    """Format a number with K/M suffixes."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


if __name__ == "__main__":
    # Test with sample data
    sample_data = {
        "posts": [
            {
                "platform": "youtube",
                "title": "Sample YouTube Video",
                "author": "Test Channel",
                "published": datetime.now().isoformat(),
                "url": "https://youtube.com/watch?v=example",
                "views": 10000,
            },
            {
                "platform": "twitter",
                "text": "This is a sample tweet for testing the dashboard!",
                "author": "testuser",
                "published": datetime.now().isoformat(),
                "likes": 150,
                "retweets": 25,
            },
        ],
        "stats": {
            "total_posts": 2,
            "by_platform": {"youtube": 1, "twitter": 1},
            "total_likes": 150,
            "total_comments": 0,
            "total_shares": 25,
        },
    }

    generate_dashboard(sample_data, "test_dashboard.html")
    print("Test dashboard generated: test_dashboard.html")
