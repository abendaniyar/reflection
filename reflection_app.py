import streamlit as st
from fpdf import FPDF

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

# Функция генерации PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Моя рефлексия по курсу", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
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
