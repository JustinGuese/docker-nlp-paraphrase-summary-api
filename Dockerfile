FROM python:3.9-slim
RUN mkdir /app
WORKDIR /app
RUN apt update && apt install -y --no-install-recommends gcc git build-essential
# install parrot
RUN pip install pandas protobuf
RUN pip install git+https://github.com/PrithivirajDamodaran/Parrot_Paraphraser.git
COPY ./src/requirements.txt /app
RUN pip install -r requirements.txt
RUN apt purge -y --auto-remove gcc git build-essential
COPY ./src/install.py /app
RUN python install.py
COPY ./src/nlpapp.py /app
CMD ["uvicorn", "nlpapp:app", "--host", "0.0.0.0", "--workers", "1"]