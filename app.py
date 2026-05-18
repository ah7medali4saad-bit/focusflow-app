import streamlit as st
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Ultimate AI", page_icon="🚀", layout="wide")

# --- 2. التنسيق (CSS) لضمان عدم تداخل الكلام وظهور كل شيء ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%) !important; }
    
    /* تنسيق القائمة الجانبية */
    [data-testid="stSidebar"] { 
        min-width: 320px !important; 
        background-color: #ffffff !important; 
        border-right: 1px solid #ddd; 
    }
    
    /* منع تداخل النصوص في الجنب */
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label { 
        white-space: normal !important; 
        word-wrap: break-word !important; 
        font-size: 16px !important; 
        line-height: 1.6 !important; 
        color: #2c3e50 !important; 
    }

    /* كروت المهام والأوسمة */
    .badge-card { background: white; border-radius: 15px; padding: 15px; text-align: center; border: 2px solid #eef2f3; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .badge-locked { opacity: 0.2; filter: grayscale(1); }
    .ai-plan-box { background: #e3f2fd; border-radius: 15px; padding: 20px; border-right: 8px solid #1e88e5; margin-bottom: 20px; }
    .streak-container { background: #fff5f5; border: 2px solid #ff4d4d; border-radius: 20px; padding: 20px; text-align: center; }

    /* تاجات مصفوفة آيزنهاور */
    .priority-1 { color: #e74c3c; font-weight: bold; }
    .priority-2 { color: #e67e22; font-weight: bold; }
    .priority-3 { color: #2980b9; font-weight: bold; }
    .priority-4 { color: #7f8c8d; font-weight: bold; }

    /* زر الواتساب */
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
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. نظام إدارة البيانات ---
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
st.session_state.level = (st.session_state.xp // 500) + 1

# قاموس لترجمة مصفوفة آيزنهاور وعرضها بشكل جمالي
matrix_options = {
    1: "🔴 مهم وعاجل (افعل الآن)",
    2: "🟠 مهم وغير عاجل (خطط له)",
    3: "🔵 غير مهم وعاجل (فوّضه/انجزه سريعاً)",
    4: "⚪ غير مهم وغير عاجل (اتركه/احذفه)"
}

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>الملف الشخصي 👤</h2>", unsafe_allow_html=True)
    st.markdown(f"**المستوى الحالي:** {st.session_state.level}")
    
    # شريط التقدم
    progress_val = (st.session_state.xp % 500) / 500
    st.progress(min(progress_val, 1.0))
    st.caption(f"متبقي {500 - (st.session_state.xp % 500)} XP للمستوى القادم")
    
    st.divider()
    st.subheader("📒 نوتة تصفية الذهن")
    st.session_state.notes = st.text_area("اكتب أي فكرة تشتتك هنا لتركز:", value=st.session_state.notes, height=120)
    
    st.divider()
    # زرار الواتساب
    share_msg = f"أنا في المستوى {st.session_state.level} بنقاط {st.session_state.xp} XP في تطبيق Study Flow! 🔥🚀"
    st.markdown(f'<a href="https://wa.me/?text={share_msg}" target="_blank" class="whatsapp-btn">🚀 نشر الإنجاز (واتساب)</a>', unsafe_allow_html=True)
    
    st.divider()
    if st.button("🔥 جرعة حماس"):
        st.warning(random.choice(["أنت بطل!", "كل دقيقة مذاكرة بتقربك لحلمك.", "استمر، العظماء لا يتوقفون."]))

# --- 5. الهيدر والستريك ---
c_h1, c_h2 = st.columns([2.5, 1])
with c_h1:
    st.title("Study Flow Ultimate AI 🌊")
    st.info(f"💡 نصيحة ذكية: {random.choice(['المذاكرة الصبح بركة.', 'قاعدة الـ 10 دقائق: ابدأ وهتكمل.', 'ابعد موبايلك عنك تماماً.'])}")

with c_h2:
    st.markdown(f"""<div class="streak-container"><h1 style="color:#ff4d4d; margin:0;">🔥 {st.session_state.streak}</h1><p style="margin:0; font-weight:bold;">يوم استمرار</p></div>""", unsafe_allow_html=True)

# --- 6. خزانة الأوسمة ---
st.divider()
st.subheader("🏅 حائط الإنجازات")
b_cols = st.columns(5)
for idx, (k, b) in enumerate(st.session_state.badges.items()):
    with b_cols[idx]:
        lock = "" if b["un"] else "badge-locked"
        st.markdown(f"""<div class="badge-card {lock}"><div style="font-size:35px;">{b['i']}</div><b>{b['n']}</b><br><small>{b['d']}</small></div>""", unsafe_allow_html=True)

# --- 7. منظم الجدول الذكي (AI Planner مع مصفوفة آيزنهاور) ---
st.divider()
st.subheader("🤖 منظم الجدول بالذكاء الاصطناعي (ترتيب حسب الأولوية)")
ai_col1, ai_col2 = st.columns([1, 2])

with ai_col1:
    st.write("يقوم الذكاء الاصطناعي بترتيب وقتك تلقائياً بحيث يبدأ بالمهام الأكثر أهمية (مصفوفة آيزنهاور):")
    if st.button("🪄 توليد جدول مذاكرة ذكي"):
        # جلب المهام غير المكتملة وترتيبها بناءً على رقم الأولوية (الأقل رقماً يعني أعلى أهمية)
        active_tasks = [t for t in st.session_state.tasks if not t['done']]
        active_tasks.sort(key=lambda x: x.get('priority', 4))
        
        if active_tasks:
            st.session_state.badges["b4"]["un"] = True
            current_time = datetime.now()
            plan = []
            for task in active_tasks:
                start_str = current_time.strftime("%I:%M %p")
                current_time += timedelta(minutes=45)
                end_str = current_time.strftime("%I:%M %p")
                p_text = matrix_options[task.get('priority', 4)].split(' ')[0] # جلب الإيموجي فقط
                plan.append(f"{p_text} **{start_str} - {end_str}**: مذاكرة ({task['name']})")
                current_time += timedelta(minutes=10)
                plan.append(f"🥤 **راحة 10 دقائق**")
            st.session_state.ai_plan = plan
        else:
            st.error("أضف مهامك أولاً في القائمة بالأسفل!")

with ai_col2:
    if st.session_state.ai_plan:
        with st.container():
            st.markdown('<div class="ai-plan-box"><b>📅 خطتك الزمنية الذكية المرتبة بالأولويات:</b></div>', unsafe_allow_html=True)
            for step in st.session_state.ai_plan:
                st.write(step)

# --- 8. إدارة المهام والإحصائيات ---
st.divider()
task_col, stat_col = st.columns([1.5, 1])

with task_col:
    st.subheader("📋 قائمة المهام اليومية (مصفوفة آيزنهاور)")
    with st.expander("➕ أضف مهمة جديدة وتحديد أولويتها"):
        new_task = st.text_input("ناوي تذاكر إيه النهاردة؟")
        # اختيار درجة الأهمية تبعا للمصفوفة
        task_priority = st.selectbox(
            "حدد تصنيف المهمة تبعاً لمصفوفة آيزنهاور:", 
            options=list(matrix_options.keys()), 
            format_func=lambda x: matrix_options[x]
        )
        if st.button("حفظ المهمة"):
            if new_task:
                st.session_state.tasks.append({"name": new_task, "done": False, "priority": task_priority})
                if len(st.session_state.tasks) >= 5: st.session_state.badges["b5"]["un"] = True
                st.rerun()

    for i, t in enumerate(st.session_state.tasks):
        with st.container():
            tc1, tc2, tc3 = st.columns([0.1, 0.85, 0.05])
            is_done = tc1.checkbox("", value=t['done'], key=f"tcheck_{i}")
            if is_done != t['done']:
                st.session_state.tasks[i]['done'] = is_done
                if is_done: 
                    st.session_state.xp += 30
                    st.session_state.badges["b1"]["un"] = True
                st.rerun()
            
            # عرض اسم المهمة مع درجة الأولوية بلونها الخاص
            p_id = t.get('priority', 4)
            p_label = matrix_options[p_id].split(' ')[0] # الإيموجي الدال على التصنيف
            
            txt = f"~~{t['name']}~~ ({p_label})" if t['done'] else f"**{t['name']}** <span class='priority-{p_id}'>({p_label})</span>"
            tc2.markdown(txt, unsafe_allow_html=True)
            
            if tc3.button("🗑️", key=f"tdel_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

with stat_col:
    st.subheader("📊 نسبة الإنجاز")
    done_n = len([t for t in st.session_state.tasks if t['done']])
    total_n = len(st.session_state.tasks)
    if total_n > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم', 'باقي'], values=[done_n, total_n-done_n], hole=.6, marker_colors=['#27ae60', '#f1f1f1'])])
        fig.update_layout(height=250, margin=dict(t=0,b=0,l=0,r=0), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("أضف مهام لترى تقدمك هنا!")

# --- 9. التحدي والمؤقت ---
st.divider()
f1, f2 = st.columns(2)
with f1:
    st.subheader("🎯 تحدي اليوم")
    if not st.session_state.challenge_done:
        st.warning("تحدي اليوم: خلص 3 مهام وخد 100 XP إضافية!")
        if st.button("أتممت التحدي! ✅"):
            st.session_state.xp += 100
            st.session_state.challenge_done = True
            st.rerun()
    else:
        st.success("🎉 أنت وحش! التحدي اكتمل.")

with f2:
    st.subheader("⏳ مؤقت التركيز (بومودورو)")
    if st.button("🚀 ابدأ التركيز الآن"):
        st.session_state.badges["b2"]["un"] = True
        timer_placeholder = st.empty()
        for s in range(25 * 60, 0, -1):
            m, sc = divmod(s, 60)
            timer_placeholder.metric("الوقت المتبقي", f"{m:02d}:{sc:02d}")
            time.sleep(1)
        st.session_state.xp += 50
        st.rerun()

st.divider()
st.caption(f"Study Flow AI Ultimate v3.0 | 2026 | مصفوفة آيزنهاور الذكية المدمجة")
