import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow", page_icon="🎓", layout="wide")

# --- 2. تحسين الألوان والتنسيق (CSS) لضمان وضوح الكلام ---
st.markdown("""
    <style>
    /* تحسين الخلفية والنصوص العامة */
    .main { background-color: #1a1c24; color: #ffffff; }
    
    /* تنسيق كروت الإحصائيات */
    .stat-card {
        background-color: #2d333b;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #444c56;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* تنسيق العناوين لضمان ظهورها */
    h1, h2, h3 { color: #58a6ff !important; font-weight: bold; }
    p, label, .stMarkdown { color: #adbac7 !important; font-size: 1.1rem; }
    
    /* تنسيق الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #238636;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2ea043; border: none; }
    
    /* تنسيق التحدي اليومي */
    .challenge-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 15px;
        color: white !important;
        margin-bottom: 25px;
        border: 1px solid #60a5fa;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام البيانات (Session State) ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'goal' not in st.session_state: st.session_state.goal = ""

# --- 4. المحتوى المتغير (Quotes & Challenges) ---
quotes = [
    "النجاح يبدأ بخطوة واحدة مدروسة. | Success starts with a single step.",
    "ركز على الإنجاز وليس الانشغال. | Focus on being productive, not busy.",
    "وقتك هو أغلى ما تملك، استثمره بذكاء. | Time is your most valuable asset."
]

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.title("🎓 Study Flow")
    st.markdown(f"### مستوى الخبرة: `{st.session_state.xp} XP` 🔥")
    st.divider()
    
    # اختيار اللغة
    lang = st.selectbox("Language / اللغة", ["العربية", "English"])
    
    st.divider()
    st.subheader("🎯 هدف اليوم / Today's Goal")
    st.session_state.goal = st.text_input("اكتب هدفك هنا", value=st.session_state.goal)
    
    st.divider()
    st.info("💡 **نصيحة اليوم:** ترتيب المهام من الأصعب إلى الأسهل يقلل من التوتر ويزيد الإنجاز.")

# --- 6. الهيدر والتحفيز ---
col_head1, col_head2 = st.columns([2, 1])

with col_head1:
    st.title("Study Flow 🌊")
    st.markdown(f"**{random.choice(quotes)}**")

with col_head2:
    st.markdown(f"""
    <div class="challenge-container">
        <b>🏆 تحدي اليوم:</b><br>
        ذاكر مادة واحدة بتركيز كامل لمدة 45 دقيقة!
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 7. لوحة الإنجاز (Dashboard) ---
col_chart, col_stats = st.columns([1.5, 1])

with col_chart:
    st.subheader("📊 تقدمك الحالي / Progress")
    done = len([t for t in st.session_state.tasks if t['done']])
    total = len(st.session_state.tasks)
    
    if total > 0:
        fig = go.Figure(data=[go.Pie(labels=['Completed', 'Remaining'], 
                             values=[done, total-done], 
                             hole=.5, 
                             marker_colors=['#238636', '#f85149'])])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          font=dict(color="white"), height=300, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("ابدأ بإضافة مهامك ليظهر الرسم البياني هنا.")

with col_stats:
    st.subheader("🔔 تنبيهات ذكية")
    high_prio = [t for t in st.session_state.tasks if t['pri'] == "High" and not t['done']]
    if high_prio:
        for hp in high_prio:
            st.error(f"⚠️ مهم جداً: لا تنسَ إنهاء {hp['name']}")
    else:
        st.success("كل شيء يسير حسب الخطة! استمر.")

st.divider()

# --- 8. إضافة المهام وتنظيمها ---
st.subheader("➕ إضافة مهمة جديدة")
with st.expander("اضغط هنا لإضافة مادة أو مهمة"):
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1: t_name = st.text_input("اسم المهمة (Task Name)")
    with c2: t_sub = st.text_input("اسم المادة (Subject)")
    with c3: t_deadline = st.date_input("الموعد النهائي")
    with c4: t_pri = st.selectbox("الأولوية", ["High", "Med", "Low"])
    
    if st.button("حفظ في الجدول"):
        if t_name:
            st.session_state.tasks.append({
                "name": t_name, "sub": t_sub, "deadline": t_deadline, 
                "pri": t_pri, "done": False
            })
            st.rerun()

# --- 9. عرض المهam المنظمة ---
st.subheader("📋 جدول المهام")
if not st.session_state.tasks:
    st.info("جدولك فارغ حالياً.")
else:
    for i, t in enumerate(st.session_state.tasks):
        with st.container():
            col_check, col_text, col_prio, col_del = st.columns([0.1, 0.6, 0.2, 0.1])
            
            # حالة الإتمام
            is_done = col_check.checkbox("", value=t['done'], key=f"c_{i}")
            if is_done != t['done']:
                st.session_state.tasks[i]['done'] = is_done
                st.session_state.xp += 15 if is_done else -15
                st.rerun()
            
            # النص والمادة
            label = f"~~{t['name']}~~" if t['done'] else t['name']
            col_text.markdown(f"**{label}** | مادة: `{t['sub']}`")
            
            # الأولوية بشكل دوائر ملونة
            p_icon = "🔴" if t['pri'] == "High" else "🟡" if t['pri'] == "Med" else "🟢"
            col_prio.write(f"{p_icon} {t['pri']}")
            
            # الحذف
            if col_del.button("🗑️", key=f"d_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

# --- 10. مؤقت الدراسة والراحة التلقائي ---
st.divider()
st.header("⏳ مؤقت الدراسة (30:10)")
st.write("نظام التوقيت التلقائي: كل 30 دقيقة مذاكرة تمنحك 10 دقائق راحة.")

st_col1, st_col2 = st.columns([1, 2])
with st_col1:
    duration = st.number_input("دقائق المذاكرة:", min_value=5, value=30, step=5)
    rest = (duration // 30) * 10
    st.write(f"⏱️ الراحة المكتسبة: **{rest} دقائق**")

with st_col2:
    if st.button("🚀 ابدأ الجلسة"):
        # عداد المذاكرة
        timer_place = st.empty()
        for s in range(duration * 60, 0, -1):
            m, s_remainder = divmod(s, 60)
            timer_place.metric("وقت التركيز ✍️", f"{m:02d}:{s_remainder:02d}")
            time.sleep(1)
        st.balloons()
        
        # عداد الراحة
        if rest > 0:
            st.success(f"أحسنت! وقت الراحة بدأ ({rest} دقائق)")
            for s in range(rest * 60, 0, -1):
                m, s_remainder = divmod(s, 60)
                timer_place.metric("وقت الراحة ☕", f"{m:02d}:{s_remainder:02d}")
                time.sleep(1)
            st.warning("انتهت الراحة، هل نعود للعمل؟")

# --- تذييل ---
st.divider()
st.caption("Study Flow 🌊 - رفيقك الأول للنجاح | 2026")
