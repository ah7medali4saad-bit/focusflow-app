import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow AI Ultimate", page_icon="🤖", layout="wide")

# --- 2. محرك التنسيق المتقدم (CSS) - حل مشكلة القائمة الجانبية نهائياً ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%) !important; }
    
    /* إصلاح القائمة الجانبية ومنع تداخل الكلام */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        min-width: 300px !important; /* تكبير عرض القائمة قليلاً */
    }
    
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label {
        color: #2c3e50 !important;
        white-space: normal !important; /* السماح للكلام بالنزول لسطر جديد */
        word-wrap: break-word !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
    }

    /* كروت الأوسمة */
    .badge-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .badge-locked { opacity: 0.2; filter: grayscale(1); }

    /* صندوق الجدولة الذكية */
    .ai-schedule {
        background: #e3f2fd;
        border-right: 5px solid #1e88e5;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    /* الستريك الناري */
    .streak-box {
        background: #fff5f5;
        border: 2px solid #ff4d4d;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام البيانات الشامل ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'ai_plan' not in st.session_state: st.session_state.ai_plan = None
if 'badges' not in st.session_state:
    st.session_state.badges = {
        "b1": {"un": False, "n": "بداية بطل", "i": "🌱", "d": "أكملت أول مهمة!"},
        "b2": {"un": False, "n": "سيد الوقت", "i": "⏳", "d": "استخدمت المؤقت!"},
        "b3": {"un": False, "n": "الأسطورة", "i": "👑", "d": "وصلت لـ 500 XP!"},
        "b4": {"un": False, "n": "المخطط الذكي", "i": "🧠", "d": "استخدمت اقتراح الـ AI!"},
        "b5": {"un": False, "n": "المنظم", "i": "📚", "d": "أضفت 5 مهام!"}
    }

# --- 4. القائمة الجانبية (تم تحسين الوضوح هنا) ---
with st.sidebar:
    st.title("👤 ملفك الشخصي")
    xp = st.session_state.xp
    rank = "طالب مستجد 🌱" if xp < 200 else "محارب ⚔️" if xp < 1000 else "دكتور 🎓"
    
    st.subheader(f"الرتبة الحالية: \n{rank}")
    st.progress(min(xp/1000, 1.0))
    st.write(f"**مجموع النقاط:** {xp} XP")
    
    st.divider()
    st.subheader("📒 مفكرة التشتت")
    st.session_state.notes = st.text_area("إذا جاءت فكرة في بالك وأنت تذاكر، اكتبها هنا لتفرغ عقلك وتركز:", value=st.session_state.notes, height=150)
    
    st.divider()
    share_msg = f"أنا برتبة {rank} في Study Flow! 🚀"
    st.markdown(f'<a href="https://wa.me/?text={share_msg}" target="_blank"><button style="width:100%; background:#25d366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold;">🚀 شارك مستواك الآن</button></a>', unsafe_allow_html=True)

# --- 5. الهيدر والستريك ---
c_h1, c_h2 = st.columns([2, 1])
with c_h1:
    st.title("Study Flow AI 🌊")
    st.info(f"💡 نصيحة ذكية: {random.choice(['الدراسة في الصباح الباكر تضاعف التركيز.', 'استخدم تقنية فيمان لشرح الدروس المعقدة.', 'اشرب ماء بانتظام أثناء المذاكرة.'])}")

with c_h2:
    st.markdown(f"""<div class="streak-box"><h2 style="color:#ff4d4d !important; margin:0;">🔥 {st.session_state.streak}</h2><p style="margin:0; font-weight:bold;">يوم متتالي</p></div>""", unsafe_allow_html=True)

# --- 6. خزانة الأوسمة ---
st.divider()
st.subheader("🏅 إنجازاتك")
cols = st.columns(5)
for idx, (k, b) in enumerate(st.session_state.badges.items()):
    with cols[idx]:
        lock = "" if b["un"] else "badge-locked"
        st.markdown(f"""<div class="badge-card {lock}"><div style="font-size:30px;">{b['i']}</div><b>{b['n']}</b><br><small>{b['d']}</small></div>""", unsafe_allow_html=True)

# --- 7. قسم التخطيط الذكي (AI Suggestion) ---
st.divider()
st.subheader("🤖 مساعد الجدول الذكي")
col_ai1, col_ai2 = st.columns([1, 2])

with col_ai1:
    st.write("بعد إضافة مهامك، اضغط الزر ليقوم الذكاء الاصطناعي بتنظيم وقتك:")
    if st.button("🪄 توليد جدول مذاكرة"):
        active_tasks = [t['name'] for t in st.session_state.tasks if not t['done']]
        if not active_tasks:
            st.error("أضف بعض المهام في قائمة المهام أولاً!")
        else:
            st.session_state.badges["b4"]["un"] = True
            current_time = datetime.now()
            plan = []
            for task in active_tasks:
                start_str = current_time.strftime("%I:%M %p")
                current_time += timedelta(minutes=45)
                end_str = current_time.strftime("%I:%M %p")
                plan.append(f"⏱️ **{start_str} - {end_str}**: {task}")
                current_time += timedelta(minutes=10)
                plan.append(f"☕ **راحة 10 دقائق**")
            st.session_state.ai_plan = plan

with col_ai2:
    if st.session_state.ai_plan:
        with st.container():
            st.markdown('<div class="ai-schedule"><b>📅 جدولك المقترح لليوم:</b></div>', unsafe_allow_html=True)
            for step in st.session_state.ai_plan:
                st.write(step)

# --- 8. إدارة المهام والإحصائيات ---
st.divider()
c1, c2 = st.columns([1.5, 1])
with c1:
    st.subheader("📋 قائمة المهام")
    with st.expander("➕ أضف مهمة جديدة"):
        t_name = st.text_input("ماذا ستذاكر اليوم؟")
        if st.button("حفظ المهمة"):
            if t_name:
                st.session_state.tasks.append({"name": t_name, "done": False})
                if len(st.session_state.tasks) >= 5: st.session_state.badges["b5"]["un"] = True
                st.rerun()

    for i, t in enumerate(st.session_state.tasks):
        with st.container():
            tc1, tc2, tc3 = st.columns([0.1, 0.8, 0.1])
            d = tc1.checkbox("", value=t['done'], key=f"tk_{i}")
            if d != t['done']:
                st.session_state.tasks[i]['done'] = d
                if d: 
                    st.session_state.xp += 30
                    st.session_state.badges["b1"]["un"] = True
                    st.balloons()
                st.rerun()
            txt = f"~~{t['name']}~~" if t['done'] else t['name']
            tc2.write(f"**{txt}**")
            if tc3.button("🗑️", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

with c2:
    st.subheader("📊 إحصائيات الإنجاز")
    done_n = len([t for t in st.session_state.tasks if t['done']])
    total_n = len(st.session_state.tasks)
    if total_n > 0:
        fig = go.Figure(data=[go.Pie(labels=['تمت', 'باقية'], values=[done_n, total_n-done_n], hole=.6, marker_colors=['#27ae60', '#ecf0f1'])])
        fig.update_layout(height=250, margin=dict(t=0,b=0,l=0,r=0), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

# --- 9. التحدي والمؤقت ---
st.divider()
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.subheader("🎯 تحدي اليوم")
    if not st.session_state.challenge_done:
        st.warning("التحدي: ذاكر لمدة 25 دقيقة بتركيز عميق (جلسة بومودورو)!")
        if st.button("أتممت التحدي! (+100 XP)"):
            st.session_state.challenge_done = True
            st.session_state.xp += 100
            st.rerun()
    else: st.success("🎉 تحدي اليوم مكتمل بنجاح!")

with col_f2:
    st.subheader("⏳ مؤقت التركيز")
    if st.button("🚀 ابدأ مؤقت 25 دقيقة"):
        st.session_state.badges["b2"]["un"] = True
        ph = st.empty()
        for s in range(25 * 60, 0, -1):
            m, sec = divmod(s, 60)
            ph.metric("متبقي", f"{m:02d}:{sec:02d}")
            time.sleep(1)
        st.session_state.xp += 50
        st.rerun()

st.divider()
st.caption("Study Flow AI Pro 🌊 - الإصدار النهائي المنظم 2026")
