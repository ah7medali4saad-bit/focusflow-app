import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Ultimate AI", page_icon="🚀", layout="wide")

# --- 2. التنسيق الفائق (CSS) لمنع تداخل الكلام تماماً ---
st.markdown("""
    <style>
    /* خلفية متدرجة هادئة وضع فاتح */
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%) !important; }
    
    /* إصلاح القائمة الجانبية (Sidebar) لضمان عدم اختفاء الكلام */
    [data-testid="stSidebar"] { 
        min-width: 320px !important; 
        background-color: #ffffff !important; 
        border-right: 1px solid #ddd; 
    }
    
    /* إجبار النصوص على النزول لسطر جديد وعدم التداخل */
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label { 
        white-space: normal !important; 
        word-wrap: break-word !important; 
        font-size: 16px !important; 
        line-height: 1.6 !important; 
        color: #2c3e50 !important; 
    }

    /* كروت المهام والأوسمة */
    .stCheckbox { background: white; padding: 10px; border-radius: 10px; margin-bottom: 5px; border: 1px solid #eee; }
    .badge-card { background: white; border-radius: 15px; padding: 15px; text-align: center; border: 2px solid #eef2f3; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .badge-locked { opacity: 0.2; filter: grayscale(1); }

    /* صناديق التخطيط الذكي */
    .ai-plan-box { background: #e3f2fd; border-radius: 15px; padding: 20px; border-right: 8px solid #1e88e5; margin-bottom: 20px; }
    
    /* الستريك الناري */
    .streak-container { background: #fff5f5; border: 2px solid #ff4d4d; border-radius: 20px; padding: 20px; text-align: center; }

    /* زر الواتساب الجانبي المحسن */
    .whatsapp-btn {
        display: block;
        width: 100%;
        background-color: #25d366;
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 15px;
        border: none;
    }
    .whatsapp-btn:hover { background-color: #128c7e; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام إدارة الحالة (Session State) ---
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

# تحديث الليفل
new_level = (st.session_state.xp // 500) + 1
if new_level > st.session_state.level:
    st.session_state.level = new_level
    st.balloons()

# --- 4. القائمة الجانبية (التي كان بها المشكلة) ---
with st.sidebar:
    st.markdown(f"<h2 style='text-align:center;'>الملف الشخصي 👤</h2>", unsafe_allow_html=True)
    st.markdown(f"**المستوى الحالي:** {st.session_state.level}")
    
    # شريط التقدم لليفل القادم
    progress_val = (st.session_state.xp % 500) / 500
    st.progress(progress_val)
    st.caption(f"متبقي {500 - (st.session_state.xp % 500)} XP للفل القادم")
    
    st.divider()
    st.subheader("📒 نوتة تصفية الذهن")
    st.session_state.notes = st.text_area("فرغ أفكارك هنا لتركز في المذاكرة:", value=st.session_state.notes, height=120)
    
    st.divider()
    # زر مشاركة الواتساب
    share_msg = f"أنا الآن في المستوى {st.session_state.level} بنقاط {st.session_state.xp} XP في تطبيق Study Flow! 🚀"
    st.markdown(f'<a href="https://wa.me/?text={share_msg}" target="_blank" class="whatsapp-btn">🚀 شارك مستواك على واتساب</a>', unsafe_allow_html=True)
    
    st.divider()
    if st.button("🔥 جرعة حماس"):
        st.warning(random.choice(["الاستمرارية أهم من السرعة.", "مستقبلك يبدأ من قرارك الآن.", "أنت بطل قصتك!"]))

# --- 5. الهيدر والستريك ---
c1, c2 = st.columns([2.5, 1])
with c1:
    st.title("Study Flow Ultimate AI 🌊")
    st.info(f"✨ نصيحة اليوم: {random.choice(['ذاكر 50 دقيقة وارتاح 10 دقائق.', 'اشرب ماء بانتظام.', 'النوم الجيد هو وقود الذاكرة.'])}")

with c2:
    st.markdown(f"""<div class="streak-container"><h1 style="color:#ff4d4d; margin:0;">🔥 {st.session_state.streak}</h1><p style="margin:0; font-weight:bold;">يوم استمرار</p></div>""", unsafe_allow_html=True)

# --- 6. الأوسمة ---
st.divider()
st.subheader("🏅 حائط الإنجازات")
cols = st.columns(5)
for idx, (k, b) in enumerate(st.session_state.badges.items()):
    with cols[idx]:
        lock = "" if b["un"] else "badge-locked"
        st.markdown(f"""<div class="badge-card {lock}"><div style="font-size:35px;">{b['i']}</div><b>{b['n']}</b><br><small>{b['d']}</small></div>""", unsafe_allow_html=True)

# --- 7. منظم الجدول الذكي (AI Planner) ---
st.divider()
st.subheader("🤖 المساعد الذكي لتنظيم الوقت")
ai_c1, ai_c2 = st.columns([1, 2])

with ai_col1 := ai_c1:
    st.write("حلل مهامك واحصل على جدول مثالي:")
    if st.button("🪄 توليد جدول المذاكرة"):
        active = [t['name'] for t in st.session_state.tasks if not t['done']]
        if not active:
            st.error("من فضلك أضف مهامك أولاً بالأسفل!")
        else:
            st.session_state.badges["b4"]["un"] = True
            curr = datetime.now()
            plan = []
            for task in active:
                s = curr.strftime("%I:%M %p")
                curr += timedelta(minutes=45)
                e = curr.strftime("%I:%M %p")
                plan.append(f"📖 **{s} - {e}**: {task}")
                curr += timedelta(minutes=10)
                plan.append(f"☕ **راحة 10 دقائق**")
            st.session_state.ai_plan = plan

with ai_col2 := ai_c2:
    if st.session_state.ai_plan:
        with st.container():
            st.markdown('<div class="ai-plan-box"><b>📅 خطتك الزمنية الذكية:</b></div>', unsafe_allow_html=True)
            for step in st.session_state.ai_plan:
                st.write(step)

# --- 8. قائمة المهام والإحصائيات ---
st.divider()
t_col, s_col = st.columns([1.5, 1])

with t_col:
    st.subheader("📋 قائمة المهام")
    with st.expander("➕ أضف مهمة"):
        name = st.text_input("ماذا ستنجز اليوم؟")
        if st.button("حفظ"):
            if name:
                st.session_state.tasks.append({"name": name, "done": False})
                if len(st.session_state.tasks) >= 5: st.session_state.badges["b5"]["un"] = True
                st.rerun()

    for i, t in enumerate(st.session_state.tasks):
        with st.container():
            tc1, tc2, tc3 = st.columns([0.1, 0.85, 0.05])
            done = tc1.checkbox("", value=t['done'], key=f"t_{i}")
            if done != t['done']:
                st.session_state.tasks[i]['done'] = done
                if done: 
                    st.session_state.xp += 30
                    st.session_state.badges["b1"]["un"] = True
                st.rerun()
            txt = f"~~{t['name']}~~" if t['done'] else t['name']
            tc2.write(f"**{txt}**")
            if tc3.button("🗑️", key=f"d_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

with s_col:
    st.subheader("📊 إحصائياتك")
    done_c = len([t for t in st.session_state.tasks if t['done']])
    total = len(st.session_state.tasks)
    if total > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم', 'باقي'], values=[done_c, total-done_c], hole=.6, marker_colors=['#27ae60', '#f1f1f1'])])
        fig.update_layout(height=250, margin=dict(t=0,b=0,l=0,r=0), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

# --- 9. التحدي والمؤقت ---
st.divider()
f1, f2 = st.columns(2)
with f1:
    st.subheader("🎯 تحدي اليوم")
    if not st.session_state.challenge_done:
        st.warning("تحدي اليوم: أنهِ جميع مهامك لتحصل على 100 XP إضافية!")
        if st.button("تم الإنجاز! ✅"):
            st.session_state.xp += 100
            st.session_state.challenge_done = True
            st.rerun()
    else: st.success("🎉 أنت مذهل! التحدي اكتمل.")

with f2:
    st.subheader("⏳ مؤقت التركيز")
    if st.button("🚀 ابدأ 25 دقيقة تركيز"):
        st.session_state.badges["b2"]["un"] = True
        timer_ph = st.empty()
        for s in range(25 * 60, 0, -1):
            m, sc = divmod(s, 60)
            timer_ph.metric("باقي على الانتهاء", f"{m:02d}:{sc:02d}")
            time.sleep(1)
        st.session_state.xp += 50
        st.rerun()

st.divider()
st.caption(f"Study Flow AI Ultimate v2.2 | 2026 | مجموع نقاطك: {st.session_state.xp}")
