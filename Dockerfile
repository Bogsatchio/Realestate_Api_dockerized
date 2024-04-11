FROM python:3.10
EXPOSE 5050
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Run app.py when the container launches
#CMD ["python", "./data_prep_and_insert.py"]
CMD  ["flask", "run", "--host", "0.0.0.0"]