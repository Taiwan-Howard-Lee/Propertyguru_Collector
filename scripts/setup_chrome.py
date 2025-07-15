#!/usr/bin/env python3
"""
🔧 Chrome Debug Setup Helper
Helps you enable Chrome remote debugging for PropertyGuru scraping
"""

import subprocess
import time
import requests
import json
import os

def kill_chrome():
    """Kill all Chrome processes"""
    try:
        subprocess.run(['pkill', '-f', 'Google Chrome'], check=False)
        print("🔄 Closing existing Chrome instances...")
        time.sleep(3)
    except Exception as e:
        print(f"ℹ️ Chrome processes: {e}")

def start_chrome_with_debug():
    """Start Chrome with remote debugging enabled (stealth mode)"""
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    if not os.path.exists(chrome_path):
        print("❌ Chrome not found at expected location")
        return False

    # Stealth Chrome setup - minimal flags to avoid detection and warnings
    cmd = [
        chrome_path,
        "--remote-debugging-port=9222",
        "--user-data-dir=/tmp/chrome_stealth_profile",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-blink-features=AutomationControlled"
    ]

    try:
        print("🚀 Starting Chrome with stealth debugging enabled...")
        print("🔒 Using minimal flags to avoid detection")
        subprocess.Popen(cmd)
        time.sleep(5)
        return True
    except Exception as e:
        print(f"❌ Failed to start Chrome: {e}")
        return False

def test_debug_connection():
    """Test if Chrome debugging is working"""
    try:
        response = requests.get('http://localhost:9222/json', timeout=5)
        tabs = response.json()
        print(f"✅ Chrome debugging active! Found {len(tabs)} tabs")
        return True
    except Exception as e:
        print(f"❌ Debug connection failed: {e}")
        return False

def open_propertyguru():
    """Open PropertyGuru in a new tab with comprehensive district coverage"""
    try:
        url = "https://www.propertyguru.com.sg/property-for-sale?freetext=D01+Boat+Quay+%2F+Raffles+Place+%2F+Marina%2C+D02+Chinatown+%2F+Tanjong+Pagar%2C+D03+Alexandra+%2F+Commonwealth%2C+D04+Harbourfront+%2F+Telok+Blangah%2C+D05+Buona+Vista+%2F+West+Coast+%2F+Clementi+New+Town%2C+D06+City+Hall+%2F+Clarke+Quay%2C+D07+Beach+Road+%2F+Bugis+%2F+Rochor%2C+D08+Farrer+Park+%2F+Serangoon+Rd%2C+D09+Orchard+%2F+River+Valley%2C+D10+Tanglin+%2F+Holland+%2F+Bukit+Timah%2C+D11+Newton+%2F+Novena%2C+D21+Clementi+Park+%2F+Upper+Bukit+Timah%2C+D12+Balestier+%2F+Toa+Payoh%2C+D13+Macpherson+%2F+Potong+Pasir%2C+D14+Eunos+%2F+Geylang+%2F+Paya+Lebar%2C+D15+East+Coast+%2F+Marine+Parade%2C+D16+Bedok+%2F+Upper+East+Coast%2C+D17+Changi+Airport+%2F+Changi+Village%2C+D18+Pasir+Ris+%2F+Tampines%2C+D19+Hougang+%2F+Punggol+%2F+Sengkang%2C+D20+Ang+Mo+Kio+%2F+Bishan+%2F+Thomson%2C+D22+Boon+Lay+%2F+Jurong+%2F+Tuas%2C+D23+Dairy+Farm+%2F+Bukit+Panjang+%2F+Choa+Chu+Kang%2C+D24+Lim+Chu+Kang+%2F+Tengah%2C+D25+Admiralty+%2F+Woodlands%2C+D26+Mandai+%2F+Upper+Thomson%2C+D27+Sembawang+%2F+Yishun%2C+D28+Seletar+%2F+Yio+Chu+Kang&districtCode=D01&districtCode=D02&districtCode=D03&districtCode=D04&districtCode=D05&districtCode=D06&districtCode=D07&districtCode=D08&districtCode=D09&districtCode=D10&districtCode=D11&districtCode=D21&districtCode=D12&districtCode=D13&districtCode=D14&districtCode=D15&districtCode=D16&districtCode=D17&districtCode=D18&districtCode=D19&districtCode=D20&districtCode=D22&districtCode=D23&districtCode=D24&districtCode=D25&districtCode=D26&districtCode=D27&districtCode=D28&isCommercial=false"
        response = requests.post(f'http://localhost:9222/json/new?{url}')
        print("🏠 Opening PropertyGuru with comprehensive district coverage...")
        print("🎯 All Singapore districts (D01-D28) included")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"❌ Failed to open PropertyGuru: {e}")
        return False

def main():
    print("🔧 Chrome Debug Setup Helper")
    print("=" * 50)
    
    # Step 1: Kill existing Chrome
    kill_chrome()
    
    # Step 2: Start Chrome with debugging
    if not start_chrome_with_debug():
        print("\n❌ Failed to start Chrome")
        print("💡 Try manually running:")
        print("/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222")
        return
    
    # Step 3: Test connection
    print("\n🔍 Testing debug connection...")
    for i in range(10):
        if test_debug_connection():
            break
        print(f"⏳ Waiting for Chrome... ({i+1}/10)")
        time.sleep(2)
    else:
        print("❌ Chrome debugging not responding")
        return
    
    # Step 4: Open PropertyGuru
    print("\n🏠 Opening PropertyGuru...")
    if open_propertyguru():
        print("\n✅ Setup complete!")
        print("🎯 Chrome is ready for scraping")
        print("🔗 Debug URL: http://localhost:9222")
    else:
        print("❌ Failed to open PropertyGuru")

if __name__ == "__main__":
    main()
