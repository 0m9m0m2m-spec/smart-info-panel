import pandas as pd
import json
import os
from pathlib import Path
from typing import List, Dict, Any

class DataLoader:
    """بارگذار داده‌های چند فرمت (Excel, CSV, JSON)"""
    
    def __init__(self, data_folder: str = "data"):
        self.data_folder = Path(data_folder)
        self.data_folder.mkdir(exist_ok=True)
        self.all_data = []
        self.file_sources = {}  # ذخیره مکان فایل‌ها
    
    def create_sample_data(self):
        """ایجاد داده‌های نمونه اگر فایل وجود ندارد"""
        # فایل کاربران
        users_df = pd.DataFrame({
            'شماره': ['001', '002', '003', '004', '005'],
            'نام': ['احمد محمد', 'فاطمه علی', 'علی حسن', 'مریم محمود', 'حسن رضا'],
            'ایمیل': ['ahmad@email.com', 'fatema@email.com', 'ali@email.com', 
                     'maryam@email.com', 'hasan@email.com'],
            'تلفن': ['09121234567', '09121234568', '09121234569', '09121234570', '09121234571'],
            'شهر': ['تهران', 'اصفهان', 'شیراز', 'مشهد', 'تبریز']
        })
        users_df.to_excel(self.data_folder / 'users.xlsx', index=False)
        
        # فایل سفارشات (CSV)
        orders_df = pd.DataFrame({
            'کد_سفارش': ['S001', 'S002', 'S003', 'S004', 'S005'],
            'شماره_کاربر': ['001', '002', '001', '003', '002'],
            'محصول': ['لپتاپ', 'موبایل', 'تبلت', 'هدفون', 'شارژر'],
            'مبلغ': [5000000, 15000000, 8000000, 500000, 200000],
            'تاریخ': ['1402-01-15', '1402-02-20', '1402-03-10', '1402-04-05', '1402-05-12'],
            'وضعیت': ['تحویل شده', 'درحال بررسی', 'تحویل شده', 'تحویل شده', 'لغو شده']
        })
        orders_df.to_csv(self.data_folder / 'orders.csv', index=False, encoding='utf-8-sig')
        
        # فایل تیکت‌های پشتیبانی (Excel)
        tickets_df = pd.DataFrame({
            'شماره_تیکت': ['T001', 'T002', 'T003', 'T004', 'T005'],
            'شماره_کاربر': ['001', '002', '003', '001', '004'],
            'موضوع': ['مشکل نرم‌افزار', 'سؤال درباره محصول', 'درخواست بازگشت', 
                     'مشکل پرداخت', 'مشکل ارسال'],
            'توضیحات': ['نرم‌افزار از کار می‌افتد', 'آیا گارانتی دارد؟', 
                      'میخواهم محصول را برگردانم', 'پرداخت موفق نشد', 'هنوز نرسیده'],
            'وضعیت': ['حل شده', 'در انتظار', 'درحال بررسی', 'حل شده', 'درحال بررسی']
        })
        tickets_df.to_excel(self.data_folder / 'tickets.xlsx', index=False)
        
        print("✅ داده‌های نمونه ایجاد شد")
    
    def load_csv_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """خواندن فایل CSV"""
        records = []
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            file_name = file_path.stem
            
            for _, row in df.iterrows():
                record = {
                    'source_file': file_name,
                    'file_type': 'CSV',
                    'file_path': str(file_path),
                    'data': row.to_dict()
                }
                records.append(record)
            
            print(f"✅ {len(records)} رکورد از {file_path.name} خوانده شد")
            return records
        
        except Exception as e:
            print(f"❌ خطا در خواندن {file_path.name}: {e}")
            return []
    
    def load_excel_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """خواندن فایل Excel"""
        records = []
        try:
            df = pd.read_excel(file_path)
            file_name = file_path.stem
            
            for _, row in df.iterrows():
                record = {
                    'source_file': file_name,
                    'file_type': 'Excel',
                    'file_path': str(file_path),
                    'data': row.to_dict()
                }
                records.append(record)
            
            print(f"✅ {len(records)} رکورد از {file_path.name} خوانده شد")
            return records
        
        except Exception as e:
            print(f"❌ خطا در خواندن {file_path.name}: {e}")
            return []
    
    def load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """خواندن فایل JSON"""
        records = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_name = file_path.stem
            
            if isinstance(data, list):
                for item in data:
                    record = {
                        'source_file': file_name,
                        'file_type': 'JSON',
                        'file_path': str(file_path),
                        'data': item if isinstance(item, dict) else {'value': item}
                    }
                    records.append(record)
            
            print(f"✅ {len(records)} رکورد از {file_path.name} خوانده شد")
            return records
        
        except Exception as e:
            print(f"❌ خطا در خواندن {file_path.name}: {e}")
            return []
    
    def load_all_data(self) -> List[Dict[str, Any]]:
        """بارگذاری تمام فایل‌ها (CSV, Excel, JSON)"""
        self.all_data = []
        
        # بررسی اینکه فایلی وجود دارد یا نه
        if not any(self.data_folder.glob('*.csv')) and \
           not any(self.data_folder.glob('*.xlsx')) and \
           not any(self.data_folder.glob('*.json')):
            self.create_sample_data()
        
        print(f"\n📂 بارگذاری فایل‌ها از پوشه: {self.data_folder}")
        print("=" * 60)
        
        # خواندن فایل‌های CSV
        for csv_file in self.data_folder.glob('*.csv'):
            csv_records = self.load_csv_file(csv_file)
            self.all_data.extend(csv_records)
            self.file_sources[csv_file.stem] = str(csv_file)
        
        # خواندن فایل‌های Excel
        for excel_file in self.data_folder.glob('*.xlsx'):
            excel_records = self.load_excel_file(excel_file)
            self.all_data.extend(excel_records)
            self.file_sources[excel_file.stem] = str(excel_file)
        
        # خواندن فایل‌های JSON
        for json_file in self.data_folder.glob('*.json'):
            json_records = self.load_json_file(json_file)
            self.all_data.extend(json_records)
            self.file_sources[json_file.stem] = str(json_file)
        
        print("=" * 60)
        print(f"✅ کل {len(self.all_data)} رکورد بارگذاری شد\n")
        
        return self.all_data
    
    def get_available_files(self) -> Dict[str, str]:
        """دریافت لیست فایل‌های موجود"""
        return self.file_sources
    
    def get_data_summary(self) -> Dict[str, Any]:
        """خلاصه اطلاعات داده‌های بارگذاری شده"""
        summary = {
            'total_records': len(self.all_data),
            'files': {},
            'sample_data': []
        }
        
        # خلاصه برای هر فایل
        for record in self.all_data:
            source = record['source_file']
            if source not in summary['files']:
                summary['files'][source] = {
                    'type': record['file_type'],
                    'count': 0,
                    'columns': set(record['data'].keys())
                }
            summary['files'][source]['count'] += 1
        
        # نمونه داده
        if self.all_data:
            summary['sample_data'] = [self.all_data[0]['data'] for _ in range(min(3, len(self.all_data)))]
        
        return summary
