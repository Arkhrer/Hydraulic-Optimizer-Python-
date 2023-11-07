FROM python

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir epyt pandas numpy matplotlib

WORKDIR /app

COPY . .

ENTRYPOINT [ "python", "app/ObjectiveFunction.py" ]