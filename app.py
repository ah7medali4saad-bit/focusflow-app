import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Pro", page_icon="🎓", layout="wide")

# --- 2. CSS محسن جداً للوضوح والتفاعل ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stButton>button { border-radius: 10px; font-weight: bold; transition: 0.3s; }
    .badge-box {
        background: linear-gradient(45deg, #f39c12, #d35400);
        padding: 10px; border-radius: 10px; text-align: center; color: white; font-weight: bold;
    }
    .streak-card {
        background-color: #161b22; border: 2px solid #f85149;
        padding: 15px; border-radius: 15px; text-align: center;
    }
    .share-btn {
        background-color: #25d366 !important; color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام البيانات (Session State) ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'last_date' not in st.session_state: st.session_state.last_date = str(date.today())

# تحديث الستريك تلقائياً
today = str(date.today())
if st.session_state.last_date != today:
    # لو فتح الموقع في يوم جديد، نزيد الستريك لو كان مخلص مهام أمس (تبسيطاً)
    st.session_state.streak += 1
    st.session_state.last_date = today

# --- 4. بنك التحفيز والتحديات (أكثر من 100 جملة محتملة) ---
quotes_bank = [
    "النجاح ليس نهائياً، والفشل ليس قاتلاً: الشجاعة للاستمرار هي ما يهم.",
    "Don't decrease the goal. Increase the effort.",
    "أنت اليوم حيث أوصلتك أفكارك، وستكون غداً حيث تأخذك أفكارك.",
    "The way to get started is to quit talking and begin doing.",
    "كل ثانية تذاكرها هي استثمار في مستقبلك العظيم.",
    "صناع المجد لا يعرفون النوم الطويل، استيقظ وواجه التحدي!"
]

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.title("🎓 Study Flow")
    
    # عرض الرتبة بناءً على XP
    xp = st.session_state.xp
    rank = "مبتدئ 🌱" if xp < 100 else "محارب ⚔️" if xp < 500 else "أسطورة 👑"
    st.markdown(f"""<div class="badge-box">الرتبة: {rank}</div>""", unsafe_allow_html=True)
    
    st.metric("XP النقاط", xp, delta=f"+{xp//10} اليوم")
    
    st.divider()
    # زر مشاركة الواتساب
    st.subheader("📢 شارك إنجازك")
    share_text = f"أنا الآن في مستوى {rank} بـ {xp} نقطة وستريك {st.session_state.streak} أيام على تطبيق Study Flow! 🚀"
    whatsapp_url = f"https://wa.me/?text={share_text}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer;">مشاركة على واتساب ✅</button></a>', unsafe_allow_html=True)

# --- 6. الواجهة الرئيسية ---
col_h1, col_h2 = st.columns([2, 1])

with col_h1:
    st.title("Study Flow 🌊")
    st.info(f"✨ {random.choice(quotes_bank)}")

with col_h2:
    st.markdown(f"""
    <div class="streak-card">
        <h2 style="color:#f85149 !important; margin:0;">🔥 {st.session_state.streak}</h2>
        <p style="margin:0;">أيام متتالية (STREAK)</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 7. لوحة الإنجاز التفاعلية ---
c_chart, c_interact = st.columns([1, 1])

with c_chart:
    done = len([t for t in st.session_state.tasks if t['done']])
    total = len(st.session_state.tasks)
    if total > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم بنجاح', 'متبقي'], values=[done, total-done], hole=.6, marker_colors=['#238636', '#30363d'])])
        fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

with c_interact:
    st.subheader("🏆 تحدي اليوم")
    st.success("ذاكر لمدة ساعة واحصل على وسام 'المثابر'!")
    if st.button("✅ أتممت التحدي!"):
        st.session_state.xp += 50
        st.balloons()
        st.rerun()

st.divider()

# --- 8. إدارة المهام ---
st.subheader("➕ أضف مهمتك القادمة")
with st.expander("اضغط هنا لكتابة مهمة"):
    cols = st.columns([2, 1, 1])
    name = cols[0].text_input("المهمة")
    subject = cols[1].text_input("المادة")
    prio = cols[2].selectbox("الأهمية", ["عالية", "متوسطة", "عادية"])
    if st.button("إضافة"):
        if name:
            st.session_state.tasks.append({"name": name, "sub": subject, "prio": prio, "done": False})
            st.rerun()

# عرض المهام
for i, t in enumerate(st.session_state.tasks):
    with st.container():
        c1, c2, c3, c4 = st.columns([0.1, 0.6, 0.2, 0.1])
        is_done = c1.checkbox("", value=t['done'], key=f"t_{i}")
        if is_done != t['done']:
            st.session_state.tasks[i]['done'] = is_done
            if is_done:
                st.session_state.xp += 20
                st.snow() # تأثير بصري عند الإنجاز
            st.rerun()
        
        label = f"~~{t['name']}~~" if t['done'] else t['name']
        c2.write(f"**{label}** | {t['sub']}")
        color = "🔴" if t['prio'] == "عالية" else "🟡"
        c3.write(f"{color} {t['prio']}")
        if c4.button("🗑️", key=f"d_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 9. مؤقت المذاكرة (30:10) ---
st.divider()
st.header("⏳ مؤقت التركيز الذكي")
t_col1, t_col2 = st.columns([1, 2])

with t_col1:
    mins = st.number_input("دقائق الدراسة:", value=30, step=5)
    st.write(f"🎁 ستحصل على { (mins//30)*10 } دقائق راحة.")

with t_col2:
    if st.button("🚀 ابدأ الآن"):
        ph = st.empty()
        for s in range(mins * 60, 0, -1):
            m, sc = divmod(s, 60)
            ph.metric("تركيز... ✍️", f"{m:02d}:{sc:02d}")
            time.sleep(1)
        st.balloons()
        st.session_state.xp += 30
        st.success("رائع! انتهت الجلسة وزاد رصيدك 30 XP")
