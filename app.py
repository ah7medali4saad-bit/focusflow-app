import streamlit as st
import time
import random
import plotly.graph_objects as go

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="Study Flow Pro", page_icon="🎓", layout="wide")

# --- 2. محرك الألوان الفاتحة (CSS) - وضوح 100% ---
st.markdown("""
    <style>
    /* جعل الخلفية بيضاء تماماً */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* جعل كل النصوص سوداء غامقة وواضحة */
    h1, h2, h3, p, span, label, li, .stMarkdown {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', sans-serif !important;
    }

    /* تحسين القائمة الجانبية لتكون رمادي فاتح مريح */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 1px solid #dee2e6;
    }
    
    /* صناديق المهام والجمل */
    .quote-box { 
        padding: 15px; 
        border-radius: 10px; 
        background: #e9ecef; 
        border-right: 5px solid #007bff; 
        margin-bottom: 20px; 
    }
    
    .streak-card { 
        background-color: #fff5f5; 
        border: 2px solid #ff4d4d; 
        padding: 15px; 
        border-radius: 15px; 
        text-align: center; 
    }

    /* كروت الأوسمة في الوضع الفاتح */
    .badge-card {
        background: #ffffff;
        border: 2px solid #f0883e;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .badge-locked { opacity: 0.3; filter: grayscale(1); border: 2px dashed #adb5bd; }

    /* الأزرار */
    .stButton>button {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. بنك البيانات ---
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
        "b4": {"un": False, "n": "وحش المذاكرة", "i": "🔥", "d": "أتممت تحدي اليوم!"}
    }

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='color:#007bff;'>📊 لوحة التحكم</h2>", unsafe_allow_html=True)
    st.metric("رصيد النقاط", f"{st.session_state.xp} XP")
    
    st.divider()
    st.subheader("📒 نوتة التشتت")
    st.session_state.notes = st.text_area("اكتب فكرتك هنا..", value=st.session_state.notes, height=120)
    
    st.divider()
    share_msg = f"نقاطي {st.session_state.xp} في Study Flow! 🚀"
    st.markdown(f'<a href="https://wa.me/?text={share_msg}" target="_blank"><button style="width:100%; background:#25d366; color:white; border:none; padding:10px; border-radius:10px; font-weight:bold; cursor:pointer;">شارك مستواك ✅</button></a>', unsafe_allow_html=True)

# --- 5. الهيدر والستريك ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.title("Study Flow 🌊")
    st.markdown('<div class="quote-box">"النجاح ليس صدفة، بل هو نتيجة العمل الذكي والمستمر."</div>', unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""<div class="streak-card"><h1 style="color:#ff4d4d !important; margin:0;">🔥 {st.session_state.streak}</h1><p style="margin:0;">يوم متتالي</p></div>""", unsafe_allow_html=True)

# --- 6. الأوسمة ---
st.divider()
st.subheader("🏅 الأوسمة المحققة")
b_cols = st.columns(4)
for idx, (k, b) in enumerate(st.session_state.badges.items()):
    with b_cols[idx]:
        lock = "" if b["un"] else "badge-locked"
        st.markdown(f"""<div class="badge-card {lock}"><div style="font-size:30px;">{b['i']}</div><b style="color:#f0883e;">{b['n']}</b><div style="font-size:10px; color:#6c757d;">{b['d']}</div></div>""", unsafe_allow_html=True)
        if b["un"]:
            st.markdown(f'<a href="https://wa.me/?text=حصلت على وسام {b["n"]} {b["i"]}!" target="_blank"><button style="width:100%; background:#075e54; font-size:10px; color:white; border:none; padding:5px; border-radius:5px; cursor:pointer;">شارك الوسام ✅</button></a>', unsafe_allow_html=True)

# --- 7. التحدي والإحصائيات ---
st.divider()
c_ch, c_gr = st.columns([1.5, 1])
with c_ch:
    st.subheader("🎯 تحدي اليوم")
    if not st.session_state.challenge_done:
        st.info("التحدي: ذاكر لمدة 25 دقيقة بتركيز كامل!")
        if st.button("أتممت التحدي ✅"):
            st.session_state.challenge_done = True
            st.session_state.xp += 100
            st.session_state.badges["b4"]["un"] = True
            st.balloons()
            st.rerun()
    else:
        st.success("🎉 أحسنت! التحدي اكتمل.")

with c_gr:
    done_n = len([t for t in st.session_state.tasks if t['done']])
    total_n = len(st.session_state.tasks)
    if total_n > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم', 'متبقي'], values=[done_num, total_n-done_n], hole=.6, marker_colors=['#28a745', '#e9ecef'])])
        fig.update_layout(height=200, margin=dict(t=0,b=0,l=0,r=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# --- 8. قائمة المهام ---
st.divider()
st.subheader("📋 قائمة المهام")
with st.expander("➕ أضف مهمة"):
    name = st.text_input("اسم المهمة")
    if st.button("حفظ المهمة"):
        if name:
            st.session_state.tasks.append({"name": name, "done": False})
            st.rerun()

for i, t in enumerate(st.session_state.tasks):
    c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
    done = c1.checkbox("", value=t['done'], key=f"t_{i}")
    if done != t['done']:
        st.session_state.tasks[i]['done'] = done
        if done: st.session_state.xp += 20
        st.rerun()
    txt = f"~~{t['name']}~~" if t['done'] else t['name']
    c2.write(f"**{txt}**")
    if c3.button("🗑️", key=f"d_{i}"):
        st.session_state.tasks.pop(i)
        st.rerun()

# --- 9. المؤقت ---
st.divider()
st.subheader("⏳ مؤقت التركيز")
if st.button("🚀 ابدأ 30 دقيقة"):
    st.session_state.badges["b2"]["un"] = True
    ph = st.empty()
    for s in range(30 * 60, 0, -1):
        m, sc = divmod(s, 60)
        ph.metric("متبقي", f"{m:02d}:{sc:02d}")
        time.sleep(1)
    st.session_state.xp += 50
    st.rerun()

st.divider()
st.caption("Study Flow Pro 🌊 - Light Edition 2026")
