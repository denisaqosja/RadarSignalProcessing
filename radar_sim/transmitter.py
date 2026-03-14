"""
This file contains the main steps in transmitting the radar signal
"""
import torch 

from radar_sim.config import GLOBAL_PARAMETERS, TX_PARAMETERS, ANTENNA_PARAMETERS
from radar_sim.waveform import PulseRadar, CWRadar


class Transmitter:
    """
    Models the transmit chain of a pulsed / CW radar:
    Baseband waveform -> RF upconversion -> power amplifier -> forward propagation
    """
    def __init__(self):

        self.tx_parameters = TX_PARAMETERS
        self.global_parameters = GLOBAL_PARAMETERS
        self.antenna_parameters = ANTENNA_PARAMETERS

        self.bandwidth = self.global_parameters["bandwidth"]
        self.fs = self.global_parameters["fs"]

            
    def signal_generator(self, waveform_type):
        """
        Generates the baseband signal, according to the desired type of the waveform
        Supported: Pulse & CW Radar 
        """
        if waveform_type == "pulse":
            radar = PulseRadar(self.global_parameters, self.tx_parameters)
        elif waveform_type == "cw":
            radar = CWRadar(self.global_parameters, self.tx_parameters)
        else:
            raise NotImplementedError(f"Waveform type {waveform_type} is not supported yet.")
        
        reference_signal, t = radar.signal_generator_baseband()
        return reference_signal, t


    def local_oscillator(self, fc, t):
        """
        Generates the carrier sinusoid at RF frequency (f_c).
        """
        return torch.exp(2j * torch.pi * fc * t) 
    

    def mixer(self, baseband_signal, carrier):
        """
        s_rf(t) = Re{ s_bb(t) * e^{j2π f_c t} }
        Upconverts the baseband signal to RF by multiplying with the carrier.
        """
        tx_waveform = torch.real(carrier * baseband_signal)
        return tx_waveform
    

    def power_amplifier(self, x_t):
        """
        Amplifies the RF signal before transmission.
        """
        # given the power gain (in dB) obtain the gain in voltage
        gain_dB = self.antenna_parameters["Gain"]
        gain_linear = 10 ** (gain_dB / 20.0)

        return gain_linear * x_t
    

    def transmit_waveform(self, waveform_type):
        """ Propagate the generated carrier waveform """
        baseband_signal, t = self.signal_generator(waveform_type)
        carrier = self.local_oscillator(self.tx_parameters["fc"], t)
        tx_waveform = self.mixer(baseband_signal, carrier)

        amplified_signal = self.power_amplifier(tx_waveform)

        return amplified_signal
    