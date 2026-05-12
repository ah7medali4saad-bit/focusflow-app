import streamlit as st
import time
import random
import plotly.graph_objects as go

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Ultimate", page_icon="🎓", layout="wide")

# --- 2. محرك التنسيق (Light Mode) ومنع التداخل ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    
    /* منع تداخل النصوص وجعلها واضحة */
    h1, h2, h3, p, span, label, li {
        color: #1a1a1a !important;
        line-height: 1.6 !important;
        font-family: 'Segoe UI', sans-serif !important;
    }

    /* تنسيق القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 2px solid #dee2e6;
    }

    /* كروت الأوسمة */
    .badge-card {
        background-color: #ffffff;
        border: 2px solid #f0883e;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .badge-locked { opacity: 0.2; filter: grayscale(1); border: 2px dashed #adb5bd; }

    /* صندوق الجمل والستريك */
    .quote-box {
        padding: 20px;
        background: #f1f3f5;
        border-right: 6px solid #007bff;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .streak-card {
        background-color: #fff5f5;
        border: 2px solid #ff4d4d;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
    }

    /* الأزرار */
    .stButton>button {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. بنك البيانات الثابت ---
if 'quotes' not in st.session_state:
    st.session_state.quotes = [
        "النجاح هو مجموع جهود صغيرة تتكرر يوماً بعد يوم.",
        "انضباطك اليوم هو حريتك غداً.",
        "تعب الدراسة يزول، وحلاوة النجاح تبقى للأبد.",
        "لا تتوقف عندما تتعب، توقف عندما تنتهي."
    ]

# --- 4. نظام إدارة الحالة (Data System) ---
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
        "b4": {"un": False, "n": "وحش المذاكرة", "i": "🔥", "d": "أتممت تحدي اليوم!"},
        "b5": {"un": False, "n": "المنظم", "i": "📚", "d": "أضفت 5 مهام!"}
    }

def check_badges():
    done_tasks = [t for t in st.session_state.tasks if t['done']]
    if len(done_tasks) >= 1: st.session_state.badges["b1"]["un"] = True
    if len(st.session_state.tasks) >= 5: st.session_state.badges["b5"]["un"] = True
    if st.session_state.xp >= 500: st.session_state.badges["b3"]["un"] = True

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:#007bff;'>📊 لوحة التحكم</h2>", unsafe_allow_html=True)
    xp = st.session_state.xp
    rank = "طالب 📖" if xp < 200 else "محارب ⚔️" if xp < 1000 else "دكتور 🎓"
    st.success(f"الرتبة: {rank}")
    st.info(f"النقاط: {xp} XP")
    
    st.divider()
    st.subheader("📒 نوتة التشتت")
    st.session_state.notes = st.text_area("أفرغ تشتتك هنا..", value=st.session_state.notes, height=120)
    
    st.divider()
    share_msg = f"أنا برتبة {rank} بنقاط {xp} في Study Flow! 🚀"
    st.markdown(f'<a href="https://wa.me/?text={share_msg}" target="_blank"><button style="width:100%; background:#25d366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer; font-weight:bold;">🚀 شارك مستواك</button></a>', unsafe_allow_html=True)

# --- 6. الهيدر والستريك ---
col_left, col_right = st.columns([2, 1])
with col_left:
    st.title("Study Flow 🌊")
    st.markdown(f'<div class="quote-box">✨ {random.choice(st.session_state.quotes)}</div>', unsafe_allow_html=True)

with col_right:
    st.markdown(f"""<div class="streak-card"><h1 style="color:#ff4d4d !important; margin:0;">🔥 {st.session_state.streak}</h1><p style="margin:0; font-weight:bold;">يوم متتالي</p></div>""", unsafe_allow_html=True)

# --- 7. الأوسمة البصرية ---
st.divider()
st.subheader("🏅 خزانة الأوسمة")
b_cols = st.columns(5)
for idx, (k, b) in enumerate(st.session_state.badges.items()):
    with b_cols[idx]:
        lock = "" if b["un"] else "badge-locked"
        st.markdown(f"""
        <div class="badge-card {lock}">
            <div style="font-size:35px;">{b['i']}</div>
            <b style="color:#f0883e;">{b['n']}</b>
            <div style="font-size:10px; color:#6c757d;">{b['d']}</div>
        </div>
        """, unsafe_allow_html=True)
        if b["un"]:
            wa_b = f"https://wa.me/?text=فتحت وسام {b['n']} {b['i']} في Study Flow! 🏆"
            st.markdown(f'<a href="{wa_b}" target="_blank"><button style="width:100%; background:#075e54; font-size:10px; color:white; border:none; padding:5px; border-radius:5px;">مشاركة ✅</button></a>', unsafe_allow_html=True)

# --- 8. التحدي اليومي والرسم البياني ---
st.divider()
c_ch, c_gr = st.columns([1.5, 1])
with c_ch:
    st.subheader("🎯 تحدي اليوم")
    if not st.session_state.challenge_done:
        st.info("التحدي: ذاكر لمدة 25 دقيقة بتركيز كامل بدون تشتت!")
        if st.button("أتممت التحدي! (+100 XP)"):
            st.session_state.challenge_done = True
            st.session_state.xp += 100
            st.session_state.badges["b4"]["un"] = True
            st.balloons()
            st.rerun()
    else:
        st.success("🎉 أحسنت! التحدي اليومي اكتمل.")

with c_gr:
    done_n = len([t for t in st.session_state.tasks if t['done']])
    total_n = len(st.session_state.tasks)
    if total_n > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم', 'متبقي'], values=[done_n, total_n-done_n], hole=.6, marker_colors=['#28a745', '#e9ecef'])])
        fig.update_layout(height=200, margin=dict(t=0,b=0,l=0,r=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# --- 9. قائمة المهام ---
st.divider()
st.subheader("📋 قائمة المهام")
with st.expander("➕ أضف مهمة جديدة"):
    c_i1, c_i2 = st.columns([3, 1])
    name = c_i1.text_input("المهمة")
    prio = c_i2.selectbox("الأولوية", ["عادية", "عالية 🔥"])
    if st.button("حفظ"):
        if name:
            st.session_state.tasks.append({"name": name, "done": False, "prio": prio})
            check_badges()
            st.rerun()

for i, t in enumerate(st.session_state.tasks):
    with st.container():
        tc1, tc2, tc3 = st.columns([0.1, 0.8, 0.1])
        done = tc1.checkbox("", value=t['done'], key=f"tk_{i}")
        if done != t['done']:
            st.session_state.tasks[i]['done'] = done
            if done: st.session_state.xp += 30
            check_badges()
            st.rerun()
        txt = f"~~{t['name']}~~" if t['done'] else t['name']
        tc2.write(f"**{txt}** ({t['prio']})")
        if tc3.button("🗑️", key=f"dl_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 10. مؤقت التركيز ---
st.divider()
st.subheader("⏳ مؤقت التركيز (30 دقيقة)")
if st.button("🚀 ابدأ المؤقت الآن"):
    st.session_state.badges["b2"]["un"] = True
    ph = st.empty()
    for s in range(30 * 60, 0, -1):
        m, sc = divmod(s, 60)
        ph.metric("متبقي", f"{m:02d}:{sc:02d}")
        time.sleep(1)
    st.balloons()
    st.session_state.xp += 50
    st.rerun()

st.divider()
st.caption("Study Flow Ultimate Pro 🌊 - 2026")
