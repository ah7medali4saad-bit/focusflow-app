import streamlit as st
import datetime

# إعدادات واجهة الموقع
st.set_page_config(page_title="FocusFlow", page_icon="🌊")

# العنوان الرئيسي
st.title("FocusFlow 🌊")
st.markdown("### رفيقك لتنظيم الدراسة والوقت")

# --- 1. قسم إضافة المهام ---
st.header("✅ قائمة المهام")

# إنشاء مخزن للمهام إذا لم يكن موجوداً
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# خانة الكتابة
new_task = st.text_input("ماذا تريد أن تنجز اليوم؟")
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("إضافة"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "done": False})
            st.rerun()

# عرض المهام المضافة
for i, task_item in enumerate(st.session_state.tasks):
    cols = st.columns([0.1, 0.8, 0.1])
    is_done = cols[0].checkbox("", value=task_item["done"], key=f"check_{i}")
    st.session_state.tasks[i]["done"] = is_done
    
    if is_done:
        cols[1].markdown(f"~~{task_item['task']}~~") # خط فوق الكلام لو انتهت
    else:
        cols[1].write(task_item["task"])
    
    if cols[2].button("🗑️", key=f"del_{i}"):
        st.session_state.tasks.pop(i)
        st.rerun()

# --- 2. قسم مؤقت التركيز ---
st.divider()
st.header("⏳ مؤقت التركيز (بومودورو)")
minutes = st.number_input("حدد دقائق المذاكرة:", min_value=1, value=25)
if st.button("بدأ المذاكرة"):
    st.info(f"تم ضبط المؤقت لـ {minutes} دقيقة. ركز في دروسك!")

# --- 3. الوضع الليلي ---
st.sidebar.title("الإعدادات")
st.sidebar.write("الموقع يدعم الوضع الليلي تلقائياً من إعدادات المتصفح.")
