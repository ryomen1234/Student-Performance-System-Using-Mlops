# base image
FROM python:3.9

# working directory
WORKDIR /app

# copy
COPY . /app

# run
RUN pip install -r requirment.txt

# port
EXPOSE 8501

# command
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]
