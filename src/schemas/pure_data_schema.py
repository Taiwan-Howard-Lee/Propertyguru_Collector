#!/usr/bin/env python3
"""
📊 Pure Data Collection Schema
Raw data collection without any market analysis or segmentation
"""

from datetime import datetime
from typing import Dict, Any, Optional

class PureDataSchema:
    """Pure data collection schema - no analysis, just clean categorized data"""
    
    @staticmethod
    def create_property_record(technical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create clean property record with pure data only"""
        
        # Extract basic data
        name = technical_data.get("property_name", "").strip()
        price_num = technical_data.get("price")
        price_formatted = technical_data.get("price_formatted", "")
        psf_num = technical_data.get("price_per_sqft")
        psf_formatted = technical_data.get("price_per_sqft_formatted", "")
        bedrooms = technical_data.get("bedrooms")
        bathrooms = technical_data.get("bathrooms")
        size_sqft = technical_data.get("floor_area_sqft")
        property_type = technical_data.get("property_type", "")
        tenure = technical_data.get("tenure", "")
        built_year = technical_data.get("built_year")
        mrt_station = technical_data.get("mrt_station", "")
        mrt_distance = technical_data.get("mrt_distance", "")
        mrt_line = technical_data.get("mrt_line", "")
        agent_name = technical_data.get("agent_name", "")
        listed_date = technical_data.get("listed_date", "")
        image_count = technical_data.get("image_count", 0)
        main_image = technical_data.get("main_image_url", "")
        listing_url = technical_data.get("listing_url", "")
        
        # Skip properties with insufficient data
        if not name or not price_num or not bedrooms:
            return None
        
        # Build pure data record
        property_record = {}
        
        # 🏠 BASIC PROPERTY DATA
        property_record["property_name"] = name
        property_record["price_numeric"] = price_num
        if price_formatted:
            property_record["price_formatted"] = price_formatted
        elif price_num and isinstance(price_num, (int, float)):
            property_record["price_formatted"] = f"S$ {price_num:,.0f}"
        else:
            property_record["price_formatted"] = "Price on request"
        property_record["bedrooms"] = bedrooms
        property_record["bathrooms"] = bathrooms if bathrooms else bedrooms
        property_record["floor_area_sqft"] = size_sqft
        property_record["property_type"] = property_type

        # 🔗 PROPERTY LINK
        if listing_url:
            property_record["property_url"] = listing_url
        
        # 💰 PRICE CATEGORIES (simple ranges, no analysis)
        if price_num < 500000:
            property_record["price_range"] = "Under 500K"
        elif price_num < 800000:
            property_record["price_range"] = "500K-800K"
        elif price_num < 1200000:
            property_record["price_range"] = "800K-1.2M"
        elif price_num < 2000000:
            property_record["price_range"] = "1.2M-2M"
        elif price_num < 3000000:
            property_record["price_range"] = "2M-3M"
        elif price_num < 5000000:
            property_record["price_range"] = "3M-5M"
        else:
            property_record["price_range"] = "Above 5M"
        
        # PSF data
        if psf_num:
            property_record["price_per_sqft_numeric"] = psf_num
            property_record["price_per_sqft_formatted"] = psf_formatted if psf_formatted else f"S$ {psf_num:,.0f} psf"
            
            # Simple PSF ranges
            if psf_num < 600:
                property_record["psf_range"] = "Under 600"
            elif psf_num < 1000:
                property_record["psf_range"] = "600-1000"
            elif psf_num < 1500:
                property_record["psf_range"] = "1000-1500"
            elif psf_num < 2000:
                property_record["psf_range"] = "1500-2000"
            else:
                property_record["psf_range"] = "Above 2000"
        
        # 📍 LOCATION DATA
        district = PureDataSchema._extract_district(name, mrt_station)
        if district:
            property_record["district_code"] = district
        
        # MRT data
        if mrt_station and mrt_distance:
            property_record["mrt_station"] = mrt_station
            property_record["mrt_distance_text"] = mrt_distance
            
            # Extract walking time
            walk_time = None
            if "min" in mrt_distance:
                try:
                    import re
                    walk_time = int(re.search(r'(\d+)', mrt_distance).group(1))
                    property_record["mrt_walk_minutes"] = walk_time
                    
                    # Simple time categories
                    if walk_time <= 5:
                        property_record["mrt_distance_category"] = "0-5 min"
                    elif walk_time <= 10:
                        property_record["mrt_distance_category"] = "6-10 min"
                    elif walk_time <= 15:
                        property_record["mrt_distance_category"] = "11-15 min"
                    else:
                        property_record["mrt_distance_category"] = "Above 15 min"
                except:
                    pass
            
            # MRT line
            if mrt_line:
                property_record["mrt_line_code"] = mrt_line
                line_code = mrt_line[:2]
                line_names = {
                    "EW": "East West Line", "NS": "North South Line", "NE": "North East Line",
                    "CC": "Circle Line", "DT": "Downtown Line", "TE": "Thomson-East Coast Line",
                    "BP": "Bukit Panjang LRT", "SK": "Sengkang LRT", "PG": "Punggol LRT"
                }
                property_record["mrt_line_name"] = line_names.get(line_code, "MRT")
        
        # 🏢 PROPERTY DETAILS
        if built_year:
            property_record["built_year"] = built_year
            current_year = datetime.now().year
            age = current_year - built_year
            property_record["property_age_years"] = age
            
            # Simple age categories
            if age < 5:
                property_record["age_category"] = "0-5 years"
            elif age < 15:
                property_record["age_category"] = "5-15 years"
            elif age < 30:
                property_record["age_category"] = "15-30 years"
            else:
                property_record["age_category"] = "Above 30 years"
        
        if tenure:
            property_record["tenure"] = tenure
        
        # Size categories
        if size_sqft:
            if size_sqft < 500:
                property_record["size_category"] = "Under 500 sqft"
            elif size_sqft < 800:
                property_record["size_category"] = "500-800 sqft"
            elif size_sqft < 1200:
                property_record["size_category"] = "800-1200 sqft"
            elif size_sqft < 1800:
                property_record["size_category"] = "1200-1800 sqft"
            else:
                property_record["size_category"] = "Above 1800 sqft"
        
        # 👤 LISTING DATA
        if agent_name:
            property_record["agent_name"] = agent_name
        
        if listed_date:
            property_record["listed_date"] = listed_date
        
        # 📸 MEDIA DATA
        if image_count:
            property_record["image_count"] = image_count
            
            # Simple image categories
            if image_count >= 15:
                property_record["image_category"] = "15+ images"
            elif image_count >= 8:
                property_record["image_category"] = "8-14 images"
            elif image_count >= 3:
                property_record["image_category"] = "3-7 images"
            else:
                property_record["image_category"] = "1-2 images"
        
        if main_image:
            property_record["main_image_url"] = main_image
        
        # 📋 METADATA
        property_record["extraction_timestamp"] = datetime.now().isoformat()
        property_record["data_source"] = "PropertyGuru"
        
        return property_record
    
    @staticmethod
    def _extract_district(name: str, mrt_station: str) -> str:
        """Extract district code from property name or MRT station"""
        # Common area to district mapping
        area_districts = {
            "commonwealth": "D03", "alexandra": "D03", "toa payoh": "D12",
            "choa chu kang": "D23", "hougang": "D19", "punggol": "D19",
            "sengkang": "D19", "bishan": "D20", "ang mo kio": "D20",
            "orchard": "D09", "newton": "D11", "novena": "D11",
            "marina": "D01", "raffles": "D01", "chinatown": "D02",
            "tanjong pagar": "D02", "harbourfront": "D04", "telok blangah": "D04",
            "buona vista": "D05", "west coast": "D05", "clementi": "D05",
            "tanglin": "D10", "holland": "D10", "bukit timah": "D10",
            "east coast": "D15", "marine parade": "D15", "bedok": "D16",
            "tampines": "D18", "pasir ris": "D18", "woodlands": "D25",
            "admiralty": "D25", "sembawang": "D27", "yishun": "D27",
            "jurong": "D22", "boon lay": "D22", "tuas": "D22"
        }
        
        text_to_search = f"{name} {mrt_station}".lower()
        
        for area, district in area_districts.items():
            if area in text_to_search:
                return district
        
        return None

def convert_to_pure_data_format(input_file: str, output_file: str = None):
    """Convert technical data to pure data format"""
    import json
    
    print("📊 CONVERTING TO PURE DATA FORMAT")
    print("=" * 50)
    print("🚫 No market analysis or segmentation")
    print("📋 Pure data collection only")
    
    try:
        # Load technical data
        with open(input_file, 'r', encoding='utf-8') as f:
            technical_data = json.load(f)
        
        print(f"📂 Processing {len(technical_data)} properties...")
        
        # Convert each property
        pure_properties = []
        skipped = 0
        
        for i, tech_prop in enumerate(technical_data):
            pure_prop = PureDataSchema.create_property_record(tech_prop)
            
            if pure_prop:
                pure_properties.append(pure_prop)
            else:
                skipped += 1
            
            if (i + 1) % 10 == 0:
                print(f"   Processed {i + 1}/{len(technical_data)}...")
        
        print(f"✅ Successfully converted {len(pure_properties)} properties")
        print(f"⚠️ Skipped {skipped} properties (insufficient data)")
        
        # Generate output filename
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"data/pure_data_{timestamp}.json"
        
        # Save pure data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(pure_properties, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Pure data saved to: {output_file}")
        
        # Show samples
        print(f"\n📋 SAMPLE PURE DATA:")
        print("=" * 40)
        
        for i, prop in enumerate(pure_properties[:3], 1):
            print(f"\n{i}. {prop['property_name']}")
            print(f"   💰 {prop['price_formatted']} ({prop.get('price_range', 'N/A')})")
            print(f"   🏠 {prop.get('property_type', 'N/A')} • {prop['bedrooms']}BR • {prop.get('floor_area_sqft', 'N/A')} sqft")
            print(f"   📍 {prop.get('district_code', 'N/A')} • {prop.get('mrt_station', 'N/A')} ({prop.get('mrt_distance_category', 'N/A')})")
            print(f"   📅 {prop.get('listed_date', 'N/A')} • {prop.get('image_count', 0)} images")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return None

if __name__ == "__main__":
    # Convert existing data to pure format
    input_file = "data/samples/advanced_extraction_2025-07-13T17-44-24.json"
    convert_to_pure_data_format(input_file)
