import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow", page_icon="🎓", layout="wide")

# --- 2. تنسيق الألوان والشكل (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #1a1c24; color: #ffffff; }
    .stat-card { background-color: #2d333b; padding: 20px; border-radius: 15px; border: 1px solid #444c56; text-align: center; }
    h1, h2, h3 { color: #58a6ff !important; font-weight: bold; }
    p, label, .stMarkdown { color: #adbac7 !important; font-size: 1.1rem; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #238636; color: white; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #2ea043; }
    .challenge-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px; border-radius: 15px; color: white !important; border: 1px solid #60a5fa;
    }
    .quote-box {
        padding: 15px; border-radius: 10px; background: #21262d; border-right: 5px solid #58a6ff; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. بنك البيانات الضخم (جمل وتحديات) ---
# ملاحظة: يمكنك إضافة مئات الجمل هنا وسيقوم الكود باختيار واحدة عشوائياً
quotes_bank = [
    "النجاح هو الانتقال من فشل إلى فشل دون فقدان الحماس.",
    "Success is stumbling from failure to failure with no loss of enthusiasm.",
    "كل إنجاز عظيم كان يعتبر مستحيلاً في البداية.",
    "Every great achievement was once considered impossible.",
    "لا تنتظر الوقت المناسب، ابدأ الآن!",
    "Don't wait for the right time, start now!",
    "السر في المضي قدماً هو البدء.",
    "The secret of getting ahead is getting started.",
    "انضباطك اليوم هو حريتك غداً.",
    "Your discipline today is your freedom tomorrow.",
    "اجعل من مذاكرتك عبادة تؤجر عليها.",
    "القمة تتسع للجميع، لكن لا يصلها إلا المجتهدون.",
    "تعب الدراسة يزول، وحلاوة النجاح تبقى للأبد.",
    "ذاكر وكأنك لا تملك فرصة ثانية.",
    "Be so good they can’t ignore you.",
    "أنت أقوى مما تعتقد، فقط استمر.",
    "Your future self will thank you for today's hard work."
]

challenges_bank = [
    "تحدي التركيز: ذاكر لمدة 25 دقيقة دون أي تشتت! (50 XP)",
    "تحدي الانطلاق: أنهِ أول مهمة في جدولك في أقل من ساعة! (40 XP)",
    "تحدي التنظيم: رتب مكتبك قبل البدء لمدة 5 دقائق! (20 XP)",
    "تحدي الصمود: اقرأ 10 صفحات من مادتك الصعبة الآن! (30 XP)",
    "تحدي المياه: اشرب كوباً من الماء وابدأ المذاكرة فوراً! (10 XP)",
    "تحدي التلخيص: اكتب ملخصاً سريعاً لأهم نقطة ذاكرتها اليوم! (45 XP)",
    "تحدي المراجعة: راجع ما ذاكرته بالأمس لمدة 10 دقائق! (35 XP)",
    "تحدي الفضول: ابحث عن معلومة إضافية خارج المنهج عن درسك! (50 XP)",
    "تحدي التدوين: اكتب هدف الغد قبل أن تغلق الموقع! (20 XP)",
    "تحدي التكرار: اشرح درساً صعباً لنفسك بصوت عالٍ! (40 XP)"
]

# --- 4. نظام البيانات ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'goal' not in st.session_state: st.session_state.goal = ""

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.title("🎓 Study Flow")
    st.markdown(f"### مستوى الخبرة: `{st.session_state.xp} XP` 🔥")
    st.divider()
    lang = st.selectbox("Language / اللغة", ["العربية", "English"])
    st.divider()
    st.subheader("🎯 هدف اليوم / Today's Goal")
    st.session_state.goal = st.text_input("اكتب هدفك هنا", value=st.session_state.goal)
    st.divider()
    st.info("💡 **نصيحة ذكية:** المخ يحتاج للأكسجين، خذ نفساً عميقاً كل 15 دقيقة.")

# --- 6. الهيدر والتحفيز العشوائي ---
# اختيار جملة وتحدي عشوائي عند كل "تشغيل" للكود
selected_quote = random.choice(quotes_bank)
selected_challenge = random.choice(challenges_bank)

col_head1, col_head2 = st.columns([2, 1])

with col_head1:
    st.title("Study Flow 🌊")
    st.markdown(f"""<div class="quote-box">✨ {selected_quote}</div>""", unsafe_allow_html=True)

with col_head2:
    st.markdown(f"""
    <div class="challenge-container">
        <b>🏆 تحدي اللحظة:</b><br>
        {selected_challenge}
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
    high_prio = [t for t in st.session_state.tasks if t['pri'] == "عالية (High)" and not t['done']]
    if high_prio:
        for hp in high_prio:
            st.error(f"⚠️ هام: لا تنسَ إنهاء {hp['name']}")
    else:
        st.success("أنت تسير بشكل رائع! استمر في الإبداع.")

st.divider()

# --- 8. إضافة المهام ---
st.subheader("➕ إضافة مهمة جديدة")
with st.expander("اضغط هنا لإضافة مادة أو مهمة"):
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1: t_name = st.text_input("اسم المهمة")
    with c2: t_sub = st.text_input("اسم المادة")
    with c3: t_deadline = st.date_input("الموعد النهائي")
    with c4: t_pri = st.selectbox("الأولوية", ["عالية (High)", "متوسطة (Med)", "منخفضة (Low)"])
    
    if st.button("حفظ في الجدول"):
        if t_name:
            st.session_state.tasks.append({
                "name": t_name, "sub": t_sub, "deadline": t_deadline, 
                "pri": t_pri, "done": False
            })
            st.rerun()

# --- 9. عرض المهام ---
st.subheader("📋 جدول المهام اليومي")
if not st.session_state.tasks:
    st.info("جدولك فارغ حالياً. ابدأ بإضافة مهامك للنجاح!")
else:
    for i, t in enumerate(st.session_state.tasks):
        with st.container():
            col_check, col_text, col_prio, col_del = st.columns([0.1, 0.6, 0.2, 0.1])
            is_done = col_check.checkbox("", value=t['done'], key=f"c_{i}")
            if is_done != t['done']:
                st.session_state.tasks[i]['done'] = is_done
                st.session_state.xp += 20 if is_done else -20
                st.rerun()
            
            label = f"~~{t['name']}~~" if t['done'] else t['name']
            col_text.markdown(f"**{label}** | مادة: `{t['sub']}` | موعد: `{t['deadline']}`")
            
            p_icon = "🔴" if t['pri'] == "عالية (High)" else "🟡" if t['pri'] == "متوسطة (Med)" else "🟢"
            col_prio.write(f"{p_icon} {t['pri']}")
            
            if col_del.button("🗑️", key=f"d_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

# --- 10. مؤقت الدراسة والراحة ---
st.divider()
st.header("⏳ مؤقت الدراسة الذكي (30:10)")
st_col1, st_col2 = st.columns([1, 2])
with st_col1:
    duration = st.number_input("دقائق المذاكرة:", min_value=5, value=30, step=5)
    rest = (duration // 30) * 10
    st.write(f"⏱️ ستحصل على **{rest} دقائق راحة** تلقائياً.")

with st_col2:
    if st.button("🚀 ابدأ الآن"):
        timer_place = st.empty()
        for s in range(duration * 60, 0, -1):
            m, s_remainder = divmod(s, 60)
            timer_place.metric("وقت التركيز ✍️", f"{m:02d}:{s_remainder:02d}")
            time.sleep(1)
        st.balloons()
        
        if rest > 0:
            st.success(f"وقت الراحة بدأ! استرخِ لمدة {rest} دقائق.")
            for s in range(rest * 60, 0, -1):
                m, s_remainder = divmod(s, 60)
                timer_place.metric("وقت الراحة ☕", f"{m:02d}:{s_remainder:02d}")
                time.sleep(1)
            st.warning("انتهت الراحة! لنكمل الرحلة.")

st.divider()
st.caption("Study Flow 🌊 - رفيقك الأول للنجاح | 2026")
