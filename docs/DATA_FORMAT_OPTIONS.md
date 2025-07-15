# 📊 PropertyGuru Data Format Options

## 🎯 Overview
The PropertyGuru scraper now offers two distinct data collection formats to meet different research and business needs.

## 📋 Format Options

### 1. 🧠 **Intelligent Sales Format**
**Perfect for: Property agents, sales teams, market analysis**

**Features:**
- ✅ Market analysis and insights
- ✅ Investment recommendations  
- ✅ Buyer targeting suggestions
- ✅ Sales-ready descriptions
- ✅ Marketing strategies
- ✅ Competitive advantages

**Sample Output:**
```json
{
  "title": "82 Commonwealth Close",
  "price": "S$ 400,000",
  "market_segment": "Entry Level",
  "target_buyers": "Young professionals, first-time buyers",
  "transport": "Great connectivity - Commonwealth MRT Station 5 min walk",
  "investment_outlook": "High rental yield potential",
  "marketing_strategy": "Emphasize affordability and growth potential",
  "rental_estimate": "S$ 1,333/month"
}
```

### 2. 📊 **Pure Data Format**
**Perfect for: Researchers, data analysts, custom analysis**

**Features:**
- ✅ Raw data collection only
- ✅ Simple categorization
- ✅ No market analysis or opinions
- ✅ Clean structured data
- ✅ Perfect for custom research

**Sample Output:**
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
  "size_category": "500-800 sqft"
}
```

## 🚀 How to Use

### **Main Scraper (Choose Format)**
```bash
python main.py

# You'll be prompted to choose:
# 1. Intelligent Sales Format
# 2. Pure Data Format
```

### **Direct Access**

**Intelligent Sales Format:**
```bash
python src/scrapers/intelligent_scraper.py
```

**Pure Data Format:**
```bash
python src/scrapers/pure_data_scraper.py
```

## 📊 Data Categories (Pure Format)

### **Price Ranges**
- Under 500K
- 500K-800K  
- 800K-1.2M
- 1.2M-2M
- 2M-3M
- 3M-5M
- Above 5M

### **PSF Ranges**
- Under 600
- 600-1000
- 1000-1500
- 1500-2000
- Above 2000

### **MRT Distance Categories**
- 0-5 min
- 6-10 min
- 11-15 min
- Above 15 min

### **Property Age Categories**
- 0-5 years
- 5-15 years
- 15-30 years
- Above 30 years

### **Size Categories**
- Under 500 sqft
- 500-800 sqft
- 800-1200 sqft
- 1200-1800 sqft
- Above 1800 sqft

### **Image Categories**
- 1-2 images
- 3-7 images
- 8-14 images
- 15+ images

## 🎯 Use Cases

### **Intelligent Sales Format**
- **Property Agents**: Instant property summaries and buyer targeting
- **Sales Teams**: Ready-to-use marketing descriptions
- **Market Analysis**: Investment insights and trend analysis
- **CRM Integration**: Structured, actionable sales data
- **Lead Qualification**: Precise buyer-property matching

### **Pure Data Format**
- **Academic Research**: Clean data for statistical analysis
- **Custom Analytics**: Build your own analysis models
- **Data Science**: Machine learning and predictive modeling
- **Market Research**: Unbiased data collection
- **Comparative Studies**: Raw data for objective comparison

## 📁 Output Locations

### **Intelligent Sales Format**
- `data/processed/intelligent_*.json`
- Ready for immediate use by sales teams

### **Pure Data Format**  
- `data/processed/pure_data_*.json`
- Ready for custom analysis and research

## ✅ Quality Assurance

### **Both Formats Include:**
- ✅ 100% field completion (or field removal)
- ✅ Clean, structured data
- ✅ Consistent formatting
- ✅ Comprehensive property coverage
- ✅ Reliable categorization

### **Key Differences:**
- **Intelligent**: Includes analysis, insights, recommendations
- **Pure**: Raw data only, no opinions or analysis

## 🎉 Perfect for Your Needs

**Choose Intelligent Sales Format if you want:**
- Ready-to-use sales data
- Market insights and analysis
- Investment recommendations
- Buyer targeting suggestions

**Choose Pure Data Format if you want:**
- Raw data for custom analysis
- No market opinions or bias
- Clean categorized data
- Research-ready format

---

*Both formats provide complete Singapore property market coverage with professional-grade data quality.*
