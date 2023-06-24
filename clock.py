import utime

class Clock:

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
        self.milliseconds = 0

    # Setters ------------------------------------------------
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
                self.hours = 59

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
                self.hours = 59
                self.set_hours(increment=False)

    def set_seconds(self):
        self.seconds = 0

    # Update the clock
    def update(self):
        
        if self.milliseconds < 99:
            utime.sleep_ms(1)
            self.milliseconds += 1
        
        else:
            self.milliseconds = 0
            if self.seconds < 59:
                self.seconds += 1
            else:
                self.seconds = 0
                self.set_minutes()


    # String format clock
    def stringify(self, twelve_hr_format=False):
        if twelve_hr_format:
            period = "AM"
            modified_hours = self.hours

            if self.hours > 12:
                modified_hours = self.hours - 12
            elif self.hours == 0:
                modified_hours = 12

            if self.hours in range(12, 24):
                period = "PM"

            return f"{modified_hours:2d}:{self.minutes:02d}:{self.seconds:02d} {period}"
        
        else:
            return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"