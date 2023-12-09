FROM python

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir epyt pandas numpy matplotlib socket.py

WORKDIR /app

COPY . .

ENTRYPOINT [ "python", "app/Main.py" ]