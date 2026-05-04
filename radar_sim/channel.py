import torch 
import math 
from radar_sim.utils import db_to_linear, linear_to_db, dBm_to_linear


class PropagationChannel:
    """
    
    """

    def __init__(self, global_parameters, antenna_parameters):
        self.global_parameters = global_parameters
        self.antenna_parameters = antenna_parameters
    

    def time_delay(self, R, prf=None):
        """
        Round-trip propagation delay in seconds:
        tau = 2R / c
        
        If PRF is None (CW radar), calculates delay based on true range.
        If PRF is provided (pulsed radar), calculates delay based on observed range,
        constrained to the unambiguous interval [0, R_max].
       
        In pulsed radar, the maximum unambiguous range is:
            R_max = c / (2 * PRF)
        
        Ranges beyond R_max fold back into [0, R_max].
        
        Args:
            R: Target range (meters)
            prf: Pulse Repetition Frequency (Hz). If provided, delay is based on 
                 observed range within unambiguous interval. If None, based on true range.
        
        Return:
            Round-trip propagation delay (seconds)
        """
        # Get observed range (constrained to unambiguous interval if prf is provided)
        R_max = self.global_parameters["c"] / (2.0 * prf) if prf is not None else R

        # Fold range into unambiguous interval [0, R_max]
        R_folded = R % (2.0 * R_max)
        if R_folded > R_max:
            R_folded = 2.0 * R_max - R_folded
        R_unamb = R_folded if prf is not None else R

        # Calculate delay based on observed range
        return 2 * R_unamb / self.global_parameters["c"]


    def doppler_shift(self, v_r, prf=None):
        """
        Doppler frequency shift for a target with radial velocity v_r (m/s).
        Positive v_r = target receding (moving away).
        Negative v_r = target approaching (closing).

        The Doppler shift can be calculated as:
            f_d = 2 * v_r / λ = 2 * v_r * f_c / c

        In pulsed radar, if PRF is provided, the Doppler shift is wrapped
        into the unambiguous range [-PRF/2, +PRF/2] to account for aliasing.
        If PRF is None (CW radar), returns the raw Doppler shift without folding.
        
        Args:
            v_r: Radial velocity (m/s)
            prf: Pulse Repetition Frequency (Hz). 
            
        Return:
            Doppler frequency shift (Hz). 
        """
        wavelength = self.global_parameters["wavelength"]
        
        # Calculate raw Doppler shift: f_d = 2 * v_r / λ
        f_d = 2 * v_r / wavelength
        
        # If PRF is provided (Pulse radar not CW), fold into unambiguous range [-PRF/2, +PRF/2]
        if prf is not None:
            # Wrap Doppler shift into [-PRF/2, +PRF/2]
            prf_half = prf / 2.0
            f_d_folded = ((f_d + prf_half) % prf) - prf_half
            return f_d_folded
        
        return f_d


    def phase_shift(self, R):
        """
        Apply the round-trip phase shift e^{-j * 4*pi*R / lambda}.
        Args:
            R: Target range (meters)

        Return:
            The phase shift
        """
        phi = 4 * torch.pi * R / self.global_parameters["wavelength"]
        return phi   
    

    def path_loss(self, R, rcs):
        """
        Path loss according to the radar range equation.
        
        The received power is:
            Pr = Pt * Gt * Gr * λ² * σ / ((4π)³ * R⁴)

        Where:
            Pt: Transmitted power (W)
            Gt, Gr: Transmit and receive antenna gains (linear scale)
            λ: Wavelength (m)
            σ: RCS (m²)
            R: Range (m)                                

        The amplitude scaling factor for voltage is:
            amplitude_factor = torch.sqrt(Pr / Pt) / R²
        Args:            
            R: Target range (meters)
            rcs: Radar cross-section (linear scale, m²)     
        Return:
            Amplitude scaling factor (voltage).
        """        
        # Convert gains from dB to linear scale
        Gain_linear = db_to_linear(self.antenna_parameters['Gain'])
        Losses_linear = db_to_linear(self.antenna_parameters["Losses"])

        # Transmitted power
        P_tx_linear = dBm_to_linear(self.global_parameters['P_tx'])
        # Wavelength
        wavelength = self.global_parameters['wavelength']
        
        # Radar range equation
        # For monostatic radar: Gt = Gr = Gain
        path_loss_factor = (Gain_linear**2 * wavelength**2 * rcs) / ((4 * torch.pi)**3 * R ** 4)
        
        # Amplitude scaling factor, while accounting for system losses
        amplitude_factor = math.sqrt(P_tx_linear * path_loss_factor / Losses_linear)
        
        return amplitude_factor

    
    def propagate(self, tx_signal, targets):
        """
        Superpose returns from multiple targets.

        targets : list of dicts, each with keys:
                    "R"   : range (m)
                    "v_r" : radial velocity (m/s)
                    "rcs" : radar cross section (m^2) .
        """
        
        rx_dtype = torch.promote_types(tx_signal.dtype, torch.complex64)
        rx_composite = torch.zeros(tx_signal.shape, dtype=rx_dtype, device=tx_signal.device)

        for target in targets:
            if isinstance(target, dict):
                target_range = target.get("R", target.get("range_m"))
                v_r = target.get("v_r", target.get("velocity_mps", 0.0))
                rcs = target.get("rcs", target.get("rcs_linear", 1.0))
            else:
                target_range = target.range_m
                v_r = getattr(target, "velocity_mps", 0.0)
                rcs = getattr(target, "rcs_linear", 1.0)

            rx = self.propagate_target(tx_signal, target_range, v_r, rcs)
            rx_composite += rx
        return rx_composite
    

    def propagate_target(self, tx_signal, range, v_r, rcs):
        """Propagate LFM signal to target at range R with radial velocity v_r."""

        fs = self.global_parameters["fs"]
        n_samples = len(tx_signal)

        # Obtain the contribution of the propagation delay in the frequency domain:
        tau = self.time_delay(range)
        # Apply the propagation delay in the frequency domain: x(t - tau) <-> X(f) * exp(-j * 2*pi*f*tau)
        freqs = torch.fft.fftfreq(n_samples, d=1/fs, device=tx_signal.device)
        delay_factor = torch.exp(-1j * 2 * torch.pi * freqs * tau)
        delayed_signal = torch.fft.ifft(torch.fft.fft(tx_signal) * delay_factor)

        # obtain the contribution of the Doppler shift in the time domain:
        f_d = self.doppler_shift(v_r)
        t = torch.arange(n_samples, device=tx_signal.device) / fs
        doppler_factor =  torch.exp(1j * 2 * torch.pi * f_d * t)
       
        # For a passband/RF tx_signal, the frequency-domain delay already includes
        # the carrier phase exp(-j * 2*pi*fc*tau) = exp(-j * 4*pi*R/lambda).
        # Do not apply phase_factor again, otherwise the carrier phase is double-counted.
        amplitude_factor = self.path_loss(range, rcs)
        return amplitude_factor * delayed_signal * doppler_factor # * self.phase_shift(range)
