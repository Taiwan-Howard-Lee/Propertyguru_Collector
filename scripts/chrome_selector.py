#!/usr/bin/env python3
"""
🔍 Manual Chrome Tab Selector
Detects existing Chrome instances and lets you select which tab to use
"""

import json
import requests
import time
from urllib.parse import urlparse

class ChromeTabSelector:
    def __init__(self):
        self.debug_ports = [9222, 9223, 9224, 9225]  # Common debug ports
        self.active_instances = []
        
    def detect_chrome_instances(self):
        """Detect all running Chrome instances with debugging enabled"""
        print("🔍 Scanning for Chrome instances with debugging enabled...")
        
        instances = []
        for port in self.debug_ports:
            try:
                response = requests.get(f"http://localhost:{port}/json", timeout=2)
                if response.status_code == 200:
                    tabs = response.json()
                    if tabs:
                        instances.append({
                            'port': port,
                            'tabs': tabs,
                            'count': len(tabs)
                        })
                        print(f"✅ Found Chrome instance on port {port} with {len(tabs)} tabs")
            except:
                continue
        
        if not instances:
            print("❌ No Chrome instances found with debugging enabled")
            print("\n💡 To enable Chrome debugging, start Chrome with:")
            print("   Chrome --remote-debugging-port=9222")
            print("   Or use our setup tool: python3 tools/setup_chrome.py")
            return []
        
        return instances
    
    def display_tabs(self, instances):
        """Display all available tabs in a user-friendly format"""
        print("\n📋 Available Chrome Tabs:")
        print("=" * 80)
        
        tab_index = 1
        tab_map = {}
        
        for instance in instances:
            port = instance['port']
            print(f"\n🌐 Chrome Instance (Port {port}):")
            print("-" * 50)
            
            for tab in instance['tabs']:
                title = tab.get('title', 'No Title')
                url = tab.get('url', 'No URL')
                tab_type = tab.get('type', 'unknown')
                
                # Truncate long titles and URLs for display
                display_title = title[:60] + "..." if len(title) > 60 else title
                display_url = url[:70] + "..." if len(url) > 70 else url
                
                # Color coding for different sites
                if 'propertyguru' in url.lower():
                    status = "🎯 PropertyGuru"
                elif 'google' in url.lower():
                    status = "🔍 Google"
                elif url.startswith('chrome://'):
                    status = "⚙️ Chrome"
                elif url.startswith('chrome-extension://'):
                    status = "🧩 Extension"
                else:
                    status = "🌐 Website"
                
                print(f"   {tab_index:2d}. {status} | {display_title}")
                print(f"       URL: {display_url}")
                print(f"       Type: {tab_type}")
                print()
                
                tab_map[tab_index] = {
                    'port': port,
                    'tab': tab,
                    'webSocketDebuggerUrl': tab.get('webSocketDebuggerUrl'),
                    'id': tab.get('id')
                }
                tab_index += 1
        
        return tab_map
    
    def select_tab(self, tab_map):
        """Let user select which tab to use"""
        if not tab_map:
            return None
        
        print("🎯 Select a tab to use for scraping:")
        print("   • PropertyGuru tabs are recommended")
        print("   • You can also select any tab and navigate to PropertyGuru")
        print()
        
        while True:
            try:
                choice = input(f"Enter tab number (1-{len(tab_map)}) or 'q' to quit: ").strip()
                
                if choice.lower() == 'q':
                    print("👋 Goodbye!")
                    return None
                
                tab_num = int(choice)
                if tab_num in tab_map:
                    selected = tab_map[tab_num]
                    tab = selected['tab']
                    
                    print(f"\n✅ Selected Tab {tab_num}:")
                    print(f"   Title: {tab.get('title', 'No Title')}")
                    print(f"   URL: {tab.get('url', 'No URL')}")
                    print(f"   Port: {selected['port']}")
                    
                    return selected
                else:
                    print(f"❌ Invalid choice. Please enter a number between 1 and {len(tab_map)}")
                    
            except ValueError:
                print("❌ Invalid input. Please enter a number or 'q' to quit")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return None
    
    def test_connection(self, selected_tab):
        """Test connection to the selected tab"""
        print(f"\n🔧 Testing connection to selected tab...")
        
        port = selected_tab['port']
        tab_id = selected_tab['id']
        
        try:
            # Test basic connection
            response = requests.get(f"http://localhost:{port}/json/{tab_id}", timeout=5)
            if response.status_code == 200:
                tab_info = response.json()
                print(f"✅ Connection successful!")
                print(f"   Current URL: {tab_info.get('url', 'Unknown')}")
                print(f"   Current Title: {tab_info.get('title', 'Unknown')}")
                return True
            else:
                print(f"❌ Connection failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def save_connection_info(self, selected_tab):
        """Save connection info for the scraper to use"""
        connection_info = {
            'port': selected_tab['port'],
            'tab_id': selected_tab['id'],
            'debugger_url': selected_tab.get('webSocketDebuggerUrl'),
            'selected_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'tab_title': selected_tab['tab'].get('title', 'Unknown'),
            'tab_url': selected_tab['tab'].get('url', 'Unknown')
        }
        
        # Save to a file that the scraper can read
        with open('chrome_connection.json', 'w') as f:
            json.dump(connection_info, f, indent=2)
        
        print(f"💾 Connection info saved to chrome_connection.json")
        return connection_info
    
    def run(self):
        """Main function to run the tab selector"""
        print("🔍 Manual Chrome Tab Selector")
        print("=" * 50)
        print("This tool helps you select which Chrome tab to use for scraping")
        print()
        
        # Detect Chrome instances
        instances = self.detect_chrome_instances()
        if not instances:
            return None
        
        # Display available tabs
        tab_map = self.display_tabs(instances)
        if not tab_map:
            print("❌ No tabs found")
            return None
        
        # Let user select a tab
        selected_tab = self.select_tab(tab_map)
        if not selected_tab:
            return None
        
        # Test connection
        if not self.test_connection(selected_tab):
            print("❌ Connection test failed. Please try another tab.")
            return None
        
        # Save connection info
        connection_info = self.save_connection_info(selected_tab)
        
        print(f"\n🎉 Setup complete!")
        print(f"You can now run the scraper with:")
        print(f"   python3 scraper/main_scraper.py")
        print(f"   python3 tools/run_all.py")
        
        return connection_info

def main():
    selector = ChromeTabSelector()
    return selector.run()

if __name__ == "__main__":
    main()
