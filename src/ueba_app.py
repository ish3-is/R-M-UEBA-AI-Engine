import os
import time
import json
import pandas as pd
from datetime import datetime
from pynput import keyboard
from sklearn.ensemble import RandomForestClassifier

# 1. إعداد المسارات واستدعاء البيانات للتدريب
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '..', 'data', 'raw', 'DSL-StrongPasswordData.csv')

print("🤖 [1/3] جاري قراءة البيانات وتدريب الذكاء الاصطناعي...")
df = pd.read_csv(file_path)
target_user = 's002'
features = df.columns[3:]

# تصنيف البيانات وتجهيز المودل (Random Forest)
df['label'] = (df['subject'] == target_user).astype(int)
legit_data = df[df['label'] == 1]
intruder_data = df[df['label'] == 0].sample(400, random_state=42)
final_data = pd.concat([legit_data, intruder_data])

X = final_data[features]
y = final_data['label']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
print("✅ تم تدريب المودل بنجاح وجاهز لتحليل بصمتك الآن!\n")

# 2. إعداد متغيرات المراقبة الحية
print("🛡️ [2/3] بدء تشغيل التتبع الحي...")
print("⚠️ المطلوب: اكتب كلمة مرورك الحالية (أو أي نص محاكي بـ 10 ضغطات على الأقل) ثم اضغط Enter.")
print("-" * 60)

key_press_times = {}
collected_dwell_times = []

def on_press(key):
    current_time = time.time()
    if key not in key_press_times:
        key_press_times[key] = current_time

def on_release(key):
    current_time = time.time()
    if key in key_press_times:
        press_time = key_press_times[key]
        dwell_time = (current_time - press_time) * 1000  # تحويل للملي ثانية
        collected_dwell_times.append(dwell_time)
        del key_press_times[key]
        
    # عند الضغط على Enter، ينتهي الإدخال ونبدأ التحليل
    if key == keyboard.Key.enter:
        return False

# تشغيل مستمع الكيبورد
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# 3. معالجة البيانات الحية والحكم عليها
print("\n🔍 [3/3] جاري تحليل البصمة الحركية ومقارنتها بالنموذج...")

if len(collected_dwell_times) < 31:
    # المودل حقنا تدرب على 31 ميزة (سرعة ضغط الأزرار)، لذا نحتاج ملء الفراغات لو كتبت نصاً قصيراً
    padding_needed = 31 - len(collected_dwell_times)
    avg_dwell = sum(collected_dwell_times) / len(collected_dwell_times) if collected_dwell_times else 100
    collected_dwell_times.extend([avg_dwell] * padding_needed)
else:
    collected_dwell_times = collected_dwell_times[:31]

# تحويل المدخلات الحية لشكل يفهمه المودل
live_sample = pd.DataFrame([collected_dwell_times], columns=features)
prediction = model.predict(live_sample)[0]

# تحديد النتيجة والخطورة
if prediction == 1:
    result_text = "✅ تم التحقق: المستخدم حقيقي وسلوكه طبيعي."
    severity = "INFO"
    action = "Access_Granted"
    print(f"\033[92m{result_text}\033[0m") # طباعة باللون الأخضر
else:
    result_text = "🚨 تحذير أمني: البصمة الحركية غير متطابقة! اشتباه في اختراق الحساب."
    severity = "CRITICAL"
    action = "Blocked_and_Alerted"
    print(f"\033[91m{result_text}\033[0m") # طباعة باللون الأحمر

# 4. حفظ النتيجة تلقائياً في سجلات الـ SIEM
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "event_type": "UEBA_Live_Inference",
    "severity": severity,
    "user_account": target_user,
    "description": result_text,
    "action": action,
    "captured_metrics_sample": collected_dwell_times[:5] # حفظ عينة من سرعة ضغطاتك للتوثيق
}

alerts_path = os.path.join(base_dir, '..', 'siem_configs', 'live_security_alerts.json')

# قراءة السجلات السابقة إن وجدت لإضافة السجل الجديد لها
if os.path.exists(alerts_path):
    with open(alerts_path, 'r', encoding='utf-8') as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
else:
    logs = []

logs.append(log_entry)

with open(alerts_path, 'w', encoding='utf-8') as f:
    json.dump(logs, f, ensure_ascii=False, indent=4)

print(f"\n📝 تم حفظ النتيجة وأرشفة الحادثة أمنياً في:\n{alerts_path}")