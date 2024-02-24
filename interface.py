import streamlit as st


def main():
    st.title("Резюме и вакансии")

    st.sidebar.title("Выгрузить JSON вакансии")
    if st.sidebar.button("Отправить", key='vacancies'):
        result = compare_vacancy_and_resume()
        st.text("Результат сравнения: {}".format(result))

    st.sidebar.title("Выгрузить резюме кандидата")
    if st.sidebar.button("Отправить", key='resume'):
        res = compare_vacancy_and_resume()
        st.text("Результат сравнения: {}".format(res))


def compare_vacancy_and_resume():
    pass


if __name__ == "__main__":
    main()
