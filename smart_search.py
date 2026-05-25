from fuzzywuzzy import fuzz
from typing import List, Dict, Tuple, Any
import re

class SmartSearch:
    """موتور جستجوی هوشمند"""
    
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
        self.search_threshold = 70
    
    def convert_to_string(self, value: Any) -> str:
        """تبدیل هر مقدار به رشته"""
        if pd.isna(value):
            return ""
        return str(value).strip()
    
    def search(self, query: str, threshold: int = None) -> Dict[str, List]:
        """جستجوی هوشمند با دسته‌بندی نتایج"""
        if threshold:
            self.search_threshold = threshold
        
        query = query.strip()
        if not query:
            return {'exact': [], 'high': [], 'medium': [], 'low': []}
        
        exact_matches = []
        high_matches = []
        medium_matches = []
        low_matches = []
        
        for record in self.data:
            data_dict = record['data']
            source_file = record['source_file']
            
            # جستجو در تمام فیلدها
            best_score = 0
            matching_field = None
            
            for field, value in data_dict.items():
                value_str = self.convert_to_string(value)
                
                # جستجوی دقیق
                if value_str == query:
                    exact_matches.append({
                        'score': 100,
                        'source': source_file,
                        'field': field,
                        'data': data_dict
                    })
                    continue
                
                # جستجوی فازی
                score = fuzz.token_set_ratio(query.lower(), value_str.lower())
                
                if score > best_score:
                    best_score = score
                    matching_field = field
            
            # دسته‌بندی براساس امتیاز
            if best_score >= 85:
                high_matches.append({
                    'score': best_score,
                    'source': source_file,
                    'field': matching_field,
                    'data': data_dict
                })
            elif best_score >= 70:
                medium_matches.append({
                    'score': best_score,
                    'source': source_file,
                    'field': matching_field,
                    'data': data_dict
                })
            elif best_score >= 50:
                low_matches.append({
                    'score': best_score,
                    'source': source_file,
                    'field': matching_field,
                    'data': data_dict
                })
        
        # مرتب‌سازی براساس امتیاز
        high_matches.sort(key=lambda x: x['score'], reverse=True)
        medium_matches.sort(key=lambda x: x['score'], reverse=True)
        low_matches.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'exact': exact_matches,
            'high': high_matches,
            'medium': medium_matches,
            'low': low_matches
        }
    
    def get_related_data(self, record: Dict) -> List[Dict]:
        """یافتن اطلاعات مرتبط براساس شماره یا کد"""
        related = []
        data_dict = record['data']
        
        # جستجو براساس شماره کاربر
        if 'شماره' in data_dict or 'شماره_کاربر' in data_dict:
            user_id = data_dict.get('شماره') or data_dict.get('شماره_کاربر')
            
            for item in self.data:
                item_data = item['data']
                for key in ['شماره', 'شماره_کاربر']:
                    if key in item_data and str(item_data[key]) == str(user_id):
                        if item != record:
                            related.append(item)
        
        return related


import pandas as pd
