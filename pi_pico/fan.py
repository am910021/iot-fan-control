import utime
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

  
@asm_pio() # No additional arguments required
def pulse_counter():
    
    label("loop")           # Start of the loop
    mov(x, null)            # Clear X
    mov(osr, null)          # Clear OSR
    pull(noblock)           # Pull from TX FIFO - if this is empty the OSR is filled from X
                            # OSR must be empty for either to work
    mov(x, osr)             # Load value from OSR into X
    
    jmp(not_x, "continue")  # If X is not empty, we're going to reset the counter and output the data
    mov(isr, y)             # Move Y (which is (2^32 - 1 - the number of edges)) into the ISR
    push()                  # Push that value into the RX FIFO
    mov(y, osr)             # Reset Y to 2^32 - 1 (which the value in the OSR right now)
       
    label("continue")       # If X is empty, we'll counting rising edges
    wait(0, pin, 0)         # wait for rising edge of input signal
    wait(1, pin, 0)
    jmp(y_dec, "loop")      # Jump back to the beginning and decrement Y.

# Create the state machine on the correct pin and start it, and initialise it.
pulse_counter_sm = StateMachine(0, pulse_counter, in_base=Pin(2)) #
pulse_counter_sm.active(1)
pulse_counter_sm.put(0xFFFFFFFF)

# Save the time in microseconds
ticks = utime.ticks_us()

while(True):
    utime.sleep(1)  # Wait for 1s
    last_ticks = ticks    
    pulse_counter_sm.put(0xFFFFFFFF) # This value both triggers the request for data and resets the counter
    ticks = utime.ticks_us() # Save the time the counter was restarted
                             # This is here so it can be right after the put() command for better accuracy
    
    if not pulse_counter_sm.rx_fifo(): # Check if there's any data to get
        print("No Data")
    else:
        pulses = 0xFFFFFFFF - pulse_counter_sm.get()            # Calculate the actual number of pulses
        period = utime.ticks_diff(utime.ticks_us(), last_ticks) # Calculate time difference
        # Display the data
        print(str(pulses) + " pulses, " + str(period/1000000) + " s, " + str(1000000 * pulses/period) + " Hz" )