# 📊 PropertyGuru Pure Data Scraper

## 🎯 Overview
This codebase has been updated to collect **PURE DATA ONLY** with no market analysis, segmentation, or investment insights. Perfect for researchers, data analysts, and custom analysis projects.

## ✅ What This Version Does

### 📊 **Pure Data Collection**
- ✅ Raw property data extraction
- ✅ Simple categorization (price ranges, size ranges, etc.)
- ✅ Clean structured JSON output
- ✅ Complete Singapore property coverage

### 🚫 **What This Version Does NOT Do**
- ❌ NO market analysis or segmentation
- ❌ NO investment recommendations
- ❌ NO buyer targeting suggestions
- ❌ NO marketing strategies
- ❌ NO market insights or opinions

## 📁 **Simplified Structure**

```
PropertyGuru_Pure_Data_Scraper/
├── 📊 main.py                          # Pure data scraper entry point
├── 📋 requirements.txt                 # Minimal dependencies
├── 📁 src/
│   ├── 🤖 scrapers/
│   │   ├── pure_data_scraper.py        # Main pure data scraper
│   │   └── main_scraper.py             # Core scraper engine
│   ├── 📊 schemas/
│   │   └── pure_data_schema.py         # Pure data schema only
│   └── 🔍 extractors/
│       └── advanced_extractor.py       # Property data extractor
├── 📊 data/                            # Pure data files only
│   ├── pure_data_YYYYMMDD_HHMMSS.json  # Raw data files
│   └── ...
├── 🧪 tests/
│   └── test_pure_data_scraping.py      # Pure data tests
├── 📜 scripts/                         # Chrome setup scripts
├── ⚙️ config/                          # Pure data configuration
└── 📝 docs/                            # Documentation
```

## 🚀 **How to Use**

### **Main Scraper**
```bash
python main.py

# You'll be prompted for:
# - Number of pages to collect
# - Starting page number
# - Confirmation to start
```

### **Test Scraper**
```bash
python tests/test_pure_data_scraping.py
```

## 📊 **Pure Data Format**

### **Sample Output**
```json
{
  "property_name": "82 Commonwealth Close",
  "price_numeric": 400000,
  "price_formatted": "S$ 400,000",
  "bedrooms": 2,
  "bathrooms": 2,
  "floor_area_sqft": 603,
  "property_type": "HDB Flat",
  "price_range": "Under 500K",
  "psf_range": "600-1000",
  "district_code": "D03",
  "mrt_station": "Commonwealth MRT Station",
  "mrt_distance_category": "0-5 min",
  "mrt_line_name": "East West Line",
  "property_age_years": 61,
  "age_category": "Above 30 years",
  "size_category": "500-800 sqft",
  "agent_name": "Ajay Nair",
  "listed_date": "Jul 13, 2025",
  "image_count": 15,
  "extraction_timestamp": "2025-07-13T18:31:24.448640",
  "data_source": "PropertyGuru"
}
```

### **Data Categories (Simple Ranges)**

**💰 Price Ranges:**
- Under 500K
- 500K-800K
- 800K-1.2M
- 1.2M-2M
- 2M-3M
- 3M-5M
- Above 5M

**📏 PSF Ranges:**
- Under 600
- 600-1000
- 1000-1500
- 1500-2000
- Above 2000

**🚇 MRT Distance:**
- 0-5 min
- 6-10 min
- 11-15 min
- Above 15 min

**🏠 Property Age:**
- 0-5 years
- 5-15 years
- 15-30 years
- Above 30 years

**📐 Size Categories:**
- Under 500 sqft
- 500-800 sqft
- 800-1200 sqft
- 1200-1800 sqft
- Above 1800 sqft

## 🎯 **Perfect For**

### **Academic Research**
- Clean, unbiased data for statistical analysis
- No market opinions to influence research
- Consistent categorization for comparison studies

### **Data Science Projects**
- Raw data for machine learning models
- Custom analysis and visualization
- Predictive modeling with clean inputs

### **Market Research**
- Objective property data collection
- Custom segmentation based on your criteria
- Comparative analysis across districts/types

### **Custom Analytics**
- Build your own analysis frameworks
- Create custom insights and reports
- Develop proprietary market models

## ⚙️ **Configuration**

The `config/scraper_config.json` is set for pure data:
```json
{
  "schema": {
    "version": "pure_data_v1.0",
    "type": "raw_data_only",
    "no_analysis": true
  }
}
```

## 📊 **Data Quality**

### **What You Get:**
- ✅ 100% raw property data
- ✅ Simple, consistent categorization
- ✅ Clean JSON format
- ✅ Complete field information
- ✅ Timestamp and source tracking

### **What You Don't Get:**
- ❌ Market analysis or opinions
- ❌ Investment recommendations
- ❌ Buyer targeting suggestions
- ❌ Marketing strategies
- ❌ Market segmentation analysis

## 🎉 **Ready for Production**

This pure data version is:
- **🔬 Research-Ready**: Perfect for academic and commercial research
- **📊 Analysis-Friendly**: Clean data for custom analysis
- **🚫 Bias-Free**: No market opinions or analysis
- **⚡ Efficient**: Streamlined for data collection only
- **🎯 Focused**: Does one thing very well - collect raw data

---

**Perfect for researchers, data analysts, and anyone who wants raw property data without market analysis!** 📊

*Version: Pure Data v1.0*  
*Last Updated: July 13, 2025*
