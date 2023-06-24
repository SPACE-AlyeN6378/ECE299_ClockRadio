from machine import Pin
from components.button import Button

class RotaryEncoder:
    states_order = ((0, 1), (0, 0), (1, 0), (1, 1)) # order in clockwise direction

    # Sequences (using indexes from the 'states_order' list above)
    counterclockwise = [2, 1, 0, 3]
    clockwise = [0, 1, 2, 3]

    def __init__(self, pin_A, pin_B, btn_pin, ccw_turn, cw_turn, on_push) -> None:
        # Pins
        self.pin_A = Pin(pin_A, Pin.IN, Pin.PULL_UP)
        self.pin_B = Pin(pin_B, Pin.IN, Pin.PULL_UP)

        # Function Callbacks
        self.ccw_turn = ccw_turn
        self.cw_turn = cw_turn

        # The last state, the present state and the register
        self.last_state = self.states_order[3]
        self.present_state = self.states_order[3]
        self.register = [] # Which holds a collection of indexes

        # Initialize the interrupts
        self.pin_A.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback)
        self.pin_B.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callback)

        # Initialize the button
        self.button = Button(btn_pin, on_push=on_push)


    def callback(self, pin):
        self.present_state = (self.pin_A.value(), self.pin_B.value())

        # Collect the index values as long as there is a state change
        if self.last_state != self.present_state:
            self.register.append(self.states_order.index(self.present_state))
            self.last_state = self.present_state

            # If the sequence is maintained, just take the last four values
            if self.register[-4:] == self.clockwise:
                self.cw_turn()
                self.register.clear()
            elif self.register[-4:] == self.counterclockwise:
                self.ccw_turn()
                self.register.clear()

    

        
