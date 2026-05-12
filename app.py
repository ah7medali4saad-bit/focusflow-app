import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Pro", page_icon="🎓", layout="wide")

# --- 2. تنسيق الألوان الفاتحة ومنع تداخل الكلام (CSS) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة */
    .stApp {
        background-color: #fdfdfd !important;
    }
    
    /* جعل النصوص واضحة وبعيدة عن بعضها */
    h1, h2, h3, p, span, label, li {
        color: #2c3e50 !important;
        line-height: 1.6 !important;
        margin-bottom: 10px !important;
    }

    /* تنسيق القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #f1f3f5 !important;
        border-right: 2px solid #e9ecef;
    }

    /* كروت الأوسمة (بدون تداخل) */
    .badge-card {
        background-color: #ffffff;
        border: 2px solid #ff922b;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin: 5px;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .badge-locked { opacity: 0.3; filter: grayscale(1); border: 2px dashed #ced4da; }

    /* صندوق الستريك والجمل */
    .quote-box {
        padding: 20px;
        background: #e7f5ff;
        border-left: 6px solid #228be6;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    .streak-card {
        background-color: #fff5f5;
        border: 2px solid #fa5252;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }

    /* تحسين شكل الأزرار */
    .stButton>button {
        background-color: #40c057 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2f9e44 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. بنك البيانات (الجمل والتحديات) ---
if 'quotes' not in st.session_state:
    st.session_state.quotes = [
        "النجاح ليس بمقدار ما تنجزه، بل بمقدار الصعاب التي تتغلب عليها.",
        "ابدأ حيث أنت، استخدم ما تملك، افعل ما تستطيع.",
        "تعب المذاكرة مؤقت، لكن لذة النجاح دائمة."
    ]
if 'challenges' not in st.session_state:
    st.session_state.challenges = [
        "ذاكر لمدة 25 دقيقة بتركيز عميق (Pomodoro).",
        "لخص أهم 3 نقاط في مادتك اليوم.",
        "اشرح ما ذاكرته لشخص آخر أو لنفسك في المرآة."
    ]

# --- 4. إدارة البيانات (Session State) ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'badges' not in st.session_state:
    st.session_state.badges = {
        "b1": {"un": False, "n": "أول خطوة", "i": "🌱", "d": "أكملت أول مهمة!"},
        "b2": {"un": False, "n": "سيد الوقت", "i": "⏳", "d": "استخدمت المؤقت!"},
        "b3": {"un": False, "n": "الأسطورة", "i": "👑", "d": "وصلت لـ 500 XP!"},
        "b4": {"un": False, "n": "الوحش", "i": "🔥", "d": "أتممت تحدي اليوم!"}
    }

def check_badges():
    done_tasks = [t for t in st.session_state.tasks if t['done']]
    if len(done_tasks) >= 1 and not st.session_state.badges["b1"]["un"]:
        st.session_state.badges["b1"]["un"] = True
        st.toast("🏆 تم فتح وسام جديد!")
        st.balloons()
    if st.session_state.xp >= 500 and not st.session_state.badges["b3"]["un"]:
        st.session_state.badges["b3"]["un"] = True
        st.balloons()

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='color:#228be6;'>📊 إحصائياتك</h2>", unsafe_allow_html=True)
    st.metric("مجموع النقاط", f"{st.session_state.xp} XP")
    
    st.divider()
    st.subheader("📒 نوتة التشتت")
    st.session_state.notes = st.text_area("أفرغ أفكارك المشتتة هنا لتنساها وتكمل..", value=st.session_state.notes, height=150)
    
    st.divider()
    share_msg = f"أنا الآن بنقاط {st.session_state.xp} في Study Flow! تابع تقدمي 🔥"
    st.markdown(f'<a href="https://wa.me/?text={share_msg}" target="_blank"><button style="width:100%; background:#25d366; color:white; border:none; padding:12px; border-radius:8px; cursor:pointer; font-weight:bold;">🚀 شارك على واتساب</button></a>', unsafe_allow_html=True)

# --- 6. الهيدر والستريك ---
col_left, col_right = st.columns([2, 1])
with col_left:
    st.title("Study Flow 🌊")
    st.markdown(f'<div class="quote-box">✨ {random.choice(st.session_state.quotes)}</div>', unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
    <div class="streak-card">
        <h1 style="color:#fa5252 !important; margin:0; font-size:45px;">🔥 {st.session_state.streak}</h1>
        <p style="margin:0; font-weight:bold; color:#2c3e50 !important;">يوم متتالي</p>
    </div>
    """, unsafe_allow_html=True)

# --- 7. قسم الأوسمة (منظم جداً) ---
st.divider()
st.subheader("🏅 خزانة الأوسمة")
b_cols = st.columns(4)
for idx, (k, b) in enumerate(st.session_state.badges.items()):
    with b_cols[idx]:
        lock_style = "" if b["un"] else "badge-locked"
        st.markdown(f"""
        <div class="badge-card {lock_style}">
            <div style="font-size:40px;">{b['i']}</div>
            <div style="font-weight:bold; color:#e67e22;">{b['n']}</div>
            <div style="font-size:12px; color:#7f8c8d;">{b['d']}</div>
        </div>
        """, unsafe_allow_html=True)
        if b["un"]:
            b_wa = f"https://wa.me/?text=حصلت على وسام {b['n']} {b['i']} في تطبيق Study Flow! 🏆"
            st.markdown(f'<a href="{b_wa}" target="_blank" style="text-decoration:none;"><button style="width:100%; background:#128c7e; color:white; border:none; padding:5px; border-radius:5px; font-size:11px; cursor:pointer;">شارك الوسام ✅</button></a>', unsafe_allow_html=True)

# --- 8. التحدي اليومي والرسم البياني ---
st.divider()
c_ch, c_gr = st.columns([1.5, 1])
with c_ch:
    st.subheader("🎯 تحدي اليوم")
    if not st.session_state.challenge_done:
        st.info(f"التحدي: {random.choice(st.session_state.challenges)}")
        if st.button("أتممت التحدي بنجاح! ✅"):
            st.session_state.challenge_done = True
            st.session_state.xp += 100
            st.session_state.badges["b4"]["un"] = True
            st.balloons()
            st.rerun()
    else:
        st.success("🎉 مذهل! أنهيت تحدي اليوم بنجاح.")

with c_gr:
    done_n = len([t for t in st.session_state.tasks if t['done']])
    total_n = len(st.session_state.tasks)
    if total_n > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم', 'متبقي'], values=[done_n, total_n-done_n], hole=.6, marker_colors=['#40c057', '#f1f3f5'])])
        fig.update_layout(height=200, margin=dict(t=0,b=0,l=0,r=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# --- 9. قائمة المهام ---
st.divider()
st.subheader("📋 قائمة مهامك")
with st.expander("➕ أضف مهمة جديدة"):
    c_in1, c_in2 = st.columns([3, 1])
    new_t = c_in1.text_input("اسم المهمة")
    prio = c_in2.selectbox("الأولوية", ["عادية", "عالية 🔥"])
    if st.button("إضافة المهمة"):
        if new_t:
            st.session_state.tasks.append({"name": new_t, "done": False, "prio": prio})
            st.rerun()

for i, t in enumerate(st.session_state.tasks):
    with st.container():
        tc1, tc2, tc3 = st.columns([0.1, 0.8, 0.1])
        d = tc1.checkbox("", value=t['done'], key=f"tsk_{i}")
        if d != t['done']:
            st.session_state.tasks[i]['done'] = d
            if d: st.session_state.xp += 30
            check_badges()
            st.rerun()
        
        label = f"~~{t['name']}~~" if t['done'] else t['name']
        tc2.write(f"**{label}** ({t['prio']})")
        if tc3.button("🗑️", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 10. مؤقت التركيز ---
st.divider()
st.subheader("⏳ مؤقت التركيز (30 دقيقة)")
if st.button("🚀 ابدأ جلسة التركيز الآن"):
    st.session_state.badges["b2"]["un"] = True
    timer_placeholder = st.empty()
    for s in range(30 * 60, 0, -1):
        m, sec = divmod(s, 60)
        timer_placeholder.metric("وقت المذاكرة", f"{m:02d}:{sec:02d}")
        time.sleep(1)
    st.balloons()
    st.session_state.xp += 50
    st.rerun()

st.divider()
st.caption("Study Flow Pro 🌊 - 2026 | Light Version")
