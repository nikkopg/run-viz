# Running Visualizer
Simple python-based app to fetch activities from Strava and visualize them.

## Usage
```
python main.py \
    --id client_id \
    --secret client_secret \
    --n_activities 666
```

### Installation
Uses Python 3.13 with [virtual environments](https://docs.python.org/3/library/venv.html).

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Create Strava Client API
This will require you to [create Strava API App](https://developers.strava.com/docs/getting-started/) to fetch the activities from your Strava account. 

*Relax, no data is sent to anywhere--they are stored on your local system.*

Once you created the Strava API App, you can get your `client_id` and `client_secret` from https://www.strava.com/settings/api.