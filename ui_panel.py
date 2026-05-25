import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from data_loader import DataLoader
from smart_search import SmartSearch
from datetime import datetime

class SmartPanel:
    """پنل مدرن جستجوی هوشمند"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 پنل جستجوی هوشمند اطلاعات")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # بارگذاری داده‌ها
        self.loader = DataLoader()
        self.data = self.loader.load_all_data()
        self.searcher = SmartSearch(self.data)
        
        self.current_results = {}
        self.setup_ui()
        
        # تنظیم رنگ‌ها
        self.root.configure(bg='#f0f0f0')
    
    def setup_ui(self):
        """تنظیم رابط کاربری"""
        # نوار بالا - جستجو
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # عنوان
        title_label = ttk.Label(top_frame, text="🔎 جستجو در تمام فایل‌ها", 
                               font=("Arial", 14, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # میدان ورودی
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        
        ttk.Label(input_frame, text="جستجو:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(input_frame, textvariable=self.search_var, 
                                font=("Arial", 11), width=40)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        search_entry.bind('<Return>', lambda e: self.perform_search())
        
        search_btn = ttk.Button(input_frame, text="🔍 جستجو", 
                               command=self.perform_search)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(input_frame, text="❌ پاک کن", 
                              command=self.clear_search)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # تب‌ها
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # تب 1: نتایج دسته‌بندی شده
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="📊 نتایج دسته‌بندی شده")
        self.setup_categorized_tab()
        
        # تب 2: تمام نتایج
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="📋 تمام نتایج")
        self.setup_all_results_tab()
        
        # تب 3: اطلاعات مرتبط
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="🔗 اطلاعات مرتبط")
        self.setup_related_tab()
        
        # تب 4: راهنما
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="❓ راهنما")
        self.setup_help_tab()
    
    def setup_categorized_tab(self):
        """تب نتایج دسته‌بندی شده"""
        tree_frame = ttk.Frame(self.tab1)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.cat_text = scrolledtext.ScrolledText(tree_frame, height=20, 
                                                 font=("Courier", 10))
        self.cat_text.pack(fill=tk.BOTH, expand=True)
        
        # تعریف تگ‌های رنگ
        self.cat_text.tag_config('exact', foreground='#00AA00', font=("Courier", 10, "bold"))
        self.cat_text.tag_config('high', foreground='#0066FF', font=("Courier", 10, "bold"))
        self.cat_text.tag_config('medium', foreground='#FF8800', font=("Courier", 10))
        self.cat_text.tag_config('low', foreground='#CC0000', font=("Courier", 10))
        self.cat_text.tag_config('header', foreground='#333333', font=("Courier", 11, "bold"))
        self.cat_text.tag_config('info', foreground='#666666')
    
    def setup_all_results_tab(self):
        """تب تمام نتایج"""
        tree_frame = ttk.Frame(self.tab2)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.all_text = scrolledtext.ScrolledText(tree_frame, height=20, 
                                                 font=("Courier", 10))
        self.all_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_related_tab(self):
        """تب اطلاعات مرتبط"""
        tree_frame = ttk.Frame(self.tab3)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.related_text = scrolledtext.ScrolledText(tree_frame, height=20, 
                                                     font=("Courier", 10))
        self.related_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_help_tab(self):
        """تب راهنما"""
        help_text = scrolledtext.ScrolledText(self.tab4, height=20, 
                                             font=("Arial", 10))
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_content = """
📌 راهنمای استفاده:

🔍 جستجو:
  • می‌توانید به صورت هوشمند با شماره، نام، ایمیل و تلفن جستجو کنید
  • مثال: "001" یا "احمد" یا "09121234567"

📊 نتایج:
  🟢 دقیق: تطابق ۱۰۰٪
  🔵 بالا: تطابق بیش از ۸۵٪
  🟠 متوسط: تطابق ۷۰-۸۵٪
  🔴 پایین: تطابق ۵۰-۷۰٪

🔗 اطلاعات مرتبط:
  سیستم خودکار تمام اطلاعات مرتبط با شماره را نمایش می‌دهد

📁 منابع داده:
  • users.xlsx - اطلاعات کاربران
  • orders.xlsx - سفارشات
  • tickets.xlsx - تیکت‌های پشتیبانی

💡 نکات:
  • برای نتایج بهتر عبارات کوتاه استفاده کنید
  • سیستم خودکار اشتباهات تایپی را تصحیح می‌کند
"""
        help_text.insert(1.0, help_content)
        help_text.config(state=tk.DISABLED)
    
    def perform_search(self):
        """انجام جستجو"""
        query = self.search_var.get()
        
        if not query:
            messagebox.showwarning("⚠️ هشدار", "لطفاً یک عبارت جستجو وارد کنید")
            return
        
        self.current_results = self.searcher.search(query)
        self.display_results()
    
    def display_results(self):
        """نمایش نتایج"""
        # تب 1: نتایج دسته‌بندی شده
        self.cat_text.config(state=tk.NORMAL)
        self.cat_text.delete(1.0, tk.END)
        
        self.cat_text.insert(tk.END, "=" * 80 + "\n", "header")
        self.cat_text.insert(tk.END, "📊 نتایج دسته‌بندی شده\n", "header")
        self.cat_text.insert(tk.END, "=" * 80 + "\n\n", "header")
        
        # نتایج دقیق
        if self.current_results['exact']:
            self.cat_text.insert(tk.END, "🟢 نتایج دقیق (۱۰۰%)\n", "exact")
            self.cat_text.insert(tk.END, "-" * 80 + "\n", "info")
            for item in self.current_results['exact']:
                self.display_record(self.cat_text, item)
            self.cat_text.insert(tk.END, "\n")
        
        # نتایج بالا
        if self.current_results['high']:
            self.cat_text.insert(tk.END, f"🔵 نتایج بالا (> ۸۵%): {len(self.current_results['high'])}\n", "high")
            self.cat_text.insert(tk.END, "-" * 80 + "\n", "info")
            for item in self.current_results['high'][:5]:
                self.display_record(self.cat_text, item)
            self.cat_text.insert(tk.END, "\n")
        
        # نتایج متوسط
        if self.current_results['medium']:
            self.cat_text.insert(tk.END, f"🟠 نتایج متوسط (۷۰-۸۵%): {len(self.current_results['medium'])}\n", "medium")
            self.cat_text.insert(tk.END, "-" * 80 + "\n", "info")
            for item in self.current_results['medium'][:3]:
                self.display_record(self.cat_text, item)
            self.cat_text.insert(tk.END, "\n")
        
        # نتایج پایین
        if self.current_results['low']:
            self.cat_text.insert(tk.END, f"🔴 نتایج پایین (۵۰-۷۰%): {len(self.current_results['low'])}\n", "low")
        
        if not any(self.current_results.values()):
            self.cat_text.insert(tk.END, "❌ نتیجه‌ای یافت نشد\n", "low")
        
        self.cat_text.config(state=tk.DISABLED)
        
        # تب 2: تمام نتایج
        self.display_all_results()
        
        # تب 3: اطلاعات مرتبط
        self.display_related_info()
    
    def display_record(self, text_widget, record):
        """نمایش یک رکورد"""
        text_widget.insert(tk.END, f"📄 منبع: {record['source']}\n", "info")
        text_widget.insert(tk.END, f"⭐ امتیاز: {record['score']}%\n", "info")
        text_widget.insert(tk.END, f"🔑 فیلد مطابق: {record['field']}\n", "info")
        text_widget.insert(tk.END, "📋 اطلاعات:\n")
        
        for key, value in record['data'].items():
            text_widget.insert(tk.END, f"   {key}: {value}\n")
        
        text_widget.insert(tk.END, "\n")
    
    def display_all_results(self):
        """نمایش تمام نتایج"""
        self.all_text.config(state=tk.NORMAL)
        self.all_text.delete(1.0, tk.END)
        
        all_results = (self.current_results['exact'] + 
                      self.current_results['high'] + 
                      self.current_results['medium'] + 
                      self.current_results['low'])
        
        self.all_text.insert(tk.END, f"📋 کل نتایج: {len(all_results)}\n\n")
        
        for i, item in enumerate(all_results, 1):
            self.all_text.insert(tk.END, f"{i}. ")
            self.display_record(self.all_text, item)
        
        if not all_results:
            self.all_text.insert(tk.END, "❌ نتیجه‌ای یافت نشد\n")
        
        self.all_text.config(state=tk.DISABLED)
    
    def display_related_info(self):
        """نمایش اطلاعات مرتبط"""
        self.related_text.config(state=tk.NORMAL)
        self.related_text.delete(1.0, tk.END)
        
        all_results = (self.current_results['exact'] + 
                      self.current_results['high'])
        
        if not all_results:
            self.related_text.insert(tk.END, "❌ نتیجه‌ای برای نمایش اطلاعات مرتبط یافت نشد\n")
            self.related_text.config(state=tk.DISABLED)
            return
        
        for main_record in all_results:
            related = self.searcher.get_related_data(main_record)
            
            self.related_text.insert(tk.END, f"📌 شماره کاربر: {main_record['data']}\n")
            self.related_text.insert(tk.END, "=" * 80 + "\n\n")
            
            if related:
                self.related_text.insert(tk.END, f"🔗 {len(related)} اطلاعات مرتبط یافت شد:\n\n")
                for item in related:
                    self.display_record(self.related_text, {
                        'source': item['source_file'],
                        'score': 100,
                        'field': 'شماره کاربر',
                        'data': item['data']
                    })
            else:
                self.related_text.insert(tk.END, "❌ اطلاعات مرتبطی یافت نشد\n\n")
        
        self.related_text.config(state=tk.DISABLED)
    
    def clear_search(self):
        """پاک کردن جستجو"""
        self.search_var.set("")
        self.cat_text.config(state=tk.NORMAL)
        self.cat_text.delete(1.0, tk.END)
        self.cat_text.config(state=tk.DISABLED)
        
        self.all_text.config(state=tk.NORMAL)
        self.all_text.delete(1.0, tk.END)
        self.all_text.config(state=tk.DISABLED)
        
        self.related_text.config(state=tk.NORMAL)
        self.related_text.delete(1.0, tk.END)
        self.related_text.config(state=tk.DISABLED)
