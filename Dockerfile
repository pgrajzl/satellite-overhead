FROM python:3.10-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ARG CU_PASS_ROOT_DIRECTORY=/cu_pass
ARG APP_DIRECTORY=$CU_PASS_ROOT_DIRECTORY/satellite_orbit_prediction
WORKDIR $APP_DIRECTORY
COPY ./requirements.txt .
RUN pip install -r requirements.txt

ARG TLE_DATA_DIRECTORY=$CU_PASS_ROOT_DIRECTORY/tle_data
VOLUME ["$TLE_DATA_DIRECTORY"]

ENTRYPOINT ["python3", "sopp.py"]
