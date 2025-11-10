import streamlit as st
from utils.ui import load_css, header, footer_nav
from utils.data_manager import load_quiz_questions
from utils.quiz_engine import pick_questions, score_quiz

def render():
    load_css()
    header("Quiz", "Quickly check your knowledge.")

    qs_all = load_quiz_questions()
    cats = ["Any"] + sorted({q.get("category", "General") for q in qs_all}) if qs_all else ["Any"]
    n = st.slider("Number of questions", 3, 10, 5)
    cat = st.selectbox("Category", cats)

    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = None

    if st.button("Start Quiz", type="primary"):
        chosen = pick_questions(qs_all, n=n, category=None if cat == "Any" else cat) if qs_all else []
        st.session_state.quiz_state = {"questions": chosen, "answers": [None] * len(chosen)}

    st.divider()

    state = st.session_state.quiz_state
    if state and state["questions"]:
        for i, q in enumerate(state["questions"]):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            picked = st.radio(" ", q["options"], index=0, key=f"q_{i}")
            state["answers"][i] = q["options"].index(picked)
            st.write("")
        if st.button("Submit"):
            s = score_quiz(state["questions"], state["answers"])
            st.success(f"Your score: {s}/{len(state['questions'])}")
            for i, q in enumerate(state["questions"]):
                st.markdown(f"- **Q{i+1} Answer:** {q['options'][q['answer_index']]}")
            st.session_state.quiz_state = None
    elif state is not None and not (state and state["questions"]):
        st.warning("No questions available. Add some in Admin Panel.")
    else:
        st.info("Choose settings and press **Start Quiz**.")
    footer_nav()
