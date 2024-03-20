from gpiozero import Button

def wait_for_button_pressed(gpio: int=17) -> None:
    """
    This function wait infinitely until the
    button linked to the given GPIO get pressed.
    
    :param int gpio: The GPIO the button is linked to.
    """

    # Wait for the button to get pressed.
    Button(gpio).wait_for_press()
