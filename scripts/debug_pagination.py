#!/usr/bin/env python3
"""
🔍 Debug PropertyGuru Pagination System
Analyze how PropertyGuru's pagination actually works
"""

import sys
import os
import time
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'scraper'))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def debug_pagination():
    """Debug PropertyGuru's pagination mechanism"""
    print("🔍 DEBUGGING PROPERTYGURU PAGINATION")
    print("=" * 60)
    
    try:
        # Connect to existing Chrome
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        
        print("✅ Connected to Chrome")
        print(f"📄 Current URL: {driver.current_url}")
        
        # 1. Analyze current page structure
        print("\n🔍 ANALYZING CURRENT PAGE STRUCTURE:")
        
        # Check pagination container
        try:
            pagination = driver.find_element(By.CSS_SELECTOR, '.hui-pagination, .pagination')
            print(f"✅ Found pagination container: {pagination.tag_name}")
            print(f"   Classes: {pagination.get_attribute('class')}")
            print(f"   Text: {pagination.text[:200]}...")
        except:
            print("❌ No pagination container found")
        
        # Check current page indicator
        try:
            current_page_elements = driver.find_elements(By.CSS_SELECTOR, '.page-item.active .page-link, .active .page-link')
            if current_page_elements:
                current_text = current_page_elements[0].text.strip()
                print(f"✅ Current page indicator: '{current_text}'")
            else:
                print("❌ No current page indicator found")
        except Exception as e:
            print(f"❌ Error finding current page: {e}")
        
        # Check next button
        try:
            next_buttons = driver.find_elements(By.CSS_SELECTOR, 'a.page-link')
            next_button = None
            for btn in next_buttons:
                if 'next' in btn.text.lower():
                    next_button = btn
                    break
            
            if next_button:
                print(f"✅ Found Next button: '{next_button.text.strip()}'")
                print(f"   Tag: {next_button.tag_name}")
                print(f"   Classes: {next_button.get_attribute('class')}")
                print(f"   Href: {next_button.get_attribute('href')}")
                print(f"   Enabled: {next_button.is_enabled()}")
                print(f"   Displayed: {next_button.is_displayed()}")
            else:
                print("❌ No Next button found")
        except Exception as e:
            print(f"❌ Error finding next button: {e}")
        
        # 2. Get initial property signatures
        print("\n📊 GETTING INITIAL PROPERTY SIGNATURES:")
        initial_properties = get_property_signatures(driver)
        print(f"✅ Found {len(initial_properties)} property signatures")
        for i, prop in enumerate(initial_properties[:3]):
            print(f"   {i+1}. {prop}")
        
        # 3. Test clicking Next button
        print("\n🔄 TESTING NEXT BUTTON CLICK:")
        
        if next_button:
            # Get initial URL and content hash
            initial_url = driver.current_url
            initial_content_hash = hash(driver.page_source)
            
            print(f"📍 Initial URL: {initial_url}")
            print(f"📍 Initial content hash: {initial_content_hash}")
            
            # Click next button
            print("🖱️ Clicking Next button...")
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)
                next_button.click()
                print("✅ Next button clicked")
                
                # Monitor changes
                print("\n⏳ Monitoring changes for 15 seconds...")
                for i in range(15):
                    time.sleep(1)
                    
                    # Check URL change
                    current_url = driver.current_url
                    url_changed = current_url != initial_url
                    
                    # Check content change
                    current_content_hash = hash(driver.page_source)
                    content_changed = current_content_hash != initial_content_hash
                    
                    # Check page number
                    try:
                        current_page_elements = driver.find_elements(By.CSS_SELECTOR, '.page-item.active .page-link, .active .page-link')
                        if current_page_elements:
                            current_page_text = current_page_elements[0].text.strip()
                        else:
                            current_page_text = "Unknown"
                    except:
                        current_page_text = "Error"
                    
                    # Check property signatures
                    current_properties = get_property_signatures(driver)
                    properties_changed = current_properties != initial_properties
                    
                    print(f"   {i+1:2d}s: URL={url_changed}, Content={content_changed}, Page='{current_page_text}', Props={properties_changed} ({len(current_properties)} found)")
                    
                    if properties_changed and len(current_properties) > 0:
                        print(f"🎉 SUCCESS! Properties changed after {i+1} seconds")
                        print("📊 New property signatures:")
                        for j, prop in enumerate(current_properties[:3]):
                            print(f"     {j+1}. {prop}")
                        break
                else:
                    print("⚠️ No property changes detected after 15 seconds")
                
            except Exception as e:
                print(f"❌ Error clicking next button: {e}")
        
        # 4. Analyze pagination URLs
        print("\n🔗 ANALYZING PAGINATION URLS:")
        try:
            page_links = driver.find_elements(By.CSS_SELECTOR, '.hui-pagination a.page-link, .pagination a.page-link')
            for i, link in enumerate(page_links[:10]):
                href = link.get_attribute('href')
                text = link.text.strip()
                if href and text:
                    print(f"   {text}: {href}")
        except Exception as e:
            print(f"❌ Error analyzing URLs: {e}")
        
        # 5. Check for AJAX indicators
        print("\n🔄 CHECKING FOR AJAX INDICATORS:")
        
        # Look for loading indicators
        loading_selectors = [
            '.loading', '.spinner', '.loader', 
            '[class*="loading"]', '[class*="spinner"]',
            '[data-testid*="loading"]', '[data-testid*="spinner"]'
        ]
        
        for selector in loading_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found loading indicator: {selector} ({len(elements)} elements)")
            except:
                continue
        
        # Check for JavaScript frameworks
        js_frameworks = [
            'window.React', 'window.Vue', 'window.Angular',
            'window.__NEXT_DATA__', 'window.__INITIAL_STATE__'
        ]
        
        for framework in js_frameworks:
            try:
                result = driver.execute_script(f"return typeof {framework} !== 'undefined';")
                if result:
                    print(f"✅ Found JS framework: {framework}")
            except:
                continue
        
        print("\n📋 PAGINATION DEBUG COMPLETE")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

def get_property_signatures(driver):
    """Get unique signatures of properties on current page"""
    signatures = []
    try:
        # Look for property elements
        property_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="listing"]:has(img)')
        
        for element in property_elements:
            try:
                text = element.text.strip()
                if len(text) > 100:  # Substantial content
                    # Create signature from first few lines
                    lines = text.split('\n')[:3]
                    signature = ' | '.join(lines).strip()[:100]
                    if signature and signature not in signatures:
                        signatures.append(signature)
            except:
                continue
                
    except Exception as e:
        print(f"⚠️ Error getting property signatures: {e}")
    
    return signatures

if __name__ == "__main__":
    debug_pagination()
