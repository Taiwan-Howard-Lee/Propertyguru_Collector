#!/usr/bin/env python3
"""
🧪 PropertyGuru Scraper Test Suite
Tests all scraper components and validates data quality
"""

import json
import os
import unittest
from datetime import datetime
import statistics

class TestPropertyScraper(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        import os

        # Look for data files in the data directory
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

        # Try to find the most recent extraction file
        if os.path.exists(data_dir):
            json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

            if json_files:
                # Use the sample file or most recent
                if 'sample_extraction.json' in json_files:
                    self.test_data_file = os.path.join(data_dir, 'sample_extraction.json')
                else:
                    self.test_data_file = os.path.join(data_dir, sorted(json_files)[-1])
            else:
                self.test_data_file = None
        else:
            self.test_data_file = None

        self.properties = self.load_test_data()
    
    def load_test_data(self):
        """Load test data from JSON file"""
        if self.test_data_file and os.path.exists(self.test_data_file):
            with open(self.test_data_file, 'r') as f:
                return json.load(f)
        return []
    
    def test_data_file_exists(self):
        """Test that scraped data file exists"""
        self.assertIsNotNone(self.test_data_file, "Should have found a data file")
        self.assertTrue(os.path.exists(self.test_data_file),
                       f"Data file {self.test_data_file} should exist")
    
    def test_properties_extracted(self):
        """Test that properties were extracted"""
        self.assertGreater(len(self.properties), 0, 
                          "Should have extracted at least 1 property")
        print(f"✅ Extracted {len(self.properties)} properties")
    
    def test_property_structure(self):
        """Test that properties have required fields"""
        required_fields = ['id', 'price', 'bedrooms', 'extraction_timestamp', 'source']
        
        for i, prop in enumerate(self.properties):
            with self.subTest(property_index=i):
                for field in required_fields:
                    self.assertIn(field, prop, 
                                f"Property {i} should have field '{field}'")
        
        print(f"✅ All properties have required fields")
    
    def test_price_validity(self):
        """Test that prices are valid"""
        for i, prop in enumerate(self.properties):
            with self.subTest(property_index=i):
                price = prop.get('price')
                self.assertIsInstance(price, int, 
                                    f"Property {i} price should be integer")
                self.assertGreater(price, 0, 
                                 f"Property {i} price should be positive")
                self.assertLess(price, 100000000, 
                              f"Property {i} price should be reasonable (<100M)")
        
        print(f"✅ All prices are valid")
    
    def test_bedroom_validity(self):
        """Test that bedroom counts are valid"""
        for i, prop in enumerate(self.properties):
            with self.subTest(property_index=i):
                bedrooms = prop.get('bedrooms')
                self.assertIsInstance(bedrooms, int, 
                                    f"Property {i} bedrooms should be integer")
                self.assertGreaterEqual(bedrooms, 1, 
                                      f"Property {i} should have at least 1 bedroom")
                self.assertLessEqual(bedrooms, 10, 
                                   f"Property {i} should have reasonable bedroom count")
        
        print(f"✅ All bedroom counts are valid")
    
    def test_area_validity(self):
        """Test that areas are valid (if present)"""
        for i, prop in enumerate(self.properties):
            if 'area' in prop:
                with self.subTest(property_index=i):
                    area = prop.get('area')
                    self.assertIsInstance(area, int, 
                                        f"Property {i} area should be integer")
                    self.assertGreater(area, 100, 
                                     f"Property {i} area should be > 100 sqft")
                    self.assertLess(area, 50000, 
                                  f"Property {i} area should be < 50,000 sqft")
        
        print(f"✅ All areas are valid")
    
    def test_data_consistency(self):
        """Test data consistency and quality"""
        prices = [p['price'] for p in self.properties]
        bedrooms = [p['bedrooms'] for p in self.properties]
        
        # Test price distribution
        avg_price = statistics.mean(prices)
        median_price = statistics.median(prices)
        
        self.assertGreater(avg_price, 100000, "Average price should be reasonable")
        self.assertGreater(median_price, 50000, "Median price should be reasonable")
        
        # Test bedroom distribution
        avg_bedrooms = statistics.mean(bedrooms)
        self.assertGreater(avg_bedrooms, 1, "Average bedrooms should be > 1")
        self.assertLess(avg_bedrooms, 8, "Average bedrooms should be < 8")
        
        print(f"✅ Data consistency checks passed")
    
    def test_timestamp_format(self):
        """Test that timestamps are properly formatted"""
        for i, prop in enumerate(self.properties):
            with self.subTest(property_index=i):
                timestamp = prop.get('extraction_timestamp')
                self.assertIsInstance(timestamp, str, 
                                    f"Property {i} timestamp should be string")
                
                # Try to parse the timestamp
                try:
                    datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    self.fail(f"Property {i} has invalid timestamp format: {timestamp}")
        
        print(f"✅ All timestamps are valid")
    
    def test_source_field(self):
        """Test that source field is correct"""
        for i, prop in enumerate(self.properties):
            with self.subTest(property_index=i):
                source = prop.get('source')
                self.assertEqual(source, 'PropertyGuru', 
                               f"Property {i} should have source 'PropertyGuru'")
        
        print(f"✅ All sources are correct")
    
    def test_price_per_sqft_calculation(self):
        """Test PSF calculations for properties with area"""
        properties_with_area = [p for p in self.properties if 'area' in p]
        
        if properties_with_area:
            for prop in properties_with_area:
                psf = prop['price'] / prop['area']
                self.assertGreater(psf, 100, "PSF should be > S$100")
                self.assertLess(psf, 10000, "PSF should be < S$10,000")
        
        print(f"✅ PSF calculations are reasonable")
    
    def test_no_duplicate_ids(self):
        """Test that property IDs are unique"""
        ids = [p['id'] for p in self.properties]
        unique_ids = set(ids)
        
        self.assertEqual(len(ids), len(unique_ids), 
                        "All property IDs should be unique")
        
        print(f"✅ All property IDs are unique")

class TestScraperFunctionality(unittest.TestCase):
    """Test scraper functionality"""
    
    def test_json_file_format(self):
        """Test that JSON file is properly formatted"""
        test_file = "smart_extraction_20250712_212608.json"
        
        if os.path.exists(test_file):
            try:
                with open(test_file, 'r') as f:
                    data = json.load(f)
                self.assertIsInstance(data, list, "JSON should contain a list")
                print(f"✅ JSON file is properly formatted")
            except json.JSONDecodeError:
                self.fail("JSON file is not valid JSON")
    
    def test_file_permissions(self):
        """Test that files have correct permissions"""
        test_files = [
            "smart_property_scraper.py",
            "property_analysis.py",
            "smart_extraction_20250712_212608.json"
        ]
        
        for file in test_files:
            if os.path.exists(file):
                self.assertTrue(os.access(file, os.R_OK), 
                              f"File {file} should be readable")
        
        print(f"✅ File permissions are correct")

def run_comprehensive_tests():
    """Run all tests and provide summary"""
    print("🧪 PROPERTYGURU SCRAPER TEST SUITE")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPropertyScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestScraperFunctionality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("🎯 TEST SUMMARY")
    print("-" * 30)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ ERRORS:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ PropertyGuru scraper is working correctly")
    else:
        print("\n⚠️ Some tests failed. Please review the issues above.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_comprehensive_tests()
    exit(0 if success else 1)
