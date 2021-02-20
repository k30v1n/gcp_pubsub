FROM python:3.8-slim

RUN useradd --create-home --shell /bin/bash app_user

WORKDIR /home/app_user

COPY src/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

USER app_user

COPY src/ .

CMD ["bash"]