import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Pro", page_icon="🎓", layout="wide")

# --- 2. هندسة الألوان (CSS) لضمان أعلى درجة وضوح ---
st.markdown("""
    <style>
    /* الخلفية العامة */
    .main { background-color: #0d1117; color: #ffffff; }
    
    /* جعل النصوص في كل مكان بيضاء وواضحة */
    p, span, label, .stMarkdown, .css-10trblm { 
        color: #ffffff !important; 
        font-weight: 500 !important;
        font-size: 1.05rem !important;
    }
    
    /* العناوين بلون أزرق فاتح جداً وواضح */
    h1, h2, h3 { color: #58a6ff !important; font-weight: bold !important; }
    
    /* صناديق المهام والإحصائيات بخلفية فاتحة قليلاً */
    .stAlert, .status-card, .quote-box {
        background-color: #1c2128 !important;
        border: 1px solid #444c56 !important;
        color: #ffffff !important;
        border-radius: 12px;
        padding: 15px;
    }

    /* أزرار واضحة جداً */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #238636 !important;
        color: white !important;
        font-weight: bold !important;
        border: 1px solid #2ea043 !important;
        height: 3em;
    }
    
    /* الأوسمة */
    .badge-unlocked { 
        background-color: #f0883e !important; 
        color: white !important; 
        padding: 5px 10px; 
        border-radius: 8px; 
        display: inline-block; 
        margin: 5px;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام البيانات ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'badges' not in st.session_state: st.session_state.badges = {"first": False, "timer": False}

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🎓 Study Flow</h2>", unsafe_allow_html=True)
    
    # الرتبة والنقاط
    xp = st.session_state.xp
    rank = "مبتدئ 🌱" if xp < 200 else "محارب ⚔️" if xp < 1000 else "أسطورة 👑"
    st.success(f"**الرتبة:** {rank}")
    st.info(f"**النقاط:** {xp} XP")
    
    st.divider()
    st.subheader("🏅 الأوسمة")
    if st.session_state.badges["first"]: st.markdown('<div class="badge-unlocked">✅ أول خطوة</div>', unsafe_allow_html=True)
    if st.session_state.badges["timer"]: st.markdown('<div class="badge-unlocked">⚡ سيد الوقت</div>', unsafe_allow_html=True)
    if not any(st.session_state.badges.values()): st.write("أنجز مهاماً لفتح الأوسمة!")

    st.divider()
    st.subheader("📝 نوتة الأفكار")
    st.session_state.notes = st.text_area("أفرغ تشتتك هنا..", value=st.session_state.notes)
    
    st.divider()
    share_msg = f"أنا الآن برتبة {rank} في Study Flow! نقاطي {xp} 🔥"
    wa_url = f"https://wa.me/?text={share_msg}"
    st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer; font-weight:bold;">نشر الإنجاز (واتساب) ✅</button></a>', unsafe_allow_html=True)

# --- 5. القسم العلوي ---
c1, c2 = st.columns([2, 1])
with c1:
    st.title("Study Flow 🌊")
    st.markdown('<div class="quote-box">"انضباطك اليوم هو حريتك غداً. استمر في السعي."</div>', unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='background:#1c2128; border:2px solid #f85149; border-radius:15px; text-align:center; padding:10px;'><h1 style='color:#f85149 !important; margin:0;'>🔥 {st.session_state.streak}</h1><p style='margin:0;'>يوم متتالي</p></div>", unsafe_allow_html=True)

# --- 6. التحدي اليومي ---
st.divider()
st.subheader("🏆 تحدي اليوم")
if not st.session_state.challenge_done:
    col_ch1, col_ch2 = st.columns([3, 1])
    col_ch1.warning("تحدي اليوم: أنهِ 3 مهام دراسية بتركيز كامل!")
    if col_ch2.button("✅ تم الإنجاز"):
        st.session_state.challenge_done = True
        st.session_state.xp += 100
        st.balloons()
        st.rerun()
else:
    st.success("🎉 أحسنت! أتممت تحدي اليوم بنجاح.")

# --- 7. الإحصائيات (الرسم البياني) ---
st.divider()
st.subheader("📊 تقدمك الدراسي")
done_tasks = len([t for t in st.session_state.tasks if t['done']])
total_tasks = len(st.session_state.tasks)

if total_tasks > 0:
    fig = go.Figure(data=[go.Pie(labels=['تم', 'متبقي'], values=[done_tasks, total_tasks-done_tasks], hole=.6, marker_colors=['#238636', '#30363d'])])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=250, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)

# --- 8. قائمة المهام ---
st.divider()
st.subheader("📋 المهام اليومية")
with st.expander("➕ أضف مهمة جديدة"):
    c_in1, c_in2, c_in3 = st.columns([2, 1, 1])
    t_name = c_in1.text_input("المهمة")
    t_sub = c_in2.text_input("المادة")
    t_prio = c_in3.selectbox("الأولوية", ["عالية", "متوسطة", "عادية"])
    if st.button("حفظ"):
        if t_name:
            st.session_state.tasks.append({"name": t_name, "sub": t_sub, "prio": t_prio, "done": False})
            st.session_state.badges["first"] = True
            st.rerun()

for i, t in enumerate(st.session_state.tasks):
    with st.container():
        tc1, tc2, tc3, tc4 = st.columns([0.1, 0.6, 0.2, 0.1])
        done = tc1.checkbox("", value=t['done'], key=f"tsk_{i}")
        if done != t['done']:
            st.session_state.tasks[i]['done'] = done
            if done: 
                st.session_state.xp += 20
                st.snow()
            st.rerun()
        
        label = f"~~{t['name']}~~" if t['done'] else t['name']
        tc2.markdown(f"<b style='font-size:1.2rem;'>{label}</b> | {t['sub']}", unsafe_allow_html=True)
        p_color = "🔴" if t['prio'] == "عالية" else "🟡"
        tc3.write(f"{p_color} {t['prio']}")
        if tc4.button("🗑️", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 9. المؤقت ---
st.divider()
st.subheader("⏳ مؤقت التركيز (30:10)")
st_c1, st_c2 = st.columns([1, 2])
with st_c1:
    duration = st.number_input("دقائق الدراسة:", value=30, step=5)
with st_c2:
    if st.button("🚀 ابدأ التركيز الآن"):
        ph = st.empty()
        for s in range(duration * 60, 0, -1):
            m, sc = divmod(s, 60)
            ph.metric("تركيز عميق ✍️", f"{m:02d}:{sc:02d}")
            time.sleep(1)
        st.balloons()
        st.session_state.xp += 50
        st.session_state.badges["timer"] = True
        st.rerun()

st.divider()
st.caption("Study Flow Pro 🌊 - 2026")
