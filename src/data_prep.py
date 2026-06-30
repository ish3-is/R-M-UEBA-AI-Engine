import pandas as pd
import os

# 1. تحديد مسار ملف Keystroke Dynamics
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '..', 'data', 'raw', 'DSL-StrongPasswordData.csv')

print("جاري محاولة قراءة بيانات بصمة لوحة المفاتيح...\n")

try:
    # 2. قراءة الملف
    df = pd.read_csv(file_path)
    
    print("✅ تم استدعاء البيانات بنجاح!")
    print(f"📊 إجمالي عدد السجلات (الصفوف): {len(df):,}")
    print(f"👥 إجمالي عدد المستخدمين (Subjects): {df['subject'].nunique()}")
    
    # 3. عرض أول 5 صفوف لمعرفة شكل الأعمدة
    print("\n--- نظرة على أول 5 صفوف ---")
    # نعرض أول 8 أعمدة فقط عشان الشاشة ما تتلخبط
    print(df.iloc[:, :8].head())
    
    # 4. عرض أسماء المستخدمين (أول 5 مستخدمين كمثال)
    print("\n--- عينة من معرفات المستخدمين ---")
    print(df['subject'].unique()[:5])

except FileNotFoundError:
    print("❌ خطأ: لم يتم العثور على الملف!")
    print("تأكد من تسمية الملف بـ 'DSL-StrongPasswordData.csv' ووضعه داخل 'data/raw'")