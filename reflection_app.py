import streamlit as st
from fpdf import FPDF
import os

st.set_page_config(page_title="Моя рефлексия по курсу", layout="centered")
st.markdown("# 🌿 Моя рефлексия по курсу")
st.markdown("Поделитесь своими впечатлениями, достижениями и трудностями, с которыми вы столкнулись во время обучения.")

# Форма ввода
learned = st.text_area("📌 Чему я научился/научилась?")
liked = st.text_area("🚀 Что мне понравилось больше всего?")
difficult = st.text_area("⚙️ Какие темы были сложными?")
skills = st.text_area("💡 Какие навыки пригодятся в будущем?")
rating = st.slider("✍️ Моя общая оценка курса (по 5-балльной шкале):", 1, 5, 4)

st.markdown("---")
name = st.text_input("Имя (по желанию):")
feedback = st.text_area("Комментарий (по желанию):")

# Загрузка шрифта с поддержкой кириллицы (DejaVuSans)
font_dir = "fonts"
os.makedirs(font_dir, exist_ok=True)
deja_path = os.path.join(font_dir, "DejaVuSans.ttf")
if not os.path.exists(deja_path):
    import requests
    url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"
    with open(deja_path, "wb") as f:
        f.write(requests.get(url).content)

# Класс PDF с поддержкой Unicode
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", deja_path, uni=True)
        self.set_font("DejaVu", size=12)

    def header(self):
        self.set_font("DejaVu", size=14)
        self.cell(0, 10, "Моя рефлексия по курсу", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("DejaVu", style="B", size=12)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, body):
        self.set_font("DejaVu", size=12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_reflection(self, data):
        for section_title, text in data:
            self.chapter_title(section_title)
            self.chapter_body(text)

# Кнопка сохранения PDF
if st.button("Сохранить как PDF"):
    pdf = PDF()
    pdf.add_page()

    reflection_data = [
        ("📌 Чему я научился/научилась?", learned),
        ("🚀 Что мне понравилось больше всего?", liked),
        ("⚙️ Какие темы были сложными?", difficult),
        ("💡 Какие навыки пригодятся в будущем?", skills),
        ("✍️ Моя общая оценка курса", f"{rating} из 5"),
    ]
    if name:
        reflection_data.append(("Имя", name))
    if feedback:
        reflection_data.append(("Комментарий", feedback))

    pdf.add_reflection(reflection_data)
    pdf_output = "reflection.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as f:
        st.download_button("📥 Скачать PDF", f, file_name=pdf_output, mime="application/pdf")
