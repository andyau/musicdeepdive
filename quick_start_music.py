#!/usr/bin/env python3
"""
Quick Start: ARIA Music Charts Analysis
Load and analyze Casey Briggs' ARIA charts dataset
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from aria_charts_explorer import ARIAChartsExplorer

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)
sns.set_style("whitegrid")

print("="*70)
print("ARIA MUSIC CHARTS - QUICK START ANALYSIS")
print("="*70)
print("\nCasey Briggs' ARIA Charts Dataset")
print("Repository: https://github.com/caseybriggs/ARIA-charts\n")

# ============================================================================
# STEP 1: Choose Data Source
# ============================================================================
print("\n" + "="*70)
print("STEP 1: Choose Your Data Source")
print("="*70)

print("\nOptions:")
print("1. Load directly from GitHub (recommended)")
print("2. Load from local file")
print("3. Demo with sample queries\n")

choice = input("Enter your choice (1-3): ").strip()

if choice == "1":
    # Load from GitHub
    print("\nLoading from GitHub...")
    explorer = ARIAChartsExplorer('github')
    
    print("\nAvailable charts:")
    print("1. Singles Chart (1988 onwards)")
    print("2. Albums Chart (1988 onwards)")  
    print("3. New Singles Chart (2022 onwards)")
    
    chart_choice = input("\nSelect chart (1-3): ").strip()
    chart_types = {'1': 'singles', '2': 'albums', '3': 'new_singles'}
    chart_type = chart_types.get(chart_choice, 'singles')
    
    explorer.load_data(chart_type)

elif choice == "2":
    # Load from local file
    filepath = input("\nEnter path to CSV file: ").strip()
    explorer = ARIAChartsExplorer(filepath)
    explorer.load_data()

else:
    # Demo mode
    print("\nRunning in demo mode with examples...")
    print("To use with real data, run this script again and choose option 1 or 2")
    print("\nHere's how the analysis works:\n")
    print("""
# Create explorer instance
explorer = ARIAChartsExplorer('github')
explorer.load_data('singles')

# Get quick overview
explorer.quick_overview()

# Find top artists
explorer.top_artists(n=20)

# Find top songs by various metrics
explorer.top_songs(n=20, by='weeks')  # Most weeks on chart
explorer.top_songs(n=20, by='number1')  # Most weeks at #1

# Analyze specific artist
explorer.artist_history('Kylie Minogue', plot=True)

# Australian content trends
explorer.australian_content_analysis()

# Compare decades
explorer.decades_comparison()
""")
    exit()

if explorer.data is None:
    print("\n❌ Failed to load data. Please check your connection or file path.")
    exit()

# ============================================================================
# STEP 2: Quick Overview
# ============================================================================
print("\n" + "="*70)
print("STEP 2: Quick Overview")
print("="*70)

explorer.quick_overview()

# ============================================================================
# STEP 3: Top Artists Analysis
# ============================================================================
print("\n" + "="*70)
print("STEP 3: Top Artists")
print("="*70)

print("\nAnalyzing top artists...")
top_artists = explorer.top_artists(n=20)

print("\n🇦🇺 Top Australian Artists:")
aus_artists = explorer.top_artists(n=10, australian_only=True)

# ============================================================================
# STEP 4: Top Songs/Albums Analysis
# ============================================================================
print("\n" + "="*70)
print("STEP 4: Top Songs/Albums")
print("="*70)

print("\n📊 By Total Weeks on Chart:")
top_by_weeks = explorer.top_songs(n=15, by='weeks')

print("\n🏆 By Peak Position:")
top_by_peak = explorer.top_songs(n=15, by='peak')

if explorer.chart_type == 'singles':
    print("\n👑 Most Weeks at #1:")
    top_number_ones = explorer.top_songs(n=15, by='number1')

# ============================================================================
# STEP 5: Australian Content Analysis
# ============================================================================
if 'aus_flag' in explorer.data.columns:
    print("\n" + "="*70)
    print("STEP 5: Australian Content Analysis")
    print("="*70)
    
    explorer.australian_content_analysis()

# ============================================================================
# STEP 6: Decades Comparison
# ============================================================================
print("\n" + "="*70)
print("STEP 6: Decades Comparison")
print("="*70)

explorer.decades_comparison()

# ============================================================================
# STEP 7: Interactive Artist Search
# ============================================================================
print("\n" + "="*70)
print("STEP 7: Artist Deep Dive (Optional)")
print("="*70)

search_more = input("\nWould you like to analyze a specific artist? (y/n): ").strip().lower()

while search_more == 'y':
    artist_name = input("\nEnter artist name (or part of it): ").strip()
    
    if artist_name:
        print(f"\n🔍 Searching for '{artist_name}'...")
        artist_data = explorer.artist_history(artist_name, plot=True)
        
        if artist_data is not None:
            # Show some interesting songs
            print("\n📀 Most Successful Songs:")
            song_stats = artist_data.groupby('title').agg({
                'chart_date': 'count',
                'rank': 'min'
            }).rename(columns={'chart_date': 'Weeks', 'rank': 'Peak'})
            song_stats = song_stats.sort_values('Weeks', ascending=False).head(10)
            print(song_stats)
    
    search_more = input("\nAnalyze another artist? (y/n): ").strip().lower()

# ============================================================================
# STEP 8: Export Results
# ============================================================================
print("\n" + "="*70)
print("STEP 8: Export Results")
print("="*70)

export = input("\nExport analysis summary to file? (y/n): ").strip().lower()

if export == 'y':
    filename = input("Enter filename (default: aria_analysis.txt): ").strip()
    if not filename:
        filename = 'aria_analysis.txt'
    
    explorer.export_insights(filename)
    print(f"\n✓ Analysis exported to {filename}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)

print(f"""
📊 Summary:
  • Chart type: {explorer.chart_type}
  • Total entries analyzed: {len(explorer.data):,}
  • Date range: {explorer.data['chart_date'].min().date()} to {explorer.data['chart_date'].max().date()}
  • Unique artists: {explorer.data['artist'].nunique():,}

🎯 What's Next:
  • Use aria_charts_explorer.py for custom analysis
  • Explore time periods: explorer.top_artists(time_period=(2010, 2020))
  • Filter by Australian content: australian_only=True
  • Analyze trends and patterns
  
📚 More Options:
  from aria_charts_explorer import ARIAChartsExplorer
  
  # Create custom analyses
  # Compare different eras
  # Track artist trajectories
  # Identify chart patterns

Happy analyzing! 🎵
""")

print("="*70)
