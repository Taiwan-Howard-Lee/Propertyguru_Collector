#!/usr/bin/env python3
"""
📊 PropertyGuru Pure Data Scraper
Raw data collection only - no market analysis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scrapers.pure_data_scraper import PureDataScraper

def main():
    """Main execution function for pure data collection"""

    print("📊 PROPERTYGURU PURE DATA SCRAPER")
    print("=" * 60)
    print("🚫 NO market analysis or investment insights")
    print("📋 Raw data collection with simple categorization")
    print("🎯 Perfect for custom research and analysis")

    try:
        print("\n⚙️ COLLECTION CONFIGURATION:")
        max_pages = int(input("📄 How many pages to collect? (default 100): ") or "100")
        start_page = int(input("🔢 Start from which page? (default 1): ") or "1")

        print(f"\n🎯 Configuration:")
        print(f"   Pages to collect: {max_pages}")
        print(f"   Starting page: {start_page}")
        print(f"   Expected properties: ~{max_pages * 20}")
        print(f"   Format: Pure data (no analysis)")

        confirm = input("\n🚀 Start pure data collection? (y/N): ").lower()
        if confirm != 'y':
            print("❌ Collection cancelled")
            return

        # Start collection
        scraper = PureDataScraper()
        success = scraper.start_pure_data_collection(max_pages, start_page)

        if success:
            print("\n🎉 Pure data collection completed successfully!")
        else:
            print("\n❌ Collection failed")

    except KeyboardInterrupt:
        print("\n⏹️ Collection interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
