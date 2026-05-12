import streamlit as st
import time

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="FocusFlow Pro", 
    page_icon="🌊", 
    layout="wide"
)

# --- 2. تنسيق الألوان والشكل (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #38bdf8; color: #000; font-weight: bold; }
    .status-box { 
        padding: 20px; 
        border-radius: 15px; 
        background-color: #1e293b; 
        text-align: center; 
        border: 1px solid #38bdf8;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام تخزين البيانات (Session State) ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'xp' not in st.session_state:
    st.session_state.xp = 0

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.title("⚙️ الإعدادات والتحفيز")
    st.metric(label="مستوى الخبرة (XP) 🔥", value=st.session_state.xp)
    
    st.divider()
    st.subheader("🎧 موسيقى التركيز")
    sound = st.selectbox("اختر الصوت المحفز:", ["بدون", "أصوات مطر 🌧️", "لوفاي هادئ ☕", "غابة طبيعية 🍃"])
    
    if sound != "بدون":
        st.info(f"تم تفعيل {sound} استمتع بالهدوء..")

# --- 5. الجزء الرئيسي للموقع ---
st.title("FocusFlow 🌊")
st.markdown("#### موقعك الذكي لتنظيم الدراسة وزيادة الإنتاجية")

# --- 6. قسم الإحصائيات (اللوحة العلوية) ---
col_a, col_b, col_c = st.columns(3)
with col_a:
    completed = len([t for t in st.session_state.tasks if t['done']])
    st.markdown(f'<div class="status-box"><b>المهام المكتملة</b><br><span style="font-size:25px;">{completed}</span></div>', unsafe_allow_html=True)
with col_b:
    total = len(st.session_state.tasks)
    progress = (completed / total) if total > 0 else 0
    st.markdown(f'<div class="status-box"><b>نسبة الإنجاز</b><br><span style="font-size:25px;">{int(progress*100)}%</span></div>', unsafe_allow_html=True)
with col_c:
    st.markdown('<div class="status-box"><b>الرتبة الحالية</b><br><span style="font-size:25px;">مبتدئ 🌟</span></div>', unsafe_allow_html=True)

st.divider()

# --- 7. قسم إضافة المهام الجديدة ---
st.subheader("➕ إضافة مهمة دراسية جديدة")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    task_name = st.text_input("اسم المهمة", placeholder="مثلاً: حل شيت الرياضيات")
with col2:
    category = st.selectbox("المادة", ["عام", "رياضيات", "برمجة", "لغات", "علوم"])
with col3:
    priority = st.select_slider("الأولوية", options=["منخفضة", "متوسطة", "عالية"])

if st.button("إضافة المهمة للجدول ✅"):
    if task_name:
        st.session_state.tasks.append({
            "name": task_name, 
            "cat": category, 
            "pri": priority, 
            "done": False
        })
        st.success("تمت الإضافة بنجاح!")
        time.sleep(0.5)
        st.rerun()

# --- 8. عرض قائمة المهام اليومية ---
st.subheader("📅 جدولك لليوم")
if not st.session_state.tasks:
    st.info("لا توجد مهام حالياً. ابدأ بإضافة مهامك!")
else:
    for i, t in enumerate(st.session_state.tasks):
        c1, c2, c3, c4 = st.columns([0.1, 0.5, 0.2, 0.2])
        
        # خانة الاختيار لإتمام المهمة
        done = c1.checkbox("", value=t['done'], key=f"task_{i}")
        if done != t['done']:
            st.session_state.tasks[i]['done'] = done
            st.session_state.xp += 10 if done else -10
            st.rerun()
            
        # تنسيق النص (شطب المهمة لو مكتملة)
        text = f"~~{t['name']}~~" if t['done'] else t['name']
        c2.write(f"**{text}** ({t['cat']})")
        
        # عرض الأولوية
        p_color = "🔴" if t['pri'] == "عالية" else "🟡" if t['pri'] == "متوسطة" else "🟢"
        c3.write(f"{p_color} {t['pri']}")
        
        # زر الحذف
        if c4.button("حذف 🗑️", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 9. مؤقت التركيز (Pomodoro) ---
st.divider()
st.header("⏳ مؤقت التركيز الذكي")
p_col1, p_col2 = st.columns([1, 2])

with p_col1:
    timer_minutes = st.number_input("حدد دقائق التركيز:", min_value=1, max_value=120, value=25)

with p_col2:
    if st.button("🚀 ابدأ جلسة التركيز الآن"):
        st.warning("الرجاء عدم إغلاق الصفحة أثناء العد!")
        with st.empty():
            for seconds in range(timer_minutes * 60, 0, -1):
                mins, secs = divmod(seconds, 60)
                st.header(f"⏱️ المتبقي: {mins:02d}:{secs:02d}")
                time.sleep(1)
            st.success("🎉 أحسنت! انتهت الجلسة. خذ راحة قصيرة الآن.")
            st.balloons()

# --- 10. تذييل الصفحة ---
st.divider()
st.caption("تم التطوير بواسطة خبير البرمجة لـ FocusFlow 🌊 - 2026")
