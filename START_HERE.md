# 🎵 START HERE: ARIA Music Charts Analysis Toolkit

**For analyzing Casey Briggs' ARIA Charts Dataset**

This toolkit is correctly built for **ARIA music charts** analysis. Here's everything you need to get started.

---

## 📦 What You Have

I've created a comprehensive Python toolkit for exploring Australian music charts:

### Files (29 KB total)
- **[aria_charts_explorer.py](computer:///mnt/user-data/outputs/aria_charts_explorer.py)** (18KB) - Full analysis class
- **[quick_start_music.py](computer:///mnt/user-data/outputs/quick_start_music.py)** (7.2KB) - Interactive script
- **[README.md](computer:///mnt/user-data/outputs/README.md)** (3.2KB) - Complete documentation
- **[sample_singles_chart.csv](computer:///mnt/user-data/outputs/sample_singles_chart.csv)** - Test dataset

---

## 🎯 The Dataset

**Casey Briggs' ARIA Charts Repository:**
- **URL:** https://github.com/caseybriggs/ARIA-charts
- **Data:** Complete ARIA singles & albums charts from 1988 to present
- **Update frequency:** Weekly (every Tuesday)
- **Size:** 100,000+ chart entries

### What's in the data:
- Chart positions for every week since 1988
- Artist names and song/album titles
- Australian vs international artist flags
- Artist locations from MusicBrainz
- Three separate datasets: singles, albums, and new singles (2022+)

---

## 🚀 Quick Start (3 Options)

### Option 1: Interactive Quick Start ⭐ RECOMMENDED
```bash
python quick_start_music.py
```
This will:
1. Help you load data (from GitHub or local file)
2. Show quick overview
3. Display top artists and songs
4. Analyze Australian content trends
5. Compare decades
6. Let you search specific artists
7. Export results

### Option 2: Test with Sample Data (Right Now!)
```python
from aria_charts_explorer import ARIAChartsExplorer

# Use included sample data
explorer = ARIAChartsExplorer('sample_singles_chart.csv')
explorer.load_data()
explorer.quick_overview()
explorer.top_artists(n=10)
```

### Option 3: Load Real Data from GitHub
```python
from aria_charts_explorer import ARIAChartsExplorer

# Load directly from Casey's GitHub
explorer = ARIAChartsExplorer('github')
explorer.load_data('singles')  # or 'albums' or 'new_singles'
explorer.quick_overview()
```

**Note:** If GitHub loading doesn't work due to network restrictions, download the CSV files manually from the repository and use Option 2 with your local path.

---

## 📊 What You Can Analyze

### 1. Top Artists Through History
```python
# Overall top artists
explorer.top_artists(n=20)

# Australian artists only
explorer.top_artists(n=20, australian_only=True)

# Specific time period
explorer.top_artists(n=20, time_period=(2010, 2020))
```

**Shows:** Appearances, best position, average position, #1 hits, career span

### 2. Top Songs & Albums
```python
# By total weeks on chart
explorer.top_songs(n=20, by='weeks')

# By peak position
explorer.top_songs(n=20, by='peak')

# By weeks in top 10
explorer.top_songs(n=20, by='top10')

# By weeks at #1
explorer.top_songs(n=20, by='number1')
```

### 3. Individual Artist Deep Dive
```python
# Complete chart history with visualization
explorer.artist_history('Kylie Minogue', plot=True)
explorer.artist_history('The Kid LAROI', plot=True)
explorer.artist_history('Tones and I', plot=True)
```

**Shows:** Career stats, #1 hits, top 10 hits, chart position graphs, yearly trends

### 4. Australian vs International Trends
```python
explorer.australian_content_analysis()
```

**Shows:** Percentage of Australian content over time, trends, peak years

### 5. Decades Comparison
```python
explorer.decades_comparison()
```

**Compares:** 1980s, 1990s, 2000s, 2010s, 2020s chart statistics

---

## 🎵 Interesting Questions to Explore

### Who had the most #1 hits?
```python
number_ones = explorer.data[explorer.data['rank'] == 1]
top_artists = number_ones.groupby('artist')['title'].nunique()
print(top_artists.sort_values(ascending=False).head(10))
```

### What song stayed on the charts longest?
```python
songs = explorer.data.groupby(['artist', 'title']).size()
longest = songs.sort_values(ascending=False).head(10)
print(longest)
```

### Which year had most Australian content?
```python
yearly = explorer.data.groupby(explorer.data['chart_date'].dt.year)['aus_flag']
aus_pct = yearly.apply(lambda x: (x == True).sum() / len(x) * 100)
print(f"Peak year: {aus_pct.idxmax()} with {aus_pct.max():.1f}%")
```

### Find one-hit wonders
```python
songs_per_artist = explorer.data.groupby('artist')['title'].nunique()
one_hit_wonders = songs_per_artist[songs_per_artist == 1]
print(f"One-hit wonders: {len(one_hit_wonders)}")
```

### Compare two artists head-to-head
```python
artist1 = explorer.artist_history('AC/DC', plot=False)
artist2 = explorer.artist_history('INXS', plot=False)
print(f"AC/DC: {len(artist1)} weeks, {(artist1['rank']==1).sum()} #1s")
print(f"INXS: {len(artist2)} weeks, {(artist2['rank']==1).sum()} #1s")
```

---

## 📥 Getting the Real Data

### Method 1: Download from GitHub
1. Visit: https://github.com/caseybriggs/ARIA-charts
2. Download these files:
   - `singles_chart.csv` (recommended, most comprehensive)
   - `albums_chart.csv` (albums data)
   - `new_singles_chart.csv` (newer chart, 2022+)
3. Save to your computer
4. Use in Python:
   ```python
   explorer = ARIAChartsExplorer('path/to/singles_chart.csv')
   explorer.load_data()
   ```

### Method 2: Clone the Repository
```bash
git clone https://github.com/caseybriggs/ARIA-charts.git
cd ARIA-charts
# Then use the CSV files
```

---

## 🎨 Visualizations Included

The toolkit creates publication-quality plots:
- **Artist History:** Chart positions over time for all songs
- **Australian Content Trend:** Line graph showing % Australian over years
- **Content Split:** Pie chart of Australian vs international
- **Yearly Appearances:** Bar chart of activity by year

All plots are automatically styled and ready to save or share!

---

## 💡 Pro Tips

### 1. Filter by Era
```python
# Only 2020s data
modern = explorer.data[explorer.data['chart_date'].dt.year >= 2020]

# Only 1990s
nineties = explorer.data[
    (explorer.data['chart_date'].dt.year >= 1990) &
    (explorer.data['chart_date'].dt.year < 2000)
]
```

### 2. Export Your Findings
```python
# Export top artists to CSV
top_artists = explorer.top_artists(n=100)
top_artists.to_csv('top_100_artists.csv')

# Export specific artist's history
kylie = explorer.artist_history('Kylie', plot=False)
kylie.to_csv('kylie_complete_history.csv')
```

### 3. Custom Visualizations
```python
import matplotlib.pyplot as plt

# Create your own charts
top_aus = explorer.data[explorer.data['aus_flag'] == True]
aus_artists = top_aus['artist'].value_counts().head(10)

plt.figure(figsize=(12, 6))
aus_artists.plot(kind='barh')
plt.title('Top 10 Australian Artists by Chart Appearances')
plt.xlabel('Weeks on Chart')
plt.tight_layout()
plt.savefig('top_australian_artists.png', dpi=300)
```

---

## 🔧 Troubleshooting

### "Can't load from GitHub"
**Solution:** Download CSV files manually and load locally
```python
explorer = ARIAChartsExplorer('/path/to/downloaded/singles_chart.csv')
explorer.load_data()
```

### "ModuleNotFoundError"
**Solution:** All required packages are already installed in your environment!
If needed: `pip install pandas numpy matplotlib seaborn`

### "File not found"
**Solution:** Use absolute paths
```python
import os
print(os.getcwd())  # Check where you are
explorer = ARIAChartsExplorer('/absolute/path/to/file.csv')
```

### "Large dataset slow"
**Solution:** Sample the data for faster exploration
```python
explorer.load_data('singles')
explorer.data = explorer.data.sample(frac=0.1)  # Use 10%
```

---

## 🎓 Learning Path

### Week 1: Basics
1. Load sample data and explore
2. Try `quick_overview()` and `top_artists()`
3. Analyze a few favorite artists
4. Create your first visualizations

### Week 2: Intermediate
1. Load full singles chart dataset
2. Compare different decades
3. Analyze Australian content trends
4. Export findings to CSV

### Week 3: Advanced
1. Custom filtering and analysis
2. Create publication-quality visualizations
3. Statistical analysis (correlations, trends)
4. Build your own analysis functions

---

## 📚 Resources

- **ARIA Official:** https://www.aria.com.au/
- **Casey Briggs:** https://www.caseybriggs.com/
- **Repository:** https://github.com/caseybriggs/ARIA-charts
- **ABC News Music Coverage:** Search for Casey's analysis articles
- **Pandas Docs:** https://pandas.pydata.org/docs/
- **Matplotlib Gallery:** https://matplotlib.org/stable/gallery/

---

## 🎉 Ready to Start?

### Immediate Actions:
1. ✅ Test with sample data right now:
   ```python
   from aria_charts_explorer import ARIAChartsExplorer
   explorer = ARIAChartsExplorer('sample_singles_chart.csv')
   explorer.load_data()
   explorer.quick_overview()
   ```

2. ✅ Download real data from GitHub repository

3. ✅ Run `python quick_start_music.py` for guided analysis

### Example Session:
```python
from aria_charts_explorer import ARIAChartsExplorer

# Load data
explorer = ARIAChartsExplorer('singles_chart.csv')
explorer.load_data()

# Quick exploration
explorer.quick_overview()
explorer.top_artists(n=20)
explorer.top_songs(n=20, by='weeks')

# Deep dives
explorer.artist_history('The Kid LAROI', plot=True)
explorer.australian_content_analysis()
explorer.decades_comparison()

# Export
explorer.export_insights('my_analysis.txt')
```

---

## 🤝 Credit the Data

When sharing your analyses, please credit:
- **Data compilation:** Casey Briggs (ABC News)
- **Sources:** ARIA, australian-charts.com, MusicBrainz
- **Repository:** https://github.com/caseybriggs/ARIA-charts

---

## ✅ Pre-Flight Checklist

Before starting your analysis:
- [ ] Downloaded toolkit files
- [ ] Tested with `sample_singles_chart.csv`
- [ ] Read README.md for detailed docs
- [ ] Downloaded real ARIA chart data OR have network access
- [ ] Python 3.8+ with pandas, matplotlib, numpy, seaborn
- [ ] Ready to explore Australian music history!

---

**🎵 You're all set! Start with:**
```bash
python quick_start_music.py
```

**Or dive right in:**
```python
from aria_charts_explorer import ARIAChartsExplorer
explorer = ARIAChartsExplorer('sample_singles_chart.csv')
explorer.load_data()
explorer.quick_overview()
```

Enjoy exploring 35+ years of Australian music charts! 🇦🇺🎶

---

*Created: 2 November 2025*  
*Dataset: Casey Briggs' ARIA Charts (1988-present)*  
*Tools tested and working!*
