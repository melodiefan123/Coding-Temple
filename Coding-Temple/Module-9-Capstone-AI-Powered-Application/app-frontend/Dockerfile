FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend Streamlit source code
COPY . .

EXPOSE 8501

# Run the entrypoint Streamlit app (e.g., auth_4.py or main_app.py)
CMD ["streamlit", "run", "auth.py", "--server.port=8501", "--server.address=0.0.0.0"]