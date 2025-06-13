# 🧠 NewsInsight AI – Inteligentna analiza wiadomości z Grok

NewsInsight AI to interaktywna aplikacja Streamlit, która łączy aktualne dane prasowe z inteligencją językową modelu Grok (xAI), aby umożliwić użytkownikom szybkie tłumaczenie, analizowanie i kategoryzowanie globalnych wiadomości w kontekście branżowym.

## 🎯 Dla kogo?

**Branża:** Finansowa  
**Dział:** PR i analityka konkurencji  
**Przykład firmy:** Międzynarodowa spółka inwestycyjna z zespołem PR i zespołem ds. ryzyk regulacyjnych

## 🔍 Problem biznesowy

Działy analiz i komunikacji muszą na bieżąco monitorować globalne wydarzenia wpływające na rynki, regulacje i reputację firmy. Ręczne przeglądanie źródeł to czasochłonny proces – NewsInsight AI automatyzuje przeszukiwanie, tłumaczenie i interpretację treści, pozwalając na szybkie reagowanie.

**Korzyści:**
- Oszczędność czasu
- Lepsze raportowanie
- Automatyczna klasyfikacja branżowa i geograficzna
- Możliwość generowania raportów PDF

## 🧠 Wykorzystane narzędzia AI

- **LLM API**: xAI Grok (`grok-3`, `grok-3-mini`)
- **Web Search API**: NewsData.io
- **Prompt Engineering**: tłumaczenie, klasyfikacja, analiza skutków
- **Structured Extraction** (planowane): generowanie raportów
- **Streamlit**: interfejs aplikacji
- **FPDF**: generowanie plików PDF (opcjonalnie)

## ⚙️ Funkcje aplikacji

✅ Wyszukiwanie wiadomości w czasie rzeczywistym  
✅ Tłumaczenie treści na wybrany język (polski, angielski, itd.)  
✅ Wyjaśnienie kontekstu i możliwych skutków  
✅ Filtrowanie według branży (technologia, finanse, zdrowie, energia)  
✅ Generowanie automatycznych raportów PDF *(beta)*  
✅ Gotowa do rozbudowy o alerty mailowe i trend detection

## ▶️ Jak uruchomić?

1. Skonfiguruj `.env`:
   ```env
   XAI_API_KEY=your_grok_key
   NEWSDATA_API_KEY=your_newsdata_key
# NewsInsightAI
