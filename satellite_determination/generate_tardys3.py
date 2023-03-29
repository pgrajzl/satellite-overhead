from datetime import datetime
import json
from satellite_determination.window_finder import SuggestedReservation

class Tardys3Generator:

    def __init__(self,
                 chosen_reservation: SuggestedReservation,
                 chosen_reservation_end_time: datetime):
        self._chosen_reservation = chosen_reservation
        self._chosen_reservation_end_time = chosen_reservation_end_time

    def generate_tardys(self):

        # Open the tardys3 reservation format
        with open('tardys3.json') as f:
            tardys3 = json.load(f)

        # Input data from variables into json file
        tardys3['definitions']['ScheduledEvents']['properties']['transactionId'] = {
            "type": "string",
            "transactionId": "c4c6f07b-e1a9-4a7c-a05e-09d186967e9b"
        }

        tardys3['definitions']['ScheduledEvents']['properties']['dateTimePublished'] = {
            "type": "string",
            "dateTimePublished": "2021-11-17T01:00:00.000Z"
        }

        tardys3['definitions']['ScheduledEvents']['properties']['dateTimeCreated'] = {
            "type": "string",
            # "default": f"{datetime.now(tz=pytz.UTC).strftime('%yyyy-%mm-%dd %H:%M:%S')}"
            "dateTimeCreated": datetime.now().isoformat()

        }

        tardys3['definitions']['ScheduledEvents']['properties']['checksum'] = {
            "type": "string",
            "checksum": "a35cf7d9"
        }

        tardys3['definitions']['ScheduledEvent']['properties']['eventId'] = {
            "type": "string",
            "eventId": "c4c6f07b-e1a9-4a7c-a05e-09d186967e9b"
        }

        tardys3['definitions']['ScheduledEvent']['properties']['dpaId'] = {
            "type": "string",
            "dpaId": "ddda9e28-18e0-4ab7-9270-4f477045f32d"
        }

        tardys3['definitions']['ScheduledEvent']['properties']['dpaName'] = {
            "type": "string",
            "dpaName": self._chosen_reservation.ideal_reservation.facility.name
        }

        tardys3['definitions']['ScheduledEvent']['properties']['channels'] = {
            "type": "array",
            "items": {
                "type": "string",
                "format": "uuid",
                "channels": ["4385ae93-5466-48d4-8024-14442193d783"]
            }
        }

        tardys3['definitions']['ScheduledEvent']['properties']['dateTimeStart'] = {
            "type": "string",
            "format": "date-time",
            "dateTimeStart": f"{self._chosen_reservation.suggested_start_time.isoformat()}"
        }

        tardys3['definitions']['ScheduledEvent']['properties']['dateTimeEnd'] = {
            "type": "string",
            "format": "date-time",
            "dateTimeEnd": f"{self._chosen_reservation_end_time.isoformat()}"
        }

        #print(json.dumps(tardys3, indent=4))
        print("Outputting tardys3 file as tardys3_reservation.json")
        with open("tardys3_reservation.json", "w") as fp:
            json.dump(tardys3, fp)
