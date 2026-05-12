import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Pro", page_icon="🎓", layout="wide")

# --- 2. الحل النهائي لمشكلة الألوان (CSS) ---
st.markdown("""
    <style>
    /* فرض لون الخلفية والنص على التطبيق بالكامل */
    .stApp {
        background-color: #0d1117 !important;
    }
    
    /* توضيح النصوص في القائمة الجانبية والرئيسية */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    
    /* جعل كل النصوص بيضاء ناصعة */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #ffffff !important;
    }

    /* تحسين شكل الكروت (الأوسمة والنوتة) */
    .stTextArea textarea {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    
    /* تنسيق الأزرار لتكون واضحة جداً */
    .stButton>button {
        background-color: #238636 !important;
        color: white !important;
        border: 1px solid #2ea043 !important;
        width: 100%;
        font-weight: bold;
    }

    /* إخفاء أي تداخل ألوان افتراضي */
    div[data-testid="stExpander"] {
        background-color: #1c2128 !important;
        border: 1px solid #30363d !important;
    }
    </style>
    """, unsafe_allow_html=True) # تم تصحيح الخطأ هنا من status لـ html

# --- 3. نظام البيانات ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'badges' not in st.session_state: st.session_state.badges = {"first": False, "timer": False}

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color: #58a6ff !important;'>🎓 القائمة الرئيسية</h2>", unsafe_allow_html=True)
    
    xp = st.session_state.xp
    rank = "مبتدئ 🌱" if xp < 200 else "محارب ⚔️" if xp < 1000 else "أسطورة 👑"
    st.success(f"🏅 الرتبة: {rank}")
    st.info(f"✨ النقاط: {xp} XP")
    
    st.divider()
    st.subheader("🎖️ الأوسمة")
    if st.session_state.badges["first"]: st.markdown("<span style='color:#f0883e;'>✅ وسام أول خطوة</span>", unsafe_allow_html=True)
    if st.session_state.badges["timer"]: st.markdown("<span style='color:#f0883e;'>✅ وسام سيد الوقت</span>", unsafe_allow_html=True)

    st.divider()
    st.subheader("📒 نوتة الأفكار")
    st.session_state.notes = st.text_area("اكتب تشتتك هنا..", value=st.session_state.notes, key="sidebar_notes")
    
    st.divider()
    share_msg = f"أنا برتبة {rank} في Study Flow! نقاطي {xp} 🔥"
    wa_url = f"https://wa.me/?text={share_msg}"
    st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer; font-weight:bold;">نشر الإنجاز (واتساب) ✅</button></a>', unsafe_allow_html=True)

# --- 5. القسم الرئيسي ---
st.title("Study Flow 🌊")
st.markdown("<p style='font-size: 1.2rem; color: #adbac7 !important;'>مرحباً بك في مساحتك الخاصة للإنجاز</p>", unsafe_allow_html=True)

# الستريك
st.markdown(f"""
    <div style="background:#161b22; border:1px solid #f85149; border-radius:15px; padding:15px; text-align:center; margin-bottom:20px;">
        <h1 style="color:#f85149 !important; margin:0;">🔥 {st.session_state.streak}</h1>
        <p style="margin:0; color:white !important;">أيام متتالية</p>
    </div>
    """, unsafe_allow_html=True)

# التحدي اليومي
st.subheader("🎯 تحدي اليوم")
if not st.session_state.challenge_done:
    col_ch1, col_ch2 = st.columns([3, 1])
    col_ch1.warning("أنهِ 3 مهام دراسية الآن!")
    if col_ch2.button("أتممت التحدي"):
        st.session_state.challenge_done = True
        st.session_state.xp += 100
        st.balloons()
        st.rerun()
else:
    st.success("🎉 أحسنت! أتممت التحدي بنجاح.")

# الرسم البياني
st.divider()
st.subheader("📊 إحصائيات الإنجاز")
done_tasks = len([t for t in st.session_state.tasks if t['done']])
total_tasks = len(st.session_state.tasks)

if total_tasks > 0:
    fig = go.Figure(data=[go.Pie(labels=['تم', 'متبقي'], values=[done_tasks, total_tasks-done_tasks], hole=.6, marker_colors=['#238636', '#30363d'])])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=250, margin=dict(t=0,b=0,l=0,r=0), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("أضف مهامك ليظهر الرسم البياني هنا.")

# قائمة المهام
st.divider()
st.subheader("📝 جدول المهام")
with st.expander("➕ أضف مهمة جديدة"):
    c_in1, c_in2 = st.columns([3, 1])
    t_name = c_in1.text_input("اسم المهمة")
    t_prio = c_in2.selectbox("الأولوية", ["عالية", "عادية"])
    if st.button("إضافة المهمة"):
        if t_name:
            st.session_state.tasks.append({"name": t_name, "done": False, "prio": t_prio})
            st.session_state.badges["first"] = True
            st.rerun()

for i, t in enumerate(st.session_state.tasks):
    with st.container():
        tc1, tc2, tc3 = st.columns([0.1, 0.8, 0.1])
        done = tc1.checkbox("", value=t['done'], key=f"task_{i}")
        if done != t['done']:
            st.session_state.tasks[i]['done'] = done
            if done: 
                st.session_state.xp += 20
                st.snow()
            st.rerun()
        
        display_text = f"~~{t['name']}~~" if t['done'] else t['name']
        tc2.write(f"**{display_text}** ({t['prio']})")
        if tc3.button("🗑️", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# المؤقت
st.divider()
st.subheader("⏳ مؤقت التركيز")
if st.button("🚀 ابدأ مؤقت 30 دقيقة"):
    st.session_state.badges["timer"] = True
    ph = st.empty()
    for s in range(30 * 60, 0, -1):
        m, sc = divmod(s, 60)
        ph.metric("وقت التركيز", f"{m:02d}:{sc:02d}")
        time.sleep(1)
    st.balloons()
    st.session_state.xp += 50
    st.rerun()

st.divider()
st.caption("Study Flow Pro 🌊 - النسخة المصححة")
