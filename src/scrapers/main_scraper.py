#!/usr/bin/env python3
"""
🧠 Smart PropertyGuru Scraper
Handles Cloudflare and extracts property data intelligently
"""

import time
import json
import re
import random
import sys
import os
from datetime import datetime
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from extractors.advanced_extractor import AdvancedPropertyExtractor

class SmartPropertyScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        # Enhanced timing patterns for human-like behavior
        self.timing_patterns = {
            'page_load': (3, 8),      # 3-8 seconds for page loads
            'action_delay': (1, 3),   # 1-3 seconds between actions
            'scroll_delay': (0.5, 2), # 0.5-2 seconds for scrolling
            'cloudflare_wait': (5, 15) # 5-15 seconds for Cloudflare
        }

    def human_delay(self, delay_type='action_delay'):
        """Add human-like delays based on timing patterns"""
        min_delay, max_delay = self.timing_patterns.get(delay_type, (1, 3))
        delay = random.uniform(min_delay, max_delay)
        print(f"⏱️ Human-like delay: {delay:.1f}s ({delay_type})")
        time.sleep(delay)

    def load_manual_connection(self):
        """Load manually selected Chrome connection info"""
        try:
            import os
            connection_file = os.path.join(os.path.dirname(__file__), '..', 'chrome_connection.json')
            if os.path.exists(connection_file):
                with open(connection_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load manual connection: {e}")
        return None

    def connect_and_navigate(self):
        """Connect to browser and navigate to PropertyGuru with enhanced stealth"""
        try:
            # Try to use manually selected Chrome tab first
            connection_info = self.load_manual_connection()
            if connection_info:
                try:
                    port = connection_info['port']
                    chrome_options = Options()
                    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
                    self.driver = webdriver.Chrome(options=chrome_options)
                    print(f"✅ Connected to manually selected Chrome tab (port {port})")
                    print(f"   Tab: {connection_info.get('tab_title', 'Unknown')}")
                except Exception as e:
                    print(f"⚠️ Manual connection failed: {e}")
                    print("🔄 Falling back to automatic detection...")
                    connection_info = None

            # Fallback to automatic Chrome detection
            if not connection_info:
                try:
                    chrome_options = Options()
                    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
                    self.driver = webdriver.Chrome(options=chrome_options)
                    print("✅ Connected to existing Chrome browser (debug mode)")
                except:
                    # Final fallback to undetected Chrome
                    print("🛡️ Starting undetected Chrome for enhanced stealth...")
                    self.driver = uc.Chrome(
                        headless=False,
                        use_subprocess=False,
                        version_main=None  # Auto-detect Chrome version
                    )
                    print("✅ Started undetected Chrome browser")

            self.wait = WebDriverWait(self.driver, 20)  # Increased timeout

            # Navigate to PropertyGuru with comprehensive district coverage
            url = "https://www.propertyguru.com.sg/property-for-sale?freetext=D01+Boat+Quay+%2F+Raffles+Place+%2F+Marina%2C+D02+Chinatown+%2F+Tanjong+Pagar%2C+D03+Alexandra+%2F+Commonwealth%2C+D04+Harbourfront+%2F+Telok+Blangah%2C+D05+Buona+Vista+%2F+West+Coast+%2F+Clementi+New+Town%2C+D06+City+Hall+%2F+Clarke+Quay%2C+D07+Beach+Road+%2F+Bugis+%2F+Rochor%2C+D08+Farrer+Park+%2F+Serangoon+Rd%2C+D09+Orchard+%2F+River+Valley%2C+D10+Tanglin+%2F+Holland+%2F+Bukit+Timah%2C+D11+Newton+%2F+Novena%2C+D21+Clementi+Park+%2F+Upper+Bukit+Timah%2C+D12+Balestier+%2F+Toa+Payoh%2C+D13+Macpherson+%2F+Potong+Pasir%2C+D14+Eunos+%2F+Geylang+%2F+Paya+Lebar%2C+D15+East+Coast+%2F+Marine+Parade%2C+D16+Bedok+%2F+Upper+East+Coast%2C+D17+Changi+Airport+%2F+Changi+Village%2C+D18+Pasir+Ris+%2F+Tampines%2C+D19+Hougang+%2F+Punggol+%2F+Sengkang%2C+D20+Ang+Mo+Kio+%2F+Bishan+%2F+Thomson%2C+D22+Boon+Lay+%2F+Jurong+%2F+Tuas%2C+D23+Dairy+Farm+%2F+Bukit+Panjang+%2F+Choa+Chu+Kang%2C+D24+Lim+Chu+Kang+%2F+Tengah%2C+D25+Admiralty+%2F+Woodlands%2C+D26+Mandai+%2F+Upper+Thomson%2C+D27+Sembawang+%2F+Yishun%2C+D28+Seletar+%2F+Yio+Chu+Kang&districtCode=D01&districtCode=D02&districtCode=D03&districtCode=D04&districtCode=D05&districtCode=D06&districtCode=D07&districtCode=D08&districtCode=D09&districtCode=D10&districtCode=D11&districtCode=D21&districtCode=D12&districtCode=D13&districtCode=D14&districtCode=D15&districtCode=D16&districtCode=D17&districtCode=D18&districtCode=D19&districtCode=D20&districtCode=D22&districtCode=D23&districtCode=D24&districtCode=D25&districtCode=D26&districtCode=D27&districtCode=D28&isCommercial=false"
            print(f"🌐 Navigating to: PropertyGuru (All Singapore Districts D01-D28)")
            print(f"🎯 Comprehensive coverage: All 28 districts included")
            self.driver.get(url)

            # Human-like delay after navigation
            self.human_delay('page_load')

            return True

        except Exception as e:
            print(f"❌ Connection/Navigation failed: {e}")
            return False
    
    def handle_cloudflare_and_wait(self):
        """Handle Cloudflare protection with enhanced timing patterns"""
        print("🛡️ Checking for Cloudflare protection...")

        max_wait_time = 90  # Increased wait time for better success
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                current_title = self.driver.title
                current_url = self.driver.current_url

                print(f"⏳ Current page: {current_title}")

                # Check if we're past Cloudflare
                if ("just a moment" not in current_title.lower() and
                    "propertyguru" in current_url and
                    "cloudflare" not in current_title.lower()):

                    print("✅ Successfully bypassed Cloudflare!")

                    # Human-like delay after successful bypass
                    self.human_delay('page_load')
                    return True

                # Check if we need to wait for Cloudflare
                if "just a moment" in current_title.lower() or "cloudflare" in current_title.lower():
                    print("🔄 Waiting for Cloudflare to pass...")
                    # Use human-like delay for Cloudflare waiting
                    self.human_delay('cloudflare_wait')
                    continue

                # Check if page has property content
                try:
                    body_text = self.driver.find_element(By.TAG_NAME, "body").text
                    if "properties for sale" in body_text.lower() or "S$" in body_text:
                        print("✅ PropertyGuru content detected!")
                        self.human_delay('action_delay')
                        return True
                except:
                    pass

                # Human-like delay between checks
                self.human_delay('action_delay')

            except Exception as e:
                print(f"⚠️ Error checking page: {e}")
                self.human_delay('action_delay')

        print("⚠️ Cloudflare wait timeout, proceeding anyway...")
        return False
    
    def extract_properties_smart(self):
        """Advanced property extraction using comprehensive extractor"""
        print("🔍 Starting smart property extraction...")

        try:
            # Use the advanced extractor first
            extractor = AdvancedPropertyExtractor(self.driver)
            properties = extractor.extract_properties_from_page()

            if properties:
                print(f"✅ Advanced extractor found {len(properties)} properties")
                return properties
            else:
                print("⚠️ Advanced extractor found no properties, trying fallback strategies...")
                return self._fallback_extraction_strategies()

        except Exception as e:
            print(f"⚠️ Advanced extraction failed: {e}")
            return self._fallback_extraction_strategies()

    def _fallback_extraction_strategies(self):
        """Fallback extraction strategies"""
        properties = []

        try:
            # Strategy 1: Look for property data in page source
            print("📊 Strategy 1: Analyzing page source...")
            page_source = self.driver.page_source

            # Look for JSON data in script tags (common in modern websites)
            json_matches = re.findall(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', page_source, re.DOTALL)
            if not json_matches:
                json_matches = re.findall(r'window\.__NEXT_DATA__\s*=\s*({.*?});', page_source, re.DOTALL)
            if not json_matches:
                json_matches = re.findall(r'"listings":\s*(\[.*?\])', page_source, re.DOTALL)

            for json_str in json_matches:
                try:
                    data = json.loads(json_str)
                    extracted = self._extract_from_json_data(data)
                    if extracted:
                        properties.extend(extracted)
                        print(f"✅ Strategy 1 found {len(extracted)} properties in JSON data")
                        break
                except:
                    continue

            # Strategy 2: Extract from visible page text
            if not properties:
                print("📊 Strategy 2: Extracting from page text...")
                properties = self._extract_from_page_text()

            # Strategy 3: Look for property elements
            if not properties:
                print("📊 Strategy 3: Looking for property elements...")
                properties = self._extract_from_elements()

        except Exception as e:
            print(f"❌ Extraction error: {e}")

        return properties

    def find_next_button(self):
        """Find and return the next page button"""
        # PropertyGuru-specific selectors based on inspection
        next_button_selectors = [
            # PropertyGuru specific - most likely to work
            '.hui-pagination a.page-link',
            '.pagination a.page-link',
            'a.page-link',

            # Generic fallbacks
            'a[aria-label="Next"]',
            'a[title="Next"]',
            'button[aria-label="Next"]',
            'button[title="Next"]',
            '.next-page',
            '.pagination-next',
            '[data-testid="next-page"]',
            '[data-testid="pagination-next"]'
        ]

        for selector in next_button_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_enabled() and element.is_displayed():
                        text = element.text.strip().lower()
                        # Check if this is actually the "Next" button
                        if 'next' in text:
                            print(f"✅ Found Next button: {selector} with text '{element.text.strip()}'")
                            return element
            except Exception as e:
                continue

        # Fallback: XPath search for "Next" text
        try:
            elements = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')] | //button[contains(text(), 'Next')]")
            for element in elements:
                if element.is_enabled() and element.is_displayed():
                    print(f"✅ Found Next button via XPath with text '{element.text.strip()}'")
                    return element
        except:
            pass

        print("❌ Next button not found with any selector")
        return None

    def click_next_page(self):
        """Navigate to next page using URL-based pagination (PropertyGuru uses URLs, not AJAX)"""
        try:
            # Get current page number
            current_page, _ = self.get_current_page_info()
            next_page = current_page + 1

            print(f"🔄 Navigating from page {current_page} to page {next_page}")

            # Get current URL and modify it for next page
            current_url = self.driver.current_url

            # PropertyGuru URL patterns:
            # Page 1: /property-for-sale?params
            # Page 2+: /property-for-sale/2?params

            if '/property-for-sale/' in current_url and '?' in current_url:
                # Already has page number - replace it
                if f'/property-for-sale/{current_page}?' in current_url:
                    next_url = current_url.replace(f'/property-for-sale/{current_page}?', f'/property-for-sale/{next_page}?')
                else:
                    # Fallback: get URL from next button
                    next_button = self.find_next_button()
                    if next_button:
                        next_url = next_button.get_attribute('href')
                        if not next_url:
                            print("❌ Next button has no href")
                            return False
                    else:
                        print("❌ Cannot find next button for URL")
                        return False
            elif '/property-for-sale?' in current_url and current_page == 1:
                # Page 1 format - add page number for page 2+
                next_url = current_url.replace('/property-for-sale?', f'/property-for-sale/{next_page}?')
            else:
                # Fallback: get URL from next button
                next_button = self.find_next_button()
                if next_button:
                    next_url = next_button.get_attribute('href')
                    if not next_url:
                        print("❌ Next button has no href")
                        return False
                else:
                    print("❌ Cannot determine next page URL")
                    return False

            print(f"🔗 Navigating to: {next_url[:100]}...")

            # Navigate to next page
            self.driver.get(next_url)

            # Wait for page to load
            self.human_delay('page_load')

            print("✅ Successfully navigated to next page")
            return True

        except Exception as e:
            print(f"❌ Error navigating to next page: {e}")
            return False

    def get_current_page_info(self):
        """Get current page number and total pages"""
        try:
            # PropertyGuru specific: look for current page in pagination
            try:
                # Look for the current page indicator in pagination
                current_page_elements = self.driver.find_elements(By.CSS_SELECTOR, '.hui-pagination .page-item.active .page-link, .pagination .page-item.active .page-link')
                if current_page_elements:
                    current_text = current_page_elements[0].text.strip()
                    # Extract number from text like "1\n(current)"
                    page_match = re.search(r'(\d+)', current_text)
                    if page_match:
                        current_page = int(page_match.group(1))
                        print(f"📄 Current page from pagination: {current_page}")
                        return current_page, None
            except:
                pass

            # Fallback: check URL for page parameter
            current_url = self.driver.current_url
            page_match = re.search(r'[?&]page=(\d+)', current_url)
            if page_match:
                current_page = int(page_match.group(1))
                print(f"📄 Current page from URL: {current_page}")
                return current_page, None

            # Fallback: look for page info in page text
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text
                # Look for patterns like "52,147 Properties" to detect content changes
                property_count_match = re.search(r'([\d,]+)\s+Properties', body_text)
                if property_count_match:
                    count = property_count_match.group(1)
                    print(f"📊 Found {count} properties on current page")
            except:
                pass

            print("📄 Defaulting to page 1")
            return 1, None  # Default to page 1

        except Exception as e:
            print(f"⚠️ Could not get page info: {e}")
            return 1, None
    
    def _extract_from_json_data(self, data):
        """Extract properties from JSON data"""
        properties = []
        
        def find_properties_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ['listings', 'properties', 'results', 'data']:
                        if isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict) and 'price' in str(item).lower():
                                    prop = self._parse_property_json(item)
                                    if prop:
                                        properties.append(prop)
                    else:
                        find_properties_recursive(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_properties_recursive(item, f"{path}[{i}]")
        
        find_properties_recursive(data)
        return properties
    
    def _parse_property_json(self, item):
        """Parse a single property from JSON"""
        try:
            prop = {
                'id': item.get('id', f'prop_{len(properties)}'),
                'extraction_timestamp': datetime.now().isoformat(),
                'source': 'PropertyGuru'
            }
            
            # Extract common fields
            if 'price' in item:
                prop['price'] = item['price']
            if 'bedrooms' in item:
                prop['bedrooms'] = item['bedrooms']
            if 'bathrooms' in item:
                prop['bathrooms'] = item['bathrooms']
            if 'area' in item:
                prop['area'] = item['area']
            if 'title' in item:
                prop['name'] = item['title']
            if 'address' in item:
                prop['address'] = item['address']
            
            return prop if 'price' in prop else None
            
        except Exception as e:
            return None
    
    def _extract_from_page_text(self):
        """Extract properties from visible page text"""
        properties = []
        
        try:
            # Get page text
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Look for property patterns
            # Pattern: Find lines with price, beds, and area
            lines = body_text.split('\n')
            
            current_property = {}
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Look for price
                price_match = re.search(r'S\$\s*([\d,]+)', line)
                if price_match:
                    if current_property:
                        # Save previous property
                        if self._is_valid_property(current_property):
                            properties.append(current_property)
                    
                    # Start new property
                    current_property = {
                        'id': f'property_{len(properties)}',
                        'price': int(price_match.group(1).replace(',', '')),
                        'extraction_timestamp': datetime.now().isoformat(),
                        'source': 'PropertyGuru'
                    }
                
                # Look for bedrooms
                bed_match = re.search(r'(\d+)\s+Beds?', line)
                if bed_match and current_property:
                    current_property['bedrooms'] = int(bed_match.group(1))
                
                # Look for area
                area_match = re.search(r'(\d+,?\d*)\s+sqft', line)
                if area_match and current_property:
                    current_property['area'] = int(area_match.group(1).replace(',', ''))
                
                # Look for property name (usually appears before price)
                if not price_match and current_property and 'name' not in current_property:
                    name_match = re.search(r'^([A-Z][a-zA-Z\s&@]+(?:Residences?|Towers?|Hill|House|Nine|Waterfront|Handy|Paterson|Promont|Emerald|Shenton|Newton|Zion|Hijauan|Cairnhill|Attitude|Leonie|Wharf|Abode|Tribeca|Haus))$', line)
                    if name_match:
                        current_property['name'] = name_match.group(1)
            
            # Add last property
            if current_property and self._is_valid_property(current_property):
                properties.append(current_property)
            
            print(f"✅ Extracted {len(properties)} properties from page text")
            
        except Exception as e:
            print(f"❌ Text extraction error: {e}")
        
        return properties
    
    def _extract_from_elements(self):
        """Extract properties from DOM elements"""
        properties = []
        
        try:
            # Try different selectors for property containers
            selectors = [
                '[data-testid*="listing"]',
                '[class*="listing"]',
                '[class*="property"]',
                '[class*="card"]',
                'article',
                'div[class*="item"]'
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"   Found {len(elements)} elements with: {selector}")
                        
                        for i, element in enumerate(elements[:20]):
                            try:
                                text = element.text
                                if 'S$' in text and 'Beds' in text:
                                    prop = self._parse_element_text(text, i)
                                    if prop:
                                        properties.append(prop)
                            except:
                                continue
                        
                        if properties:
                            break
                except:
                    continue
            
        except Exception as e:
            print(f"❌ Element extraction error: {e}")
        
        return properties
    
    def _parse_element_text(self, text, index):
        """Parse property data from element text"""
        try:
            prop = {
                'id': f'property_{index}',
                'extraction_timestamp': datetime.now().isoformat(),
                'source': 'PropertyGuru'
            }
            
            # Extract price
            price_match = re.search(r'S\$\s*([\d,]+)', text)
            if price_match:
                prop['price'] = int(price_match.group(1).replace(',', ''))
            
            # Extract bedrooms
            bed_match = re.search(r'(\d+)\s+Beds?', text)
            if bed_match:
                prop['bedrooms'] = int(bed_match.group(1))
            
            # Extract area
            area_match = re.search(r'(\d+,?\d*)\s+sqft', text)
            if area_match:
                prop['area'] = int(area_match.group(1).replace(',', ''))
            
            return prop if self._is_valid_property(prop) else None
            
        except:
            return None
    
    def _is_valid_property(self, prop):
        """Check if property has minimum required data"""
        return 'price' in prop and 'bedrooms' in prop
    
    def save_properties(self, properties):
        """Save properties to JSON file"""
        if not properties:
            print("❌ No properties to save")
            return None

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save to data directory
        import os
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, f'extraction_{timestamp}.json')

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(properties, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved {len(properties)} properties to {filename}")
        return filename
    
    def scrape_multiple_pages(self, max_pages=10, start_page=1):
        """Scrape multiple pages with pagination"""
        all_properties = []
        current_page = start_page

        print(f"🔄 Starting multi-page scraping (max {max_pages} pages)")

        try:
            while current_page <= max_pages:
                print(f"\n📄 Scraping page {current_page}...")

                # Get current page info
                page_num, total_pages = self.get_current_page_info()
                if total_pages:
                    print(f"📊 Page {page_num} of {total_pages}")
                    if page_num > max_pages:
                        print(f"✅ Reached max pages limit ({max_pages})")
                        break

                # Extract properties from current page
                properties = self.extract_properties_smart()

                if properties:
                    print(f"✅ Extracted {len(properties)} properties from page {current_page}")
                    all_properties.extend(properties)
                else:
                    print(f"⚠️ No properties found on page {current_page}")

                # Check if we should continue
                if current_page >= max_pages:
                    print(f"✅ Reached maximum pages ({max_pages})")
                    break

                # Try to go to next page
                print("🔄 Moving to next page...")
                if not self.click_next_page():
                    print("❌ Could not navigate to next page - stopping")
                    break

                # Wait for page to load and verify change
                self.human_delay('page_load')

                # Verify page changed (PropertyGuru uses URL-based pagination)
                print("⏳ Verifying page navigation...")
                new_page_num, _ = self.get_current_page_info()

                if new_page_num > page_num:
                    print(f"✅ Page changed successfully: {page_num} → {new_page_num}")
                else:
                    print(f"⚠️ Page number didn't change as expected: {page_num} → {new_page_num}")
                    # Check if we hit the last page
                    if page_num >= 2600:  # Close to max pages
                        print("📄 Likely reached the last page")
                        break
                    else:
                        print("❌ Unexpected pagination issue")
                        break

                current_page += 1

                # Add extra delay between pages to be respectful
                self.human_delay('action_delay')

        except KeyboardInterrupt:
            print("\n⚠️ Scraping interrupted by user")
        except Exception as e:
            print(f"❌ Pagination error: {e}")

        return all_properties

    def close(self):
        """Close browser connection"""
        if self.driver:
            self.driver.quit()

def main():
    scraper = SmartPropertyScraper()

    try:
        # Connect and navigate
        if not scraper.connect_and_navigate():
            return

        # Handle Cloudflare and wait for page load
        scraper.handle_cloudflare_and_wait()

        # Ask user for scraping preference
        print("\n🎯 Scraping Options:")
        print("1. Single page (quick test)")
        print("2. Multiple pages (5 pages)")
        print("3. Extended scraping (50 pages)")
        print("4. Full scraping (all 2400+ pages)")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            # Single page extraction
            properties = scraper.extract_properties_smart()
        elif choice == "2":
            # 5 pages
            properties = scraper.scrape_multiple_pages(max_pages=5)
        elif choice == "3":
            # 50 pages
            properties = scraper.scrape_multiple_pages(max_pages=50)
        elif choice == "4":
            # All pages
            properties = scraper.scrape_multiple_pages(max_pages=2500)  # Safety limit
        else:
            print("Invalid choice, defaulting to single page")
            properties = scraper.extract_properties_smart()

        if properties:
            print(f"\n🎉 SUCCESS! Extracted {len(properties)} properties total")

            # Show sample
            print("\n📋 Sample Properties:")
            for i, prop in enumerate(properties[:5], 1):
                print(f"   {i}. {prop.get('name', 'Property')}")
                print(f"      Price: S$ {prop.get('price', 'N/A'):,}" if isinstance(prop.get('price'), int) else f"      Price: {prop.get('price', 'N/A')}")
                print(f"      Bedrooms: {prop.get('bedrooms', 'N/A')}")
                print(f"      Area: {prop.get('area', 'N/A')} sqft")

            # Save data
            filename = scraper.save_properties(properties)
            print(f"\n✅ Extraction complete! Data saved to: {filename}")

        else:
            print("❌ No properties extracted")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        scraper.close()

if __name__ == "__main__":
    main()
