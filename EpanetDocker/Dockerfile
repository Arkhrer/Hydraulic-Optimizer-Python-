FROM python

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir epyt==1.0.8 pandas numpy==1.26.4 matplotlib socket.py

WORKDIR /app

COPY . .

ENTRYPOINT [ "python", "app/Main.py" ]