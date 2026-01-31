# Moltbook Data Analysis Dashboard

## 🎯 Overview

An interactive web dashboard displaying comprehensive analysis of 30,000+ posts from Moltbook social platform. Built with vanilla JavaScript and Chart.js, optimized for GitHub Pages.

## 🚀 Quick Start

### View Live Dashboard

1. **GitHub Pages Deployment:**
   ```bash
   # Push to GitHub
   git add index.html dashboard_data.json
   git commit -m "Add interactive dashboard"
   git push origin main
   
   # Enable GitHub Pages in repository settings
   # Settings → Pages → Source: main branch → Save
   ```

2. **Local Preview:**
   ```bash
   # Simple HTTP server
   python -m http.server 8000
   # Or
   npx serve .
   
   # Open browser to http://localhost:8000
   ```

## 📊 Dashboard Features

### Overview Statistics
- Total posts, authors, submolts
- Total upvotes and comments
- Average engagement metrics

### Time Series Analysis
- **Daily Posts**: Trend of posts over time
- **Hourly Pattern**: Best times to post (UTC)
- **Day of Week**: Engagement by day

### Top Content
- **Top 20 Posts**: Highest upvoted posts
- **Top Authors**: By engagement, post count, consistency
- **Top 30 Submolts**: Most active communities

### Network Analysis
- Cross-posting patterns
- Bridge authors connecting communities
- Network statistics

### Key Insights
- Viral thresholds (top 1%, top 10%)
- Author activity patterns
- Optimal posting times

## 🛠️ Technical Details

### Files
- `index.html` - Main dashboard (single-page app)
- `dashboard_data.json` - All analysis data (22KB)
- `export_dashboard_data.py` - Data export script

### Technologies
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Charts**: Chart.js 4.4.0
- **Data**: JSON (no backend required)
- **Hosting**: GitHub Pages compatible

### Data Structure

```json
{
  "generated_at": "ISO timestamp",
  "overview": { /* aggregate stats */ },
  "top_posts": [ /* 20 posts */ ],
  "top_authors": {
    "by_engagement": [ /* 20 authors */ ],
    "by_posts": [ /* 20 authors */ ],
    "by_consistency": [ /* 20 authors */ ]
  },
  "top_submolts": [ /* 30 submolts */ ],
  "time_series": {
    "daily_posts": [ /* daily data */ ],
    "hourly_pattern": [ /* 24 hours */ ],
    "day_of_week_pattern": [ /* 7 days */ ]
  },
  "network": {
    "stats": { /* network metrics */ },
    "top_cross_posters": [ /* 20 authors */ ],
    "top_bridge_authors": [ /* 20 authors */ ]
  },
  "insights": { /* key findings */ }
}
```

## 🔄 Updating Data

To refresh the dashboard with new data:

```bash
# 1. Scrape latest posts
python main.py

# 2. Run analyses
python analyze_with_metal.py
python analyze_authors.py
python network_analysis.py

# 3. Export dashboard data
python export_dashboard_data.py

# 4. Commit and push
git add dashboard_data.json
git commit -m "Update dashboard data"
git push
```

## 🎨 Customization

### Colors
Edit CSS variables in `index.html`:
```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Accent colors */
.stat-value { color: #667eea; }
```

### Charts
Modify Chart.js options in JavaScript:
```javascript
new Chart(ctx, {
  type: 'line',
  data: { /* your data */ },
  options: {
    responsive: true,
    // Add custom options
  }
});
```

### Data Display
Adjust number of items shown:
```javascript
// In export_dashboard_data.py
export_top_posts(data, n=20)  // Change n
export_top_authors(data, n=20)
export_submolt_stats(data, n=30)
```

## 📱 Responsive Design

Dashboard is fully responsive:
- Desktop: Multi-column grid layout
- Tablet: Adaptive columns
- Mobile: Single column, optimized charts

## 🔒 Privacy & Security

- **No tracking**: No analytics or cookies
- **Static only**: No server-side code
- **Public data**: Only publicly available Moltbook data
- **No PII**: Author names are public usernames

## 📈 Performance

- **Load time**: < 1 second
- **Data size**: 22KB JSON
- **Charts**: Hardware accelerated
- **Mobile**: Optimized for 3G+

## 🐛 Troubleshooting

### Dashboard not loading
1. Check browser console for errors
2. Verify `dashboard_data.json` is in same directory
3. Ensure CORS is enabled (use HTTP server, not file://)

### Charts not rendering
1. Check Chart.js CDN is accessible
2. Verify data format in JSON
3. Check browser compatibility (modern browsers only)

### Data not updating
1. Re-run `export_dashboard_data.py`
2. Clear browser cache
3. Hard refresh (Ctrl+Shift+R / Cmd+Shift+R)

## 🤝 Contributing

To add new visualizations:

1. Add data to `export_dashboard_data.py`
2. Create chart/table in `index.html`
3. Update this README

## 📄 License

MIT License - See main project LICENSE file

## 🙏 Acknowledgments

- **Data Source**: Moltbook.com
- **Analysis**: Python, pandas, scikit-learn, networkx
- **Visualization**: Chart.js
- **Acceleration**: Apple Metal (MPS)

---

**Generated**: 2026-01-31  
**Posts Analyzed**: 29,877  
**Time Period**: All available data  
**Last Update**: Check dashboard for timestamp