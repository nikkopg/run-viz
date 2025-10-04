import requests
import time
import webbrowser
from src.common.utils import load_json, save_json
from src.common.logger import Logger


class ActivityFetcher:

    def __init__(self, client_id, client_secret, logger: Logger):
        self.__logging = logger.logger
        self.logging_path = logger.log_filepath

        self.__client_id = client_id
        self.__client_secret = client_secret

        self.__tokens_file = ".local/tokens.json"
        self.__redirect_url = "http://localhost/exchange_token"


    def authorize(self):
        auth_url = (
            f"https://www.strava.com/oauth/authorize?client_id={self.__client_id}"
            f"&response_type=code&redirect_uri={self.__redirect_url}"
            f"&approval_prompt=force&scope=read,activity:read_all"
        )
        self.__logging.info("Open this URL in your browser and approve access:")
        self.__logging.info(auth_url)
        try:
            webbrowser.open(auth_url)
        except:
            pass
        code = input("Paste the 'code' parameter from the redirected URL here: ").strip()

        res = requests.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": self.__client_id,
                "client_secret": self.__client_secret,
                "code": code,
                "grant_type": "authorization_code"
            }
        )
        tokens = res.json()
        save_json(tokens, self.__tokens_file)
        return tokens
    

    def refresh_access_token(self, refresh_token):
        res = requests.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": self.__client_id,
                "client_secret": self.__client_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
        )
        tokens = res.json()
        save_json(tokens, self.__tokens_file)
        return tokens


    def get_access_token(self):
        tokens = load_json(self.__tokens_file)
        if not tokens:
            tokens = self.authorize()

        if time.time() > tokens["expires_at"]:
            tokens = self.refresh_access_token(tokens["refresh_token"])

        return tokens["access_token"]
    

    def get_n_activities(self, n=10, save=True):
        activities = self.fetch_activities(per_page=n, max_pages=1)
        self.__logging.info(f"Fetched {len(activities)} activities:")

        activity_data = []
        for act in activities:
            self.__logging.info(f"- {act['name']} on {act['start_date']} ({act['distance']/1000:.2f} km)")
            if act['type'] == 'Run':
                details = self.fetch_activity_details(act['id'], streams=True)

                # merge summary + details
                activity_data.append({
                    "summary": act,
                    "details": details
                })

        if save:
            save_json(activity_data, f"{self.logging_path}/activities.json")

        return activity_data


    def fetch_activities(self, per_page=30, max_pages=1):
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        all_activities = []
        for page in range(1, max_pages + 1):
            res = requests.get(
                "https://www.strava.com/api/v3/athlete/activities",
                headers=headers,
                params={"per_page": per_page, "page": page}
            )
            data = res.json()
            if not data:
                break
            all_activities.extend(data)
        return all_activities
    

    def fetch_activity_details(self, activity_id, streams=False):
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        if streams:
            # Activity streams (heartrate, cadence, etc.)
            res = requests.get(
                f"https://www.strava.com/api/v3/activities/{activity_id}/streams",
                headers=headers,
                params={
                    "keys": "time,heartrate,velocity_smooth,watts,temp,grade_smooth,cadence,latlng",
                    "key_by_type": "true",
                    "resolution": "high"
                }
            )

        else:
            # Detailed activity (summary info, splits, avg HR, etc.)
            res = requests.get(
                f"https://www.strava.com/api/v3/activities/{activity_id}",
                headers=headers,
                params={"include_all_efforts": False}
            )

        return res.json()

