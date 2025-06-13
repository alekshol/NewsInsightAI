import os
import streamlit as st
import requests
from openai import OpenAI
from dotenv import load_dotenv
import pycountry
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


load_dotenv()
XAI_API_KEY = os.getenv("XAI_API_KEY")
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def fetch_news(topic, max_results=5):
    url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q={topic}&language=en"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])[:max_results]
    return []

def call_grok(messages, model="grok-3"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()
def get_country_location(country_name):
    try:
        geolocator = Nominatim(user_agent="news_mapper")
        location = geolocator.geocode(country_name, timeout=5)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return None
    return None

def translate_text(text, target_lang="polish"):
    messages = [
        {"role": "system", "content": "Jesteś tłumaczem AI."},
        {"role": "user", "content": f"Przetłumacz ten tekst na {target_lang}:\n\n{text}"}
    ]
    return call_grok(messages)

def explain_text(text):
    messages = [
        {"role": "system", "content": "Jesteś analitykiem biznesowym i wyjaśniasz znaczenie wiadomości."},
        {"role": "user", "content": f"Wyjaśnij kontekst i możliwe skutki tej wiadomości:\n\n{text}"}
    ]
    return call_grok(messages)



st.set_page_config(page_title="News & Insights – z Grok", layout="wide")
st.title("NewsInsight")

with st.sidebar:
    st.header("Ustawienia")
    lang = st.selectbox("Język tłumaczenia:", ["polish", "english", "german", "french"])
    model = st.selectbox("Model Groka:", ["grok-3", "grok-3-mini"])
    max_news = st.slider("Ilość wiadomości:", 1, 10, 5)


topic = st.text_input("🔎 Podaj temat wiadomości (np. 'rynek nieruchomości USA')")


if topic:
    with st.spinner("📡 Szukam najnowszych wiadomości..."):
        news_items = fetch_news(topic, max_news)

    if not news_items:
        st.warning("Brak wyników.")
    else:
        for i, article in enumerate(news_items):

            st.markdown("---")
            st.subheader(article.get("title", f"Wiadomość {i+1}"))
            st.write(article.get("link", ""))
            description = article.get("description", "Brak opisu.")
            st.text(description)

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Tłumacz #{i+1}", key=f"tlumacz_{i}"):
                    translated = translate_text(description, target_lang=lang)
                    st.success(translated)

            with col2:
                if st.button(f"Wyjaśnij #{i+1}", key=f"analiza_{i}"):
                    explanation = explain_text(description)
                    st.info(explanation)

    if st.button("🔍 Analiza trendów i podsumowanie"):
        all_descriptions = "\n".join([n.get("description", "") for n in news_items])
        trend_messages = [
            {"role": "system", "content": "Jesteś analitykiem trendów. Zidentyfikuj główne tematy i trendy na podstawie poniższych wiadomości. Wypisz 3-5 kluczowych zagadnień, oraz przewidywania co się wydarzy dalej."},
            {"role": "user", "content": all_descriptions}
        ]
        summary = call_grok(trend_messages, model=model)
        st.markdown("### 📈 Trendy i podsumowanie")
        st.success(summary)
    if st.button("🗺️ Pokaż mapę lokalizacji wiadomości"):
        st.markdown("### 🌍 Mapa geograficzna wiadomości")
        locations = []
        for n in news_items:
            country = n.get("country") or n.get("source_country")
            if not country:
                possible_text = f"{n.get('title', '')} {n.get('description', '')}"
                guess_msg = [
                    {"role": "system", "content": "Podaj nazwę kraju, którego dotyczy ten tekst:"},
                    {"role": "user", "content": possible_text}
                ]
                country = call_grok(guess_msg, model=model)

            coords = get_country_location(country)
            if coords:
                locations.append({"country": country, "lat": coords[0], "lon": coords[1]})

        if locations:
            df = pd.DataFrame(locations)
            st.map(df)
        else:
            st.warning("Nie udało się zlokalizować wiadomości geograficznie.")
