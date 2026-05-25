import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from data_loader import DataLoader
from smart_search import SmartSearch
import json
from datetime import datetime

class ModernPanel:
    """پنل کاربری مدرن برای جستجو و نمایش اطلاعات"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("پنل جستجو و دسته‌بندی اطلاعات هوشمند")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # تنظیم RTL برای فارسی
        self.root.attributes('-topmost', False)
        
        # بارگذاری داده‌ها
        self.data_loader = DataLoader()
        self.file_config = self.data_loader.create_sample_data()
        self.data = self.data_loader.load_all_data(self.file_config)
        self.search_engine = SmartSearch(self.data)
        
        # متغیرهای جهانی
        self.current_results = {}
        self.current_categorized = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """راه‌اندازی رابط کاربری"""
        # رنگ‌های مدرن
        bg_color = "#f0f2f5"
        header_color = "#2c3e50"
        button_color = "#3498db"
        accent_color = "#e74c3c"
        
        self.root.configure(bg=bg_color)
        
        # ===== Header =====
        header = tk.Frame(self.root, bg=header_color, height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="🔍 پنل جستجو و دسته‌بندی اطلاعات هوشمند",
            font=("Arial", 18, "bold"),
            bg=header_color,
            fg="white"
        )
        title_label.pack(pady=15)
        
        # ===== Search Section =====
        search_frame = tk.Frame(self.root, bg=bg_color)
        search_frame.pack(fill=tk.X, padx=20, pady=15)
        
        search_label = tk.Label(
            search_frame,
            text="جستجو (شماره، نام، یا هر اطلاعاتی):",
            font=("Arial", 11, "bold"),
            bg=bg_color,
            fg=header_color
        )
        search_label.pack(anchor=tk.E, pady=5)
        
        search_input_frame = tk.Frame(search_frame, bg=bg_color)
        search_input_frame.pack(fill=tk.X)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_input_frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            relief=tk.FLAT,
            bg="white",
            fg="black",
            bd=2
        )
        search_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        search_entry.bind('<Return>', lambda e: self.perform_search())
        
        search_button = tk.Button(
            search_input_frame,
            text="🔍 جستجو",
            font=("Arial", 11, "bold"),
            bg=button_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.perform_search,
            padx=15,
            pady=5
        )
        search_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(
            search_input_frame,
            text="🔄 پاک کردن",
            font=("Arial", 11, "bold"),
            bg=accent_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_search,
            padx=15,
            pady=5
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # ===== Notebook (Tabs) =====
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Tab 1: نتایج دسته‌بندی شده
        tab1 = tk.Frame(self.notebook, bg=bg_color)
        self.notebook.add(tab1, text="📊 نتایج دسته‌بندی شده")
        self.setup_categorized_tab(tab1, bg_color)
        
        # Tab 2: نتایج کامل
        tab2 = tk.Frame(self.notebook, bg=bg_color)
        self.notebook.add(tab2, text="📋 نتایج کامل")
        self.setup_full_results_tab(tab2, bg_color)
        
        # Tab 3: اطلاعات مرتبط
        tab3 = tk.Frame(self.notebook, bg=bg_color)
        self.notebook.add(tab3, text="🔗 اطلاعات مرتبط")
        self.setup_related_info_tab(tab3, bg_color)
        
        # Tab 4: راهنما
        tab4 = tk.Frame(self.notebook, bg=bg_color)
        self.notebook.add(tab4, text="❓ راهنما")
        self.setup_help_tab(tab4, bg_color)
    
    def setup_categorized_tab(self, parent, bg_color):
        """تب نتایج دسته‌بندی شده"""
        self.categorized_text = scrolledtext.ScrolledText(
            parent,
            font=("Arial", 10),
            bg="white",
            fg="#2c3e50",
            relief=tk.FLAT,
            bd=1,
            wrap=tk.WORD
        )
        self.categorized_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.categorized_text.config(state=tk.DISABLED)
    
    def setup_full_results_tab(self, parent, bg_color):
        """تب نتایج کامل"""
        self.full_results_text = scrolledtext.ScrolledText(
            parent,
            font=("Arial", 10),
            bg="white",
            fg="#2c3e50",
            relief=tk.FLAT,
            bd=1,
            wrap=tk.WORD
        )
        self.full_results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.full_results_text.config(state=tk.DISABLED)
    
    def setup_related_info_tab(self, parent, bg_color):
        """تب اطلاعات مرتبط"""
        frame = tk.Frame(parent, bg=bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        label = tk.Label(
            frame,
            text="جستجو برای نمایش اطلاعات مرتبط:",
            font=("Arial", 11, "bold"),
            bg=bg_color,
            fg="#2c3e50"
        )
        label.pack(anchor=tk.E, pady=5)
        
        self.related_info_text = scrolledtext.ScrolledText(
            frame,
            font=("Arial", 10),
            bg="white",
            fg="#2c3e50",
            relief=tk.FLAT,
            bd=1,
            wrap=tk.WORD
        )
        self.related_info_text.pack(fill=tk.BOTH, expand=True)
        self.related_info_text.config(state=tk.DISABLED)
    
    def setup_help_tab(self, parent, bg_color):
        """تب راهنما"""
        help_text = scrolledtext.ScrolledText(
            parent,
            font=("Arial", 10),
            bg="white",
            fg="#2c3e50",
            relief=tk.FLAT,
            bd=1,
            wrap=tk.WORD
        )
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text.config(state=tk.NORMAL)
        
        help_content = """
راهنمای استفاده از پنل جستجو و دسته‌بندی اطلاعات هوشمند
═══════════════════════════════════════════════════════

📌 نحوه استفاده:

1. در قسمت جستجو، شماره فرد یا هر اطلاعات دیگری را وارد کنید
   مثال: 001، احمد، 09121234567، تهران

2. دکمه "جستجو" را کلیک کنید یا Enter را فشار دهید

3. نتایج در سه تب مختلف نمایش داده می‌شوند:
   • نتایج دسته‌بندی شده: نتایج براساس دقت جستجو
   • نتایج کامل: تمام نتایج تفصیلی
   • اطلاعات مرتبط: تمام اطلاعات مرتبط با شماره

═══════════════════════════════════════════════════════

🔍 نوع جستجو:

• جستجوی دقیق: اگر مطابقت 100% باشد
• جستجوی فازی: جستجوی هوشمند براساس شباهت

دسته‌بندی نتایج:
✓ تطابق دقیق: 100% شباهت
✓ تطابق بالا: بیش از 90% شباهت
✓ تطابق متوسط: 60-90% شباهت
✓ تطابق پایین: کمتر از 60% شباهت

═══════════════════════════════════════════════════════

📊 فایل‌های داده:

• users.xlsx: اطلاعات کاربران (شماره، نام، شهر)
• requests.xlsx: درخواست‌ها (نوع، تاریخ، وضعیت)
• contacts.xlsx: تماس‌ها (تلفن، ایمیل، آدرس)

═══════════════════════════════════════════════════════

💡 نکات مفید:

• می‌توانید در هر جایی از صفحه جستجو کنید
• جستجو به حروف بزرگ و کوچک حساس نیست
• می‌توانید بخشی از اطلاعات را جستجو کنید
• نتایج به ترتیب دقت نمایش داده می‌شوند
        """
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)
    
    def perform_search(self):
        """انجام جستجو"""
        query = self.search_var.get().strip()
        
        if not query:
            messagebox.showwarning("هشدار", "لطفاً متنی برای جستجو وارد کنید!")
            return
        
        try:
            # انجام جستجو
            self.current_results = self.search_engine.search(query)
            self.current_categorized = self.search_engine.categorize_results()
            
            # نمایش نتایج
            self.display_categorized_results()
            self.display_full_results()
            self.display_related_info(query)
            
            # نمایش پیام موفقیت
            total_results = sum(
                len(results) 
                for results in self.current_results.values()
            )
            messagebox.showinfo(
                "موفقیت",
                f"تعداد {total_results} نتیجه یافت شد!"
            )
        
        except Exception as e:
            messagebox.showerror("خطا", f"خطایی رخ داد: {str(e)}")
    
    def display_categorized_results(self):
        """نمایش نتایج دسته‌بندی شده"""
        self.categorized_text.config(state=tk.NORMAL)
        self.categorized_text.delete(1.0, tk.END)
        
        categories_fa = {
            'exact_matches': '✅ تطابق دقیق (100%)',
            'high_matches': '⭐ تطابق بالا (90% به بالا)',
            'medium_matches': '💬 تطابق متوسط (60-90%)',
            'low_matches': '⚠️ تطابق پایین (کمتر از 60%)'
        }
        
        has_results = False
        
        for category, category_fa in categories_fa.items():
            if self.current_categorized[category]:
                has_results = True
                self.categorized_text.insert(tk.END, f"\n{'='*60}\n")
                self.categorized_text.insert(tk.END, f"{category_fa}\n")
                self.categorized_text.insert(tk.END, f"{'='*60}\n\n")
                
                for source, results in self.current_categorized[category].items():
                    self.categorized_text.insert(tk.END, f"📄 منبع: {source}\n")
                    self.categorized_text.insert(tk.END, f"{'─'*60}\n")
                    
                    for i, result in enumerate(results, 1):
                        self.categorized_text.insert(tk.END, f"\n{i}. نتیجه:\n")
                        
                        if 'row_data' in result:
                            for key, value in result['row_data'].items():
                                self.categorized_text.insert(
                                    tk.END,
                                    f"   • {key}: {value}\n"
                                )
                        elif 'path' in result:
                            self.categorized_text.insert(
                                tk.END,
                                f"   • مسیر: {result['path']}\n"
                                f"   • مقدار: {result['value']}\n"
                            )
                        
                        similarity_percent = int(result['similarity'] * 100)
                        self.categorized_text.insert(
                            tk.END,
                            f"   • درجه شباهت: {similarity_percent}%\n"
                        )
                    
                    self.categorized_text.insert(tk.END, f"\n{'─'*60}\n")
        
        if not has_results:
            self.categorized_text.insert(
                tk.END,
                "❌ نتیجه‌ای یافت نشد!\n\nلطفاً اطلاعات دیگری برای جستجو وارد کنید."
            )
        
        self.categorized_text.config(state=tk.DISABLED)
    
    def display_full_results(self):
        """نمایش نتایج کامل"""
        self.full_results_text.config(state=tk.NORMAL)
        self.full_results_text.delete(1.0, tk.END)
        
        if not self.current_results:
            self.full_results_text.insert(tk.END, "❌ نتیجه‌ای یافت نشد!")
            self.full_results_text.config(state=tk.DISABLED)
            return
        
        for source, results in self.current_results.items():
            self.full_results_text.insert(tk.END, f"\n{'='*60}\n")
            self.full_results_text.insert(tk.END, f"📄 منبع: {source}\n")
            self.full_results_text.insert(tk.END, f"{'='*60}\n\n")
            
            for i, result in enumerate(results, 1):
                self.full_results_text.insert(tk.END, f"{i}. نتیجه:\n")
                
                if 'row_data' in result:
                    for key, value in result['row_data'].items():
                        self.full_results_text.insert(
                            tk.END,
                            f"   {key}: {value}\n"
                        )
                
                similarity_percent = int(result['similarity'] * 100)
                self.full_results_text.insert(
                    tk.END,
                    f"   درجه شباهت: {similarity_percent}%\n\n"
                )
        
        self.full_results_text.config(state=tk.DISABLED)
    
    def display_related_info(self, query: str):
        """نمایش اطلاعات مرتبط"""
        self.related_info_text.config(state=tk.NORMAL)
        self.related_info_text.delete(1.0, tk.END)
        
        related = self.search_engine.get_related_info('شماره', query)
        
        if not related:
            self.related_info_text.insert(
                tk.END,
                "❌ اطلاعات مرتبطی یافت نشد!"
            )
            self.related_info_text.config(state=tk.DISABLED)
            return
        
        self.related_info_text.insert(tk.END, f"🔗 اطلاعات مرتبط با: {query}\n")
        self.related_info_text.insert(tk.END, f"{'='*60}\n\n")
        
        for source, records in related.items():
            self.related_info_text.insert(tk.END, f"📄 {source}\n")
            self.related_info_text.insert(tk.END, f"{'─'*60}\n")
            
            for i, record in enumerate(records, 1):
                self.related_info_text.insert(tk.END, f"\nرکورد {i}:\n")
                for key, value in record.items():
                    self.related_info_text.insert(
                        tk.END,
                        f"  • {key}: {value}\n"
                    )
            
            self.related_info_text.insert(tk.END, f"\n{'─'*60}\n")
        
        self.related_info_text.config(state=tk.DISABLED)
    
    def clear_search(self):
        """پاک کردن جستجو"""
        self.search_var.set("")
        self.categorized_text.config(state=tk.NORMAL)
        self.categorized_text.delete(1.0, tk.END)
        self.categorized_text.config(state=tk.DISABLED)
        
        self.full_results_text.config(state=tk.NORMAL)
        self.full_results_text.delete(1.0, tk.END)
        self.full_results_text.config(state=tk.DISABLED)
        
        self.related_info_text.config(state=tk.NORMAL)
        self.related_info_text.delete(1.0, tk.END)
        self.related_info_text.config(state=tk.DISABLED)

def main():
    """نقطه ورود برنامه"""
    root = tk.Tk()
    app = ModernPanel(root)
    root.mainloop()

if __name__ == "__main__":
    main()
