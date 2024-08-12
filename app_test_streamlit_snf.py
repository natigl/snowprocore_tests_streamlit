import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

@st.cache_data
def get_questions():
    session = get_active_session()
    questions_df = (
        session.table("quiz_certi.public.questions")
        .sample(0.13)
    )
    return questions_df.to_pandas()

def main():
    st.title("Examenes de Certificación SnowProCore ❄️")
    st.write("""1120 preguntas de exámenes pasados para que compruebes todo tu conocimiento.
        ¡Lo vas a conseguir! 💣🍀
        """
    )
    
    if 'questions' not in st.session_state:
        st.session_state.questions = get_questions()
    
    df = st.session_state.questions
    
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    
    for index, row in df.iterrows():
        st.markdown(f"**Pregunta {index + 1}:**")
        st.write(row['PREGUNTA'])
        
        options = {
            letter: str(row[letter]).strip()
            for letter in ['A', 'B', 'C', 'D', 'E', 'F']
            if pd.notna(row[letter]) and str(row[letter]).strip() != ''
        }
        
        correct_answers = [str(answer).strip() for answer in row['RESPUESTA_CORRECTA'].split(',')]
        
        if len(correct_answers) > 1:
            selected_options = st.multiselect(
                'Elige una o más opciones:',
                list(options.values()),
                key=f"question_{index}"
            )
            if selected_options:
                selected_option_letters = [k for k, v in options.items() if v in selected_options]
                st.session_state.answers.append((index, selected_option_letters, selected_options, correct_answers))
        else:
            selected_option = st.radio(
                'Elige una opción:',
                list(options.values()),
                key=f"question_{index}"
            )
            if selected_option:
                selected_option_letter = [k for k, v in options.items() if v == selected_option][0]
                st.session_state.answers.append((index, [selected_option_letter], [selected_option], correct_answers))
    
    if st.button('Submit'):
        total_questions = len(st.session_state.answers)
        correct_count = 0
        
        st.write("Respuestas enviadas y correctas:")
        for question_index, selected_option_letters, selected_option_texts, correct_answers in st.session_state.answers:
            question_text = df.loc[question_index, 'PREGUNTA']
            correct_answer_texts = [str(df.loc[question_index, letter]).strip() for letter in correct_answers]
            
            if set(selected_option_letters) == set(correct_answers):
                result = "Correcto"
                result_color = "green"
                correct_count += 1
            else:
                result = "Incorrecto"
                result_color = "red"
            
            st.markdown(f"<p><b>Pregunta {question_index + 1}:</b> <span style='color:{result_color};'>{result}</span></p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Texto de la pregunta:</b> {question_text}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Respuesta(s) enviada(s):</b> {', '.join(selected_option_texts)}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Respuesta(s) correcta(s):</b> {', '.join(correct_answer_texts)}</p>", unsafe_allow_html=True)
            st.markdown("---")
        
        accuracy = (correct_count / total_questions) * 100
        st.metric(label="Porcentaje de aciertos", value=f"{accuracy:.2f}%")

if __name__ == "__main__":
    main()