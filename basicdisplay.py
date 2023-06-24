from components.display import Display
from components.rotary_encoder import RotaryEncoder
from clock import Clock

# Assign a value to a variable
count = 6
show_alarm = False

def increment():
    global count
    count += 1
    
def decrement():
    global count
    count -= 1
    
def set_number(x):
    global count
    count = x
    
def toggle_alarm():
    global show_alarm
    show_alarm = not show_alarm


#Knob declaration
knob = RotaryEncoder(14, 15, 13, decrement, increment, toggle_alarm)

# Display
display = Display(18, 19, 21, 20, 17)

# Clock
clock = Clock(20, 31)
alarm_clock = Clock(7, 0)


while ( True ):
    display.clear_buffer()
        
#
# Update the text on the screen
#
    if show_alarm:
        display.text(alarm_clock.stringify(True), 0, 0) # Print the text starting from 0th column and 0th row
    else:
        display.text(clock.stringify(True), 0, 0) # Print the text starting from 0th column and 0th row
        
    display.text(f"Count is: {count:4d}", 0, 30 ) # Print the value stored in the variable Count. 
        
#
# Draw box below the text
#
    display.box( 0, 50, 128, 5, 1  )        
    

    
#
# Transfer the buffer to the screen
#
    
    display.update_buffer()
    clock.update()
    
    