#!/home/esgeriath/.local/state/python.venv/bin/python3
#!/usr/bin/env python3

import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import uinput

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the URL of your reMarkable tablet
BASE_URL = "https://remarkable:2001"  # HTTPS is required
EVENTS_URL = f"{BASE_URL}/events"
GESTURES_URL = f"{BASE_URL}/gestures"

# maximal outputs from goMarkableStream API on my device
MAX_X = 20966
MAX_Y = 15725

class Pen:
    def __init__(self, width=1920, height=1080, x_top=0, y_top=0, fill=True):
        self.x_top = x_top
        self.y_top = y_top
        if not fill ^ ((width / MAX_X) <= (height / MAX_Y)):
            self.scale = height / MAX_Y
        else:
            self.scale = width / MAX_X

        self.click = False
        self.delay = 0
        # virtual mouse events setup
        abs_x = uinput.ABS_X + (0, width, 0, 0)
        abs_y = uinput.ABS_Y + (0, height, 0, 0)
        events = (
            abs_x,
            abs_y,
            uinput.BTN_LEFT,
        )
        self.mouse = uinput.Device(events, name="Virtual Mouse/Tablet")
        # self.keyboard = uinput.Device()

    def press(self):
        if not self.click:
            self.click = True
            self.mouse.emit(uinput.BTN_LEFT, 1)

    def moveX(self, x):
        x = int(self.x_top + x * self.scale)
        self.mouse.emit(uinput.ABS_X, x)

    def moveY(self, y):
        y = int(self.y_top + y * self.scale)
        self.mouse.emit(uinput.ABS_Y, y)

    def lift(self):
        if self.click:
            self.click = False
            self.mouse.emit(uinput.BTN_LEFT, 0)

    def upside_down(self):
        if self.right:
            self.right = False
            # TODO
            # self.keyboard.emit()

    def rightside_up(self):
        if not self.right:
            self.right = True
            # TODO
            # self.keyboard.emit()
    


# top-left corner == charging port
mapping = {
    0: "x",
    1: "y",
    26: "x_tilt",
    27: "y_tilt",
    24: "pressure",
    25: "distance",
}

def read_pen_events(m):
    """Reads pen events from the reMarkable tablet."""
    try:
        with requests.get(EVENTS_URL, auth=HTTPBasicAuth("admin", "password"),
                          stream=True, verify=False) as response:
            response.raise_for_status()  # Raise an error for bad responses
            print("Connected to reMarkable event stream...")

            # Read the stream line by line
            for line in response.iter_lines():
                if line:
                    # '{"Source":1,"Type":3,"Code":1,"Value":3669}'
                    dec = json.loads(line.decode('utf-8')[6:]) # stripping 'data: '
                    action = mapping[dec["Code"]]
                    if action == "x":
                        m.moveX(dec["Value"])
                    elif action == "y":
                        m.moveY(dec["Value"])
                    elif action == "pressure":
                        if dec["Value"] > 5:
                            m.press()
                    elif action == "distance":
                        if dec["Value"] > 5:
                            m.lift()


    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print(" bye")
        return


if __name__ == "__main__":
    read_pen_events(Pen())
