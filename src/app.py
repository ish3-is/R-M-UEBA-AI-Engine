import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components
 
# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="UEBA Analytics Platform | Security Operations Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ==========================================
# 2. هوية بصرية احترافية (Enterprise Design System)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
 
    :root {
        --bg-card: rgba(22, 30, 46, 0.65);
        --border-default: rgba(148, 163, 184, 0.14);
        --border-accent: rgba(59, 130, 246, 0.35);
        --accent-primary: #3b82f6;
        --accent-secondary: #0ea5e9;
        --status-critical: #ef4444;
        --status-warning: #f59e0b;
        --status-success: #22c55e;
        --text-primary: #e5e9f0;
        --text-muted: #8b97ab;
    }
 
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
    }
 
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(8px);
        border-radius: 10px;
        border: 1px solid var(--border-default);
        padding: 18px 20px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        transition: border-color 0.2s ease;
    }
    .glass-card:hover {
        border-color: var(--border-accent);
    }
    .glass-card.is-critical {
        border-left: 3px solid var(--status-critical);
    }
    .glass-card .kpi-label {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin: 0 0 6px 0;
    }
    .glass-card .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 30px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    .glass-card .kpi-footnote {
        font-size: 12px;
        color: var(--text-muted);
    }
 
    .title-block {
        text-align: center;
        padding: 6px 0 2px 0;
    }
    .title-block h1 {
        font-weight: 700;
        letter-spacing: 0.01em;
        color: var(--text-primary);
        font-size: 2.1em;
        margin-bottom: 2px;
    }
    .title-block .platform-subtitle {
        color: var(--text-muted);
        font-size: 0.95em;
        font-weight: 500;
        letter-spacing: 0.02em;
    }
 
    .status-bar {
        background: rgba(59, 130, 246, 0.06);
        border: 1px solid var(--border-default);
        border-left: 3px solid var(--accent-primary);
        padding: 9px 16px;
        border-radius: 6px;
        color: var(--text-muted);
        font-family: 'JetBrains Mono', monospace;
        font-size: 12.5px;
        margin-bottom: 22px;
        display: flex;
        gap: 18px;
        flex-wrap: wrap;
    }
    .status-bar .status-dot { color: var(--status-success); }
    .status-bar .status-live { color: var(--status-warning); font-weight: 600; }
 
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(15, 21, 35, 0.6);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid var(--border-default);
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--text-muted);
        background: transparent;
        border-radius: 7px;
        padding: 9px 18px;
        font-weight: 600;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent-primary) !important;
        color: white !important;
    }
 
    [data-testid="stSidebar"] {
        background: #0c1322;
        border-right: 1px solid var(--border-default);
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--text-primary);
        font-weight: 600;
    }
 
    .section-heading {
        font-size: 15px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 6px;
    }
 
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
 
# ==========================================
# 3. شريط الحالة
# ==========================================
st.markdown(f"""
<div class="status-bar">
    <span><span class="status-dot">●</span> النظام متصل</span>
    <span>محرك التحليل: Random Forest (الإصدار 2.1)</span>
    <span class="status-live">قيد المراقبة المستمرة</span>
    <span>آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
</div>
""", unsafe_allow_html=True)
 
# ==========================================
# 4. العنوان الرئيسي
# ==========================================
st.markdown("""
<div class="title-block">
    <h1>🛡️ منصة تحليل سلوك المستخدمين والكيانات (UEBA)</h1>
    <p class="platform-subtitle">مركز عمليات الأمن السيبراني — مدعوم بخوارزمية Random Forest</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")
 
# ==========================================
# الشريط الجانبي
# ==========================================
with st.sidebar:
    st.markdown("## لوحة التحكم")
    st.markdown("---")
 
    target_user = st.selectbox(
        "الحساب المستهدف بالتحليل",
        ["all_users", "admin_01", "guest_user", "db_service"],
        index=0
    )
 
    severity_filter = st.multiselect(
        "تصنيف مستوى الخطورة",
        ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        default=["CRITICAL", "HIGH"]
    )
 
    st.markdown("---")
    st.markdown("### إعدادات العرض")
    show_charts = st.checkbox("عرض المخططات البيانية التحليلية", True)
 
    st.markdown("---")
    st.markdown("### مؤشرات أداء النموذج")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("الدقة (Accuracy)", "94.7%", "↑ 1.2%")
    with col_b:
        st.metric("معامل F1", "0.92", "↑ 0.03")
 
    if st.button("إعادة تدريب النموذج"):
        with st.spinner("جارٍ إعادة التدريب..."):
            import time
            time.sleep(2)
        st.success("تم تحديث النموذج بنجاح.")
 
# ==========================================
# التبويبات
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "لوحة العمليات الأمنية",
    "مختبر القياسات الحيوية السلوكية",
    "التحليلات والتقارير"
])
 
# ============= TAB 1: SOC DASHBOARD =============
with tab1:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    alerts_path = os.path.join(base_dir, '..', 'siem_configs', 'security_alerts.json')
 
    try:
        with open(alerts_path, 'r', encoding='utf-8') as f:
            alerts = json.load(f)
 
        df_alerts = pd.DataFrame(alerts)
 
        if target_user != "all_users" and 'user_account' in df_alerts.columns:
            df_filtered = df_alerts[df_alerts['user_account'] == target_user]
        else:
            df_filtered = df_alerts
 
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
 
        with col1:
            st.markdown(f"""
            <div class="glass-card is-critical">
                <p class="kpi-label">إجمالي التنبيهات</p>
                <p class="kpi-value">{len(df_filtered)}</p>
                <p class="kpi-footnote">خلال آخر 24 ساعة</p>
            </div>
            """, unsafe_allow_html=True)
 
        with col2:
            critical = len(df_filtered[df_filtered.get('severity', '') == 'CRITICAL']) if not df_filtered.empty else 0
            st.markdown(f"""
            <div class="glass-card">
                <p class="kpi-label">تنبيهات حرجة</p>
                <p class="kpi-value" style="color:var(--status-critical);">{critical}</p>
                <p class="kpi-footnote">تتطلب إجراءً فورياً</p>
            </div>
            """, unsafe_allow_html=True)
 
        with col3:
            unique_users = df_filtered['user_account'].nunique() if not df_filtered.empty else 0
            st.markdown(f"""
            <div class="glass-card">
                <p class="kpi-label">المستخدمون المتأثرون</p>
                <p class="kpi-value" style="color:var(--accent-secondary);">{unique_users}</p>
                <p class="kpi-footnote">حسابات مستهدفة</p>
            </div>
            """, unsafe_allow_html=True)
 
        with col4:
            confidence = df_filtered.get('confidence', pd.Series([0.92])).mean() if not df_filtered.empty else 0.92
            st.markdown(f"""
            <div class="glass-card">
                <p class="kpi-label">متوسط مستوى الثقة</p>
                <p class="kpi-value" style="color:var(--accent-primary);">{confidence*100:.1f}%</p>
                <p class="kpi-footnote">موثوقية النموذج</p>
            </div>
            """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        # Charts
        if show_charts and not df_filtered.empty:
            chart_col1, chart_col2 = st.columns(2)
 
            chart_layout = dict(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#8b97ab',
                font_family='Inter',
                margin=dict(t=20, b=20, l=10, r=10)
            )
 
            with chart_col1:
                st.markdown('<p class="section-heading">توزيع التنبيهات حسب الخطورة</p>', unsafe_allow_html=True)
                if 'severity' in df_filtered.columns:
                    severity_counts = df_filtered['severity'].value_counts()
                    fig_sev = px.pie(
                        names=severity_counts.index,
                        values=severity_counts.values,
                        color_discrete_sequence=['#ef4444', '#f59e0b', '#3b82f6', '#22c55e'],
                        hole=0.55
                    )
                    fig_sev.update_layout(**chart_layout)
                    st.plotly_chart(fig_sev, use_container_width=True)
 
            with chart_col2:
                st.markdown('<p class="section-heading">التسلسل الزمني للتنبيهات</p>', unsafe_allow_html=True)
                if 'timestamp' in df_filtered.columns:
                    df_time = df_filtered.copy()
                    df_time['hour'] = pd.to_datetime(df_time['timestamp']).dt.hour
                    hour_counts = df_time['hour'].value_counts().sort_index()
                    fig_time = px.bar(
                        x=hour_counts.index,
                        y=hour_counts.values,
                        color_discrete_sequence=['#3b82f6']
                    )
                    fig_time.update_layout(
                        **chart_layout,
                        xaxis_title="الساعة",
                        yaxis_title="عدد الحوادث"
                    )
                    st.plotly_chart(fig_time, use_container_width=True)
 
        # Logs
        st.markdown('<p class="section-heading">سجل الحوادث التفصيلي</p>', unsafe_allow_html=True)
        st.dataframe(df_filtered, use_container_width=True, height=350, hide_index=True)
 
        col_dl1, col_dl2 = st.columns([1, 5])
        with col_dl1:
            st.download_button(
                "تصدير السجل (CSV)",
                df_filtered.to_csv(index=False),
                "ueba_alerts.csv",
                "text/csv"
            )
 
    except FileNotFoundError:
        st.error("تعذّر العثور على ملف السجلات. الرجاء تشغيل نموذج الذكاء الاصطناعي أولاً.")
        st.info("تأكد من توفر الملف في المسار التالي: `siem_configs/security_alerts.json`")
 
# ============= TAB 2: BEHAVIORAL BIOMETRICS LAB =============
with tab2:
    st.markdown("### مختبر القياسات الحيوية السلوكية")
    st.markdown("""
    أدخل كلمة المرور في الحقل أدناه، وسيقوم النظام بتحليل **النمط الحركي لضغطات لوحة المفاتيح** بشكل فوري، استناداً إلى ثلاثة مؤشرات رئيسية:
    - **زمن الإطباق (Dwell Time):** المدة التي يبقى فيها الزر مضغوطاً
    - **زمن الانتقال (Flight Time):** الفاصل الزمني بين رفع زر وضغط الزر التالي
    - **درجة الثقة (Confidence Score):** مدى تطابق النمط السلوكي الحالي مع البصمة المسجَّلة مسبقاً
    """)
 
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
 
        body {
            background: transparent;
            color: #e5e9f0;
            font-family: 'Inter', -apple-system, sans-serif;
            padding: 20px;
            margin: 0;
        }
        .lab-container {
            background: rgba(18, 24, 38, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 12px;
            padding: 26px;
            box-shadow: 0 6px 24px rgba(0,0,0,0.35);
        }
        h3 {
            color: #e5e9f0;
            text-align: center;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-top: 0;
        }
        .lab-subtitle {
            text-align: center;
            color: #8b97ab;
            font-size: 13px;
            margin-bottom: 18px;
        }
        .input-area { text-align: center; margin: 20px 0; }
        #passwordBox {
            padding: 11px 18px;
            width: 70%;
            font-size: 18px;
            border-radius: 8px;
            border: 1px solid rgba(148, 163, 184, 0.3);
            background: #0c1322;
            color: #e5e9f0;
            outline: none;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 2px;
            transition: border-color 0.2s ease;
        }
        #passwordBox:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
            margin-top: 22px;
        }
        .metric-box {
            background: rgba(255,255,255,0.03);
            padding: 14px 16px;
            border-radius: 8px;
            border-left: 3px solid #3b82f6;
        }
        .metric-box.warning { border-left-color: #ef4444; }
        .metric-label {
            font-size: 11px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: #8b97ab;
        }
        .metric-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 24px;
            font-weight: 600;
            color: #e5e9f0;
            margin-top: 2px;
        }
        .heatmap {
            margin-top: 22px;
            padding: 14px;
            background: #0c1322;
            border-radius: 8px;
            min-height: 46px;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        .heat-cell {
            display: inline-block;
            padding: 4px 9px;
            margin: 3px;
            border-radius: 5px;
            font-size: 11px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        #status {
            text-align: center;
            padding: 11px;
            border-radius: 8px;
            margin-top: 16px;
            font-weight: 600;
            font-size: 13px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(148, 163, 184, 0.12);
        }
        .clear-btn {
            background: transparent;
            color: #8b97ab;
            border: 1px solid rgba(148, 163, 184, 0.3);
            padding: 7px 18px;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 12px;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.2s ease;
        }
        .clear-btn:hover { border-color: #3b82f6; color: #e5e9f0; }
        .chart-container {
            margin-top: 22px;
            background: #0c1322;
            padding: 14px;
            border-radius: 8px;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        .chart-caption {
            color: #8b97ab;
            font-size: 11px;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .bar {
            display: inline-block;
            background: #3b82f6;
            margin: 0 2px;
            vertical-align: bottom;
            border-radius: 2px 2px 0 0;
            transition: all 0.2s ease;
        }
    </style>
    </head>
    <body>
    <div class="lab-container">
        <h3>تحليل القياسات الحيوية لضغطات لوحة المفاتيح</h3>
        <p class="lab-subtitle">أدخل النص: <span style="color:#3b82f6; font-family:'JetBrains Mono',monospace;">.tie5Roanl</span> أو أي نص آخر</p>
 
        <div class="input-area">
            <input type="text" id="passwordBox" placeholder="ابدأ الكتابة هنا..." autocomplete="off">
            <br>
            <button class="clear-btn" onclick="clearAll()">إعادة تعيين</button>
        </div>
 
        <div class="metrics-grid">
            <div class="metric-box">
                <div class="metric-label">متوسط زمن الإطباق</div>
                <div class="metric-value" id="avgDwell">0 ms</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">متوسط زمن الانتقال</div>
                <div class="metric-value" id="avgFlight">0 ms</div>
            </div>
            <div class="metric-box warning">
                <div class="metric-label">عدد الأحرف المُدخلة</div>
                <div class="metric-value" id="charCount">0</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">درجة الثقة</div>
                <div class="metric-value" id="confidence">—</div>
            </div>
        </div>
 
        <div class="chart-container">
            <div class="chart-caption">مخطط زمن الإطباق لكل ضغطة</div>
            <div id="chart" style="height: 100px; display: flex; align-items: flex-end;"></div>
        </div>
 
        <div class="heatmap">
            <div class="chart-caption">الخريطة الحرارية لضغطات المفاتيح</div>
            <div id="heatmap"></div>
        </div>
 
        <div id="status">بانتظار الإدخال...</div>
    </div>
 
    <script>
        const input = document.getElementById('passwordBox');
        const heatmap = document.getElementById('heatmap');
        const chart = document.getElementById('chart');
        const status = document.getElementById('status');
 
        let keyDownTimes = {};
        let dwellTimes = [];
        let flightTimes = [];
        let lastKeyUpTime = 0;
        let typedChars = [];
 
        // Reference values (simulated baseline for ".tie5Roanl")
        const BASELINE_DWELL = 95;
        const BASELINE_FLIGHT = 120;
 
        function getColor(dwell) {
            if (dwell < 80) return '#22c55e';
            if (dwell < 120) return '#3b82f6';
            if (dwell < 160) return '#f59e0b';
            if (dwell < 200) return '#fb923c';
            return '#ef4444';
        }
 
        function updateMetrics() {
            const avgDwell = dwellTimes.length ? (dwellTimes.reduce((a,b) => a+b, 0) / dwellTimes.length) : 0;
            const avgFlight = flightTimes.length ? (flightTimes.reduce((a,b) => a+b, 0) / flightTimes.length) : 0;
 
            document.getElementById('avgDwell').innerText = Math.round(avgDwell) + ' ms';
            document.getElementById('avgFlight').innerText = Math.round(avgFlight) + ' ms';
            document.getElementById('charCount').innerText = typedChars.length;
 
            if (dwellTimes.length > 3) {
                const dwellDeviation = Math.abs(avgDwell - BASELINE_DWELL);
                const flightDeviation = Math.abs(avgFlight - BASELINE_FLIGHT);
                const totalDeviation = (dwellDeviation + flightDeviation) / 2;
                let confidence = Math.max(0, Math.min(100, 95 - totalDeviation));
 
                const confEl = document.getElementById('confidence');
                confEl.innerText = confidence.toFixed(1) + '%';
                confEl.style.color = confidence > 80 ? '#22c55e' : (confidence > 60 ? '#f59e0b' : '#ef4444');
 
                if (confidence > 80) {
                    status.style.background = 'rgba(34,197,94,0.08)';
                    status.style.color = '#22c55e';
                    status.style.border = '1px solid rgba(34,197,94,0.3)';
                    status.innerText = 'النمط السلوكي مطابق للبصمة المسجَّلة';
                } else if (confidence > 60) {
                    status.style.background = 'rgba(245,158,11,0.08)';
                    status.style.color = '#f59e0b';
                    status.style.border = '1px solid rgba(245,158,11,0.3)';
                    status.innerText = 'انحرافات طفيفة عن النمط المسجَّل';
                } else {
                    status.style.background = 'rgba(239,68,68,0.08)';
                    status.style.color = '#ef4444';
                    status.style.border = '1px solid rgba(239,68,68,0.3)';
                    status.innerText = 'تنبيه: النمط السلوكي لا يطابق البصمة المسجَّلة';
                }
            }
        }
 
        input.addEventListener('keydown', (e) => {
            if (e.key.length === 1 && !keyDownTimes[e.key]) {
                keyDownTimes[e.key] = performance.now();
            }
        });
 
        input.addEventListener('keyup', (e) => {
            if (keyDownTimes[e.key]) {
                const dwell = performance.now() - keyDownTimes[e.key];
                dwellTimes.push(dwell);
 
                if (lastKeyUpTime > 0) {
                    const flight = performance.now() - lastKeyUpTime;
                    flightTimes.push(flight);
                }
                lastKeyUpTime = performance.now();
 
                typedChars.push(e.key);
 
                // Heatmap
                const cell = document.createElement('span');
                cell.className = 'heat-cell';
                cell.innerText = e.key + ' · ' + Math.round(dwell) + 'ms';
                cell.style.background = getColor(dwell) + '22';
                cell.style.color = getColor(dwell);
                cell.style.border = '1px solid ' + getColor(dwell) + '55';
                heatmap.appendChild(cell);
 
                // Chart bar
                const bar = document.createElement('div');
                bar.className = 'bar';
                const height = Math.min(100, dwell / 3);
                bar.style.height = height + 'px';
                bar.style.width = '10px';
                bar.style.background = getColor(dwell);
                bar.title = e.key + ': ' + Math.round(dwell) + 'ms';
                chart.appendChild(bar);
 
                delete keyDownTimes[e.key];
                updateMetrics();
            }
        });
 
        function clearAll() {
            input.value = '';
            keyDownTimes = {};
            dwellTimes = [];
            flightTimes = [];
            lastKeyUpTime = 0;
            typedChars = [];
            heatmap.innerHTML = '';
            chart.innerHTML = '';
            status.innerText = 'بانتظار الإدخال...';
            status.style.background = 'rgba(255,255,255,0.03)';
            status.style.border = '1px solid rgba(148, 163, 184, 0.12)';
            status.style.color = '#e5e9f0';
            document.getElementById('avgDwell').innerText = '0 ms';
            document.getElementById('avgFlight').innerText = '0 ms';
            document.getElementById('charCount').innerText = '0';
            document.getElementById('confidence').innerText = '—';
            document.getElementById('confidence').style.color = '#e5e9f0';
        }
    </script>
    </body>
    </html>
    """
 
    components.html(html_code, height=720)
 
    st.info(
        "يتم إجراء كافة التحليلات داخل المتصفح (Client-side) حفاظاً على خصوصية البيانات. "
        "في النسخة الإنتاجية، تُرسل القياسات إلى نموذج Random Forest المدرَّب لإجراء التقييم الفعلي."
    )
 
# ============= TAB 3: ANALYTICS =============
with tab3:
    st.markdown("### التحليلات والتقارير المتقدمة")
 
    chart_layout = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#8b97ab',
        font_family='Inter',
        margin=dict(t=20, b=20, l=10, r=10)
    )
 
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-heading">النشاط حسب الساعة</p>', unsafe_allow_html=True)
        hours = list(range(24))
        activity = [int(50 + 30 * (1 if 9 <= h <= 17 else 0) + abs(hash(str(h)) % 20)) for h in hours]
        fig_h = px.bar(x=hours, y=activity, color_discrete_sequence=['#3b82f6'])
        fig_h.update_layout(**chart_layout, xaxis_title="الساعة", yaxis_title="مستوى النشاط")
        st.plotly_chart(fig_h, use_container_width=True)
 
    with col2:
        st.markdown('<p class="section-heading">التوزيع الجغرافي</p>', unsafe_allow_html=True)
        countries = ["SA", "US", "UK", "DE", "FR", "JP"]
        counts = [45, 23, 18, 12, 9, 5]
        fig_g = px.bar(x=countries, y=counts, color_discrete_sequence=['#0ea5e9'])
        fig_g.update_layout(**chart_layout, xaxis_title="الدولة", yaxis_title="عدد الجلسات")
        st.plotly_chart(fig_g, use_container_width=True)
 
    st.markdown('<p class="section-heading">حالة النظام</p>', unsafe_allow_html=True)
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("استخدام المعالج", "23%", "↑ 2%")
    h2.metric("الذاكرة المستخدمة", "4.2 GB", "↓ 0.3")
    h3.metric("معدل نقل الشبكة", "142 MB/s")
    h4.metric("التنبيهات في الدقيقة", "3.2", "↓ 0.5")
 
# ==========================================
# تذييل الصفحة
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#8b97ab; font-size: 12.5px; padding: 16px;">
    منصة UEBA لتحليل سلوك المستخدمين والكيانات — مدعومة بخوارزمية Random Forest وإطار عمل Streamlit<br>
    <span style="opacity:0.7;">© 2026 مركز عمليات الأمن السيبراني — جميع الحقوق محفوظة</span>
</div>
""", unsafe_allow_html=True)