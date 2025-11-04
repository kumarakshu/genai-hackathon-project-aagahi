# 🚀 Project AAGAHI: AI-Powered Dengue Risk Platform

**Project AAGAHI** (AI-Assisted Governance and Hazard Information) is an end-to-end AI platform built on Google Cloud. It transforms siloed public data into a proactive governance tool, predicting Dengue outbreak risks and delivering actionable insights to both officials and citizens.

---

## 🔗 Live Demos & Prototypes

This project consists of two main prototypes that you can interact with right now:

1.  **📊 Official's Dashboard:** A live Looker Studio dashboard for decision-makers to visualize high-risk zones and complaint data.
    * **Link: [Live Looker Studio Dashboard](https://lookerstudio.google.com/reporting/22faf400-21b9-40b4-b3ea-1d4ebce92233)**

2.  **🤖 Citizen AI Assistant:** A Google Colab notebook that demonstrates the complete, end-to-end AI flow—from calling our custom model to getting a response from Gemini.
    * **Link: [Live Google Colab Notebook](https://colab.research.google.com/drive/1S7bBD-tSUpWbTC6KmzJygP1Rv1-lVM5P?usp=sharing)**

---

## 🎯 The Problem

Government data for public health (like weather, infrastructure, and citizen complaints) is often siloed. This forces officials to be **reactive**, taking action only *after* a crisis, like a Dengue outbreak, has already begun. There is no system to predict and prevent these events.

## 💡 Our Solution

AAGAHI is a hybrid AI platform that bridges this gap. It provides two distinct interfaces based on one unified backend:

1.  **For Government Officials:** A **Looker Studio Dashboard** connected to a central **BigQuery** data warehouse. This gives officials a real-time, bird's-eye view of risk factors (like waste complaints, water logging) and helps them allocate resources proactively.

2.  **For Citizens:** A **Gemini-powered AI Assistant**. This assistant doesn't just give generic advice. It first calls our **custom Vertex AI model** to get a *real, data-driven prediction* (e.g., "HIGH RISK"). Then, it uses Gemini to translate that technical data into a simple, empathetic, and actionable alert in Hindi.

---

## 🛠️ Architecture & Technology Stack

This project uses a scalable, end-to-end Google Cloud architecture.

### Architecture Flow

1.  **Data Ingestion:** Mock CSV data (representing various departments) is unified in **Google BigQuery**.
2.  **Model Training:** A Scikit-learn (RandomForest) model is trained on this data in a Jupyter Notebook and saved as `dengue_risk_model.joblib`.
3.  **Model Deployment:**
    * A **Flask API** (`main.py`) is created to serve the `.joblib` model.
    * The API is containerized using a **Dockerfile**.
    * The Docker image is pushed to **Google Artifact Registry**.
    * The image is deployed as a 24/7 service using a **Vertex AI Endpoint**.
4.  **Prototyping & Consumption:**
    * **Looker Studio** connects to **BigQuery** to build the official's dashboard.
    * A **Google Colab App** acts as the citizen frontend. It calls **both** our **Vertex AI Endpoint** (for the prediction) and the **Gemini API** (for the natural language response).

### Technology Stack

* **Data Warehouse:** Google BigQuery
* **Data Visualization:** Looker Studio
* **AI Model Training:** Scikit-learn, Pandas, Jupyter Notebook
* **Custom AI Deployment:** Google Vertex AI Endpoint
* **Generative AI:** Google Gemini (via AI Studio API)
* **Backend API:** Flask
* **Containerization:** Docker, Gunicorn
* **Cloud Infrastructure:** Google Artifact Registry, Google Cloud Shell
* **Prototyping:** Google Colab

---

## ⚙️ How to Run This Project

This repository contains the code for the central component: the **Vertex AI Model API**.

### Project Structure

├── app/
│ ├── dengue_risk_model.joblib # The pre-trained AI model
│ ├── main.py # Flask API server
│ └── requirements.txt # Python dependencies
│
├── data/
│ └── mock_dengue_data.csv # Sample data used for training
│
├── Dockerfile # Recipe to build the container
│
└── Dengue_Prediction_Model.ipynb # Jupyter Notebook for model training & experimentation


### Local API Setup (Testing)

1.  Clone the repository:
    ```bash
    git clone [https://github.com/kumarakshu/genai-hackathon-project-aagahi.git](https://github.com/kumarakshu/genai-hackathon-project-aagahi.git)
    cd genai-hackathon-project-aagahi
    ```
2.  Navigate into the `app` directory:
    ```bash
    cd app
    ```
3.  Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # or .\venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```
4.  Run the Flask server:
    ```bash
    python main.py
    ```
5.  In a new terminal, test the API:
    ```bash
    curl -X POST [http://127.0.0.1:8080/predict](http://127.0.0.1:8080/predict) \
    -H "Content-Type: application/json" \
    -d '{"instances": [ {"rainfall_mm": 15, "avg_temp_c": 27.0, "water_logging_complaints": 20, "waste_complaints": 12} ]}'
    ```
    **Expected Response:**
    ```json
    {
      "predictions": [
        {
          "input_data_received": { ... },
          "prediction": "HIGH RISK"
        }
      ]
    }
    ```

### Deployment to Vertex AI (Overview)

The live endpoint was deployed by:
1.  Building the Docker image: `docker build -t ...`
2.  Pushing it to Artifact Registry: `docker push ...`
3.  Importing the model into **Vertex AI Model Registry** from the container image.
4.  Deploying the model to a **Vertex AI Endpoint** with the correct health (`/`) and predict (`/predict`) routes on port `8080`.
