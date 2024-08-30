import streamlit as st
import pandas as pd
import random
import os

# Función para cargar y preparar los datos
def load_data():
    # Usamos st.secrets para manejar la ruta del archivo de manera segura
    csv_path = st.secrets["global"]["csv_path"]
    df = pd.read_csv(csv_path)
    questions = []
    for _, row in df.iterrows():
        question = {
            'text': row[0],
            'options': row[1:6].dropna().tolist(),
            'correct': row[7]
        }
        questions.append(question)
    return questions

# Función para mostrar una pregunta
def show_question(question):
    st.write(question['text'])
    user_answer = st.multiselect("Selecciona la(s) respuesta(s) correcta(s):", 
                                 [opt.split('. ', 1)[1] for opt in question['options']],
                                 key=question['text'])
    return [chr(65 + question['options'].index(f"{chr(65 + i)}. {opt}")) for opt in user_answer]

# Función principal de la app
def main():
    st.title("Quiz App")

    # Cargar preguntas
    questions = load_data()

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.total_questions = len(questions)
        random.shuffle(questions)

    if st.session_state.current_question < st.session_state.total_questions:
        question = questions[st.session_state.current_question]
        user_answer = show_question(question)

        if st.button("Siguiente"):
            correct_answer = question['correct'].split(',')
            if set(user_answer) == set(correct_answer):
                st.session_state.score += 1
            st.session_state.current_question += 1
            st.experimental_rerun()

    else:
        st.write(f"Quiz completado. Tu puntuación: {st.session_state.score}/{st.session_state.total_questions}")
        if st.button("Reiniciar Quiz"):
            st.session_state.current_question = 0
            st.session_state.score = 0
            random.shuffle(questions)
            st.experimental_rerun()

if __name__ == "__main__":
    main()