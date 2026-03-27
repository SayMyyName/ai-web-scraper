# AI Web Scraper with Local LLM (Ollama)

## Overview

This project is an AI-powered web scraper that extracts structured data from websites using a **local Large Language Model (LLM)** via Ollama.

It supports **multi-page scraping, parallel processing, and structured data export (JSON/CSV)** through an interactive Streamlit interface.

---

## Features

* Scrape multiple URLs at once
* Parallel scraping using multithreading
* Clean and process HTML using BeautifulSoup
* AI-powered data extraction using local LLM (Ollama)
* Structured output in JSON format
* Download extracted data as JSON or CSV
* Simple and interactive UI with Streamlit

---

## Tech Stack

* **Python**
* **Streamlit**
* **Selenium**
* **BeautifulSoup**
* **LangChain**
* **Ollama (Local LLM)**

---

## How It Works

1. Input one or more website URLs
2. Scrape content using Selenium
3. Clean and preprocess HTML data
4. Split content into manageable chunks
5. Use LLM to extract structured information
6. Display and download results

---

## Installation

```bash
git clone https://github.com/SayMyyName/ai-web-scraper.git
cd ai-web-scraper
pip install -r requirements.txt
```

---

## Setup Ollama

Make sure Ollama is installed and running, then pull the model:

```bash
ollama pull qwen3:8b
```

---

## Run the App

```bash
streamlit run main.py
```

---

## Example Use Cases

* Extract product details (name, price, ratings)
* Extract blog information (title, author, date)
* Extract job listings
* Convert unstructured web data into structured datasets

---

## Project Structure

```
ai-web-scraper/
│
├── main.py          # Streamlit app (UI + pipeline)
├── scrape.py        # Web scraping logic (Selenium)
├── parse.py         # LLM-based parsing (Ollama)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Notes

* Requires Google Chrome installed
* ChromeDriver is handled dynamically (no manual setup required)
* Works fully offline using local LLM
* Performance depends on system RAM (16GB recommended)

---

## Future Improvements

* Agent-based automatic field detection
* Retry mechanism for failed LLM outputs
* API integration (FastAPI)
* Deployment using Docker or cloud platforms

---

## Key Highlights

* Built with **local LLM (no API costs)**
* Handles **multi-page scraping efficiently**
* Designed with **modular and scalable architecture**

