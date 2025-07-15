# 🎯 Manual Chrome Setup Guide

## ✨ **New Feature: Manual Chrome Tab Selection**

You can now manually select which Chrome tab to use for scraping! This gives you full control over the browser setup.

## 🚀 **How It Works**

### **Step 1: Start Chrome with Debugging** 
Open Chrome manually with debugging enabled:

#### **macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

#### **Linux:**
```bash
google-chrome --remote-debugging-port=9222
```

#### **Windows:**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

### **Step 2: Open Your Tabs**
- Navigate to PropertyGuru: `https://www.propertyguru.com.sg/property-for-sale`
- Open any other tabs you want
- Keep Chrome running

### **Step 3: Run Manual Tab Selector**
```bash
python3 tools/manual_chrome_selector.py
```

**Or use the interactive launcher:**
```bash
python3 run.py
# Choose option 2: Select Chrome Tab (manual)
```

## 📋 **Example Output**

```
🔍 Manual Chrome Tab Selector
==================================================
This tool helps you select which Chrome tab to use for scraping

🔍 Scanning for Chrome instances with debugging enabled...
✅ Found Chrome instance on port 9222 with 4 tabs

📋 Available Chrome Tabs:
================================================================================

🌐 Chrome Instance (Port 9222):
--------------------------------------------------

   1. 🎯 PropertyGuru | Properties for Sale in Singapore - PropertyGuru
       URL: https://www.propertyguru.com.sg/property-for-sale
       Type: page

   2. 🔍 Google | Google Search
       URL: https://www.google.com/search?q=singapore+property
       Type: page

   3. ⚙️ Chrome | New Tab
       URL: chrome://newtab/
       Type: page

   4. 🌐 Website | GitHub - PropertyGuru Scraper
       URL: https://github.com/user/propertyguru-scraper
       Type: page

🎯 Select a tab to use for scraping:
   • PropertyGuru tabs are recommended
   • You can also select any tab and navigate to PropertyGuru

Enter tab number (1-4) or 'q' to quit: 1

✅ Selected Tab 1:
   Title: Properties for Sale in Singapore - PropertyGuru
   URL: https://www.propertyguru.com.sg/property-for-sale
   Port: 9222

🔧 Testing connection to selected tab...
✅ Connection successful!
   Current URL: https://www.propertyguru.com.sg/property-for-sale
   Current Title: Properties for Sale in Singapore - PropertyGuru

💾 Connection info saved to chrome_connection.json

🎉 Setup complete!
You can now run the scraper with:
   python3 scraper/main_scraper.py
   python3 tools/run_all.py
```

## 🎯 **Benefits of Manual Selection**

### **1. Full Control** 🎮
- Choose exactly which tab to use
- See all available Chrome instances
- Switch between different browser sessions

### **2. Multiple Chrome Instances** 🌐
- Supports multiple Chrome instances on different ports
- Automatically detects ports 9222, 9223, 9224, 9225
- Choose from any running instance

### **3. Flexibility** ⚡
- Use existing tabs (no need to open new ones)
- Navigate to PropertyGuru in your preferred way
- Keep your browsing session intact

### **4. Visual Feedback** 👁️
- See tab titles and URLs before selecting
- Color-coded tab types (PropertyGuru, Google, Chrome, etc.)
- Connection testing before proceeding

## 🔧 **Advanced Usage**

### **Multiple Chrome Instances**
You can run multiple Chrome instances on different ports:

```bash
# Instance 1
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome1

# Instance 2  
google-chrome --remote-debugging-port=9223 --user-data-dir=/tmp/chrome2
```

The selector will detect all instances and let you choose.

### **Persistent Connection**
Once you select a tab, the connection info is saved to `chrome_connection.json`. The scraper will automatically use this connection until you select a different tab.

### **Connection File Format**
```json
{
  "port": 9222,
  "tab_id": "E4F8B7A2-1234-5678-9ABC-DEF012345678",
  "debugger_url": "ws://localhost:9222/devtools/page/E4F8B7A2...",
  "selected_at": "2025-07-12 22:30:15",
  "tab_title": "Properties for Sale in Singapore - PropertyGuru",
  "tab_url": "https://www.propertyguru.com.sg/property-for-sale"
}
```

## 🆚 **Manual vs Automatic Setup**

### **Manual Setup (NEW!)** 🎯
```bash
# 1. Start Chrome manually
google-chrome --remote-debugging-port=9222

# 2. Navigate to PropertyGuru in browser
# 3. Select tab via CLI
python3 tools/manual_chrome_selector.py

# 4. Run scraper
python3 scraper/main_scraper.py
```

**Pros:**
- ✅ Full control over browser and tabs
- ✅ Use existing browsing session
- ✅ Visual tab selection
- ✅ Support multiple Chrome instances

### **Automatic Setup** 🔧
```bash
# 1. Run automatic setup
python3 tools/setup_chrome.py

# 2. Run scraper
python3 scraper/main_scraper.py
```

**Pros:**
- ✅ Quick and simple
- ✅ No manual intervention needed
- ✅ Good for automation

## 🎯 **Recommended Workflow**

### **For Interactive Use (Recommended):**
1. **Start Chrome manually** with debugging
2. **Navigate to PropertyGuru** in your browser
3. **Use manual tab selector** to choose the tab
4. **Run scraper** - it will use your selected tab

### **For Automation:**
1. **Use automatic setup** for hands-off operation
2. **Run scraper** - it handles everything automatically

## 🔍 **Troubleshooting**

### **No Chrome Instances Found**
```
❌ No Chrome instances found with debugging enabled

💡 To enable Chrome debugging, start Chrome with:
   Chrome --remote-debugging-port=9222
   Or use our setup tool: python3 tools/setup_chrome.py
```

**Solution:** Start Chrome with debugging enabled using the commands above.

### **Connection Test Failed**
```
❌ Connection test failed: Connection refused
```

**Solution:** 
- Make sure Chrome is still running
- Check that the tab hasn't been closed
- Try selecting a different tab

### **Tab Closed After Selection**
If you close the selected tab, the scraper will automatically fall back to:
1. Try automatic Chrome detection (port 9222)
2. Start undetected Chrome as final fallback

## 🎉 **Summary**

The manual Chrome tab selector gives you:
- **🎮 Full control** over browser setup
- **👁️ Visual tab selection** with clear information
- **🌐 Multiple instance support** for advanced users
- **⚡ Flexible workflow** that adapts to your needs
- **🔄 Automatic fallback** if manual connection fails

Choose the method that works best for your workflow! 🚀
