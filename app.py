import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Pro - Ultimate", page_icon="🏆", layout="wide")

# --- 2. محرك التنسيق البصري (CSS) - وضوح 100% ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117 !important; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #ffffff !important; }
    
    /* تنسيق كارت الوسام */
    .badge-card {
        background: linear-gradient(135deg, #1c2128 0%, #2d333b 100%);
        border: 2px solid #f0883e;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .badge-icon { font-size: 40px; margin-bottom: 10px; }
    .badge-name { color: #f0883e !important; font-weight: bold; font-size: 18px; }
    .badge-locked { opacity: 0.3; filter: grayscale(1); border: 2px dashed #484f58; }
    
    /* تنسيق الستريك */
    .streak-box {
        background-color: #161b22;
        border: 2px solid #f85149;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
    }
    
    /* القائمة الجانبية */
    section[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام إدارة الحالة (Data System) ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""

# نظام الأوسمة (قائمة قابلة للتوسع)
if 'badges' not in st.session_state:
    st.session_state.badges = {
        "first_task": {"unlocked": False, "name": "أول خطوة", "icon": "🌱", "desc": "أكملت أول مهمة بنجاح!"},
        "five_tasks": {"unlocked": False, "name": "المجتهد", "icon": "🚀", "desc": "أكملت 5 مهام دراسية!"},
        "xp_1000": {"unlocked": False, "name": "الأسطورة", "icon": "👑", "desc": "وصلت إلى 1000 نقطة خبرة!"},
        "timer_king": {"unlocked": False, "name": "سيد الوقت", "icon": "⏳", "desc": "استخدمت مؤقت التركيز بنجاح!"},
        "streak_expert": {"unlocked": False, "name": "الصامد", "icon": "🔥", "desc": "حافظت على ستريك يومي!"}
    }

# دالة للتحقق من الأوسمة وعرض تنبيه
def check_badges():
    # وسام أول مهمة
    done_count = len([t for t in st.session_state.tasks if t['done']])
    if done_count >= 1 and not st.session_state.badges["first_task"]["unlocked"]:
        st.session_state.badges["first_task"]["unlocked"] = True
        st.toast(f"🏆 مبروك! حصلت على وسام: {st.session_state.badges['first_task']['name']}")
        st.balloons()
    
    # وسام 5 مهام
    if done_count >= 5 and not st.session_state.badges["five_tasks"]["unlocked"]:
        st.session_state.badges["five_tasks"]["unlocked"] = True
        st.toast("🏆 وسام جديد: المجتهد 🚀")
        st.balloons()

    # وسام 1000 نقطة
    if st.session_state.xp >= 1000 and not st.session_state.badges["xp_1000"]["unlocked"]:
        st.session_state.badges["xp_1000"]["unlocked"] = True
        st.toast("🏆 وسام العمالقة: الأسطورة 👑")
        st.balloons()

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h1 style='color:#58a6ff;'>Control Center</h1>", unsafe_allow_html=True)
    xp = st.session_state.xp
    st.metric("رصيد النقاط", f"{xp} XP")
    
    st.divider()
    st.subheader("📒 مفكرة التشتت")
    st.session_state.notes = st.text_area("أفرغ أفكارك هنا..", value=st.session_state.notes, height=150)
    
    st.divider()
    # زر مشاركة عام للموقع
    share_msg = f"أنا أحقق أرقاماً قياسية في Study Flow! مجموع نقاطي {xp} XP 🔥"
    wa_url = f"https://wa.me/?text={share_msg}"
    st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background:#25d366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold;">🚀 شارك مستواك العام</button></a>', unsafe_allow_html=True)

# --- 5. الهيدر والستريك ---
c_head, c_streak = st.columns([2, 1])
with c_head:
    st.title("Study Flow 🌊")
    st.markdown("### رحلتك نحو القمة تبدأ بمهمة واحدة.")

with c_streak:
    st.markdown(f"""
    <div class="streak-box">
        <h1 style="color:#f85149 !important; margin:0;">🔥 {st.session_state.streak}</h1>
        <p style="margin:0; font-weight:bold;">STREAK</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. عرض الأوسمة (بشكل تفاعلي) ---
st.divider()
st.subheader("🏅 خزانة الأوسمة الملكية")
badge_cols = st.columns(len(st.session_state.badges))

for idx, (key, b) in enumerate(st.session_state.badges.items()):
    with badge_cols[idx]:
        status_class = "" if b["unlocked"] else "badge-locked"
        st.markdown(f"""
        <div class="badge-card {status_class}">
            <div class="badge-icon">{b['icon']}</div>
            <div class="badge-name">{b['name']}</div>
            <div style="font-size:12px; color:#adbac7;">{b['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if b["unlocked"]:
            # زر مشاركة خاص بكل وسام
            b_msg = f"لقد حصلت للتو على وسام '{b['name']}' {b['icon']} في تطبيق Study Flow! 🏆"
            b_url = f"https://wa.me/?text={b_msg}"
            st.markdown(f'<a href="{b_url}" target="_blank" style="text-decoration:none;"><button style="width:100%; background:#075e54; color:white; border:none; border-radius:5px; font-size:11px; cursor:pointer;">شارك الوسام ✅</button></a>', unsafe_allow_html=True)
        else:
            st.button("🔒 مغلق", key=f"lock_{key}", disabled=True)

# --- 7. التحدي اليومي والمهام ---
st.divider()
col_tasks, col_stats = st.columns([2, 1])

with col_tasks:
    st.subheader("📋 المهام والجدول")
    with st.expander("➕ إضافة مهمة جديدة"):
        t_in = st.text_input("ماذا ستنجز الآن؟")
        if st.button("حفظ المهمة"):
            if t_in:
                st.session_state.tasks.append({"name": t_in, "done": False})
                st.rerun()

    for i, t in enumerate(st.session_state.tasks):
        c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
        done = c1.checkbox("", value=t['done'], key=f"t_{i}")
        if done != t['done']:
            st.session_state.tasks[i]['done'] = done
            if done: 
                st.session_state.xp += 30
                st.snow()
            check_badges() # التحقق من الأوسمة فوراً
            st.rerun()
        
        txt = f"~~{t['name']}~~" if t['done'] else t['name']
        c2.markdown(f"<span style='font-size:18px;'>{txt}</span>", unsafe_allow_html=True)
        if c3.button("🗑️", key=f"d_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

with col_stats:
    st.subheader("📊 الرسم البياني")
    done_num = len([t for t in st.session_state.tasks if t['done']])
    total_num = len(st.session_state.tasks)
    if total_num > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم', 'متبقي'], values=[done_num, total_num-done_num], hole=.6, marker_colors=['#238636', '#161b22'])])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=250, showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

# --- 8. مؤقت التركيز ---
st.divider()
st.subheader("⏳ مؤقت التركيز العميق")
if st.button("🚀 ابدأ جلسة تركيز (30 دقيقة)"):
    st.session_state.badges["timer_king"]["unlocked"] = True
    check_badges()
    ph = st.empty()
    for s in range(30 * 60, 0, -1):
        m, sc = divmod(s, 60)
        ph.metric("تركيز...", f"{m:02d}:{sc:02d}")
        time.sleep(1)
    st.balloons()
    st.session_state.xp += 100
    st.rerun()

st.divider()
st.caption("Study Flow Pro 🌊 - 2026 | نظام الأوسمة المطور")
