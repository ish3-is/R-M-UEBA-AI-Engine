import pandas as pd
import os
import json
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 1. استدعاء البيانات
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '..', 'data', 'raw', 'DSL-StrongPasswordData.csv')
df = pd.read_csv(file_path)

# 2. تجهيز البيانات (التعلم الخاضع للإشراف)
target_user = 's002'
features = df.columns[3:]

# تصنيف البيانات: 1 للموظف الحقيقي، 0 للمخترقين (باقي المستخدمين)
df['label'] = (df['subject'] == target_user).astype(int)

# أخذ عينة متوازنة عشان الخوارزمية تتعلم صح (400 محاولة للموظف، و 400 محاولة للمخترقين)
legit_data = df[df['label'] == 1]
intruder_data = df[df['label'] == 0].sample(400, random_state=42)

# دمج البيانات وفصلها (70% للتدريب و 30% للاختبار)
final_data = pd.concat([legit_data, intruder_data])
X = final_data[features]
y = final_data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. بناء وتدريب النظام (Random Forest)
print("🤖 جاري تدريب النظام بذكاء عالي (Random Forest)...")
# الخوارزمية بتصنع 100 شجرة قرار عشان تصوت على النتيجة النهائية
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. الاختبار وفحص النتائج
print("🔍 جاري اختبار محاولات الدخول...\n")

test_results = pd.DataFrame(X_test)
test_results['Actual'] = y_test
test_results['Predicted'] = model.predict(X_test)

# فصلنا نتائج الموظف عن نتائج المخترقين عشان نحسب الدقة لكل واحد
legit_test = test_results[test_results['Actual'] == 1]
intruder_test = test_results[test_results['Actual'] == 0]

legit_accuracy = (legit_test['Predicted'] == 1).mean() * 100
intruder_accuracy = (intruder_test['Predicted'] == 0).mean() * 100

# 5. طباعة النتائج
print("--- 🎯 نتائج كشف الاختراق (Random Forest) ---")
print(f"✅ نسبة السماح للمستخدم الحقيقي بالدخول: {legit_accuracy:.2f}%")
print(f"🚨 نسبة كشف وطرد المخترقين بنجاح: {intruder_accuracy:.2f}%")
# 6. تصدير التنبيهات لنظام الـ SIEM
print("\n📝 جاري إنشاء ملف سجلات التنبيهات (Logs) للـ SIEM...")

# استخراج محاولات الدخول اللي صنفها النظام كـ "اختراق" (0)
alerts = intruder_test[intruder_test['Predicted'] == 0].copy()

# تحويلها لصيغة JSON يقرأها Splunk أو ELK
alert_logs = []
for index, row in alerts.iterrows():
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "UEBA_Keystroke_Anomaly",
        "severity": "CRITICAL",
        "user_account": target_user,
        "description": "تم رصد سرعة كتابة غير مطابقة للبصمة الحركية للمستخدم الحقيقي.",
        "action": "Blocked_and_Alerted"
    }
    alert_logs.append(log_entry)

# حفظ الملف في مجلد siem_configs
alerts_path = os.path.join(base_dir, '..', 'siem_configs', 'security_alerts.json')
with open(alerts_path, 'w', encoding='utf-8') as f:
    json.dump(alert_logs, f, ensure_ascii=False, indent=4)

print(f"✅ تم تصدير {len(alert_logs)} تنبيه أمني بنجاح في المسار:\n{alerts_path}")