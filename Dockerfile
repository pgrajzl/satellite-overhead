FROM python:3.10-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ARG CU_PASS_ROOT_DIRECTORY=/cu_pass
ARG APP_DIRECTORY=$CU_PASS_ROOT_DIRECTORY/satellite_orbit_prediction
WORKDIR $APP_DIRECTORY
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:$APP_DIRECTORY"

ARG TLE_DATA_DIRECTORY=$APP_DIRECTORY/TLEData
VOLUME ["$TLE_DATA_DIRECTORY"]

ENTRYPOINT ["python3", "satellite_determination/sopp.py"]
