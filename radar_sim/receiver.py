"""
This file contains the main steps in receving the radar signal and 
demodulating it to baseband frequency. 
"""

from radar_sim.config import GLOBAL_PARAMETERS, RX_PARAMETERS

class Receiver:
    def __init__(self):
        self.global_parameters = GLOBAL_PARAMETERS
        self.rx_parameters = RX_PARAMETERS

    def low_noise_amplifier(self, rf_signal):
        """First stage — amplify before any other processing to set the noise figure."""
        # noise figure = minimum
        pass

    def bandpass_filter(self, rf_signal):
        """Suppress out-of-band interference and image frequencies before mixing."""
        pass

    def local_oscillator(self):
        """Same LO as transmitter — must be phase-coherent with TX LO for coherent processing."""
        pass

    def mixer(self, rf_signal, lo_signal):
        """Downconvert RF to baseband: multiply then lowpass filter to remove the 2fc component."""
        pass

    def if_amplifier(self, bb_signal):
        """Amplify and filter the baseband signal before ADC."""
        pass

    def adc(self, bb_signal):
        """Quantise the analogue baseband signal to discrete samples."""
        pass

    def receive(self, rf_signal):
        """Full receiver chain."""
        rf_signal   = self.low_noise_amplifier(rf_signal)
        rf_signal   = self.bandpass_filter(rf_signal)
        lo_signal   = self.local_oscillator()
        bb_signal   = self.mixer(rf_signal, lo_signal)
        bb_signal   = self.if_amplifier(bb_signal)
        digital     = self.adc(bb_signal)
        return digital
 
 
 # TODO: don't forget to add the noise floor! 


