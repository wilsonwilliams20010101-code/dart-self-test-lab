import streamlit as st
from utils.ui import load_css, header, footer_nav
from utils.data_manager import load_quiz_questions
from utils.quiz_engine import pick_questions, score_quiz

def render():
    load_css()
    header("Quiz", "Quickly check your knowledge.")

    qs_all = load_quiz_questions()
    cats = ["Any"] + sorted({q.get("category","General") for q in qs_all}) if qs_all else ["Any"]
    n = st.slider("Number of questions", 3, 10, 5)
    cat = st.selectbox("Category", cats)

    if "quiz" not in st.session_state:
        st.session_state.quiz = None

    if st.button("Start Quiz", type="primary"):
        chosen = pick_questions(qs_all, n=n, category=None if cat=="Any" else cat) if qs_all else []
        st.session_state.quiz = {"i":0, "qs":chosen, "ans":[None]*len(chosen)}

    st.divider()
    qstate = st.session_state.quiz
    if not qstate:
        st.info("Choose settings and press **Start Quiz**.")
        footer_nav(); return
    if not qstate["qs"]:
        st.warning("No questions available. Add some in Admin Panel.")
        footer_nav(); return

    i = qstate["i"]; qs = qstate["qs"]; cur = qs[i]
    st.progress((i)/len(qs))
    st.markdown(f"**Q{i+1}/{len(qs)}. {cur['question']}**")

    picked = st.radio(" ", cur["options"], index=0 if qstate["ans"][i] is None else qstate["ans"][i], key=f"q_{i}")
    qstate["ans"][i] = cur["options"].index(picked)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⟵ Back", disabled=i==0):
            qstate["i"] -= 1
    with c2:
        if st.button("Next ⟶", disabled=i==len(qs)-1):
            qstate["i"] += 1
    with c3:
        if st.button("✅ Submit", disabled=None in qstate["ans"]):
            s = score_quiz(qs, qstate["ans"])
            st.success(f"Your score: {s}/{len(qs)}")
            st.write("### Review")
            for j, q in enumerate(qs):
                correct = q["answer_index"]
                your = qstate["ans"][j]
                ok = (your == correct)
                st.markdown(f"- {'✅' if ok else '❌'} **Q{j+1}** – Correct: **{q['options'][correct]}**  |  Your: **{q['options'][your]}**")
            st.session_state.quiz = None

    footer_nav()