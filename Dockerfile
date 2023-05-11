FROM python:3.10-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ARG APP_DIRECTORY=/satellite_orbit_prediction
WORKDIR $APP_DIRECTORY
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:$APP_DIRECTORY"

ARG SUPPLEMENTAL_DIRECTORY=$APP_DIRECTORY/supplements
VOLUME ["$SUPPLEMENTAL_DIRECTORY"]

ENTRYPOINT ["python3", "sopp.py"]
