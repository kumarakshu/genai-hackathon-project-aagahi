# Step 1: Base image (Python 3.10)
FROM python:3.10-slim

# Step 2: Server par ek '/app' folder banana
WORKDIR /app

# Step 3: Pehle requirements ko copy karke install karna
# Isse build process fast hota hai
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Baaki ka 'app' folder (main.py, model.joblib) copy karna
COPY app/ .

# Step 5: Google Cloud ko batana ki aapka app port 8080 par chalega
EXPOSE 8080

# Step 6: App ko 'gunicorn' se run karna (yeh production server hai)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]