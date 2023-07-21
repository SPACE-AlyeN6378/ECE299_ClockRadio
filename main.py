from cr_system import CRSystem

button_pins = (4, 5, 6, 7)
rotary_encoder_pins = (3, 0, 1)
system = CRSystem(*button_pins, *rotary_encoder_pins)

system.mainloop()