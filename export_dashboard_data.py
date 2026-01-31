#!/usr/bin/env python3
"""
Export Dashboard Data for GitHub Pages
Exports all interesting insights and statistics to JSON for web dashboard
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
from collections import Counter

def load_all_data():
    """Load all analysis results"""
    print("Loading data...")
    
    data = {
        'posts': pd.read_csv('data/posts_latest.csv'),
        'author_stats': pd.read_csv('data/author_stats.csv'),
    }
    
    # Load JSON files if they exist
    try:
        with open('data/cross_posters.json', 'r') as f:
            data['cross_posters'] = json.load(f)
    except:
        data['cross_posters'] = {}
    
    try:
        with open('data/bridge_authors.json', 'r') as f:
            data['bridge_authors'] = json.load(f)
    except:
        data['bridge_authors'] = {}
    
    try:
        with open('data/network_stats.json', 'r') as f:
            data['network_stats'] = json.load(f)
    except:
        data['network_stats'] = {}
    
    return data

def export_overview_stats(data):
    """Export high-level overview statistics"""
    df = data['posts']
    
    overview = {
        'total_posts': int(len(df)),
        'total_authors': int(df['author_name'].nunique()),
        'total_submolts': int(df['submolt_display_name'].nunique()),
        'total_upvotes': int(df['upvotes'].sum()),
        'total_comments': int(df['comment_count'].sum()),
        'avg_upvotes_per_post': float(df['upvotes'].mean()),
        'median_upvotes': float(df['upvotes'].median()),
        'avg_comments_per_post': float(df['comment_count'].mean()),
        'date_range': {
            'start': str(df['created_at'].min()),
            'end': str(df['created_at'].max())
        }
    }
    
    return overview

def export_top_posts(data, n=20):
    """Export top posts by upvotes"""
    df = data['posts']
    
    # Replace NaN values before export
    df = df.fillna({'title': '', 'author_name': 'Unknown', 'submolt_display_name': 'Unknown'})
    
    top_posts = df.nlargest(n, 'upvotes')[
        ['title', 'upvotes', 'comment_count', 'author_name', 'submolt_display_name', 'created_at']
    ].to_dict('records')
    
    # Convert to serializable format
    for post in top_posts:
        post['upvotes'] = int(post['upvotes']) if pd.notna(post['upvotes']) else 0
        post['comment_count'] = int(post['comment_count']) if pd.notna(post['comment_count']) else 0
        post['created_at'] = str(post['created_at']) if pd.notna(post['created_at']) else ''
        post['title'] = str(post['title']) if post['title'] else 'Untitled'
    
    return top_posts

def export_top_authors(data, n=20):
    """Export top authors by various metrics"""
    author_stats = data['author_stats'].fillna(0)
    
    top_authors = {
        'by_engagement': [],
        'by_posts': [],
        'by_consistency': []
    }
    
    # By engagement rate
    active = author_stats[author_stats['total_posts'] >= 5]
    for _, row in active.nlargest(n, 'engagement_rate').iterrows():
        top_authors['by_engagement'].append({
            'name': str(row.name),
            'engagement_rate': float(row['engagement_rate']) if pd.notna(row['engagement_rate']) else 0.0,
            'total_posts': int(row['total_posts']) if pd.notna(row['total_posts']) else 0,
            'avg_upvotes': float(row['avg_upvotes']) if pd.notna(row['avg_upvotes']) else 0.0,
            'success_rate': float(row['success_rate']) if pd.notna(row['success_rate']) else 0.0
        })
    
    # By post count
    for _, row in author_stats.nlargest(n, 'total_posts').iterrows():
        top_authors['by_posts'].append({
            'name': str(row.name),
            'total_posts': int(row['total_posts']) if pd.notna(row['total_posts']) else 0,
            'avg_upvotes': float(row['avg_upvotes']) if pd.notna(row['avg_upvotes']) else 0.0,
            'posts_per_day': float(row['posts_per_day']) if pd.notna(row['posts_per_day']) else 0.0
        })
    
    # By consistency
    for _, row in active.nlargest(n, 'consistency_score').iterrows():
        top_authors['by_consistency'].append({
            'name': str(row.name),
            'consistency_score': float(row['consistency_score']) if pd.notna(row['consistency_score']) else 0.0,
            'total_posts': int(row['total_posts']) if pd.notna(row['total_posts']) else 0,
            'avg_upvotes': float(row['avg_upvotes']) if pd.notna(row['avg_upvotes']) else 0.0,
            'upvotes_std': float(row['upvotes_std']) if pd.notna(row['upvotes_std']) else 0.0
        })
    
    return top_authors

def export_submolt_stats(data, n=30):
    """Export submolt statistics"""
    df = data['posts'].fillna({'submolt_display_name': 'Unknown', 'upvotes': 0, 'comment_count': 0})
    
    submolt_stats = df.groupby('submolt_display_name').agg({
        'id': 'count',
        'upvotes': ['sum', 'mean', 'median'],
        'comment_count': ['sum', 'mean'],
        'author_name': lambda x: x.nunique()
    }).round(2).fillna(0)
    
    submolt_stats.columns = ['_'.join(col).strip() for col in submolt_stats.columns.values]
    submolt_stats = submolt_stats.rename(columns={
        'id_count': 'post_count',
        'upvotes_sum': 'total_upvotes',
        'upvotes_mean': 'avg_upvotes',
        'upvotes_median': 'median_upvotes',
        'comment_count_sum': 'total_comments',
        'comment_count_mean': 'avg_comments',
        'author_name_<lambda>': 'unique_authors'
    })
    
    # Top submolts
    top_submolts = []
    for submolt, row in submolt_stats.nlargest(n, 'post_count').iterrows():
        top_submolts.append({
            'name': submolt,
            'post_count': int(row['post_count']),
            'total_upvotes': int(row['total_upvotes']),
            'avg_upvotes': float(row['avg_upvotes']),
            'median_upvotes': float(row['median_upvotes']),
            'total_comments': int(row['total_comments']),
            'avg_comments': float(row['avg_comments']),
            'unique_authors': int(row['unique_authors'])
        })
    
    return top_submolts

def export_time_series(data):
    """Export time series data for charts"""
    df = data['posts'].copy().fillna({'upvotes': 0})
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at'].dt.date
    df['hour'] = df['created_at'].dt.hour
    df['day_of_week'] = df['created_at'].dt.day_name()
    
    # Daily posts
    daily = df.groupby('date').agg({
        'id': 'count',
        'upvotes': 'sum'
    }).reset_index().fillna(0)
    daily['date'] = daily['date'].astype(str)
    
    # Hourly patterns
    hourly = df.groupby('hour').agg({
        'id': 'count',
        'upvotes': 'mean'
    }).reset_index().fillna(0)
    
    # Day of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_pattern = df.groupby('day_of_week').agg({
        'id': 'count',
        'upvotes': 'mean'
    }).reindex(day_order).reset_index().fillna(0)
    
    return {
        'daily_posts': daily.to_dict('records'),
        'hourly_pattern': hourly.to_dict('records'),
        'day_of_week_pattern': daily_pattern.to_dict('records')
    }

def export_network_data(data):
    """Export network analysis data"""
    network = {
        'stats': data.get('network_stats', {}),
        'top_cross_posters': [],
        'top_bridge_authors': []
    }
    
    # Top cross-posters
    cross_posters = data.get('cross_posters', {})
    cross_poster_counts = [(author, len(submolts)) for author, submolts in cross_posters.items()]
    cross_poster_counts.sort(key=lambda x: x[1], reverse=True)
    
    for author, count in cross_poster_counts[:20]:
        network['top_cross_posters'].append({
            'author': author,
            'submolt_count': count,
            'submolts': cross_posters[author][:5]  # First 5 submolts
        })
    
    # Top bridge authors
    bridge_authors = data.get('bridge_authors', {})
    bridge_sorted = sorted(bridge_authors.items(), key=lambda x: x[1], reverse=True)
    
    for author, score in bridge_sorted[:20]:
        network['top_bridge_authors'].append({
            'author': author,
            'bridge_score': float(score)
        })
    
    return network

def export_insights(data):
    """Export key insights and findings"""
    df = data['posts'].fillna({'upvotes': 0, 'title': '', 'url': ''})
    author_stats = data['author_stats'].fillna(0)
    
    insights = {
        'engagement': {
            'avg_upvotes': float(df['upvotes'].mean()) if not df['upvotes'].isna().all() else 0.0,
            'median_upvotes': float(df['upvotes'].median()) if not df['upvotes'].isna().all() else 0.0,
            'top_1_percent_threshold': float(df['upvotes'].quantile(0.99)) if not df['upvotes'].isna().all() else 0.0,
            'viral_threshold': float(df['upvotes'].quantile(0.90)) if not df['upvotes'].isna().all() else 0.0
        },
        'authors': {
            'total': int(df['author_name'].nunique()),
            'active_5plus': int(len(author_stats[author_stats['total_posts'] >= 5])),
            'avg_posts_per_author': float(author_stats['total_posts'].mean()) if not author_stats['total_posts'].isna().all() else 0.0,
            'cross_posting_rate': float(len(data.get('cross_posters', {})) / len(author_stats) * 100) if len(author_stats) > 0 else 0.0
        },
        'content': {
            'total_posts': int(len(df)),
            'total_submolts': int(df['submolt_display_name'].nunique()),
            'avg_title_length': float(df['title'].str.len().mean()) if not df['title'].isna().all() else 0.0,
            'posts_with_urls': int(df['url'].notna().sum())
        },
        'timing': {
            'best_hour': int(df.groupby(pd.to_datetime(df['created_at']).dt.hour)['upvotes'].mean().fillna(0).idxmax()),
            'best_day': str(df.groupby(pd.to_datetime(df['created_at']).dt.day_name())['upvotes'].mean().fillna(0).idxmax())
        }
    }
    
    return insights

def main():
    print("\n" + "="*60)
    print("EXPORTING DASHBOARD DATA")
    print("="*60)
    
    # Load all data
    data = load_all_data()
    
    # Export all sections
    dashboard_data = {
        'generated_at': datetime.now().isoformat(),
        'overview': export_overview_stats(data),
        'top_posts': export_top_posts(data),
        'top_authors': export_top_authors(data),
        'top_submolts': export_submolt_stats(data),
        'time_series': export_time_series(data),
        'network': export_network_data(data),
        'insights': export_insights(data)
    }
    
    # Save to JSON (replace NaN with null)
    output_path = 'dashboard_data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False, allow_nan=False)
    
    print(f"\n✅ Dashboard data exported to {output_path}")
    print(f"   File size: {len(json.dumps(dashboard_data)) / 1024:.1f} KB")
    print(f"\n📊 Data Summary:")
    print(f"   Posts: {dashboard_data['overview']['total_posts']:,}")
    print(f"   Authors: {dashboard_data['overview']['total_authors']:,}")
    print(f"   Submolts: {dashboard_data['overview']['total_submolts']:,}")
    print(f"   Top Posts: {len(dashboard_data['top_posts'])}")
    print(f"   Top Authors: {len(dashboard_data['top_authors']['by_engagement'])}")
    print(f"   Top Submolts: {len(dashboard_data['top_submolts'])}")

if __name__ == "__main__":
    main()
