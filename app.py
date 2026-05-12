import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Ultimate AI", page_icon="🚀", layout="wide")

# --- 2. التنسيق النهائي الفائق (CSS) ---
st.markdown("""
    <style>
    /* خلفية متدرجة هادئة */
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%) !important; }
    
    /* منع تداخل الكلام في القائمة الجانبية وتحسين عرضها */
    [data-testid="stSidebar"] { min-width: 320px !important; background-color: #ffffff !important; border-right: 1px solid #ddd; }
    [data-testid="stSidebar"] .stMarkdown p { font-size: 16px !important; line-height: 1.6 !important; color: #2c3e50 !important; }

    /* كروت المهام والأوسمة */
    .stCheckbox { background: white; padding: 10px; border-radius: 10px; margin-bottom: 5px; border: 1px solid #eee; }
    .badge-card { background: white; border-radius: 15px; padding: 15px; text-align: center; border: 2px solid #eef2f3; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .badge-locked { opacity: 0.2; filter: grayscale(1); }

    /* صناديق التخطيط الذكي */
    .ai-plan-box { background: #e3f2fd; border-radius: 15px; padding: 20px; border-right: 8px solid #1e88e5; margin-bottom: 20px; }
    
    /* الستريك الناري */
    .streak-container { background: #fff5f5; border: 2px solid #ff4d4d; border-radius: 20px; padding: 20px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام إدارة الحالة (Data System) ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'ai_plan' not in st.session_state: st.session_state.ai_plan = None
if 'badges' not in st.session_state:
    st.session_state.badges = {
        "b1": {"un": False, "n": "بداية بطل", "i": "🌱", "d": "أكملت أول مهمة!"},
        "b2": {"un": False, "n": "سيد الوقت", "i": "⏳", "d": "استخدمت المؤقت!"},
        "b3": {"un": False, "n": "الأسطورة", "i": "👑", "d": "وصلت لـ 500 XP!"},
        "b4": {"un": False, "n": "المخطط الذكي", "i": "🧠", "d": "استخدمت الـ AI!"},
        "b5": {"un": False, "n": "المنظم", "i": "📚", "d": "أضفت 5 مهام!"}
    }

# تحديث الليفل بناءً على النقاط
new_level = (st.session_state.xp // 500) + 1
if new_level > st.session_state.level:
    st.session_state.level = new_level
    st.balloons()
    st.toast(f"🎊 مبروك! وصلت للمستوى {st.session_state.level}")

# --- 4. القائمة الجانبية ( sidebar ) ---
with st.sidebar:
    st.markdown(f"<h1 style='text-align:center;'>المستقبل يبدأ الآن 🚀</h1>", unsafe_allow_html=True)
    st.markdown(f"### المستوى: {st.session_state.level}")
    
    # شريط التقدم للمستوى القادم
    progress_to_next = (st.session_state.xp % 500) / 500
    st.progress(progress_to_next)
    st.caption(f"متبقي {500 - (st.session_state.xp % 500)} XP للمستوى القادم")
    
    st.divider()
    st.subheader("📝 نوتة تصفية الذهن")
    st.session_state.notes = st.text_area("اكتب أي فكرة تزعجك هنا لتنساها وتذاكر:", value=st.session_state.notes, height=150)
    
    st.divider()
    if st.button("🔥 جرعة حماس سريعة"):
        quotes = ["أنت أقوى مما تعتقد!", "تذكر لماذا بدأت.", "القمة تتسع للجميع، لا تتوقف.", "كل دقيقة مذاكرة هي استثمار في مستقبلك."]
        st.warning(random.choice(quotes))

# --- 5. الهيدر والستريك ---
c_head, c_str = st.columns([2.5, 1])
with c_head:
    st.title("Study Flow Ultimate AI 🌊")
    st.markdown("#### منصتك الذكية لإدارة المذاكرة والتركيز")
    st.info(f"✨ نصيحة اليوم: {random.choice(['المراجعة قبل النوم تثبت المعلومات بنسبة 40%', 'اشرب الماء لتنشيط خلايا مخك', 'قاعدة الـ 10 دقائق: ابدأ وسوف تكمل'])}")

with c_str:
    st.markdown(f"""<div class="streak-container"><h1 style="color:#ff4d4d; margin:0;">🔥 {st.session_state.streak}</h1><p style="margin:0; font-weight:bold; color:#2c3e50;">يوم استمرار</p></div>""", unsafe_allow_html=True)

# --- 6. خزانة الأوسمة ---
st.divider()
st.subheader("🏅 حائط الإنجازات")
b_cols = st.columns(5)
for idx, (k, b) in enumerate(st.session_state.badges.items()):
    with b_cols[idx]:
        lock = "" if b["un"] else "badge-locked"
        st.markdown(f"""<div class="badge-card {lock}"><div style="font-size:35px;">{b['i']}</div><b>{b['n']}</b><br><small style="color:#7f8c8d;">{b['d']}</small></div>""", unsafe_allow_html=True)

# --- 7. المساعد الذكي (AI Planner) ---
st.divider()
st.subheader("🤖 منظم الجدول الذكي")
ai_col1, ai_col2 = st.columns([1, 2])

with ai_col1:
    st.write("اضغط لتوليد جدول زمني مثالي بناءً على مهامك المتبقية:")
    if st.button("🪄 ابدأ التخطيط بالذكاء الاصطناعي"):
        active = [t['name'] for t in st.session_state.tasks if not t['done']]
        if not active:
            st.error("أضف مهامك أولاً في القائمة بالأسفل!")
        else:
            st.session_state.badges["b4"]["un"] = True
            current = datetime.now()
            plan = []
            for task in active:
                start = current.strftime("%I:%M %p")
                current += timedelta(minutes=45)
                end = current.strftime("%I:%M %p")
                plan.append(f"📖 **{start} - {end}**: {task}")
                current += timedelta(minutes=10)
                plan.append(f"🥤 **راحة (10 دقائق)**")
            st.session_state.ai_plan = plan

with ai_col2:
    if st.session_state.ai_plan:
        with st.container():
            st.markdown('<div class="ai-plan-box"><b>📅 خطتك الزمنية المقترحة:</b></div>', unsafe_allow_html=True)
            for step in st.session_state.ai_plan:
                st.write(step)

# --- 8. إدارة المهام والتقدم ---
st.divider()
task_col, stat_col = st.columns([1.5, 1])

with task_col:
    st.subheader("📋 قائمة المهام اليومية")
    with st.expander("➕ إضافة مهمة جديدة"):
        name = st.text_input("ماذا ستنجز؟")
        if st.button("حفظ"):
            if name:
                st.session_state.tasks.append({"name": name, "done": False})
                if len(st.session_state.tasks) >= 5: st.session_state.badges["b5"]["un"] = True
                st.rerun()

    for i, t in enumerate(st.session_state.tasks):
        with st.container():
            c1, c2, c3 = st.columns([0.1, 0.85, 0.05])
            done = c1.checkbox("", value=t['done'], key=f"check_{i}")
            if done != t['done']:
                st.session_state.tasks[i]['done'] = done
                if done: 
                    st.session_state.xp += 30
                    st.session_state.badges["b1"]["un"] = True
                    st.snow()
                st.rerun()
            txt = f"~~{t['name']}~~" if t['done'] else t['name']
            c2.write(f"**{txt}**")
            if c3.button("🗑️", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

with stat_col:
    st.subheader("📊 إحصائيات الإنجاز")
    done_count = len([t for t in st.session_state.tasks if t['done']])
    total_count = len(st.session_state.tasks)
    if total_count > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم', 'باقي'], values=[done_count, total_count-done_count], hole=.6, marker_colors=['#27ae60', '#f1f1f1'])])
        fig.update_layout(height=250, margin=dict(t=0,b=0,l=0,r=0), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("أضف مهام لترى إحصائياتك هنا!")

# --- 9. التحدي والمؤقت ---
st.divider()
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.subheader("🎯 تحدي اليوم")
    if not st.session_state.challenge_done:
        st.warning("تحدي اليوم: أنهِ 3 مهام دفعة واحدة!")
        if st.button("تم التحدي! (+100 XP)"):
            st.session_state.xp += 100
            st.session_state.challenge_done = True
            st.rerun()
    else: st.success("🎉 أنت بطل! أنهيت تحدي اليوم.")

with f_col2:
    st.subheader("⏳ مؤقت بومودورو")
    if st.button("🚀 ابدأ مؤقت التركيز (25 دقيقة)"):
        st.session_state.badges["b2"]["un"] = True
        timer = st.empty()
        for s in range(25 * 60, 0, -1):
            m, sec = divmod(s, 60)
            timer.metric("وقت التركيز", f"{m:02d}:{sec:02d}")
            time.sleep(1)
        st.session_state.xp += 50
        st.rerun()

st.divider()
st.caption(f"Study Flow AI Ultimate v2.0 | 2026 | النقاط الإجمالية: {st.session_state.xp}")
