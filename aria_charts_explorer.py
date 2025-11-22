#!/usr/bin/env python3
"""
ARIA Music Charts Explorer
Comprehensive analysis tool for Casey Briggs' ARIA charts dataset
Repository: https://github.com/caseybriggs/ARIA-charts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


class ARIAChartsExplorer:
    """
    A comprehensive class for exploring and analysing ARIA music charts data
    """
    
    def __init__(self, data_source):
        """
        Initialise the explorer with path to CSV file or directory
        
        Parameters:
        -----------
        data_source : str or Path
            Path to CSV file, directory, or GitHub raw URL
        """
        self.data_source = data_source
        self.data = None
        self.chart_type = None
        
    def load_data(self, chart_type='singles'):
        """
        Load ARIA charts data
        
        Parameters:
        -----------
        chart_type : str
            Type of chart: 'singles', 'albums', or 'new_singles'
        """
        print(f"\n{'='*70}")
        print(f"Loading ARIA {chart_type.upper()} Chart Data")
        print(f"{'='*70}")
        
        # If it's a URL or specific file
        if isinstance(self.data_source, str):
            if self.data_source.startswith('http'):
                filepath = self.data_source
            elif Path(self.data_source).is_file():
                filepath = self.data_source
            elif Path(self.data_source).is_dir():
                # Look for chart files in directory
                chart_files = {
                    'singles': 'single_charts.csv',
                    'albums': 'album_charts.csv',
                    'new_singles': 'newsingle_charts.csv'
                }
                filepath = Path(self.data_source) / chart_files[chart_type]
            else:
                # Assume it's from GitHub
                base_url = "https://raw.githubusercontent.com/caseybriggs/aria-charts/main/"
                chart_files = {
                    'singles': 'single_charts.csv',
                    'albums': 'album_charts.csv',
                    'new_singles': 'newsingle_charts.csv'
                }
                filepath = base_url + chart_files[chart_type]
        
        print(f"\n🔄 Loading from: {filepath}")
        
        try:
            self.data = pd.read_csv(filepath)
            self.data['chart_date'] = pd.to_datetime(self.data['chart_date'])
            self.chart_type = chart_type
            
            print(f"✓ Successfully loaded {len(self.data):,} chart entries")
            print(f"  Date range: {self.data['chart_date'].min().date()} to {self.data['chart_date'].max().date()}")
            print(f"  Unique artists: {self.data['artist'].nunique():,}")
            print(f"  Unique songs/albums: {self.data['title'].nunique():,}")
            
            return self.data
            
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return None
    
    def quick_overview(self):
        """Display quick overview of the dataset"""
        if self.data is None:
            print("No data loaded. Run load_data() first.")
            return
        
        print(f"\n{'='*70}")
        print(f"ARIA CHARTS QUICK OVERVIEW")
        print(f"{'='*70}")
        
        print(f"\n📊 Dataset Statistics:")
        print(f"  Total entries: {len(self.data):,}")
        print(f"  Date range: {self.data['chart_date'].min().date()} to {self.data['chart_date'].max().date()}")
        print(f"  Years covered: {self.data['chart_date'].dt.year.nunique()}")
        print(f"  Weeks of data: {self.data['chart_date'].nunique():,}")
        
        print(f"\n🎵 Content Statistics:")
        print(f"  Unique artists: {self.data['artist'].nunique():,}")
        print(f"  Unique songs/albums: {self.data['title'].nunique():,}")
        print(f"  Chart positions: {self.data['rank'].min()} to {self.data['rank'].max()}")
        
        if 'aus_flag' in self.data.columns:
            aus_data = self.data[self.data['aus_flag'] == True]
            aus_pct = (len(aus_data) / len(self.data)) * 100
            print(f"\n🇦🇺 Australian Content:")
            print(f"  Australian entries: {len(aus_data):,} ({aus_pct:.1f}%)")
            print(f"  Australian artists: {aus_data['artist'].nunique():,}")
        
        print(f"\n📋 Data Structure:")
        print(f"  Columns: {', '.join(self.data.columns)}")
        
        print(f"\n📅 Sample Data:")
        print(self.data.head(10))
    
    def top_artists(self, n=20, australian_only=False, time_period=None):
        """
        Find top artists by chart appearances or other metrics
        
        Parameters:
        -----------
        n : int
            Number of top artists to return
        australian_only : bool
            Only include Australian artists
        time_period : tuple
            (start_year, end_year) to filter data
        """
        df = self.data.copy()
        
        # Filter by time period
        if time_period:
            start_year, end_year = time_period
            df = df[(df['chart_date'].dt.year >= start_year) & 
                    (df['chart_date'].dt.year <= end_year)]
        
        # Filter Australian
        if australian_only and 'aus_flag' in df.columns:
            df = df[df['aus_flag'] == True]
        
        print(f"\n{'='*70}")
        title = f"TOP {n} ARTISTS"
        if australian_only:
            title += " (Australian Only)"
        if time_period:
            title += f" ({time_period[0]}-{time_period[1]})"
        print(title)
        print(f"{'='*70}")
        
        # Calculate metrics
        artist_stats = df.groupby('artist').agg({
            'title': 'count',  # Total chart appearances
            'rank': ['min', 'mean'],  # Best and average position
            'chart_date': ['min', 'max']  # First and last appearance
        }).round(1)
        
        artist_stats.columns = ['Appearances', 'Best Position', 'Avg Position', 'First Chart', 'Last Chart']
        artist_stats = artist_stats.sort_values('Appearances', ascending=False).head(n)
        
        # Calculate number one hits
        number_ones = df[df['rank'] == 1].groupby('artist').size()
        artist_stats['#1 Hits'] = artist_stats.index.map(lambda x: number_ones.get(x, 0))
        
        print(artist_stats)
        return artist_stats
    
    def top_songs(self, n=20, by='weeks', australian_only=False):
        """
        Find top songs/albums by various metrics
        
        Parameters:
        -----------
        n : int
            Number of top songs to return
        by : str
            Metric: 'weeks' (total weeks on chart), 'peak' (best position),
                   'top10' (weeks in top 10), 'number1' (weeks at #1)
        australian_only : bool
            Only include Australian artists
        """
        df = self.data.copy()
        
        if australian_only and 'aus_flag' in df.columns:
            df = df[df['aus_flag'] == True]
        
        print(f"\n{'='*70}")
        title = f"TOP {n} SONGS/ALBUMS"
        if australian_only:
            title += " (Australian)"
        print(title)
        print(f"{'='*70}")
        
        if by == 'weeks':
            # Total weeks on chart
            songs = df.groupby(['artist', 'title']).agg({
                'chart_date': 'count',
                'rank': 'min'
            }).rename(columns={'chart_date': 'Weeks on Chart', 'rank': 'Peak Position'})
            songs = songs.sort_values('Weeks on Chart', ascending=False).head(n)
            
        elif by == 'peak':
            # Best peak position
            songs = df.groupby(['artist', 'title']).agg({
                'rank': 'min',
                'chart_date': 'count'
            }).rename(columns={'rank': 'Peak Position', 'chart_date': 'Weeks on Chart'})
            songs = songs.sort_values(['Peak Position', 'Weeks on Chart'], ascending=[True, False]).head(n)
            
        elif by == 'top10':
            # Weeks in top 10
            top10_df = df[df['rank'] <= 10]
            songs = top10_df.groupby(['artist', 'title']).agg({
                'chart_date': 'count',
                'rank': 'min'
            }).rename(columns={'chart_date': 'Weeks in Top 10', 'rank': 'Peak Position'})
            songs = songs.sort_values('Weeks in Top 10', ascending=False).head(n)
            
        elif by == 'number1':
            # Weeks at #1
            number1_df = df[df['rank'] == 1]
            songs = number1_df.groupby(['artist', 'title']).size().to_frame('Weeks at #1')
            # Add total weeks on chart
            total_weeks = df.groupby(['artist', 'title']).size()
            songs['Total Weeks'] = songs.index.map(lambda x: total_weeks.get(x, 0))
            songs = songs.sort_values('Weeks at #1', ascending=False).head(n)
        
        print(songs)
        return songs
    
    def artist_history(self, artist_name, plot=True):
        """
        Analyze an artist's complete chart history
        
        Parameters:
        -----------
        artist_name : str
            Artist name (case-insensitive partial match)
        plot : bool
            Create visualization of chart history
        """
        # Find artist (case-insensitive)
        mask = self.data['artist'].str.contains(artist_name, case=False, na=False)
        artist_data = self.data[mask].copy()
        
        if len(artist_data) == 0:
            print(f"❌ No data found for artist matching '{artist_name}'")
            return None
        
        actual_name = artist_data['artist'].mode()[0]
        
        print(f"\n{'='*70}")
        print(f"CHART HISTORY: {actual_name}")
        print(f"{'='*70}")
        
        # Overall statistics
        print(f"\n📊 Career Statistics:")
        print(f"  First chart appearance: {artist_data['chart_date'].min().date()}")
        print(f"  Most recent appearance: {artist_data['chart_date'].max().date()}")
        print(f"  Total weeks on chart: {len(artist_data):,}")
        print(f"  Different songs/albums: {artist_data['title'].nunique()}")
        print(f"  Best chart position: #{artist_data['rank'].min()}")
        print(f"  Average chart position: #{artist_data['rank'].mean():.1f}")
        
        # Number one hits
        number_ones = artist_data[artist_data['rank'] == 1]
        if len(number_ones) > 0:
            print(f"\n🏆 #1 Hits ({len(number_ones['title'].unique())}):")
            for title in number_ones['title'].unique():
                weeks = len(number_ones[number_ones['title'] == title])
                print(f"  • {title} ({weeks} week{'s' if weeks > 1 else ''} at #1)")
        
        # Top 10 hits
        top10 = artist_data[artist_data['rank'] <= 10]
        if len(top10) > 0:
            print(f"\n⭐ Top 10 Hits ({len(top10['title'].unique())}):")
            for title in top10.groupby('title')['rank'].min().nsmallest(10).index:
                peak = top10[top10['title'] == title]['rank'].min()
                weeks = len(top10[top10['title'] == title])
                print(f"  • {title} (peaked at #{peak}, {weeks} weeks in top 10)")
        
        # Visualization
        if plot and len(artist_data) > 0:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
            
            # Chart positions over time
            for title in artist_data['title'].unique()[:10]:  # Top 10 songs
                song_data = artist_data[artist_data['title'] == title].sort_values('chart_date')
                ax1.plot(song_data['chart_date'], song_data['rank'], 
                        marker='o', label=title[:40], linewidth=2, markersize=4)
            
            ax1.set_ylabel('Chart Position', fontsize=12)
            ax1.set_title(f'{actual_name} - Chart History', fontsize=14, fontweight='bold')
            ax1.invert_yaxis()  # Lower numbers (better positions) at top
            ax1.grid(True, alpha=0.3)
            ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
            ax1.set_ylim(bottom=max(artist_data['rank'].max(), 50), top=1)
            
            # Chart appearances by year
            yearly = artist_data.groupby(artist_data['chart_date'].dt.year).size()
            ax2.bar(yearly.index, yearly.values, color='steelblue', edgecolor='black')
            ax2.set_xlabel('Year', fontsize=12)
            ax2.set_ylabel('Weeks on Chart', fontsize=12)
            ax2.set_title('Chart Appearances by Year', fontsize=12, fontweight='bold')
            ax2.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            plt.show()
        
        return artist_data
    
    def australian_content_analysis(self):
        """Analyze Australian vs international content trends"""
        if 'aus_flag' not in self.data.columns:
            print("❌ Australian flag data not available in this dataset")
            return None
        
        print(f"\n{'='*70}")
        print("AUSTRALIAN CONTENT ANALYSIS")
        print(f"{'='*70}")
        
        # Overall statistics
        aus_count = (self.data['aus_flag'] == True).sum()
        total = len(self.data)
        aus_pct = (aus_count / total) * 100
        
        print(f"\n📊 Overall Statistics:")
        print(f"  Australian entries: {aus_count:,} ({aus_pct:.1f}%)")
        print(f"  International entries: {total - aus_count:,} ({100-aus_pct:.1f}%)")
        
        # By year
        yearly = self.data.groupby([self.data['chart_date'].dt.year, 'aus_flag']).size().unstack(fill_value=0)
        yearly_pct = yearly.div(yearly.sum(axis=1), axis=0) * 100
        
        print(f"\n📅 Trends Over Time:")
        print(f"  Most Australian year: {yearly_pct[True].idxmax()} ({yearly_pct[True].max():.1f}% Australian)")
        print(f"  Least Australian year: {yearly_pct[True].idxmin()} ({yearly_pct[True].min():.1f}% Australian)")
        
        # Visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Trend over time
        yearly_pct[True].plot(ax=ax1, linewidth=3, color='#008751', marker='o')
        ax1.set_xlabel('Year', fontsize=12)
        ax1.set_ylabel('% Australian Content', fontsize=12)
        ax1.set_title('Australian Content Trend Over Time', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, max(yearly_pct[True].max() + 5, 50))
        
        # Overall pie chart
        overall_counts = self.data['aus_flag'].value_counts()
        ax2.pie(overall_counts, labels=['Australian', 'International'], 
               autopct='%1.1f%%', startangle=90, colors=['#008751', '#888888'])
        ax2.set_title('Overall Content Split', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        return yearly_pct
    
    def decades_comparison(self):
        """Compare chart trends across decades"""
        print(f"\n{'='*70}")
        print("DECADES COMPARISON")
        print(f"{'='*70}")
        
        self.data['decade'] = (self.data['chart_date'].dt.year // 10) * 10
        
        for decade in sorted(self.data['decade'].unique()):
            decade_data = self.data[self.data['decade'] == decade]
            print(f"\n{decade}s:")
            print(f"  Chart entries: {len(decade_data):,}")
            print(f"  Unique artists: {decade_data['artist'].nunique():,}")
            print(f"  Unique songs: {decade_data['title'].nunique():,}")
            
            if 'aus_flag' in self.data.columns:
                aus_pct = (decade_data['aus_flag'] == True).sum() / len(decade_data) * 100
                print(f"  Australian content: {aus_pct:.1f}%")
            
            top_artist = decade_data['artist'].value_counts().iloc[0]
            top_count = decade_data['artist'].value_counts().values[0]
            print(f"  Top artist: {top_artist} ({top_count} weeks)")
    
    def export_insights(self, filename='aria_charts_analysis.txt'):
        """Export analysis summary to text file"""
        if self.data is None:
            print("No data loaded.")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write(f"ARIA CHARTS ANALYSIS SUMMARY\n")
            f.write(f"Chart Type: {self.chart_type}\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Date Range: {self.data['chart_date'].min().date()} to {self.data['chart_date'].max().date()}\n")
            f.write(f"Total Entries: {len(self.data):,}\n")
            f.write(f"Unique Artists: {self.data['artist'].nunique():,}\n\n")
            
            f.write("TOP 20 ARTISTS BY APPEARANCES:\n")
            f.write(str(self.data['artist'].value_counts().head(20)))
            
        print(f"\n✓ Analysis exported to: {filename}")


def main():
    """Main function with usage examples"""
    print("="*70)
    print("ARIA MUSIC CHARTS EXPLORER")
    print("Analyzing Casey Briggs' ARIA Charts Dataset")
    print("="*70)
    print("\nRepository: https://github.com/caseybriggs/ARIA-charts")
    print("\nUsage examples:\n")
    print("""
# Load singles chart data from GitHub
explorer = ARIAChartsExplorer('github')
explorer.load_data('singles')

# Or load from local file
explorer = ARIAChartsExplorer('path/to/singles_chart.csv')
explorer.load_data()

# Quick overview
explorer.quick_overview()

# Top artists
explorer.top_artists(n=20, australian_only=False)

# Top songs by weeks on chart
explorer.top_songs(n=20, by='weeks')

# Analyze specific artist
explorer.artist_history('Kylie Minogue', plot=True)

# Australian content analysis
explorer.australian_content_analysis()

# Decades comparison
explorer.decades_comparison()
""")


if __name__ == "__main__":
    main()
