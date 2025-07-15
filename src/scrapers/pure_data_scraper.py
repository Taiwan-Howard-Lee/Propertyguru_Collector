#!/usr/bin/env python3
"""
📊 Pure Data Scraper
Raw data collection without any market analysis or segmentation
"""

import sys
import os
import json
import time
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scrapers.main_scraper import SmartPropertyScraper
from schemas.pure_data_schema import PureDataSchema

class PureDataScraper:
    """Pure data collection scraper - no analysis, just clean categorized data"""
    
    def __init__(self):
        self.scraper = SmartPropertyScraper()
        self.start_time = None
        self.total_properties = 0
        self.successful_conversions = 0
        
    def start_pure_data_collection(self, max_pages: int = 100, start_page: int = 1):
        """Start pure data collection without any analysis"""

        print("📊 PURE DATA COLLECTION")
        print("=" * 60)
        print("🚫 NO market analysis or segmentation")
        print("📋 Raw data collection with simple categorization only")
        print(f"📄 Target: {max_pages} pages (~{max_pages * 20} properties)")
        print(f"🔢 Starting from page: {start_page}")

        self.start_time = datetime.now()

        # Fix SSL certificate issues
        self._fix_ssl_certificates()

        try:
            # Start scraping with main scraper
            print(f"\n🚀 Starting data collection...")

            # Try to connect to existing Chrome session first
            if not self._connect_to_existing_chrome():
                print("❌ Failed to connect to existing Chrome session")
                return False

            # Start multi-page scraping directly (skip navigation since Chrome is already on PropertyGuru)
            properties = self.scraper.scrape_multiple_pages(max_pages=max_pages, start_page=start_page)

            if not properties:
                print("❌ No properties extracted")
                return False

            # Save the technical data first
            filename = self.scraper.save_properties(properties)
            print(f"📂 Technical data saved to: {filename}")

            success = True

            if not success:
                print("❌ Data collection failed")
                return False

            # Convert to pure data format using the saved file
            pure_data_file = self._convert_to_pure_data(filename)

            if pure_data_file:
                self._show_collection_summary(pure_data_file)
                return True
            else:
                print("❌ Pure data conversion failed")
                return False

        except KeyboardInterrupt:
            print("\n⏹️ Data collection interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Error during data collection: {e}")
            return False
        finally:
            # Close browser connection
            if hasattr(self.scraper, 'close'):
                self.scraper.close()

    def _fix_ssl_certificates(self):
        """Fix SSL certificate issues on macOS"""
        import os
        import ssl
        import certifi

        print("🔒 Fixing SSL certificate issues...")

        # Tell Python to use certifi's certificates
        os.environ['SSL_CERT_FILE'] = certifi.where()

        # Create default SSL context with certificate verification disabled
        ssl._create_default_https_context = ssl._create_unverified_context

        print("✅ SSL certificate verification disabled")

    def _connect_to_existing_chrome(self):
        """Connect to existing Chrome session or start new undetected Chrome"""
        try:
            # First try to connect to existing Chrome on port 9222
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.support.ui import WebDriverWait

            try:
                chrome_options = Options()
                chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
                self.scraper.driver = webdriver.Chrome(options=chrome_options)
                self.scraper.wait = WebDriverWait(self.scraper.driver, 20)

                print("✅ Connected to existing Chrome session")
                print(f"   Current URL: {self.scraper.driver.current_url}")

                # Check if we're on PropertyGuru
                if "propertyguru.com.sg" in self.scraper.driver.current_url:
                    print("✅ Already on PropertyGuru - ready to scrape!")
                    return True
                else:
                    print("⚠️ Not on PropertyGuru - navigating now...")
                    return self._navigate_to_propertyguru()

            except Exception as e:
                print(f"⚠️ Existing Chrome connection failed: {e}")
                print("🛡️ Starting new undetected Chrome session...")

                # Fallback to undetected Chrome
                import undetected_chromedriver as uc
                import time

                self.scraper.driver = uc.Chrome(
                    headless=False,
                    use_subprocess=False,
                    version_main=None
                )
                self.scraper.wait = WebDriverWait(self.scraper.driver, 20)

                print("✅ Started new undetected Chrome session")
                return self._navigate_to_propertyguru()

        except Exception as e:
            print(f"❌ Failed to connect to Chrome: {e}")
            return False

    def _navigate_to_propertyguru(self):
        """Navigate to PropertyGuru with comprehensive district coverage"""
        try:
            import time

            url = "https://www.propertyguru.com.sg/property-for-sale?freetext=D01+Boat+Quay+%2F+Raffles+Place+%2F+Marina%2C+D02+Chinatown+%2F+Tanjong+Pagar%2C+D03+Alexandra+%2F+Commonwealth%2C+D04+Harbourfront+%2F+Telok+Blangah%2C+D05+Buona+Vista+%2F+West+Coast+%2F+Clementi+New+Town%2C+D06+City+Hall+%2F+Clarke+Quay%2C+D07+Beach+Road+%2F+Bugis+%2F+Rochor%2C+D08+Farrer+Park+%2F+Serangoon+Rd%2C+D09+Orchard+%2F+River+Valley%2C+D10+Tanglin+%2F+Holland+%2F+Bukit+Timah%2C+D11+Newton+%2F+Novena%2C+D21+Clementi+Park+%2F+Upper+Bukit+Timah%2C+D12+Balestier+%2F+Toa+Payoh%2C+D13+Macpherson+%2F+Potong+Pasir%2C+D14+Eunos+%2F+Geylang+%2F+Paya+Lebar%2C+D15+East+Coast+%2F+Marine+Parade%2C+D16+Bedok+%2F+Upper+East+Coast%2C+D17+Changi+Airport+%2F+Changi+Village%2C+D18+Pasir+Ris+%2F+Tampines%2C+D19+Hougang+%2F+Punggol+%2F+Sengkang%2C+D20+Ang+Mo+Kio+%2F+Bishan+%2F+Thomson%2C+D22+Boon+Lay+%2F+Jurong+%2F+Tuas%2C+D23+Dairy+Farm+%2F+Bukit+Panjang+%2F+Choa+Chu+Kang%2C+D24+Lim+Chu+Kang+%2F+Tengah%2C+D25+Admiralty+%2F+Woodlands%2C+D26+Mandai+%2F+Upper+Thomson%2C+D27+Sembawang+%2F+Yishun%2C+D28+Seletar+%2F+Yio+Chu+Kang&districtCode=D01&districtCode=D02&districtCode=D03&districtCode=D04&districtCode=D05&districtCode=D06&districtCode=D07&districtCode=D08&districtCode=D09&districtCode=D10&districtCode=D11&districtCode=D21&districtCode=D12&districtCode=D13&districtCode=D14&districtCode=D15&districtCode=D16&districtCode=D17&districtCode=D18&districtCode=D19&districtCode=D20&districtCode=D22&districtCode=D23&districtCode=D24&districtCode=D25&districtCode=D26&districtCode=D27&districtCode=D28&isCommercial=false"

            print("🌐 Navigating to PropertyGuru (All Singapore Districts D01-D28)")
            self.scraper.driver.get(url)

            # Wait for page load
            time.sleep(5)

            print("✅ Successfully navigated to PropertyGuru")
            return True

        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False
    
    def _get_latest_extraction_file(self):
        """Get the most recent extraction file"""
        
        data_dir = "data"
        if not os.path.exists(data_dir):
            return None
        
        # Look for extraction files
        extraction_files = []
        for file in os.listdir(data_dir):
            if file.startswith("extraction_") and file.endswith(".json"):
                file_path = os.path.join(data_dir, file)
                extraction_files.append((file_path, os.path.getmtime(file_path)))
        
        if not extraction_files:
            return None
        
        # Return the most recent file
        latest_file = max(extraction_files, key=lambda x: x[1])[0]
        return latest_file
    
    def _convert_to_pure_data(self, extraction_file: str):
        """Convert technical extraction to pure data format"""
        
        print(f"\n📊 CONVERTING TO PURE DATA FORMAT")
        print("=" * 50)
        
        try:
            # Load technical data
            with open(extraction_file, 'r', encoding='utf-8') as f:
                technical_data = json.load(f)
            
            print(f"📂 Processing {len(technical_data)} properties...")
            
            # Convert each property
            pure_properties = []
            skipped = 0
            
            for i, tech_prop in enumerate(technical_data):
                pure_prop = PureDataSchema.create_property_record(tech_prop)
                
                if pure_prop:
                    pure_properties.append(pure_prop)
                    self.successful_conversions += 1
                else:
                    skipped += 1
                
                if (i + 1) % 20 == 0:
                    print(f"   📊 Processed {i + 1}/{len(technical_data)} properties...")
            
            self.total_properties = len(pure_properties)
            
            print(f"✅ Successfully converted {len(pure_properties)} properties")
            print(f"⚠️ Skipped {skipped} properties (insufficient data)")
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"data/pure_data_{timestamp}.json"

            # Ensure directory exists
            os.makedirs("data", exist_ok=True)
            
            # Save pure data
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(pure_properties, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Pure data saved to: {output_file}")
            
            return output_file
            
        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return None
    
    def _show_collection_summary(self, pure_data_file: str):
        """Show summary of pure data collection"""
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print(f"\n🎉 PURE DATA COLLECTION COMPLETE!")
        print("=" * 60)
        print(f"⏱️ Duration: {duration}")
        print(f"📊 Total properties: {self.total_properties}")
        print(f"✅ Successful conversions: {self.successful_conversions}")
        print(f"💾 Output file: {pure_data_file}")
        
        # Load and analyze the pure data
        try:
            with open(pure_data_file, 'r', encoding='utf-8') as f:
                pure_data = json.load(f)
            
            print(f"\n📋 DATA CATEGORIES (NO ANALYSIS):")
            print("=" * 40)
            
            # Price range distribution
            price_ranges = {}
            for prop in pure_data:
                price_range = prop.get('price_range', 'Unknown')
                price_ranges[price_range] = price_ranges.get(price_range, 0) + 1
            
            print("💰 Price Ranges:")
            for price_range, count in sorted(price_ranges.items()):
                print(f"   {price_range}: {count} properties")
            
            # Property type distribution
            property_types = {}
            for prop in pure_data:
                prop_type = prop.get('property_type', 'Unknown')
                property_types[prop_type] = property_types.get(prop_type, 0) + 1
            
            print("\n🏠 Property Types:")
            for prop_type, count in sorted(property_types.items()):
                print(f"   {prop_type}: {count} properties")
            
            # MRT distance categories
            mrt_categories = {}
            for prop in pure_data:
                mrt_cat = prop.get('mrt_distance_category', 'Unknown')
                mrt_categories[mrt_cat] = mrt_categories.get(mrt_cat, 0) + 1
            
            print("\n🚇 MRT Distance Categories:")
            for mrt_cat, count in sorted(mrt_categories.items()):
                print(f"   {mrt_cat}: {count} properties")
            
            # Show sample properties
            print(f"\n📋 SAMPLE PURE DATA:")
            print("=" * 40)
            
            for i, prop in enumerate(pure_data[:3], 1):
                print(f"\n{i}. {prop['property_name']}")
                print(f"   💰 {prop['price_formatted']} ({prop.get('price_range', 'N/A')})")
                print(f"   🏠 {prop.get('property_type', 'N/A')} • {prop['bedrooms']}BR • {prop.get('floor_area_sqft', 'N/A')} sqft")
                print(f"   📍 {prop.get('district_code', 'N/A')} • {prop.get('mrt_station', 'N/A')} ({prop.get('mrt_distance_category', 'N/A')})")
                print(f"   📅 {prop.get('listed_date', 'N/A')} • {prop.get('image_count', 0)} images")
                if prop.get('property_url'):
                    print(f"   🔗 {prop['property_url']}")
            
            print(f"\n🎯 PURE DATA READY FOR USE!")
            print("📊 No market analysis or segmentation included")
            print("📋 Raw categorized data only")
            
        except Exception as e:
            print(f"⚠️ Could not analyze data: {e}")

def main():
    """Main execution function for pure data collection"""
    
    print("📊 PROPERTYGURU PURE DATA COLLECTOR")
    print("=" * 60)
    print("🚫 NO market analysis or investment insights")
    print("📋 Raw data collection with simple categorization")
    print("🎯 Perfect for custom analysis and research")
    
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
