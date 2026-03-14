"""
Supports the creation of different signal types waveforms
"""

import torch 


class PulseRadar:
    def __init__(self, global_parameters, tx_parameters):
        self.tx_parameters = tx_parameters
        self.global_parameters = global_parameters

        self.bandwidth = self.global_parameters["bandwidth"]
        self.fs = self.global_parameters["fs"]

        self.pulse_width = self.tx_parameters["pulse"]["pulse_width"]
        self.prf = self.tx_parameters["pulse"]["prf"]

        self.duty_cycle = self.pulse_width * self.prf                # duty cycle = pulse_width / PRI
        
        # number of samples in a pulse and in PRI
        self.n_samples = int(self.pulse_width * self.fs)
        self.n_samples_pri = int(self.fs * (1 / self.prf))

        # time vector for one pulse and for PRI
        self.t = torch.linspace(start=torch.tensor(0), end=torch.tensor(self.pulse_width), steps=self.n_samples)
        self.t_pri = torch.linspace(start=torch.tensor(0), end=(1 / self.prf), steps=int(self.n_samples_pri))
        return 
    
    
    def pulse_signal(self, A, t, f0=0, phase=0):
        """
        Generate complex baseband pulse with no modulation, i.e. a rectangular pulse in time domain

        Args: 
            A: amplitude of the signal
            t: The time vector of tx signal
            f0: Initial (lower-bound) frequency at time t=0. At baseband, f0 = 0 Hz
            phase (int, optional): initial phase
        """
        x_complex = A * torch.exp(2j* torch.pi * f0 * t + phase)
        return x_complex


    def chirp(self, A, B, tao, t, f0=0, phase=0):
        """
        Generate complex baseband LFM pulse

        Args:
            A: amplitude of the signal
            B: bandwidth of the chirp signal
            tao: pulse width
            t: Times at which to evaluate the waveform
            f0: Initial (lower-bound) frequency at time t=0, At baseband, f0 is typically set to 0 Hz
            t: The time vector of tx signal
            phase (int, optional): initial phase

        Returns:
            chirp: the LFM signal
        """
        k = B / tao                                                          # chirp slope = rate of change of frequency
        f_chirp = f0 + (k/2) * t                                             # instantaneous frequency of the chirp signal
        chirp = A * torch.exp(2j * torch.pi * f_chirp * t + phase)

        return chirp   
    

    def generate_pulse_train(self, n_samples_tao, n_samples_pri, modulation_type="lfm"):
        """
        Append the generated pulse signal to create a pulse train,
        based on the number of pulses and the pulse repetition frequency (prf)
        Args:
            single_pulse_signal: Description
            n_samples_tao: Description
        Return 
            pulse train
        """
        # obtain the base signal for one pulse
        if modulation_type == "lfm":
            signal = self.chirp(self.tx_parameters["amplitude"], 
                                    self.bandwidth, 
                                    self.pulse_width,
                                    self.t)
        elif modulation_type == "None":
            signal = self.pulse_signal(self.tx_parameters["amplitude"], 
                                          self.t)
        else:
            raise NotImplementedError(f"Modulation type {modulation_type} is not supported yet.")
        
        # create the full PRI vector for the pulse train
        pulse_signal_pri = torch.zeros(n_samples_pri, dtype=torch.complex64)
        pulse_signal_pri[:n_samples_tao] = signal
        
        # repeat the pulse signal for n_pulses to create the pulse train
        pulse_train = pulse_signal_pri.repeat(self.tx_parameters["pulse"]["n_pulses"])
        
        # create the time vector for the whole pulse train
        num_samples_pulse_train = n_samples_pri * self.tx_parameters["pulse"]["n_pulses"]
        t_pulse_train = torch.arange(num_samples_pulse_train) / self.fs 

        return pulse_train, t_pulse_train
    

    def signal_generator_baseband(self):
        reference_signal = self.generate_pulse_train(self.n_samples, 
                                                     self.n_samples_pri, 
                                                     modulation_type=self.tx_parameters["pulse"]["modulation_type"])
        
        return reference_signal
    

    

class CWRadar:
    def __init__(self, tx_parameters, global_parameters, ):
        self.tx_parameters = tx_parameters
        self.global_parameters = global_parameters

        return 

    def signal_generator_baseband(self):
        t = ...
        refence_signal = ...
        return
