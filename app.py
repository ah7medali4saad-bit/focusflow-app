import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, date

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Ultimate Pro", page_icon="🎓", layout="wide")

# --- 2. محرك الألوان الفائق (CSS) - وضوح 100% بغض النظر عن إعدادات المتصفح ---
st.markdown("""
    <style>
    /* فرض الخلفية الداكنة العميقة */
    .stApp { background-color: #0d1117 !important; }
    
    /* جعل كل النصوص بيضاء تماماً وواضحة */
    h1, h2, h3, p, span, label, li, div { color: #ffffff !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تنسيق كروت الأوسمة */
    .badge-card {
        background: linear-gradient(135deg, #1c2128 0%, #2d333b 100%);
        border: 2px solid #f0883e;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    .badge-locked { opacity: 0.2; filter: grayscale(1); border: 2px dashed #484f58; }
    
    /* الجمل التحفيزية والستريك */
    .quote-box { padding: 15px; border-radius: 10px; background: #21262d; border-right: 5px solid #58a6ff; margin-bottom: 20px; }
    .streak-card { background-color: #161b22; border: 2px solid #f85149; padding: 15px; border-radius: 15px; text-align: center; }
    
    /* تنسيق المدخلات والنوتة */
    .stTextArea textarea, .stTextInput input { background-color: #1c2128 !important; color: white !important; border: 1px solid #30363d !important; }
    
    /* الأزرار */
    .stButton>button {
        background-color: #238636 !important;
        color: white !important;
        border: 1px solid #2ea043 !important;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. بنك البيانات الضخم (الجمل والتحديات) ---
quotes_bank = [
    "النجاح هو الانتقال من فشل إلى فشل دون فقدان الحماس.",
    "انضباطك اليوم هو حريتك غداً.",
    "السر في المضي قدماً هو البدء.",
    "تعب الدراسة يزول، وحلاوة النجاح تبقى للأبد.",
    "Be so good they can’t ignore you.",
    "Your future self will thank you for today's hard work."
]

challenges_bank = [
    "ذاكر لمدة 25 م دقيقة دون أي تشتت! (50 XP)",
    "رتب مكتبك قبل البدء لمدة 5 دقائق! (20 XP)",
    "اشرح درساً صعباً لنفسك بصوت عالٍ! (40 XP)",
    "اقرأ 10 صفحات من مادتك الصعبة الآن! (30 XP)",
    "أنهِ أول مهمة في جدولك في أقل من ساعة! (40 XP)"
]

# --- 4. نظام إدارة البيانات (Session State) ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'daily_q' not in st.session_state: st.session_state.daily_q = random.choice(quotes_bank)
if 'daily_c' not in st.session_state: st.session_state.daily_c = random.choice(challenges_bank)
if 'badges' not in st.session_state:
    st.session_state.badges = {
        "b1": {"un": False, "n": "أول خطوة", "i": "🌱", "d": "أكملت أول مهمة!"},
        "b2": {"un": False, "n": "سيد الوقت", "i": "⏳", "d": "استخدمت المؤقت!"},
        "b3": {"un": False, "n": "الأسطورة", "i": "👑", "d": "وصلت لـ 500 XP!"},
        "b4": {"un": False, "n": "وحش المذاكرة", "i": "🔥", "d": "أتممت تحدي اليوم!"}
    }

# دالة تحديث الأوسمة
def check_badges():
    done_tasks = [t for t in st.session_state.tasks if t['done']]
    if len(done_tasks) >= 1 and not st.session_state.badges["b1"]["un"]:
        st.session_state.badges["b1"]["un"] = True
        st.toast("🏆 وسام جديد: أول خطوة 🌱")
        st.balloons()
    if st.session_state.xp >= 500 and not st.session_state.badges["b3"]["un"]:
        st.session_state.badges["b3"]["un"] = True
        st.toast("🏆 وسام جديد: الأسطورة 👑")
        st.balloons()

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>📊 لوحة التحكم</h2>", unsafe_allow_html=True)
    xp = st.session_state.xp
    rank = "مبتدئ 🌱" if xp < 200 else "محارب ⚔️" if xp < 1000 else "أسطورة 👑"
    st.success(f"الرتبة: {rank}")
    st.info(f"النقاط: {xp} XP")
    
    st.divider()
    st.subheader("📒 مفكرة التشتت")
    st.session_state.notes = st.text_area("أفرغ تشتتك هنا..", value=st.session_state.notes, height=150)
    
    st.divider()
    share_msg = f"أنا برتبة {rank} بنقاط {xp} في Study Flow! 🔥"
    st.markdown(f'<a href="https://wa.me/?text={share_msg}" target="_blank"><button style="width:100%; background:#25d366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer; font-weight:bold;">🚀 مشاركة على واتساب</button></a>', unsafe_allow_html=True)

# --- 6. الواجهة الرئيسية (الهيدر والستريك) ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.title("Study Flow 🌊")
    st.markdown(f'<div class="quote-box">✨ {st.session_state.daily_q}</div>', unsafe_allow_html=True)
with col_h2:
    st.markdown(f"""<div class="streak-card"><h1 style="color:#f85149 !important; margin:0;">🔥 {st.session_state.streak}</h1><p style="margin:0;">يوم متتالي</p></div>""", unsafe_allow_html=True)

# --- 7. قسم الأوسمة التفاعلي ---
st.divider()
st.subheader("🏅 خزانة الأوسمة")
b_cols = st.columns(4)
for idx, (k, b) in enumerate(st.session_state.badges.items()):
    with b_cols[idx]:
        lock = "" if b["un"] else "badge-locked"
        st.markdown(f"""<div class="badge-card {lock}"><div style="font-size:30px;">{b['i']}</div><div style="color:#f0883e; font-weight:bold;">{b['n']}</div><div style="font-size:10px;">{b['d']}</div></div>""", unsafe_allow_html=True)
        if b["un"]:
            b_wa = f"https://wa.me/?text=حصلت على وسام {b['n']} {b['i']} في Study Flow! 🏆"
            st.markdown(f'<a href="{b_wa}" target="_blank"><button style="width:100%; background:#075e54; font-size:10px; color:white; border:none; padding:5px; border-radius:5px;">مشاركة الوسام ✅</button></a>', unsafe_allow_html=True)

# --- 8. تحدي اليوم والإحصائيات ---
st.divider()
col_ch, col_gr = st.columns([1.5, 1])
with col_ch:
    st.subheader("🎯 تحدي اليوم")
    if not st.session_state.challenge_done:
        st.warning(f"**التحدي:** {st.session_state.daily_c}")
        if st.button("✅ أتممت التحدي!"):
            st.session_state.challenge_done = True
            st.session_state.xp += 100
            st.session_state.badges["b4"]["un"] = True
            st.balloons()
            st.rerun()
    else:
        st.success("🎉 أحسنت! أتممت تحدي اليوم بنجاح.")

with col_gr:
    done_n = len([t for t in st.session_state.tasks if t['done']])
    total_n = len(st.session_state.tasks)
    if total_n > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم', 'متبقي'], values=[done_n, total_n-done_n], hole=.6, marker_colors=['#238636', '#30363d'])])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=200, showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

# --- 9. إدارة المهام ---
st.divider()
st.subheader("📋 قائمة المهام")
with st.expander("➕ أضف مهمة جديدة"):
    c_i1, c_i2 = st.columns([3, 1])
    name = c_i1.text_input("المهمة")
    prio = c_i2.selectbox("الأولوية", ["عالية 🔥", "عادية 🟢"])
    if st.button("حفظ"):
        if name:
            st.session_state.tasks.append({"name": name, "done": False, "prio": prio})
            st.rerun()

for i, t in enumerate(st.session_state.tasks):
    with st.container():
        c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
        done = c1.checkbox("", value=t['done'], key=f"tk_{i}")
        if done != t['done']:
            st.session_state.tasks[i]['done'] = done
            if done: 
                st.session_state.xp += 20
                st.snow()
            check_badges()
            st.rerun()
        txt = f"~~{t['name']}~~" if t['done'] else t['name']
        c2.write(f"**{txt}** | {t['prio']}")
        if c3.button("🗑️", key=f"dl_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 10. مؤقت التركيز ---
st.divider()
st.subheader("⏳ مؤقت التركيز الذكي")
if st.button("🚀 ابدأ مؤقت 30 دقيقة"):
    st.session_state.badges["b2"]["un"] = True
    check_badges()
    ph = st.empty()
    for s in range(30 * 60, 0, -1):
        m, sc = divmod(s, 60)
        ph.metric("وقت التركيز ✍️", f"{m:02d}:{sc:02d}")
        time.sleep(1)
    st.balloons()
    st.session_state.xp += 50
    st.rerun()

st.divider()
st.caption("Study Flow Pro 🌊 - الإصدار الشامل 2026")
