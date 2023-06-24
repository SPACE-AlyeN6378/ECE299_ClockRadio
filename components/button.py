from machine import Pin
import utime

class Button:
    def __init__(self, pin_number, on_push) -> None:
        # Initialize the pin
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        
        # What will happen if I push this button?
        self.callback = on_push
        
        # Initialize interrupt
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.interrupt_handler)
    
    # This interrupt handler contains the debounce algorithm
    def interrupt_handler(self, pin):
        if pin.value() == 0: # check if the button is pressed
            utime.sleep_ms(10) # Wait for the button signal to settle
            if pin.value() == 0: # Then check if the button is still pressed
                self.callback() # Trigger the function!

