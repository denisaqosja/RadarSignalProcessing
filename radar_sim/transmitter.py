"""
This file contains the main steps in transmitting the radar signal
"""
import torch 

from radar_sim.waveform import PulseRadar, CWRadar


class Transmitter:
    """
    Models the transmit chain of a pulsed / CW radar:
    Baseband waveform -> RF upconversion -> power amplifier -> forward propagation
    """
    
    def __init__(self):
        pass

            
    def signal_generator(self, waveform_type):
        """
        Generates the baseband signal, according to the desired type of the waveform
        Supported: Pulse & CW Radar 
        """
        
        return 


    def local_oscillator(self, fc, t):
        """
        Generates the carrier sinusoid at RF frequency (f_c).
        """
        return 
    

    def mixer(self, baseband_signal, carrier):
        """
        s_rf(t) = Re{ s_bb(t) * e^{j2π f_c t} }
        Upconverts the baseband signal to RF by multiplying with the carrier.
        """
       
        return 
    

    def power_amplifier(self, x_t):
        """
        Amplifies the RF signal before transmission.
        """
        
        return 
    

    def propagate_waveform(self, waveform_type):
        
        return 
    