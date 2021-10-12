FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get install -y locales locales-all

RUN sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG pt_BR.UTF-8  
ENV LANGUAGE pt_BR:en  
ENV LC_ALL pt_BR.UTF-8
ENV TZ="America/Sao_Paulo"
RUN touch /usr/share/locale/locale.alias

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]