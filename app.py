import streamlit as st
import time
import random
import plotly.graph_objects as go

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Study Flow Pro", page_icon="🎓", layout="wide")

# --- 2. منع تداخل الكلام نهائياً (CSS) ---
st.markdown("""
    <style>
    /* تحسين المسافات العامة */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* منع تداخل النصوص وجعل المسافة بين الأسطر مريحة */
    h1, h2, h3, p, span, label {
        line-height: 1.8 !important;
        margin-bottom: 15px !important;
        display: block; /* لضمان عدم ركوب النصوص فوق بعضها */
    }

    /* كروت الأوسمة: حجم ثابت ومنظم */
    .badge-box {
        background-color: #ffffff;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 10px;
        min-width: 150px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .badge-locked { opacity: 0.3; filter: grayscale(1); }

    /* تنسيق القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        padding: 20px 10px !important;
    }

    /* صناديق واضحة لكل قسم */
    .section-container {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة البيانات ---
if 'tasks' not in st.session_state: st.session_state.tasks = []
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'challenge_done' not in st.session_state: st.session_state.challenge_done = False
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'badges' not in st.session_state:
    st.session_state.badges = {
        "b1": {"un": False, "n": "أول خطوة", "i": "🌱", "d": "أكملت أول مهمة!"},
        "b2": {"un": False, "n": "سيد الوقت", "i": "⏳", "d": "استخدمت المؤقت!"},
        "b3": {"un": False, "n": "الأسطورة", "i": "👑", "d": "وصلت لـ 500 XP!"},
        "b4": {"un": False, "n": "الوحش", "i": "🔥", "d": "أتممت التحدي!"},
        "b5": {"un": False, "n": "المنظم", "i": "📚", "d": "أضفت 5 مهام!"}
    }

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.title("📊 بروفايلك")
    xp = st.session_state.xp
    rank = "طالب 📖" if xp < 200 else "محارب ⚔️" if xp < 1000 else "دكتور 🎓"
    st.success(f"الرتبة: {rank}")
    st.info(f"النقاط: {xp} XP")
    
    st.divider()
    st.subheader("📒 نوتة التشتت")
    st.session_state.notes = st.text_area("اكتب فكرتك هنا..", value=st.session_state.notes, height=150)
    
    st.divider()
    st.markdown(f'<a href="https://wa.me/?text=أنا برتبة {rank} في Study Flow!" target="_blank"><button style="width:100%; background:#25d366; color:white; border:none; padding:10px; border-radius:10px; cursor:pointer; font-weight:bold;">🚀 شارك مستواك</button></a>', unsafe_allow_html=True)

# --- 5. الهيدر والستريك ---
col_head, col_str = st.columns([2, 1])
with col_head:
    st.title("Study Flow 🌊")
    st.info("💡 النجاح هو مجموع جهود صغيرة تتكرر كل يوم.")

with col_str:
    st.markdown(f"""
    <div style="background:#fff5f5; border:2px solid #ff4d4d; border-radius:15px; padding:15px; text-align:center;">
        <h2 style="color:#ff4d4d !important; margin:0;">🔥 {st.session_state.streak}</h2>
        <p style="margin:0; font-weight:bold; color:#333 !important;">يوم متتالي</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. الأوسمة (توزيع أفقي بمسافات) ---
st.divider()
st.subheader("🏅 خزانة الأوسمة")
cols = st.columns(5)
for idx, (k, b) in enumerate(st.session_state.badges.items()):
    with cols[idx]:
        lock = "" if b["un"] else "badge-locked"
        st.markdown(f"""
        <div class="badge-box {lock}">
            <div style="font-size:35px;">{b['i']}</div>
            <b style="color:#f0883e;">{b['n']}</b><br>
            <small style="color:#666;">{b['d']}</small>
        </div>
        """, unsafe_allow_html=True)

# --- 7. التحدي والإحصائيات ---
st.divider()
c1, c2 = st.columns([1.5, 1])
with c1:
    st.subheader("🎯 تحدي اليوم")
    if not st.session_state.challenge_done:
        st.warning("التحدي: ذاكر لمدة 25 دقيقة بتركيز كامل!")
        if st.button("أتممت التحدي ✅"):
            st.session_state.challenge_done = True
            st.session_state.xp += 100
            st.session_state.badges["b4"]["un"] = True
            st.balloons()
            st.rerun()
    else:
        st.success("🎉 أحسنت! التحدي اكتمل.")

with c2:
    done_n = len([t for t in st.session_state.tasks if t['done']])
    total_n = len(st.session_state.tasks)
    if total_n > 0:
        fig = go.Figure(data=[go.Pie(labels=['تم', 'باقي'], values=[done_n, total_n-done_n], hole=.6, marker_colors=['#28a745', '#eee'])])
        fig.update_layout(height=200, margin=dict(t=0,b=0,l=0,r=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# --- 8. قائمة المهام (منظمة في حاويات) ---
st.divider()
st.subheader("📋 قائمة المهام")
with st.expander("➕ أضف مهمة"):
    name = st.text_input("المهمة")
    if st.button("حفظ"):
        if name:
            st.session_state.tasks.append({"name": name, "done": False})
            if len(st.session_state.tasks) >= 5: st.session_state.badges["b5"]["un"] = True
            st.rerun()

for i, t in enumerate(st.session_state.tasks):
    # استخدام Container لكل مهمة لضمان عدم التداخل
    with st.container():
        tc1, tc2, tc3 = st.columns([0.1, 0.8, 0.1])
        done = tc1.checkbox("", value=t['done'], key=f"k_{i}")
        if done != t['done']:
            st.session_state.tasks[i]['done'] = done
            if done: 
                st.session_state.xp += 30
                st.session_state.badges["b1"]["un"] = True
            st.rerun()
        txt = f"~~{t['name']}~~" if t['done'] else t['name']
        tc2.markdown(f"**{txt}**")
        if tc3.button("🗑️", key=f"d_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 9. المؤقت ---
st.divider()
st.subheader("⏳ مؤقت التركيز")
if st.button("🚀 ابدأ المؤقت (30 دقيقة)"):
    st.session_state.badges["b2"]["un"] = True
    ph = st.empty()
    for s in range(30 * 60, 0, -1):
        m, sec = divmod(s, 60)
        ph.metric("متبقي", f"{m:02d}:{sec:02d}")
        time.sleep(1)
    st.session_state.xp += 50
    st.rerun()

st.divider()
st.caption("Study Flow Pro 🌊 - النسخة المنظمة 2026")
