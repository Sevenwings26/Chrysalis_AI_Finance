# Chrysalis Finance Intelligence AI

**Chrysalis Finance Intelligence AI** is a financial intelligence platform designed for Nigerian equities, combining real-time market data, portfolio simulation, and AI-powered financial decision support.

It enables users to explore NGX stocks, simulate trading with a virtual wallet, and interact with an LLM-powered assistant that explains market movements and supports smarter investment decisions using Retrieval-Augmented Generation (RAG).

---

## 🚀 Core Features

### 📊 Real-Time Market Intelligence

* Live integration with NGX stock market data API
* Structured equity data: price, volume, sector, P/E ratio, and change metrics
* Enriched analytics including recommendation signals (Buy / Sell / Hold)

### 💼 Virtual Wallet & Paper Trading

* Simulated wallet system for users
* Deposit, transaction tracking, and balance management
* Buy/sell stock simulation without real financial risk
* Full transaction history ledger

### 🧠 AI Financial Assistant (RAG-Based)

* Context-aware financial chatbot
* Explains stocks, trends, and financial concepts in simple language
* Uses Retrieval-Augmented Generation (RAG) to ground responses in market data
* Supports decision-making for buy/sell/hold scenarios

### 📈 Stock Intelligence Layer

* Automated enrichment of stock data
* Upside potential estimation
* Recommendation engine based on market movement heuristics

---

## 🏗️ System Architecture

* **Backend:** Django (Monolithic modular architecture)
* **Market Data Layer:** External NGX API integration service
* **Service Layer:** Provider-based design for extensible market sources
* **Caching Layer:** Django cache (upgradeable to Redis)
* **AI Layer:** LLM + RAG pipeline for financial reasoning
* **Frontend:** Django templates (HTMX-ready architecture)

---

## 🧰 Tech Stack

* Python 3.x
* Django
* Requests (API integration)
* Django ORM
* LLM (Gemini / OpenAI-compatible architecture)
* RAG pipeline (vector retrieval system)
* HTML/CSS/JS (progressively HTMX-enabled)

---

## 🧠 Key Design Principles

* **Service-Oriented Architecture inside Django**
* **Separation of Concerns (API, Service, UI layers)**
* **Fail-safe financial data handling (retry + caching + fallback)**
* **AI-first financial experience design**
* **Paper trading simulation over real-money risk**

---

## 🔐 Environment Variables

Create a `.env` file:

```env
NGX_API_KEY=your_api_key_here
SECRET_KEY=your_django_secret
DEBUG=True
EMAIL_HOST_USER=mail.com 
EMAIL_HOST_PASSWORD=emailcssaaw11om

```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-org/chrysalis-ai.git
cd chrysalis-ai

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## 📊 Core Modules

### Market Module

* NGX stock ingestion service
* Stock enrichment + recommendation engine
* Stock listing and detail views

### Wallet Module

* User wallet creation (auto-generated)
* Deposit and transaction ledger
* Balance tracking

### Trading Module

* Simulated buy/sell execution
* Portfolio tracking (planned enhancement)

### AI Module

* RAG-based financial assistant
* Market-aware conversational interface
* Stock explanation and insight generation

---

## 🔮 Roadmap

* [ ] Portfolio & holdings engine
* [ ] Real-time websocket stock updates
* [ ] Advanced AI trading assistant (multi-step reasoning)
* [ ] Redis caching layer upgrade
* [ ] Charting & technical analysis module
* [ ] HTMX-powered dynamic UI
* [ ] Mobile API layer (FastAPI extension)


## 👨‍💻 Author

Built by **Iyanu Arowosola**
Backend/ML Engineer | AI Systems Developer 
