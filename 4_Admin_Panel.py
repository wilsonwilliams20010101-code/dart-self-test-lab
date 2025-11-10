import streamlit as st
from utils.ui import load_css, header, footer_nav
from utils.data_manager import load_tests, save_tests, load_quiz_questions, save_quiz_questions
from utils.auth import is_admin, login_form

def render():
    load_css()
    header("Admin Panel", "Manage tests and quiz content.")

    if not is_admin():
        login_form()
        return

    tab1, tab2 = st.tabs(["Tests", "Quiz Questions"])

    with tab1:
        tests = load_tests()
        st.subheader("Current Tests")
        for idx, t in enumerate(tests):
            with st.expander(f"{t['item']} — {t['category']}"):
                t['category'] = st.text_input("Category", t['category'], key=f"cat_{idx}")
                t['item'] = st.text_input("Item", t['item'], key=f"item_{idx}")
                adulterants = st.text_area("Adulterants (comma-separated)", ", ".join(t.get('adulterants',[])), key=f"adul_{idx}")
                t['adulterants'] = [a.strip() for a in adulterants.split(",") if a.strip()]
                materials = st.text_area("Materials (comma-separated)", ", ".join(t.get('materials',[])), key=f"mat_{idx}")
                t['materials'] = [m.strip() for m in materials.split(",") if m.strip()]
                steps_text = st.text_area("Steps (one per line)", "\n".join(t.get('steps',[])), key=f"steps_{idx}")
                t['steps'] = [s.strip() for s in steps_text.splitlines() if s.strip()]
                t['safety'] = st.text_input("Safety note", t.get('safety',''), key=f"safety_{idx}")
                if st.button("Delete", key=f"del_test_{idx}"):
                    tests.pop(idx)
                    save_tests(tests)
                    st.rerun()
        st.divider()
        with st.form("add_test"):
            st.subheader("Add New Test")
            cat = st.text_input("Category")
            item = st.text_input("Item")
            adulterants = st.text_area("Adulterants (comma-separated)")
            materials = st.text_area("Materials (comma-separated)")
            steps = st.text_area("Steps (one per line)")
            safety = st.text_input("Safety note")
            if st.form_submit_button("Add Test"):
                tests.append({
                    "category": cat, "item": item,
                    "adulterants": [a.strip() for a in adulterants.split(",") if a.strip()],
                    "materials": [m.strip() for m in materials if (m:=m.strip())],
                    "steps": [s.strip() for s in steps.splitlines() if s.strip()],
                    "safety": safety
                })
                save_tests(tests)
                st.success("Test added.")
        if st.button("Save All Changes"):
            save_tests(tests)
            st.success("Saved.")

    with tab2:
        qs = load_quiz_questions()
        st.subheader("Current Questions")
        for i, q in enumerate(qs):
            with st.expander(f"Q{i+1}: {q['question'][:60]}"):
                q['question'] = st.text_area("Question", q['question'], key=f"qtext_{i}")
                opts = q['options']
                for j in range(len(opts)):
                    opts[j] = st.text_input(f"Option {j+1}", opts[j], key=f"opt_{i}_{j}")
                q['category'] = st.text_input("Category", q.get('category','General'), key=f"qcat_{i}")
                q['answer_index'] = st.number_input("Answer index (0-based)", 0, len(opts)-1, q['answer_index'], key=f"ans_{i}")
                if st.button("Delete", key=f"del_q_{i}"):
                    qs.pop(i)
                    save_quiz_questions(qs)
                    st.rerun()
        st.divider()
        with st.form("add_q"):
            st.subheader("Add New Question")
            qt = st.text_area("Question")
            o1 = st.text_input("Option 1")
            o2 = st.text_input("Option 2")
            o3 = st.text_input("Option 3")
            o4 = st.text_input("Option 4")
            cat = st.text_input("Category", "General")
            ans = st.selectbox("Correct option", [1,2,3,4], index=0)
            if st.form_submit_button("Add Question"):
                qs.append({"question": qt, "options": [o1,o2,o3,o4], "answer_index": ans-1, "category": cat})
                save_quiz_questions(qs)
                st.success("Question added.")
        if st.button("Save All Changes", key="save_qs"):
            save_quiz_questions(qs)
            st.success("Saved.")
    footer_nav()