from components.display import Display
from components.fm_radio import Radio
from components.rotary_encoder import RotaryEncoder
from components.button import Button
from clock import Clock


# ENUMS (for readability purposes) --------------------------

# Modes
NORMAL = 0
TIME_SETTINGS = 1
ALARM_SETTINGS = 2
RADIO_SCHEDULE_SETTINGS = 3

# Type of clock
MAIN_CLOCK = 5
TEMP_CLOCK = 6
ALARM = 7
PLAY_RADIO = 8
MUTE_RADIO = 9

# Pointer movement direction
LEFT = False
RIGHT = True

class CRSystem:
    
    def __init__(self, btn1_pin, btn2_pin, btn3_pin, btn4_pin, rt_btn_pin, rt_pinA, rt_pinB):
        # MODES AND SETTINGS ----------------------------------------
        self.twelve_hr_ft = True
        self.pointer = 0 # The pointer is used to highlight selection
        self.change_vol_mode = False
        self.mode = NORMAL

        # TIMES ----------------------------------------------------
        self.clock = Clock(0, 0)
        self.temp_clock = Clock(0, 0) # To set to a new time while the main clock is running
        
        
        # COMPONENTS ----------------------------------------------------
        self.screen = Display(18, 19, 21, 20, 17)
        self.knob = RotaryEncoder(rt_pinA, rt_pinB, rt_btn_pin, lambda: self.set_freq_vol(False), lambda: self.set_freq_vol(True), self.toggle_vol_control)
        self.button1 = Button(btn1_pin, self.mute)
        self.button2 = Button(btn2_pin, self.toggle_12_24)
        self.button3 = Button(btn3_pin, lambda: self.switch_mode(TIME_SETTINGS))
        self.button4 = Button(btn4_pin, lambda: self.switch_mode(ALARM_SETTINGS))
        
        # RADIO ---------------------------------------------------------
        self.volume = 11
        self.frequency = 100.3
        self.new_frequency = 100.3
        self.is_mute = False
        self.radio = Radio( self.frequency, self.volume, self.is_mute )
        
        # ALARM STATE ---------------------------------------------------
        self.alarm = False
        # If this countdown timer runs out, the alarm will stop and set it to snooze, unless the user hits STOP
        self.countdown = 0
        self.snooze = False
        self.alarm_time = Clock(0, 0)
        self.snooze_time = Clock(0, 0)
    
    # Set all the input configurations to default
    def default_config(self):
        self.pointer = 0
        self.change_vol_mode = False
        self.knob.ccw_turn = lambda: self.set_freq_vol(False)
        self.knob.cw_turn = lambda: self.set_freq_vol(True)
        self.knob.button.on_push = self.toggle_vol_control
        self.button1.on_push = self.mute
        self.button2.on_push = self.toggle_12_24
        self.button3.on_push = lambda: self.switch_mode(TIME_SETTINGS)
        self.button4.on_push = lambda: self.switch_mode(ALARM_SETTINGS)
    
    # A do-nothing function for restricting callback
    def do_nothing(self):
        pass

    # RADIO FUNCTIONALITY ---------------------------------------
    
    # To mute the radio
    def mute(self):
        if not self.alarm:
            self.is_mute = not self.is_mute
            if ( self.radio.SetMute( self.is_mute ) == True ):
                self.radio.ProgramRadio()
            
            
    # To change the volume level (not to be used in the knob)
    def set_volume(self, increment):
        if increment:
            if self.volume < 15:
                self.volume += 1
                
                if ( self.radio.SetVolume( self.volume ) == True ):
                    self.radio.ProgramRadio()
                
        else:
            if self.volume >= 1:
                self.volume -= 1
                
                if ( self.radio.SetVolume( self.volume ) == True ):
                    self.radio.ProgramRadio()
            
        
    # To change the radio frequency (not to be used in the knob)
    def set_frequency(self, increment):
        if increment:
            if self.frequency < 107.9:
                self.frequency += 0.1
                
                if ( self.radio.SetFrequency( self.frequency ) == True ):
                    self.radio.ProgramRadio()
                
        else:
            if self.frequency >= 88.1:
                self.frequency -= 0.1
                
                if ( self.radio.SetFrequency( self.frequency ) == True ):
                    self.radio.ProgramRadio()
                    
    # This is a function for the knob to change either the frequency or the volume, depending on the mode
    def set_freq_vol(self, increment):
        if self.change_vol_mode:
            self.set_volume(increment)
        else:
            self.set_frequency(increment)
                

    # To toggle between volume and frequency control
    def toggle_vol_control(self):
        self.change_vol_mode = not self.change_vol_mode
    
            
    # CLOCK FUNCTIONALITY ---------------------------------------

    # Changes the speed of the clock
    def change_speed(self, increment=True):
        if increment:
            self.clock.speed += 1
        else:
            self.clock.speed -= 1
            
    # Moves the pointer while setting the time/alarm/schedule
    def move_pointer(self, direction, lower_limit=0, upper_limit=9):

        if direction: # Towards the right?
            if self.pointer < upper_limit:
                self.pointer += 1
        else: # Towards the left
            if self.pointer > lower_limit:
                self.pointer -= 1
                        
    # Change the time for the clock/alarm
    def change_time(self, increment=True):
        
        if self.pointer == 1:
            self.temp_clock.set_hours(increment)
        elif self.pointer == 2:
            self.temp_clock.set_minutes(increment)
        elif self.pointer == 3:
            self.temp_clock.set_seconds(increment)
        elif self.pointer == 4:
            self.alarm_time.set_hours(increment)
        elif self.pointer == 5:
            self.alarm_time.set_minutes(increment)
            
    # Toggle 12 and 24-hour clock format
    def toggle_12_24(self):
        self.twelve_hr_ft = not self.twelve_hr_ft 
    
    # ALARM FUNCTIONALITY ---------------------------------------
    # Turn alarm on/off
    def toggle_alarm(self):
        self.alarm = not self.alarm
    
    # Start ringing the alarm
    def start(self):
        self.volume = 11
        self.is_mute = False
        if ( self.radio.SetMute( self.is_mute ) == True ):
            self.radio.ProgramRadio()
    
    # Stop the alarm
    def stop(self):
        self.countdown = 0
        self.is_mute = True
        if ( self.radio.SetMute( self.is_mute ) == True ):
            self.radio.ProgramRadio()
            
        self.default_config()
    
    # Activate the snooze alarm
    def activate_snooze(self):
        self.stop()
        self.snooze = True
        self.snooze_time += 5 # Increment the snooze time by about 5 minutes
    
    # The alarm will ring only when the clock reaches the alarm time
    def ring_alarm(self):
        if (self.alarm and self.clock == self.alarm_time) or (self.snooze and self.clock == self.snooze_time):
            
            self.switch_mode(NORMAL) 
            self.snooze = False
            self.start()
            self.countdown = 30 # Ring the alarm for about 30 seconds, unless it is stopped by the user
            
            self.button1.on_push = self.stop
            self.button2.on_push = self.activate_snooze
            self.button3.on_push = self.do_nothing
            self.button4.on_push = self.do_nothing
                
        if self.countdown > 0:
            self.countdown -= 1
            # print(self.countdown)
            
            # If the alarm rings for 30 seconds, then snooze will be activated
            if self.countdown == 0:
                self.activate_snooze()
                
            
    
    # MODE SWITCHING --------------------------------------------
    def switch_mode(self, given_mode):
        
        self.mode = given_mode
        self.change_vol_mode = False
        
        
        if self.mode == TIME_SETTINGS:
            self.pointer = 1
            self.temp_clock.set_all(self.clock.hours, self.clock.minutes, self.clock.seconds)
            
            # Assign/change the functions for each inputs
            self.knob.ccw_turn = lambda: self.change_time(False) # Decrease Value
            self.knob.cw_turn = lambda: self.change_time(True) # Increase Value
            self.knob.button.on_push = lambda: (self.clock.set_all(self.temp_clock.hours,
                                                                   self.temp_clock.minutes,
                                                                   self.temp_clock.seconds),
                                                self.switch_mode(NORMAL)) # Confirm
            
            self.button1.on_push = lambda: self.move_pointer(LEFT, lower_limit=1) # Move selection to the left
            self.button2.on_push = lambda: self.move_pointer(RIGHT, upper_limit=3) # Move selection to the right
            self.button3.on_push = lambda: self.switch_mode(NORMAL) # Cancel changes
            self.button4.on_push = lambda: self.switch_mode(ALARM_SETTINGS) # Cancel changes and change alarm
            
        elif self.mode == ALARM_SETTINGS:
            self.pointer = 4
            self.snooze = False
            self.alarm = True
            self.stop()
            self.knob.ccw_turn = lambda: self.change_time(False) if self.alarm else self.do_nothing() # Decrease Value
            self.knob.cw_turn = lambda: self.change_time(True) if self.alarm else self.do_nothing() # Increase Value
            self.knob.button.on_push = lambda: (self.snooze_time.set_all(self.alarm_time.hours,
                                                                         self.alarm_time.minutes,
                                                                         self.alarm_time.seconds),
                                                
                                                self.switch_mode(NORMAL)) # Confirm and go back
            
            self.button1.on_push = lambda: self.move_pointer(LEFT, lower_limit=4) if self.alarm else self.do_nothing() # Move selection to the left
            self.button2.on_push = lambda: self.move_pointer(RIGHT, upper_limit=5) if self.alarm else self.do_nothing() # Move selection to the right
            self.button3.on_push = lambda: (self.snooze_time.set_all(self.alarm_time.hours,
                                                                     self.alarm_time.minutes,
                                                                     self.alarm_time.seconds),
                                                
                                                self.snooze_time.print_to_console(True),
                                                self.switch_mode(TIME_SETTINGS))
            
            self.button4.on_push = self.toggle_alarm # Turn alarm on/off
            
        else:
            self.default_config()
    
    # DISPLAY ON SCREEN --------------------------------------------
    def draw(self):
        
        # Dimensions and positions *********************************
        BOX_WIDTH = 128
        UPPER_BOX_HEIGHT = 25
        LOWER_BOX_HEIGHT = 64 - UPPER_BOX_HEIGHT
        CLOCK_POSITION = (8, 9)
        ALARM_LABEL_POS = (7, 31)
        ALARM_POSITION = (7+12*4, 31)
        FREQ_POSITION = (39, 50)
        VOL_LABEL_POS = (7, 50)
        VOL_BAR_POS = (48, 50)
        VOL_BAR_WIDTH = 72
        VOL_BAR_HEIGHT = 7
        # **********************************************************
        
        self.screen.clear_buffer()
        
        # The borders
        self.screen.box( 0, 0, BOX_WIDTH, UPPER_BOX_HEIGHT )
        self.screen.box( 0, UPPER_BOX_HEIGHT, BOX_WIDTH, LOWER_BOX_HEIGHT )
        
        # The main clock
        if self.mode == TIME_SETTINGS:
            self.temp_clock.print_to_display(*CLOCK_POSITION, self.screen, self.pointer, self.twelve_hr_ft)
        else:
            self.clock.print_to_display(*CLOCK_POSITION, self.screen, 0, self.twelve_hr_ft)
        
        # The alarm
        self.screen.text("AL: ", *ALARM_LABEL_POS)
        if self.alarm:
            self.alarm_time.print_to_display(*ALARM_POSITION, self.screen, self.pointer - 3, self.twelve_hr_ft, show_seconds=False)
        else:
            self.screen.text("Alarm off", ALARM_POSITION[0] - 4, ALARM_POSITION[1], self.mode == ALARM_SETTINGS)
        
        if self.change_vol_mode:
            # Volume Control
            self.screen.text("Vol: ", *VOL_LABEL_POS)
            self.screen.box(*VOL_BAR_POS, VOL_BAR_WIDTH, self.VOL_BAR_HEIGHT)
            self.screen.box(*VOL_BAR_POS, int(self.volume * VOL_BAR_WIDTH / 15), self.VOL_BAR_HEIGHT, True)
                
        else:
            # Frequency
            self.screen.text(f"FM   {self.frequency:3.1f}", *FREQ_POSITION)
            
        
        self.screen.update_buffer()
        
    def mainloop(self):
        while True:
            self.draw()
            self.clock.update(self.ring_alarm)
