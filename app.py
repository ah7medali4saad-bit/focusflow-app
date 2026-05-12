import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, date

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="Study Flow Pro", page_icon="🎓", layout="wide")

# --- 2. تصميم الواجهة (CSS) لتنسيق الألوان والوضوح ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stButton>button { border-radius: 12px; font-weight: bold; transition: 0.3s; border: none; }
    .badge-unlocked { background: linear-gradient(45deg, #f39c12, #d35400); padding: 8px; border-radius: 8px; color: white; font-size: 13px; margin: 4px; display: inline-block; font-weight: bold; border: 1px solid #ffaa00; }
    .badge-locked { background: #21262d; padding: 8px; border-radius: 8px; color: #484f58; font-size: 13px; margin: 4px; display: inline-block; border: 1px dashed #484f58; }
    .streak-card { background-color: #161b22; border: 2px solid #f85149; padding: 15px; border-radius: 15px; text-align: center; }
    .quote-box { padding: 15px; border-radius: 10px; background: #21262d; border-right: 5px solid #58a6ff; margin-bottom: 20px; font-style: italic; }
    .status-card { background-color: #1f2937; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام إدارة البيانات (Session State) ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1 # نبدأ بـ 1 كتحفيز
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'badges' not in st.session_state: st.session_state.badges = {"first_task": False, "timer_master": False, "xp_500": False}

# --- 4. القائمة الجانبية (Sidebar) - مركز التحكم ---
with st.sidebar:
    st.title("🎓 Study Flow Pro")
    
    # عرض الرتبة والنقاط
    xp_val = st.session_state.xp
    rank = "مبتدئ 🌱" if xp_val < 200 else "محارب ⚔️" if xp_val < 1000 else "أسطورة 👑"
    st.markdown(f"<div class='status-card'>الرتبة: <b>{rank}</b><br>نقاطك: <b>{xp_val} XP</b></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # خزانة الأوسمة
    st.subheader("🏅 خزانة الأوسمة")
    if st.session_state.badges["first_task"]: st.markdown('<div class="badge-unlocked">✅ أول خطوة</div>', unsafe_allow_html=True)
    else: st.markdown('<div class="badge-locked">🔒 أول خطوة</div>', unsafe_allow_html=True)
    
    if st.session_state.badges["timer_master"]: st.markdown('<div class="badge-unlocked">⚡ سيد الوقت</div>', unsafe_allow_html=True)
    else: st.markdown('<div class="badge-locked">🔒 سيد الوقت</div>', unsafe_allow_html=True)
    
    if xp_val >= 500: st.markdown('<div class="badge-unlocked">🏆 خبير النقاط</div>', unsafe_allow_html=True)
    else: st.markdown('<div class="badge-locked">🔒 خبير النقاط</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # مفكرة التشتت
    st.subheader("📝 مفكرة التشتت")
    st.session_state.notes = st.text_area("اكتب أي فكرة تشتتك هنا لتنساها وتكمل مذاكرة..", value=st.session_state.notes, height=120)
    
    st.divider()
    
    # زر مشاركة الواتساب
    share_msg = f"أنا الآن برتبة {rank} في تطبيق Study Flow! مجموع نقاطي {xp_val} XP وستريك {st.session_state.streak} أيام 🔥"
    wa_url = f"https://wa.me/?text={share_msg}"
    st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background:#25d366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer; font-weight:bold;">شارك إنجازك على واتساب ✅</button></a>', unsafe_allow_html=True)

# --- 5. الهيدر (العنوان، الجملة التحفيزية، والستريك) ---
col_h1, col_h2 = st.columns([2, 1])

with col_h1:
    st.title("Study Flow 🌊")
    quotes = [
        "النجاح يبدأ بقرار التجربة، وينتهي بقرار الاستمرار.",
        "ذاكر بذكاء وليس بجهد فقط.",
        "مستقبلك يصنع مما تفعله اليوم، وليس غداً."
    ]
    st.markdown(f'<div class="quote-box">✨ {random.choice(quotes)}</div>', unsafe_allow_html=True)

with col_h2:
    st.markdown(f"""
    <div class="streak-card">
        <h2 style="color:#f85149 !important; margin:0;">🔥 {st.session_state.streak}</h2>
        <p style="margin:0; font-weight:bold;">يوم متتالي (Streak)</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. تحدي اليوم (تفاعلي ويختفي عند الإنجاز) ---
st.divider()
st.subheader("🏆 تحدي اليوم الذكي")
if not st.session_state.challenge_done:
    ch_col1, ch_col2 = st.columns([2, 1])
    ch_col1.info("تحدي اليوم: ذاكر لمدة 45 دقيقة متواصلة دون لمس الهاتف تماماً! (جائزة 100 XP)")
    if ch_col2.button("✅ أتممت التحدي!"):
        st.session_state.challenge_done = True
        st.session_state.xp += 100
        st.balloons()
        st.rerun()
else:
    st.success("🎊 مذهل! أتممت تحدي اليوم وحصلت على النقاط. نراك غداً في تحدٍ جديد!")

# --- 7. لوحة الإنجاز والنصائح الذكية ---
st.divider()
col_graph, col_tips = st.columns([1, 1])

with col_graph:
    done_count = len([t for t in st.session_state.tasks if t['done']])
    total_count = len(st.session_state.tasks)
    if total_count > 0:
        fig = go.Figure(data=[go.Pie(labels=['إنجاز', 'متبقي'], values=[done_count, total_count-done_count], hole=.6, marker_colors=['#238636', '#30363d'])])
        fig.update_layout(showlegend=True, height=280, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("أضف مهامك لترى رسمك البياني هنا.")

with col_tips:
    st.subheader("💡 نصيحة ذكية")
    tips = [
        "جرب تقنية 'فاينمان': اشرح ما ذاكرته لنفسك بصوت عالٍ.",
        "اشرب كوباً من الماء كل ساعة لتحافظ على نشاط عقلك.",
        "ابدأ دائماً بالمهمة التي تسبب لك أكبر قدر من القلق."
    ]
    st.write(random.choice(tips))
    if total_count > 0 and done_count == 0:
        st.info("نصيحة إضافية: ابدأ بأصغر مهمة في جدولك لتكسر حاجز الملل.")

# --- 8. إدارة جدول المهام ---
st.divider()
st.subheader("📋 الجدول الدراسي اليومي")
with st.expander("➕ أضف مهمة جديدة"):
    c1, c2, c3 = st.columns([2, 1, 1])
    t_name = c1.text_input("اسم المهمة")
    t_sub = c2.text_input("المادة")
    t_prio = c3.selectbox("الأولوية", ["عالية 🔥", "متوسطة 🟡", "عادية 🟢"])
    if st.button("حفظ المهمة"):
        if t_name:
            st.session_state.tasks.append({"name": t_name, "sub": t_sub, "prio": t_prio, "done": False})
            st.session_state.badges["first_task"] = True
            st.rerun()

# عرض المهام
for i, t in enumerate(st.session_state.tasks):
    with st.container():
        col_check, col_text, col_del = st.columns([0.1, 0.8, 0.1])
        is_done = col_check.checkbox("", value=t['done'], key=f"t_{i}")
        if is_done != t['done']:
            st.session_state.tasks[i]['done'] = is_done
            if is_done:
                st.session_state.xp += 20
                st.snow()
            st.rerun()
        
        label = f"~~{t['name']}~~" if t['done'] else t['name']
        col_text.write(f"**{label}** | {t['sub']} | {t['prio']}")
        if col_del.button("🗑️", key=f"d_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 9. مؤقت التركيز الذكي ---
st.divider()
st.header("⏳ مؤقت التركيز (30:10)")
st_c1, st_c2 = st.columns([1, 2])

with st_c1:
    m_study = st.number_input("دقائق الدراسة:", value=30, step=5)
    st.write(f"🎁 ستحصل على **{(m_study//30)*10} دقائق راحة** تلقائياً.")

with st_c2:
    if st.button("🚀 ابدأ جلسة التركيز"):
        timer_ph = st.empty()
        for s in range(m_study * 60, 0, -1):
            mins, secs = divmod(s, 60)
            timer_ph.metric("تركيز عميق ✍️", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
        st.balloons()
        st.session_state.xp += 50
        st.session_state.badges["timer_master"] = True
        st.success("عمل رائع! انتهت الجلسة وحصلت على 50 XP.")

st.divider()
st.caption("Study Flow Pro 🌊 - رفقي المخلص للنجاح | 2026")
