# ARIA Music Charts Analysis Toolkit

Python tools for exploring and analysing Casey Briggs' comprehensive ARIA (Australian Recording Industry Association) music charts dataset.

## 📀 About the Dataset

**Repository:** https://github.com/caseybriggs/ARIA-charts

Casey Briggs (ABC News data analyst) has compiled complete ARIA chart data from **1988 to present**, updated weekly every Tuesday.

### Available Charts:
1. **singles_chart.csv** - Singles chart from 1988 onwards
2. **albums_chart.csv** - Albums chart from 1988 onwards  
3. **new_singles_chart.csv** - New singles chart (started 2022)

### Data Columns:
- **chart_date** - First day of each chart week (Monday)
- **rank** - Chart position (1-50 or 1-100)
- **artist** - Artist name as shown on ARIA charts
- **title** - Song/album title
- **musicbrainz_name** - Artist ID from MusicBrainz
- **aus_flag** - TRUE if Australian artist, FALSE otherwise
- **location** - Artist's location/country

## 🚀 Quick Start

### Interactive Quick Start (Easiest!)
```bash
python quick_start_music.py
```

### Load from GitHub (Recommended)
```python
from aria_charts_explorer import ARIAChartsExplorer

explorer = ARIAChartsExplorer('github')
explorer.load_data('singles')
explorer.quick_overview()
```

### Load from Local Files
```python
explorer = ARIAChartsExplorer('path/to/singles_chart.csv')
explorer.load_data()
```

## 📊 Key Features

### 1. Top Artists
```python
explorer.top_artists(n=20)  # Overall
explorer.top_artists(n=20, australian_only=True)  # Australian only
explorer.top_artists(n=20, time_period=(2010, 2020))  # Specific era
```

### 2. Top Songs
```python
explorer.top_songs(n=20, by='weeks')  # By total weeks
explorer.top_songs(n=20, by='peak')  # By peak position
explorer.top_songs(n=20, by='number1')  # By weeks at #1
```

### 3. Artist Analysis
```python
explorer.artist_history('Kylie Minogue', plot=True)
```
Shows complete chart history with visualizations!

### 4. Australian Content Trends
```python
explorer.australian_content_analysis()
```
Tracks Australian vs international music over time

### 5. Decades Comparison
```python
explorer.decades_comparison()
```
Compare chart trends across decades

## 🎯 Example Analyses

### Longest-Charting Songs
```python
explorer.load_data('singles')
long_runners = explorer.top_songs(n=30, by='weeks')
```

### Find One-Hit Wonders
```python
songs_per_artist = explorer.data.groupby('artist')['title'].nunique()
one_hit = songs_per_artist[songs_per_artist == 1]
print(f"One-hit wonders: {len(one_hit)}")
```

### Most #1 Hits
```python
number_ones = explorer.data[explorer.data['rank'] == 1]
top = number_ones.groupby('artist')['title'].nunique()
print(top.sort_values(ascending=False).head(10))
```

### Australian Music Growth
```python
explorer.australian_content_analysis()
# See trends from 1988 to now!
```

## 📋 Requirements

All packages already installed:
- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0

## 🤝 Attribution

When using this data, please credit:
- **Data:** Casey Briggs (ABC News)
- **Sources:** ARIA, australian-charts.com, MusicBrainz
- **Repository:** https://github.com/caseybriggs/ARIA-charts

---

**Start exploring:** `python quick_start_music.py` 🎵
