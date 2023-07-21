import utime

class Clock:
    
    count = 0
    
    # For correction purposes if the programmer enters a number outside the given range in the constructor
    def clamp(self, value, upper_bound):
        if value < 0:
            return 0
        elif value > upper_bound:
            return upper_bound
        else:
            return value

    # Constructor
    def __init__(self, hours, minutes):
        
        self.hours = self.clamp(hours, 23)
        self.minutes = self.clamp(minutes, 59)
        self.seconds = 0
        self.speed = 95 # In number of counts per tick
        
    def __eq__(self, other):
        if not isinstance(other, Clock):
            return False
        return self.hours == other.hours and self.minutes == other.minutes and self.seconds == other.seconds
        
    # Setters ------------------------------------------------
    def set_all(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def set_hours(self, increment=True):
        if increment:
            if self.hours < 23:
                self.hours += 1
            else:
                self.hours = 0
        else:
            # Decrement instead
            if self.hours > 0:
                self.hours -= 1
            else:
                self.hours = 23

    def set_minutes(self, increment=True):
        if increment:
            if self.minutes < 59:
                self.minutes += 1
            else:
                self.minutes = 0
                self.set_hours()
        else:
            # Decrement instead
            if self.minutes > 0:
                self.minutes -= 1
            else:
                self.minutes = 59
                self.set_hours(increment=False)

    def set_seconds(self, increment=True):

        if increment:
            if self.seconds < 59:
                self.seconds += 1
            else:
                self.seconds = 0
                self.set_minutes()

        else:
            # Decrement instead
            if self.seconds > 0:
                self.seconds -= 1
            else:
                self.seconds = 59
                self.set_minutes(increment=False)
    
    # Adds the given value of minutes into the time
    def __add__(self, minutes_to_add):
        
        if not isinstance(minutes_to_add, int):
            raise ValueError("Only integer value of minutes can be added.")
        
        if minutes_to_add < 0:
            raise ValueError("Minutes cannot be negative.")
        
        new_time = Clock(self.hours, self.minutes)
        for i in range(minutes_to_add):
            new_time.set_minutes()
            
        return new_time
            
        
    # Update the clock
    def update(self, trigger_func):
        if self.count < (self.speed - 1):
            self.count += 1
        
        else:
            self.count = 0
            self.set_seconds()
            trigger_func()
            
    
    # Print the time on to the screen
    def print_to_display(self, x, y, display, selected, twelve_hr_format=False, show_seconds=True): # The 'selected' is in integer
        
        period = "HR"
        hours = self.hours
        
        if twelve_hr_format:
            period = "AM"
            
            hours = hours % 12 if hours % 12 != 0 else 12
                
            if self.hours in range(12, 24):
                period = "PM"
                
        display.text(f"{hours:2d}", x, y, selected == 1)
        display.text(f"{self.minutes:02d}", x + 24, y, selected == 2)
        
        if show_seconds:
            display.text("  :  :", x, y)
            display.text(f"{self.seconds:02d}", x + 48, y, selected == 3)
            display.text(period, x + 72, y)
        else:
            display.text("  :", x, y)
            display.text(period, x + 48, y)
            
    # Print the time on to the console
    def print_to_console(self, twelve_hr_format=False): # The 'selected' is in integer
        
        period = "HR"
        hours = self.hours
        
        if twelve_hr_format:
            period = "AM"
            
            hours = hours % 12 if hours % 12 != 0 else 12
                
            if self.hours in range(12, 24):
                period = "PM"
        
        print(f"{hours:2d}:{self.minutes:02d}:{self.seconds:02d}", period)
        
        