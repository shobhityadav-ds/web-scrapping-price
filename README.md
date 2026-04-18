# web-scrapping-price
# 🕸️ Web Scraping Project (Amazon + Flipkart)

## 📌 Overview

This project is a **Python-based web scraping system** that extracts product data from multiple e-commerce platforms and stores it in structured Excel files.

It follows a **modular architecture** with separate scrapers for each platform, making it scalable and easy to maintain.

---

## 🚀 Features

* 🔍 Scrapes product data from Amazon and Flipkart
* 📂 Modular scraper structure (`scraper/` folder)
* 📊 Saves data into Excel files (`.xlsx`)
* ⚡ Clean and reusable code
* 🧩 Easy to extend for more websites

---

## 📁 Project Structure

```
web_scraping_project/
│── main.py
│── requirements.txt
│── README.md
│
├── scraper/
│   │── __init__.py
│   │── amazon_scraper.py
│   │── flipkart_scraper.py
│
└── data/
    │── amazon_data.xlsx
    │── flipkart_data.xlsx
```

---

## 🛠️ Tech Stack

* Python 
* Pandas
* BeautifulSoup
* Requests
* OpenPyXL

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/web_scraping_project.git
cd web_scraping_project
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ How to Run

```
python main.py
```

✔ This will:

* Scrape data from Amazon and Flipkart
* Save results in the `data/` folder as Excel files

---

## 📊 Output

The scraped data is stored in:

* `data/amazon_data.xlsx`
* `data/flipkart_data.xlsx`

Each file contains:

* Product Name
* Price

---

## ⚠️ Note

* This project is for **educational purposes only**
* Websites may block scraping if proper headers or delays are not used
* Use responsibly and follow website policies

---

## 🚀 Future Improvements

* Add Selenium for dynamic content scraping
* Integrate database (MySQL / MongoDB)
* Build a web dashboard for visualization
* Add AI-based data analysis
* Schedule automated scraping

---

## 👨‍💻 Author

Shobhit Kumar Yadav

---

## ⭐ Contribute

Feel free to fork this repository and improve it!

---

