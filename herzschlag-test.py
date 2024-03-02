import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)


if __name__ == '__main__':

   
    # initialization 
    GAIN = 2/3  
    curState = 0
    thresh = 525  # mid point in the waveform
    P = 512
    T = 512
    stateChanged = 0
    sampleCounter = 0
    lastBeatTime = 0
    firstBeat = True
    secondBeat = False
    Pulse = False
    IBI = 600
    rate = [0]*10
    amp = 100

    lastTime = int(time.time()*1000)

    # Main loop. use Ctrl-c to stop the code
    while True:
        # read from the ADC
        Signal = chan0.value   #TODO: Select the correct ADC channel. I have selected A0 here
        curTime = int(time.time()*1000)

        sampleCounter += curTime - lastTime;      ## keep track of the time in mS with this variable
        lastTime = curTime
        N = sampleCounter - lastBeatTime;     #  # monitor the time since the last beat to avoid noise
       

        ##  find the peak 
        if Signal < thresh and N > (IBI/5.0)*3.0 :  #       # avoid dichrotic noise by waiting 3/5 of last IBI
            if Signal < T :                        # T is the trough
              T = Signal;                         # keep track of lowest point in pulse wave 

        if Signal > thresh and  Signal > P:           # thresh condition helps avoid noise
            P = Signal;                             # P is the peak
                                                # keep track of highest point in pulse wave

         
          # signal surges up in value every time there is a pulse
        if N > 250 :                                   # avoid high frequency noise
            if  (Signal > thresh) and  (Pulse == False) and  (N > (IBI/5.0)*3.0)  :       
              Pulse = True;                               # set the Pulse flag when we think there is a pulse
              IBI = sampleCounter - lastBeatTime;         # measure time between beats in mS
              lastBeatTime = sampleCounter;               # keep track of time for next pulse

              if secondBeat :                        # if this is the second beat, if secondBeat == TRUE
                secondBeat = False;                  # clear secondBeat flag
                for i in range(0,10):             # seed the running total to get a realisitic BPM at startup
                  rate[i] = IBI;                      

              if firstBeat :
                firstBeat = False;                   
                secondBeat = True;
                continue                              


              # keep a running total of the last 10 IBI values
              runningTotal = 0;                  # clear the runningTotal variable    

              for i in range(0,9):                # shift data in the rate array
                rate[i] = rate[i+1];                   
                runningTotal += rate[i];              

              rate[9] = IBI;                          
              runningTotal += rate[9];                
              runningTotal /= 10;                     
              BPM = 60000/runningTotal;               
              print ('BPM: {}'.format(BPM))

        if Signal > thresh and Pulse == True :   # when the values are going down, the beat is over
            Pulse = False;                         
            amp = P - T;                           
            thresh = amp/2 + T;                    
            P = thresh                          
            T = thresh

        if N > 2500 :                          # if 2.5 seconds go by without a beat
            thresh = 512;                          # set thresh default
            P = 512;                               # set P default
            T = 512;                               # set T default
            lastBeatTime = sampleCounter;          # bring the lastBeatTime up to date        
            firstBeat = True;                      # set these to avoid noise
            secondBeat = False;                    # when we get the heartbeat back
            print ("no beats found")

        time.sleep(0.005)