FROM python:3.8.12

WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Create and activate virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["python3", "app.py"]
