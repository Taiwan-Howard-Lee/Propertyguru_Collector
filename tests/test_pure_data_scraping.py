#!/usr/bin/env python3
"""
🧪 Test Pure Data Scraping - 5 Pages
Test the pure data scraping system with clean data extraction
"""

import sys
import os
import json
import time
from collections import Counter, defaultdict

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from scrapers.pure_data_scraper import PureDataScraper

def analyze_pure_data_quality(properties):
    """Analyze pure data quality and categories"""
    print("\n📊 PURE DATA QUALITY ANALYSIS")
    print("=" * 50)
    print("🚫 NO market analysis - raw data only")
    
    if not properties:
        print("❌ No properties to analyze")
        return
    
    total = len(properties)
    print(f"📊 Total properties: {total}")
    
    # Price range distribution
    price_ranges = {}
    for prop in properties:
        price_range = prop.get('price_range', 'Unknown')
        price_ranges[price_range] = price_ranges.get(price_range, 0) + 1
    
    print(f"\n💰 PRICE RANGES:")
    for price_range, count in sorted(price_ranges.items()):
        percentage = (count / total) * 100
        print(f"   {price_range}: {count} properties ({percentage:.1f}%)")
    
    # Property type distribution
    property_types = {}
    for prop in properties:
        prop_type = prop.get('property_type', 'Unknown')
        property_types[prop_type] = property_types.get(prop_type, 0) + 1
    
    print(f"\n🏠 PROPERTY TYPES:")
    for prop_type, count in sorted(property_types.items()):
        percentage = (count / total) * 100
        print(f"   {prop_type}: {count} properties ({percentage:.1f}%)")
    
    # MRT distance categories
    mrt_categories = {}
    for prop in properties:
        mrt_cat = prop.get('mrt_distance_category', 'Unknown')
        mrt_categories[mrt_cat] = mrt_categories.get(mrt_cat, 0) + 1
    
    print(f"\n🚇 MRT DISTANCE CATEGORIES:")
    for mrt_cat, count in sorted(mrt_categories.items()):
        percentage = (count / total) * 100
        print(f"   {mrt_cat}: {count} properties ({percentage:.1f}%)")
    
    # Size categories
    size_categories = {}
    for prop in properties:
        size_cat = prop.get('size_category', 'Unknown')
        size_categories[size_cat] = size_categories.get(size_cat, 0) + 1
    
    print(f"\n📏 SIZE CATEGORIES:")
    for size_cat, count in sorted(size_categories.items()):
        percentage = (count / total) * 100
        print(f"   {size_cat}: {count} properties ({percentage:.1f}%)")
    
    # Data completeness
    print(f"\n✅ DATA COMPLETENESS:")
    fields_to_check = ['property_name', 'price_numeric', 'bedrooms', 'property_type', 'mrt_station']
    for field in fields_to_check:
        complete_count = sum(1 for prop in properties if prop.get(field))
        percentage = (complete_count / total) * 100
        print(f"   {field}: {complete_count}/{total} ({percentage:.1f}%)")

def show_sample_properties(properties, count=5):
    """Show sample properties"""
    print(f"\n📋 SAMPLE PURE DATA PROPERTIES:")
    print("=" * 50)
    
    for i, prop in enumerate(properties[:count], 1):
        print(f"\n{i}. {prop.get('property_name', 'N/A')}")
        print(f"   💰 {prop.get('price_formatted', 'N/A')} ({prop.get('price_range', 'N/A')})")
        print(f"   🏠 {prop.get('property_type', 'N/A')} • {prop.get('bedrooms', 'N/A')}BR • {prop.get('floor_area_sqft', 'N/A')} sqft")
        print(f"   📍 {prop.get('district_code', 'N/A')} • {prop.get('mrt_station', 'N/A')} ({prop.get('mrt_distance_category', 'N/A')})")
        print(f"   📅 {prop.get('listed_date', 'N/A')} • {prop.get('image_count', 0)} images")
        if prop.get('property_url'):
            print(f"   🔗 {prop['property_url']}")

def test_pure_data_scraping():
    """Test pure data scraping with 5 pages"""
    
    print("🧪 PURE DATA SCRAPING TEST")
    print("=" * 60)
    print("📊 Testing 5 pages of pure data collection")
    print("🚫 NO market analysis or segmentation")
    
    start_time = time.time()
    
    try:
        # Initialize scraper
        scraper = PureDataScraper()
        
        # Start scraping
        print("\n🚀 Starting 5-page pure data test...")
        success = scraper.start_pure_data_collection(max_pages=5, start_page=1)
        
        if not success:
            print("❌ Pure data scraping test failed")
            return
        
        # Find the latest pure data file
        data_files = []
        if os.path.exists('data'):
            for file in os.listdir('data'):
                if file.startswith('pure_data_') and file.endswith('.json'):
                    file_path = os.path.join('data', file)
                    data_files.append((file_path, os.path.getmtime(file_path)))
        
        if not data_files:
            print("❌ No pure data file found")
            return
        
        # Get the most recent file
        latest_file = max(data_files, key=lambda x: x[1])[0]
        print(f"\n📂 Analyzing: {latest_file}")
        
        # Load and analyze data
        with open(latest_file, 'r', encoding='utf-8') as f:
            properties = json.load(f)
        
        # Analyze data quality
        analyze_pure_data_quality(properties)
        
        # Show samples
        show_sample_properties(properties)
        
        # Test summary
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n🎉 PURE DATA TEST COMPLETE!")
        print("=" * 50)
        print(f"⏱️ Duration: {duration:.1f} seconds")
        print(f"📊 Properties collected: {len(properties)}")
        print(f"💾 Data file: {latest_file}")
        print("✅ Pure data format verified")
        print("🚫 No market analysis included")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    test_pure_data_scraping()
