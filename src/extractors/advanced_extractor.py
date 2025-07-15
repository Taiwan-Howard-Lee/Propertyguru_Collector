#!/usr/bin/env python3
"""
🔍 Advanced PropertyGuru Data Extractor
Extracts comprehensive property details from PropertyGuru listings
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
# Advanced Property Extractor - Pure Data Only

class AdvancedPropertyExtractor:
    """Advanced extractor for comprehensive PropertyGuru property data"""
    
    def __init__(self, driver):
        self.driver = driver
        
    def extract_properties_from_page(self) -> List[Dict[str, Any]]:
        """Extract all properties from current page with comprehensive details"""
        print("🔍 Starting advanced property extraction...")

        properties = []

        # More specific PropertyGuru selectors to avoid sub-elements
        property_selectors = [
            # PropertyGuru specific main property containers
            'article[data-testid="listing-card"]',
            'div[data-testid="listing-card"]',
            '.listing-card',
            '.property-card',
            '.search-result-item',
            # More specific to avoid sub-elements
            'div[class*="listing"]:has(img)',
            'div[class*="property"]:has(img)',
            # Fallback with stricter criteria
            'div:has(> img):has(h3)',
            'div:has(> img):has(h2)'
        ]

        property_elements = []
        for selector in property_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found {len(elements)} elements with selector: {selector}")
                    # Filter out elements that are too small (likely sub-elements)
                    filtered_elements = []
                    for elem in elements:
                        try:
                            text_length = len(elem.text.strip())
                            if text_length > 100:  # Property cards should have substantial text
                                filtered_elements.append(elem)
                        except:
                            continue

                    if filtered_elements:
                        print(f"✅ Filtered to {len(filtered_elements)} substantial property elements")
                        property_elements = filtered_elements
                        break
            except:
                continue

        if not property_elements:
            # Fallback: extract from page structure
            print("🔄 Using fallback extraction method...")
            return self._extract_from_page_text()

        # Extract each property and deduplicate
        seen_properties = set()
        for i, element in enumerate(property_elements):
            try:
                property_data = self._extract_single_property(element, i)
                if property_data and property_data.get("property_name"):
                    # Create unique key for deduplication
                    unique_key = (
                        property_data.get("property_name", ""),
                        property_data.get("price", 0),
                        property_data.get("bedrooms", 0)
                    )

                    if unique_key not in seen_properties:
                        seen_properties.add(unique_key)
                        properties.append(property_data)
                    else:
                        print(f"🔄 Skipping duplicate: {property_data.get('property_name', 'Unknown')}")
            except Exception as e:
                print(f"⚠️ Error extracting property {i}: {e}")
                continue

        print(f"✅ Extracted {len(properties)} unique properties with advanced method")
        return properties
    
    def _extract_single_property(self, element: WebElement, position: int) -> Dict[str, Any]:
        """Extract comprehensive data from a single property element"""
        property_data = {}
        
        try:
            # Basic metadata
            property_data["id"] = f"property_{position}"
            property_data["position_on_page"] = position
            property_data["extraction_method"] = "advanced_element"

            # Extract listing URL
            try:
                link_elements = element.find_elements(By.TAG_NAME, 'a')
                for link in link_elements:
                    href = link.get_attribute('href')
                    if href and 'property' in href.lower():
                        property_data["listing_url"] = href
                        break
            except:
                pass

            # Property name/title
            name_selectors = ['h3', 'h2', '.property-title', '.listing-title', '[class*="title"]', 'a[href*="property"]']
            property_data["property_name"] = self._extract_text(element, name_selectors)

            # Address (often same as name for PropertyGuru)
            property_data["full_address"] = property_data["property_name"]
            property_data["street_address"] = property_data["property_name"]

            # Try to extract postal code from address
            if property_data["property_name"]:
                postal_match = re.search(r'(\d{6})', property_data["property_name"])
                if postal_match:
                    property_data["postal_code"] = postal_match.group(1)
            
            # Price information
            self._extract_price_info(element, property_data)
            
            # Property details (beds, baths, area)
            self._extract_property_details(element, property_data)
            
            # Property type and tenure
            self._extract_property_type(element, property_data)
            
            # Location and MRT info
            self._extract_location_info(element, property_data)
            
            # Listing information
            self._extract_listing_info(element, property_data)
            
            # Agent information
            self._extract_agent_info(element, property_data)
            
            # Images
            self._extract_image_info(element, property_data)
            
            # Additional features
            self._extract_additional_features(element, property_data)
            
            # Raw data for debugging
            property_data["raw_text"] = element.text[:500] if element.text else ""
            
            # Basic validation - ensure we have essential data
            if not property_data.get("property_name") or not property_data.get("price"):
                return None
            
            return property_data
            
        except Exception as e:
            print(f"⚠️ Error in single property extraction: {e}")
            return property_data
    
    def _extract_text(self, element: WebElement, selectors: List[str]) -> str:
        """Extract text using multiple selectors"""
        for selector in selectors:
            try:
                sub_element = element.find_element(By.CSS_SELECTOR, selector)
                text = sub_element.text.strip()
                if text:
                    return text
            except:
                continue
        return ""
    
    def _extract_price_info(self, element: WebElement, property_data: Dict[str, Any]):
        """Extract price information"""
        try:
            # Look for price text
            price_selectors = ['.price', '[class*="price"]', '.amount', '[class*="amount"]']
            price_text = self._extract_text(element, price_selectors)
            
            if not price_text:
                # Search in element text
                text = element.text
                price_match = re.search(r'S\$\s*([\d,]+(?:\.\d+)?)', text)
                if price_match:
                    price_text = f"S$ {price_match.group(1)}"
            
            if price_text:
                property_data["price_formatted"] = price_text
                
                # Extract numeric price
                price_numbers = re.findall(r'[\d,]+', price_text.replace('S$', ''))
                if price_numbers:
                    try:
                        property_data["price"] = int(price_numbers[0].replace(',', ''))
                    except:
                        pass
            
            # Extract price per sqft
            psf_match = re.search(r'S\$\s*([\d,]+(?:\.\d+)?)\s*psf', element.text, re.IGNORECASE)
            if psf_match:
                property_data["price_per_sqft_formatted"] = f"S$ {psf_match.group(1)} psf"
                try:
                    property_data["price_per_sqft"] = float(psf_match.group(1).replace(',', ''))
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠️ Price extraction error: {e}")
    
    def _extract_property_details(self, element: WebElement, property_data: Dict[str, Any]):
        """Extract bedrooms, bathrooms, area"""
        try:
            text = element.text
            
            # Bedrooms
            bed_match = re.search(r'(\d+)\s*Bed', text, re.IGNORECASE)
            if bed_match:
                property_data["bedrooms"] = int(bed_match.group(1))
            
            # Bathrooms  
            bath_match = re.search(r'(\d+)\s*Bath', text, re.IGNORECASE)
            if bath_match:
                property_data["bathrooms"] = int(bath_match.group(1))
            
            # Floor area
            area_match = re.search(r'([\d,]+)\s*sqft', text, re.IGNORECASE)
            if area_match:
                property_data["floor_area_formatted"] = f"{area_match.group(1)} sqft"
                try:
                    property_data["floor_area_sqft"] = int(area_match.group(1).replace(',', ''))
                except:
                    pass
            
            # Land area (for landed properties)
            land_match = re.search(r'([\d,]+)\s*sqft\s*\(land\)', text, re.IGNORECASE)
            if land_match:
                property_data["land_area_formatted"] = f"{land_match.group(1)} sqft (land)"
                try:
                    property_data["land_area_sqft"] = int(land_match.group(1).replace(',', ''))
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠️ Property details extraction error: {e}")
    
    def _extract_property_type(self, element: WebElement, property_data: Dict[str, Any]):
        """Extract property type and tenure"""
        try:
            text = element.text
            
            # Property types
            property_types = [
                'HDB Flat', 'Condominium', 'Apartment', 'Terraced House', 
                'Semi-Detached House', 'Detached House', 'Good Class Bungalow',
                'Shophouse', 'Commercial', 'Industrial'
            ]
            
            for prop_type in property_types:
                if prop_type in text:
                    property_data["property_type"] = prop_type
                    break
            
            # Tenure
            tenures = ['Freehold', '99-year Leasehold', '999-year Leasehold', 'Leasehold']
            for tenure in tenures:
                if tenure in text:
                    property_data["tenure"] = tenure
                    break
            
            # Built year
            built_match = re.search(r'Built:\s*(\d{4})', text)
            if built_match:
                property_data["built_year"] = int(built_match.group(1))
            
            # New project completion
            completion_match = re.search(r'New Project:\s*(\d{4})', text)
            if completion_match:
                property_data["completion_year"] = int(completion_match.group(1))
                
        except Exception as e:
            print(f"⚠️ Property type extraction error: {e}")
    
    def _extract_location_info(self, element: WebElement, property_data: Dict[str, Any]):
        """Extract MRT and location information"""
        try:
            text = element.text

            # Multiple MRT patterns to catch different formats
            mrt_patterns = [
                # Standard format: "5 min (410 m) from NE11 Woodleigh MRT Station"
                r'(\d+)\s*min\s*\(([^)]+)\)\s*from\s*([A-Z0-9]+)\s*([^MRT\n]*)\s*MRT Station',
                # Alternative format: "5 min (410 m) from NE11 Woodleigh"
                r'(\d+)\s*min\s*\(([^)]+)\)\s*from\s*([A-Z0-9]+)\s*([^\n]*)',
                # Simple format: "NE11 Woodleigh MRT Station"
                r'([A-Z0-9]+)\s*([^MRT\n]*)\s*MRT Station',
                # Distance only: "5 min from Woodleigh MRT"
                r'(\d+)\s*min.*?from\s*([^MRT\n]*)\s*MRT'
            ]

            for pattern in mrt_patterns:
                mrt_match = re.search(pattern, text, re.IGNORECASE)
                if mrt_match:
                    groups = mrt_match.groups()

                    if len(groups) >= 4:  # Full format
                        time_dist = f"{groups[0]} min ({groups[1]})"
                        mrt_code = groups[2]
                        station_name = groups[3].strip()

                        property_data["mrt_distance"] = time_dist
                        property_data["mrt_line"] = mrt_code
                        property_data["mrt_station"] = station_name
                        property_data["nearest_mrt"] = f"{mrt_code} {station_name} MRT Station"
                    elif len(groups) >= 2:  # Partial format
                        if groups[0].isdigit():  # Has time
                            property_data["mrt_distance"] = f"{groups[0]} min"
                            property_data["mrt_station"] = groups[1].strip()
                        else:  # Just station info
                            property_data["mrt_line"] = groups[0]
                            property_data["mrt_station"] = groups[1].strip()
                            property_data["nearest_mrt"] = f"{groups[0]} {groups[1].strip()} MRT Station"

                    print(f"✅ Found MRT: {property_data.get('nearest_mrt', 'Partial info')}")
                    break

            # Extract district from address if possible
            address = property_data.get("property_name", "")
            # Singapore district patterns
            district_patterns = [
                r'D(\d{2})',  # D01, D02, etc.
                r'District\s*(\d{1,2})',
                # Could add more patterns based on area names
            ]

            for pattern in district_patterns:
                district_match = re.search(pattern, text, re.IGNORECASE)
                if district_match:
                    property_data["district"] = f"D{district_match.group(1).zfill(2)}"
                    break

        except Exception as e:
            print(f"⚠️ Location extraction error: {e}")
    
    def _extract_listing_info(self, element: WebElement, property_data: Dict[str, Any]):
        """Extract listing date and time information"""
        try:
            text = element.text
            
            # Listed date
            date_match = re.search(r'Listed on\s*([^(]+)\s*\(([^)]+)\)', text)
            if date_match:
                property_data["listed_date"] = date_match.group(1).strip()
                property_data["listed_time_ago"] = date_match.group(2).strip()
                
        except Exception as e:
            print(f"⚠️ Listing info extraction error: {e}")
    
    def _extract_agent_info(self, element: WebElement, property_data: Dict[str, Any]):
        """Extract agent information"""
        try:
            text = element.text

            # Agent name patterns
            agent_patterns = [
                r'Listed by\s*([^\n\d]+?)(?:\s*\d|\n|$)',  # "Listed by John Doe"
                r'Agent:\s*([^\n\d]+?)(?:\s*\d|\n|$)',     # "Agent: John Doe"
                r'Contact\s*([^\n\d]+?)(?:\s*\d|\n|$)',    # "Contact John Doe"
            ]

            for pattern in agent_patterns:
                agent_match = re.search(pattern, text, re.IGNORECASE)
                if agent_match:
                    agent_name = agent_match.group(1).strip()
                    # Clean up common suffixes
                    agent_name = re.sub(r'\s*(Contact|Agent)$', '', agent_name, flags=re.IGNORECASE)
                    if len(agent_name) > 2:  # Valid name
                        property_data["agent_name"] = agent_name
                        break

            # Agent rating - look for patterns like "4.5" or "5.0" near agent name
            rating_patterns = [
                r'(?:Listed by|Agent:).*?(\d+\.\d+)',
                r'(\d+\.\d+)(?:\s*stars?|\s*rating|\s*/\s*5)',
                r'Rating:\s*(\d+\.\d+)',
            ]

            for pattern in rating_patterns:
                rating_match = re.search(pattern, text, re.IGNORECASE)
                if rating_match:
                    try:
                        rating = float(rating_match.group(1))
                        if 0 <= rating <= 5:  # Valid rating range
                            property_data["agent_rating"] = rating
                            break
                    except:
                        continue

            # Agent description (property description/tagline)
            desc_patterns = [
                r'"([^"]+)"',  # Text in quotes
                r'["""]([^"""]+)["""]',  # Smart quotes
            ]

            for pattern in desc_patterns:
                desc_match = re.search(pattern, text)
                if desc_match:
                    description = desc_match.group(1).strip()
                    if len(description) > 10:  # Substantial description
                        property_data["agent_description"] = description
                        break

        except Exception as e:
            print(f"⚠️ Agent info extraction error: {e}")
    
    def _extract_image_info(self, element: WebElement, property_data: Dict[str, Any]):
        """Extract image information"""
        try:
            # Look for images
            img_elements = element.find_elements(By.TAG_NAME, 'img')
            if img_elements:
                property_data["image_count"] = len(img_elements)
                # Get main image URL
                main_img = img_elements[0]
                src = main_img.get_attribute('src')
                if src and 'http' in src:
                    property_data["main_image_url"] = src
                    property_data["image_urls"] = [src]
                    
        except Exception as e:
            print(f"⚠️ Image extraction error: {e}")
    
    def _extract_additional_features(self, element: WebElement, property_data: Dict[str, Any]):
        """Extract additional features and amenities"""
        try:
            text = element.text.lower()
            
            # Check for special features
            if 'virtual tour' in text:
                property_data["has_virtual_tour"] = True
            if 'verified listing' in text:
                property_data["verified_listing"] = True
            if 'featured' in text:
                property_data["featured_listing"] = True
                
        except Exception as e:
            print(f"⚠️ Additional features extraction error: {e}")
    
    def _extract_from_page_text(self) -> List[Dict[str, Any]]:
        """Fallback: extract from page text when elements not found"""
        print("🔄 Using text-based extraction fallback...")
        
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            properties = []
            
            # Split by property patterns
            property_blocks = re.split(r'S\$\s*[\d,]+', page_text)
            
            for i, block in enumerate(property_blocks[1:], 1):  # Skip first empty block
                if len(block.strip()) < 50:  # Too short to be a property
                    continue
                    
                property_data = {}
                property_data["id"] = f"property_{i-1}"
                property_data["extraction_method"] = "text_fallback"
                
                # Extract what we can from the text block
                lines = block.strip().split('\n')
                if lines:
                    property_data["property_name"] = lines[0].strip()
                    property_data["raw_text"] = block[:300]
                
                # Try to extract basic info
                self._extract_price_info_from_text(block, property_data)
                self._extract_property_details_from_text(block, property_data)
                
                if property_data.get("property_name"):
                    properties.append(property_data)
            
            return properties[:25]  # Limit to reasonable number
            
        except Exception as e:
            print(f"⚠️ Text extraction error: {e}")
            return []
    
    def _extract_price_info_from_text(self, text: str, property_data: Dict[str, Any]):
        """Extract price from text block"""
        # Find price before this block
        price_match = re.search(r'S\$\s*([\d,]+)', text)
        if price_match:
            property_data["price_formatted"] = f"S$ {price_match.group(1)}"
            try:
                property_data["price"] = int(price_match.group(1).replace(',', ''))
            except:
                pass
    
    def _extract_property_details_from_text(self, text: str, property_data: Dict[str, Any]):
        """Extract property details from text block"""
        # Bedrooms
        bed_match = re.search(r'(\d+)\s*Bed', text, re.IGNORECASE)
        if bed_match:
            property_data["bedrooms"] = int(bed_match.group(1))
        
        # Area
        area_match = re.search(r'([\d,]+)\s*sqft', text, re.IGNORECASE)
        if area_match:
            try:
                property_data["floor_area_sqft"] = int(area_match.group(1).replace(',', ''))
            except:
                pass
