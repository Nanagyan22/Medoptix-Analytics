# 🩺 MedOptix Analytics | The HealSight Initiative

MedOptix Analytics is a predictive capacity management suite designed to transform reactive hospital operations into proactive, data-driven strategies. As part of the HealSight Initiative, this tool forecasts patient inflows **7–30 days** in advance, enabling hospital administrators to align staffing, bed capacity, and resources efficiently.

---

## 📋 Table of Contents
- [Business Case](#-business-case)
- [Key Features](#-key-features)
- [Technical Architecture](#-technical-architecture)
- [Author](#-author)

---

## 💼 Business Case

### **The Challenge: Reactive Operations**

Hospitals in the Nordic public health network faced significant inefficiencies due to reactive management:

- ❌ **25%** longer patient wait times during peak surges  
- ❌ **20%** inefficiency in bed allocation  
- ❌ Severe staff burnout and soaring overtime costs (**€125k/month**)  

### **The Solution**  
A unified intelligence platform combining **real-time visualization** with **AI-driven forecasting** to improve operational decision-making.

### 🏆 Quantifiable Impact (Pilot Results)

- ✅ **88% Bed Utilization Efficiency** (up from 68%)  
- 💰 **€35,000/month reduction** in overtime costs  
- 📉 Overflow incidents reduced **from 32 → 11 per month**

---

## 🚀 Key Features

### **1. 📊 Executive Operations Dashboard (Power BI)**  
A real-time command center embedded directly into the application.

- **Live Metrics:** Total Admissions, Avg Wait Time, Staffing Index  
- **Risk Analysis:** Color-coded gauges showing capacity thresholds  
- **Drill-down:** Filter by hospital (Helsinki, Tampere…) or ward (ED, ICU)

---

### **2. 🔮 ML Forecast Engine (Streamlit)**  
An interactive tool for operational scenario planning.

- **Input:** Lagged metrics such as occupancy rate, overflow, wait time, etc.  
- **Output:** Patient inflow predictions **7–30 days ahead**  
- **Scenario Testing:** Adjust “Effective Capacity” to simulate resource changes  

---

## ⚙ Technical Architecture

### **The Model: SARIMAX**
We use a **Seasonal ARIMA with Exogenous Variables (SARIMAX)** model. It captures:

- **Seasonality** (e.g., predictable Monday demand spikes)  
- **External variables (exog):**  
  - Occupancy Rate (Lag 1)  
  - Overflow Count  
  - Staffing Index  
  - Performance Metrics  

### **Model Performance**
- **R²:** 88.4%  
- **RMSE:** 0.553  
- **MAE:** 0.463  
High accuracy with <1 patient average error margin.

---

**Francis Afful Gyan**    
📧 Email: francisaffulgyan@gmail.com  
🔗 LinkedIn: [https://www.linkedin.com/in/francis-afful-gyan-2b27a5153/]  
📅 Date: November 2025

---

**🌐 Live Demo**: [https://perishables.streamlit.app/](https://perishables.streamlit.app/)

**📊 Project Status**: Active Development

**⭐ If you find this project useful, please consider giving it a star!**

## Thank You
![Thank You](Thankyou1.png)

