from inputs import get_gamepad
import time

def perform_action():
    """
    Function to perform the action when the button is pressed.
    """
    print("Button 'A' pressed! Performing action...")

def listen_to_controller():
    """
    Listen for button presses on the Xbox controller.
    """
    print("Listening for controller input...")
    while True:
        events = get_gamepad()
        for event in events:
            # Check if it's a button press event
            if event.ev_type == "Key" and event.state == 1:  # state == 1 means button pressed
                if event.code == "BTN_SOUTH":  # BTN_SOUTH corresponds to the 'A' button
                    perform_action()

if __name__ == "__main__":
    try:
        listen_to_controller()
    except KeyboardInterrupt:
        print("\nExiting...")
