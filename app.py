import streamlit as st
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="FocusFlow Pro", page_icon="🌊", layout="wide")

# --- تنسيق CSS إضافي لتحسين الشكل ---
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stButton>button { width: 100%; border-radius: 20px; }
    .status-box { padding: 20px; border-radius: 15px; background-color: #1e293b; text-align: center; }
    </style>
    """, unsafe_allow_status=True)

# --- نظام المخزن (Session State) ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.title("⚙️ الإعدادات والتحفيز")
    st.metric(label="مستوى الخبرة (XP) 🔥", value=st.session_state.xp)
    
    st.divider()
    st.subheader("🎧 موسيقى التركيز")
    sound = st.selectbox("اختر الصوت المحفز:", ["بدون", "أصوات مطر 🌧️", "لوفاي هادئ ☕", "غابة طبيعية 🍃"])
    
    # روابط وهمية كمثال (تقدر تحط روابط يوتيوب حقيقية هنا لاحقاً)
    if "مطر" in sound: st.write("🎵 تشغيل صوت المطر الهادئ...")
    elif "لوفاي" in sound: st.write("🎵 تشغيل موسيقى لوفاي...")

# --- الجزء الرئيسي للموقع ---
st.title("FocusFlow 🌊")
st.write(f"مرحباً بك! لديك {len([t for t in st.session_state.tasks if not t['done']])} مهام متبقية اليوم.")

# --- قسم الإحصائيات السريع ---
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown('<div class="status-box"><b>المهام المكتملة</b><br>'+str(len([t for t in st.session_state.tasks if t['done']]))+'</div>', unsafe_allow_status=True)
with col_b:
    progress = len([t for t in st.session_state.tasks if t['done']]) / len(st.session_state.tasks) if st.session_state.tasks else 0
    st.markdown('<div class="status-box"><b>نسبة الإنجاز</b><br>'+str(int(progress*100))+'%</div>', unsafe_allow_status=True)
with col_c:
    st.markdown('<div class="status-box"><b>ساعات التركيز</b><br>0.5h</div>', unsafe_allow_status=True)

st.divider()

# --- إضافة المهام ---
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    task_name = st.text_input("", placeholder="ما هي المهمة القادمة؟")
with col2:
    category = st.selectbox("المادة:", ["عام", "رياضيات", "برمجة", "لغات"])
with col3:
    priority = st.select_slider("الأولوية:", options=["Low", "Med", "High"])

if st.button("إضافة للمخطط ➕"):
    if task_name:
        st.session_state.tasks.append({"name": task_name, "cat": category, "pri": priority, "done": False})
        st.rerun()

# --- عرض المهام بتصميم احترافي ---
st.subheader("📝 جدول المهام اليومي")
for i, t in enumerate(st.session_state.tasks):
    c1, c2, c3, c4 = st.columns([0.1, 0.5, 0.2, 0.2])
    
    done = c1.checkbox("", value=t['done'], key=f"task_{i}")
    if done != t['done']:
        t['done'] = done
        st.session_state.xp += 10 if done else -10 # زيادة XP عند الإنجاز
        st.rerun()
        
    text = f"~~{t['name']}~~" if t['done'] else t['name']
    c2.write(f"**{text}** ({t['cat']})")
    
    color = "🔴" if t['pri'] == "High" else "🟡" if t['pri'] == "Med" else "🟢"
    c3.write(f"الأولوية: {color}")
    
    if c4.button("حذف 🗑️", key=f"del_{i}"):
        st.session_state.tasks.pop(i)
        st.rerun()

# --- مؤقت البومودورو المطور ---
st.divider()
st.header("⏳ وقت الجد (Pomodoro)")
p_col1, p_col2 = st.columns([1, 2])
with p_col1:
    timer_time = st.number_input("دقائق التركيز:", value=25)
with p_col2:
    if st.button("ابدأ جلسة التركيز الآن"):
        with st.empty():
            for seconds in range(timer_time * 60, 0, -1):
                mins, secs = divmod(seconds, 60)
                st.header(f"⏱️ المتبقي: {mins:02d}:{secs:02d}")
                time.sleep(1)
            st.success("🎉 انتهت الجلسة! خذ راحة 5 دقائق.")
            st.balloons()
