import time
from pynput import keyboard

print("🛡️ بدء تشغيل وكيل الحماية (Defensive Keystroke Agent)...")
print("👀 النظام الآن يراقب بصمتك الحركية في الخلفية (اضغط ESC للإيقاف).")
print("-" * 50)

# قواميس لتخزين أوقات الضغط والرفع
key_press_times = {}
key_release_times = {}
last_release_time = None

def on_press(key):
    global last_release_time
    current_time = time.time()
    
    # تسجيل وقت الضغطة
    if key not in key_press_times:
        key_press_times[key] = current_time
    
    # حساب Flight Time (زمن الانتقال من الحرف السابق للحرف الحالي)
    if last_release_time is not None:
        flight_time = (current_time - last_release_time) * 1000 # تحويل للملي ثانية
        # نتجاهل الأوقات الطويلة جداً (يعني المستخدم وقف كتابة)
        if flight_time < 2000: 
            pass # هنا يتم إرسال البيانات لخوارزمية الذكاء الاصطناعي في النظام الحقيقي

def on_release(key):
    global last_release_time
    current_time = time.time()
    last_release_time = current_time
    
    # حساب Dwell Time (مدة بقاء الإصبع على الزر)
    if key in key_press_times:
        press_time = key_press_times[key]
        dwell_time = (current_time - press_time) * 1000 # تحويل للملي ثانية
        
        try:
            char = key.char if hasattr(key, 'char') else str(key)
            # طباعة السلوك الحي للمحلل الأمني (في الواقع يتم إرسالها للـ Model بصمت)
            print(f"[+] الزر: {char: <10} | مدة الضغطة (Dwell): {dwell_time:.2f} ms")
        except AttributeError:
            pass
            
        # مسح الزر من القاموس استعداداً للضغطة القادمة
        del key_press_times[key]
    
    # إيقاف البرنامج إذا ضغط المستخدم ESC
    if key == keyboard.Key.esc:
        print("🛑 تم إيقاف وكيل الحماية.")
        return False

# تشغيل المستمع (Listener) في الخلفية
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()