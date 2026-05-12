import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow", page_icon="🎓", layout="wide")

# --- 2. ملف المتطلبات التجميلية CSS ---
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stProgress > div > div > div > div { background-color: #10b981; }
    .quote-box { padding: 20px; border-radius: 10px; border-left: 5px solid #38bdf8; background: #1e293b; margin-bottom: 20px; }
    .challenge-box { padding: 15px; border-radius: 10px; background: linear-gradient(90deg, #4f46e5, #3b82f6); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام تخزين البيانات ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'daily_goal' not in st.session_state: st.session_state.daily_goal = ""

# --- 4. محتوى عشوائي (تحفيز وتحديات) ---
quotes = [
    "النجاح هو مجموع جهود صغيرة تتكرر يوماً بعد يوم.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "لا تتوقف عندما تتعب، توقف عندما تنتهي.",
    "Believe you can and you're halfway there."
]

challenges = [
    "تحدي اليوم: ذاكر لمدة 50 دقيقة بدون لمس الهاتف! (الجائزة: 50 XP)",
    "Today's Challenge: Study for 50 mins without phone! (Reward: 50 XP)",
    "تحدي اليوم: أنهِ أصعب مهمة في جدولك أولاً! (الجائزة: 30 XP)"
]

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.title("🎓 Study Flow")
    st.subheader("XP: " + str(st.session_state.xp))
    
    st.divider()
    # جزء الأهداف اليومية
    st.session_state.daily_goal = st.text_area("🎯 هدفك اليومي / Daily Goal", value=st.session_state.daily_goal)
    
    st.divider()
    st.write("💡 **نصيحة الإنتاجية:**")
    st.caption("أفضل وقت للمذاكرة الصعبة هو بين 8 صباحاً و 11 صباحاً حيث يكون التركيز في قمته.")
    
    st.divider()
    lang = st.radio("Language / اللغة", ["العربية", "English"])

# --- 6. الواجهة الرئيسية ---
st.markdown(f'<div class="quote-box"><i>{random.choice(quotes)}</i></div>', unsafe_allow_html=True)

# عرض التحدي اليومي
st.markdown(f'<div class="challenge-box">🏆 {random.choice(challenges)}</div>', unsafe_allow_html=True)

st.title("لوحة الإنجاز / Dashboard")

# --- 7. الرسم البياني الدائري (Chart) ---
col_chart, col_info = st.columns([1, 1])

with col_chart:
    done_count = len([t for t in st.session_state.tasks if t['done']])
    pending_count = len(st.session_state.tasks) - done_count
    
    if len(st.session_state.tasks) > 0:
        fig = go.Figure(data=[go.Pie(labels=['Done', 'Pending'], 
                             values=[done_count, pending_count], 
                             hole=.6, 
                             marker_colors=['#10b981', '#ef4444'])])
        fig.update_layout(showlegend=False, height=300, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("أضف مهام لرؤية تقدمك / Add tasks to see progress")

with col_info:
    st.subheader("التذكير بالمهام 🔔")
    for t in st.session_state.tasks:
        if not t['done'] and t['pri'] == "High":
            st.warning(f"تذكير: لا تنسَ إنهاء {t['name']} (أولوية عالية!)")

st.divider()

# --- 8. إضافة المهام ---
st.subheader("➕ إضافة مهمة / Add Task")
c1, c2, c3, c4 = st.columns([2, 1, 1, 1])

with c1: t_name = st.text_input("المهمة / Task")
with c2: t_subject = st.text_input("المادة / Subject")
with c3: t_deadline = st.date_input("الموعد / Deadline")
with c4: t_pri = st.radio("الأولوية / Priority", ["High", "Med", "Low"], horizontal=True)

if st.button("حفظ المهمة / Save"):
    if t_name:
        st.session_state.tasks.append({
            "name": t_name, "sub": t_subject, "deadline": t_deadline, 
            "pri": t_pri, "done": False
        })
        st.rerun()

# --- 9. عرض المهام ---
st.subheader("📋 الجدول الحالي / Schedule")
for i, t in enumerate(st.session_state.tasks):
    color = "🔴" if t['pri'] == "High" else "🟡" if t['pri'] == "Med" else "🟢"
    cols = st.columns([0.1, 0.4, 0.2, 0.2, 0.1])
    
    is_done = cols[0].checkbox("", value=t['done'], key=f"chk_{i}")
    if is_done != t['done']:
        st.session_state.tasks[i]['done'] = is_done
        st.session_state.xp += 20 if is_done else -20
        st.rerun()
        
    cols[1].write(f"**{t['name']}** | {t['sub']}")
    cols[2].write(f"📅 {t['deadline']}")
    cols[3].write(f"{color} {t['pri']}")
    if cols[4].button("🗑️", key=f"del_{i}"):
        st.session_state.tasks.pop(i)
        st.rerun()

# --- 10. مؤقت المذاكرة والراحة التلقائي ---
st.divider()
st.header("⏳ مؤقت الدراسة الذكي / Smart Timer")
study_mins = st.number_input("كم دقيقة ستذاكر؟ / Study Mins:", value=30)
break_mins = (study_mins // 30) * 10  # معادلة الراحة التلقائية

st.write(f"💡 نظامنا خصص لك **{break_mins} دقائق راحة** بعد هذه الجلسة.")

if st.button("ابدأ الآن / Start Now"):
    # وقت المذاكرة
    with st.empty():
        for s in range(study_mins * 60, 0, -1):
            m, sec = divmod(s, 60)
            st.metric("Focus Time ✍️", f"{m:02d}:{sec:02d}")
            time.sleep(1)
    st.balloons()
    st.success("انتهى وقت المذاكرة! ابدأ وقت الراحة الآن.")
    
    # وقت الراحة
    with st.empty():
        for s in range(break_mins * 60, 0, -1):
            m, sec = divmod(s, 60)
            st.metric("Break Time ☕", f"{m:02d}:{sec:02d}")
            time.sleep(1)
    st.warning("انتهت الراحة! هل أنت مستعد لجلسة أخرى؟")
