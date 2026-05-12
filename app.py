import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Pro", page_icon="🎓", layout="wide")

# --- 2. تحسين الشكل العام (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stButton>button { border-radius: 12px; font-weight: bold; transition: 0.3s; height: 3em; }
    .badge-box { background: linear-gradient(45deg, #f39c12, #d35400); padding: 10px; border-radius: 10px; text-align: center; color: white; font-weight: bold; }
    .streak-card { background-color: #161b22; border: 2px solid #f85149; padding: 15px; border-radius: 15px; text-align: center; }
    .challenge-complete { background-color: #238636; color: white; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; border: 2px solid #2ea043; }
    .quote-box { padding: 15px; border-radius: 10px; background: #21262d; border-right: 5px solid #58a6ff; margin-bottom: 20px; color: #adbac7; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام البيانات (Session State) ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'last_date' not in st.session_state: st.session_state.last_date = str(date.today())

# إعادة ضبط التحدي اليومي إذا تغير اليوم
if st.session_state.last_date != str(date.today()):
    st.session_state.challenge_done = False
    st.session_state.last_date = str(date.today())
    st.session_state.streak += 1

# --- 4. بنك التحديات والجمل (تم توسيعه) ---
challenges_bank = [
    "ذاكر لمدة 45 دقيقة متواصلة دون تشتت 🧠",
    "أنهِ أصعب مهمة في جدولك الآن ⚡",
    "اشرح درساً صعباً لنفسك في المرآة 🗣️",
    "رتب مكان مذاكرتك بالكامل في 5 دقائق 🧹",
    "قم بحل 10 تمارين أو قراءة 10 صفحات فورا 📖",
    "اكتب ملخصاً لأهم فكرة ذاكرتها اليوم ✍️",
    "ذاكر بعيداً عن هاتفك تماماً لمدة ساعة 📵"
]

if 'daily_challenge' not in st.session_state:
    st.session_state.daily_challenge = random.choice(challenges_bank)

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.title("🎓 Study Flow")
    xp = st.session_state.xp
    rank = "مبتدئ 🌱" if xp < 200 else "محارب ⚔️" if xp < 1000 else "أسطورة 👑"
    st.markdown(f"""<div class="badge-box">الرتبة الحالية: {rank}</div>""", unsafe_allow_html=True)
    st.divider()
    st.metric("رصيد النقاط (XP)", xp)
    st.divider()
    # زر مشاركة الواتساب
    share_text = f"أنا الآن في رتبة {rank} وستريك {st.session_state.streak} أيام ببرنامج Study Flow! 🚀"
    whatsapp_url = f"https://wa.me/?text={share_text}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer; font-weight:bold;">شارك مستواك على واتساب ✅</button></a>', unsafe_allow_html=True)

# --- 6. الواجهة الرئيسية ---
col_h1, col_h2 = st.columns([2, 1])

with col_h1:
    st.title("Study Flow 🌊")
    st.markdown(f'<div class="quote-box">"النجاح هو مجموع جهود صغيرة تتكرر يوماً بعد يوم."</div>', unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""
    <div class="streak-card">
        <h2 style="color:#f85149 !important; margin:0;">🔥 {st.session_state.streak}</h2>
        <p style="margin:0; color:white;">يوم متتالي (Streak)</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 7. قسم التحدي التفاعلي (يختفي عند الإنجاز) ---
st.subheader("🏆 تحدي اليوم")
if not st.session_state.challenge_done:
    c_col1, c_col2 = st.columns([2, 1])
    c_col1.info(f"**تحدي اللحظة:** {st.session_state.daily_challenge}")
    if c_col2.button("✅ أتممت التحدي بنجاح!"):
        st.session_state.challenge_done = True
        st.session_state.xp += 100
        st.balloons()
        st.rerun()
else:
    st.markdown(f"""
    <div class="challenge-complete">
        🎊 أحسنت! لقد أتممت تحدي اليوم وحصلت على +100 XP. عد غداً لتحدٍ جديد!
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 8. الإحصائيات (الرسم البياني) ---
st.subheader("📊 لوحة إنجاز المهام")
done = len([t for t in st.session_state.tasks if t['done']])
total = len(st.session_state.tasks)

if total > 0:
    fig = go.Figure(data=[go.Pie(labels=['تم', 'متبقي'], values=[done, total-done], hole=.6, marker_colors=['#238636', '#30363d'])])
    fig.update_layout(showlegend=True, height=300, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

# --- 9. إدارة المهام ---
st.subheader("📋 قائمة المهام")
with st.expander("➕ أضف مهمة جديدة"):
    cols = st.columns([2, 1, 1])
    name = cols[0].text_input("اسم المهمة")
    sub = cols[1].text_input("المادة")
    prio = cols[2].selectbox("الأولوية", ["عالية", "متوسطة", "عادية"])
    if st.button("حفظ المهمة"):
        if name:
            st.session_state.tasks.append({"name": name, "sub": sub, "prio": prio, "done": False})
            st.rerun()

for i, t in enumerate(st.session_state.tasks):
    with st.container():
        c1, c2, c3, c4 = st.columns([0.1, 0.6, 0.2, 0.1])
        is_done = c1.checkbox("", value=t['done'], key=f"task_{i}")
        if is_done != t['done']:
            st.session_state.tasks[i]['done'] = is_done
            if is_done:
                st.session_state.xp += 20
                st.snow()
            st.rerun()
        
        label = f"~~{t['name']}~~" if t['done'] else t['name']
        c2.write(f"**{label}** | {t['sub']}")
        color = "🔴" if t['prio'] == "عالية" else "🟡"
        c3.write(f"{color} {t['prio']}")
        if c4.button("🗑️", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 10. مؤقت الدراسة (30:10) ---
st.divider()
st.header("⏳ مؤقت التركيز الذكي")
t_col1, t_col2 = st.columns([1, 2])
with t_col1:
    mins = st.number_input("دقائق الدراسة:", value=30, step=5)
    st.write(f"🎁 راحة تلقائية: { (mins//30)*10 } دقائق.")

with t_col2:
    if st.button("🚀 ابدأ الآن"):
        ph = st.empty()
        for s in range(mins * 60, 0, -1):
            m, sc = divmod(s, 60)
            ph.metric("تركيز... ✍️", f"{m:02d}:{sc:02d}")
            time.sleep(1)
        st.balloons()
        st.session_state.xp += 50
        st.success("انتهت الجلسة! حصلت على 50 XP")

st.divider()
st.caption("Study Flow 🌊 - 2026")
