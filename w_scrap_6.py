from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time

# Configurar el servicio de ChromeDriver usando WebDriver Manager
service = ChromeService(ChromeDriverManager().install())

# Crear una nueva instancia del navegador Chrome
driver = webdriver.Chrome(service=service)

# Navegar a la página de examtopics
url = "https://www.examtopics.com/exams/snowflake/snowpro-core/view/111/"
driver.get(url)

# Esperar a que la página cargue completamente
wait = WebDriverWait(driver, 5)
time.sleep(40)

# Intentar aceptar cookies si aparece el cuadro de diálogo
try:
    # Ajusta el selector según el HTML actual de la página
    accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept") or contains(text(), "Accept All Cookies")]')))
    accept_cookies_button.click()
    print("Botón de cookies aceptado.")
except Exception as e:
    print("No se encontró el botón de aceptación de cookies o ocurrió otro error:", e)

# Esperar a que las preguntas se carguen
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card")))

# Obtiene el HTML de la página
page_source = driver.page_source

# Analiza el HTML con BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Abrir un archivo para guardar el output
with open('output.txt', 'a', encoding='utf-8') as file:
    # Extrae las preguntas y respuestas
    questions = soup.find_all('div', class_='card')
    for i, question in enumerate(questions):
        try:
            # Localizar la cabecera de la pregunta
            card_header = question.find('div', class_='card-header')
            question_number_match = re.search(r'Question #(\d+)', card_header.text)
            
            # Obtener el número de la pregunta
            if question_number_match:
                question_number = question_number_match.group(1)
            else:
                question_number = "Desconocido"
            
            # Extraer el texto de la pregunta
            question_body = question.find('div', class_='card-body question-body')
            question_text = question_body.find('p', class_='card-text').text.strip()
            
            file.write(f"Pregunta {question_number}: {question_text}\n")

            # Extraer las respuestas posibles
            answers = question_body.find_all('li', class_='multi-choice-item')
            for answer in answers:
                answer_letter = answer.find('span', class_='multi-choice-letter').text.strip()
                answer_text = answer.get_text(separator=' ', strip=True)
                # Eliminar la letra duplicada al inicio de la respuesta
                answer_text = re.sub(r'^\w\.\s+', '', answer_text)
                file.write(f"{answer_letter} {answer_text}\n")
            
            # Extraer la respuesta votada
            #script_tag = question.find('script', type='application/json')
            #if script_tag:
            #    data = json.loads(script_tag.string)
            #    if 'voted_answers' in data[0]:
            #        voted_answers = data[0]['voted_answers']
            #        file.write(f"Respuestas votadas: {voted_answers}\n")
            
            # Extraer la respuesta correcta
            correct_answer_tag = question.find('p', class_='card-text question-answer bg-light white-text')
            if correct_answer_tag:
                correct_answer = correct_answer_tag.find('span', class_='correct-answer').text
                file.write(f"Respuesta correcta: {correct_answer}\n")

        except Exception as e:
            pass

# Cerrar el navegador
driver.quit()
