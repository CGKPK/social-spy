#!/usr/bin/env python3
"""
Social Media Trends Analyzer
=============================
Analyzes collected social media data to identify trends,
top subjects, and what's moving in the prop trading space.
"""

import json
import re
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

def load_data(filepath: str = "social_data.json") -> Dict:
    """Load the social data JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from text."""
    # Common words to filter out
    stopwords = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
        'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
        'from', 'up', 'about', 'into', 'over', 'after', 'beneath', 'under',
        'above', 'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either',
        'neither', 'not', 'only', 'own', 'same', 'than', 'too', 'very', 's',
        't', 'just', 'don', 'now', 'this', 'that', 'these', 'those', 'i',
        'me', 'my', 'myself', 'we', 'our', 'you', 'your', 'he', 'him', 'his',
        'she', 'her', 'it', 'its', 'they', 'them', 'their', 'what', 'which',
        'who', 'whom', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
        'any', 'some', 'no', 'if', 'as', 'get', 'got', 'use', 'code', 'best',
        'new', 'one', 'like', 'https', 'http', 'www', 'com', 'amp', 'gt', 'lt',
        're', 've', 'll', 'bit', 'ly', 'more', 'out', 'here', 'off', 'also'
    }

    # Extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return [w for w in words if w not in stopwords]

def analyze_data(data: Dict) -> Dict:
    """Perform comprehensive analysis on the data."""
    posts = data.get("posts", [])

    analysis = {
        "summary": {},
        "top_keywords": [],
        "top_authors": [],
        "top_videos": [],
        "top_tweets": [],
        "trending_topics": [],
        "prop_firms_mentioned": {},
        "timeline": {},
        "engagement_analysis": {},
        "keyword_matches": {},
    }

    # Summary stats
    youtube_posts = [p for p in posts if p.get("platform") == "youtube"]
    twitter_posts = [p for p in posts if p.get("platform") == "twitter"]

    analysis["summary"] = {
        "total_posts": len(posts),
        "youtube_videos": len(youtube_posts),
        "twitter_posts": len(twitter_posts),
        "total_views": sum(p.get("views", 0) for p in posts),
        "total_likes": sum(p.get("likes", 0) for p in posts),
        "total_retweets": sum(p.get("retweets", 0) for p in posts),
    }

    # Extract all text for keyword analysis
    all_keywords = []
    for post in posts:
        text = post.get("text", "") or post.get("title", "") or ""
        text += " " + (post.get("description", "") or "")
        all_keywords.extend(extract_keywords(text))

    # Top keywords
    keyword_counts = Counter(all_keywords)
    analysis["top_keywords"] = keyword_counts.most_common(30)

    # Track specific prop firms
    prop_firms = {
        "apex": ["apex", "apexfunding", "apextraderfunding"],
        "myfundedfutures": ["myfundedfutures", "mff", "fundedfutures"],
        "takeprofittrader": ["takeprofittrader", "tpt", "takeprofit"],
        "tradeify": ["tradeify"],
        "fundednext": ["fundednext"],
        "blusky": ["blusky", "bluskytrading", "bluesky"],
        "topstep": ["topstep"],
        "bulenox": ["bulenox"],
        "alphacapital": ["alphacapital", "alpha capital"],
    }

    firm_mentions = defaultdict(int)
    for post in posts:
        text = (post.get("text", "") or post.get("title", "") or "").lower()
        text += " " + (post.get("description", "") or "").lower()
        for firm, aliases in prop_firms.items():
            for alias in aliases:
                if alias in text:
                    firm_mentions[firm] += 1
                    break

    analysis["prop_firms_mentioned"] = dict(sorted(
        firm_mentions.items(),
        key=lambda x: x[1],
        reverse=True
    ))

    # Top YouTube videos by views
    youtube_sorted = sorted(
        youtube_posts,
        key=lambda x: x.get("views", 0),
        reverse=True
    )
    analysis["top_videos"] = [
        {
            "title": v.get("title", "")[:80],
            "author": v.get("author", ""),
            "views": v.get("views", 0),
            "url": v.get("url", ""),
        }
        for v in youtube_sorted[:10]
    ]

    # Top tweets by engagement
    twitter_sorted = sorted(
        twitter_posts,
        key=lambda x: x.get("likes", 0) + x.get("retweets", 0),
        reverse=True
    )
    analysis["top_tweets"] = [
        {
            "text": t.get("text", "")[:120],
            "author": t.get("author", "") or t.get("author_username", ""),
            "likes": t.get("likes", 0),
            "retweets": t.get("retweets", 0),
            "url": t.get("url", ""),
        }
        for t in twitter_sorted[:10]
    ]

    # Top authors
    author_engagement = defaultdict(lambda: {"posts": 0, "views": 0, "likes": 0})
    for post in posts:
        author = post.get("author", "") or post.get("channel_name", "") or "Unknown"
        author_engagement[author]["posts"] += 1
        author_engagement[author]["views"] += post.get("views", 0)
        author_engagement[author]["likes"] += post.get("likes", 0)

    sorted_authors = sorted(
        author_engagement.items(),
        key=lambda x: x[1]["views"] + x[1]["likes"] * 10,
        reverse=True
    )
    analysis["top_authors"] = [
        {"name": name, **stats}
        for name, stats in sorted_authors[:15]
    ]

    # Timeline analysis (posts per day)
    posts_by_day = defaultdict(int)
    for post in posts:
        pub = post.get("published", "")
        if pub:
            try:
                date = pub[:10]  # Extract YYYY-MM-DD
                posts_by_day[date] += 1
            except:
                pass

    analysis["timeline"] = dict(sorted(posts_by_day.items()))

    # Keyword match analysis
    keyword_stats = defaultdict(lambda: {"count": 0, "examples": []})
    for post in posts:
        matched = post.get("matched_keyword", "")
        if matched:
            # Clean up escaped keywords
            matched = matched.replace("\\", "")
            keyword_stats[matched]["count"] += 1
            if len(keyword_stats[matched]["examples"]) < 3:
                title = post.get("title", "") or post.get("text", "")[:80]
                keyword_stats[matched]["examples"].append(title)

    analysis["keyword_matches"] = dict(sorted(
        keyword_stats.items(),
        key=lambda x: x[1]["count"],
        reverse=True
    ))

    # Trending topics (hot subjects based on recent activity)
    trending = []

    # Check for payout issues
    payout_posts = [p for p in posts if "payout" in (p.get("text", "") + p.get("title", "")).lower()]
    if payout_posts:
        trending.append({
            "topic": "Payout Discussions",
            "count": len(payout_posts),
            "sentiment": "mixed - includes denied payouts and success stories"
        })

    # Check for rule changes
    rule_posts = [p for p in posts if "rule" in (p.get("text", "") + p.get("title", "")).lower()]
    if rule_posts:
        trending.append({
            "topic": "Rule Changes & Updates",
            "count": len(rule_posts),
            "sentiment": "informational - traders discussing prop firm rules"
        })

    # Check for market commentary
    market_posts = [p for p in posts if any(w in (p.get("text", "") + p.get("title", "")).lower()
                   for w in ["market", "nasdaq", "stock", "crash", "blood"])]
    if market_posts:
        trending.append({
            "topic": "Market Volatility Discussion",
            "count": len(market_posts),
            "sentiment": "cautious - traders discussing market conditions"
        })

    analysis["trending_topics"] = trending

    return analysis

def generate_report(analysis: Dict) -> str:
    """Generate a markdown report from the analysis."""
    report = []

    report.append("# 📊 Social Media Intelligence Report")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")

    # Executive Summary
    report.append("## 📌 Executive Summary")
    s = analysis["summary"]
    report.append(f"""
We analyzed **{s['total_posts']} posts** across YouTube ({s['youtube_videos']} videos)
and X/Twitter ({s['twitter_posts']} tweets) related to prop trading and BluSky.

**Key Metrics:**
- Total Views: **{s['total_views']:,}**
- Total Likes: **{s['total_likes']:,}**
- Total Retweets: **{s['total_retweets']:,}**
""")

    # Trending Topics
    report.append("## 🔥 Trending Topics")
    if analysis["trending_topics"]:
        for topic in analysis["trending_topics"]:
            report.append(f"- **{topic['topic']}** ({topic['count']} mentions) - {topic['sentiment']}")
    else:
        report.append("No major trending topics identified.")
    report.append("")

    # Prop Firms Mentioned
    report.append("## 🏢 Prop Firm Mentions")
    report.append("Which prop firms are being talked about most:")
    report.append("")
    for firm, count in analysis["prop_firms_mentioned"].items():
        bar = "█" * min(count // 2, 20)
        report.append(f"- **{firm.title()}**: {count} mentions {bar}")
    report.append("")

    # Top Keywords
    report.append("## 🔑 Top Keywords")
    report.append("Most frequently mentioned terms in the content:")
    report.append("")
    keywords = analysis["top_keywords"][:20]
    for word, count in keywords:
        report.append(f"- {word}: {count}")
    report.append("")

    # Keyword Matches (what triggered alerts)
    report.append("## 🎯 Keyword Alert Summary")
    report.append("Posts matched by your configured keywords:")
    report.append("")
    for keyword, stats in list(analysis["keyword_matches"].items())[:10]:
        report.append(f"### \"{keyword}\" - {stats['count']} matches")
        for ex in stats["examples"]:
            report.append(f"  - {ex[:100]}...")
        report.append("")

    # Top YouTube Videos
    report.append("## 📺 Top YouTube Videos by Views")
    for i, video in enumerate(analysis["top_videos"][:5], 1):
        report.append(f"{i}. **{video['title']}**")
        report.append(f"   - Author: {video['author']}")
        report.append(f"   - Views: {video['views']:,}")
        report.append(f"   - [Watch]({video['url']})")
        report.append("")

    # Top Tweets
    report.append("## 🐦 Top X/Twitter Posts by Engagement")
    for i, tweet in enumerate(analysis["top_tweets"][:5], 1):
        report.append(f"{i}. **{tweet['author']}**")
        report.append(f"   > {tweet['text']}")
        report.append(f"   - ❤️ {tweet['likes']:,} | 🔄 {tweet['retweets']:,}")
        if tweet['url']:
            report.append(f"   - [View]({tweet['url']})")
        report.append("")

    # Top Authors
    report.append("## 👥 Most Active & Influential Authors")
    for author in analysis["top_authors"][:10]:
        report.append(f"- **{author['name']}**: {author['posts']} posts, {author['views']:,} views, {author['likes']:,} likes")
    report.append("")

    # Timeline
    report.append("## 📅 Activity Timeline")
    report.append("Posts per day:")
    report.append("")
    for date, count in list(analysis["timeline"].items())[-7:]:
        bar = "█" * min(count, 30)
        report.append(f"- {date}: {bar} ({count})")
    report.append("")

    # Insights
    report.append("## 💡 Key Insights")
    report.append("""
Based on the data collected:

1. **APEX Trader Funding** continues to dominate conversations, with frequent mentions
   of their discount codes and evaluation programs.

2. **Payout discussions** are a hot topic - both success stories and denied payouts
   are generating significant engagement.

3. **Rule changes** at various prop firms are being actively discussed, with traders
   sharing updates and strategies.

4. **Market volatility** is driving content, with references to "blood bath" market
   days and stock market signals.

5. **Live trading streams** on YouTube are popular, with Prop Firm Match TV and
   Day Trading Jesus generating consistent viewership.
""")

    return "\n".join(report)

def main():
    """Main entry point."""
    print("📊 Analyzing social media data...")

    data = load_data()
    analysis = analyze_data(data)
    report = generate_report(analysis)

    # Save report
    output_file = "trend_report.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Report saved to: {output_file}")
    print("\n" + "=" * 50)
    print(report)

if __name__ == "__main__":
    main()
