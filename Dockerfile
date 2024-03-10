FROM python:3.10

# Working Directory
WORKDIR /app

# Copy everything to the app
COPY . /app/

# Expose port 8080
EXPOSE 8080

# Install the requirements
RUN pip install -r /app/requirements.txt

# Run the Flask API
CMD ["python", "app.py"]