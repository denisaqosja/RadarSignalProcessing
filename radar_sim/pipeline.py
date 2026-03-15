"""
End-to-end radar simulation pipeline.

Brings together waveform generation, target models, 
channel propagation, receiver and signal processing.
"""

import numpy as np 
import os, scipy
import matplotlib.pyplot as plt

from radar_sim.config import load_config, GLOBAL_PARAMETERS
from radar_sim.config import TX_PARAMETERS, RX_PARAMETERS, TARGET_PARAMETERS

from radar_sim.transmitter import Transmitter as TX
from radar_sim.receiver import Receiver as RX
from radar_sim.target_modeling import PointTargets


class Pipeline:
    def __init__(self, config_params):
        self.config_params = config_params


    def transmit_signal(self, tx_signal_type):
        # design the transmit signal based on the requirements set the the transmitter config
        transmitter = TX()
        tx_signal = transmitter.transmit_waveform(tx_signal_type)

        return tx_signal


    def propagate_signal(self, targets):
        # propagate the signal

        return  
    

    def receive_echoes(self, rx_signal_type):
        # bring the recieved signal to baseband 
        rx_signal = RX(self.rx_parameters).return_signal_to_baseband()

        return rx_signal


    def signal_processor(self):
        # process the signal along range and Doppler dimensions

        return 
    
    
class Simulator:
    def __init__(self, targets_type="point_target"):
        """
        Initialize radar simulator.
        
        Args:
            targets_type (str): Type of targets ('point_target' by default)
        """
        self.targets_type = targets_type
        self._targets = None

        # Load the config parameters 
        config_params = load_config()
        self.pipeline = Pipeline(config_params)
    
    
    def build_targets(self, targets_type="point_target"):
        """
        Build target collection based on target type.
        
        Args:
            targets_type (str): Type of targets to build. 
                - "point_target": Point targets from configuration
                - "custom": Custom targets (can be extended)
                
        Returns:
            PointTargets: Collection of targets loaded from configuration
        """
        if targets_type == "point_target":
            # Load point targets from configuration
            targets = PointTargets(TARGET_PARAMETERS)
            return targets
        else:
            raise ValueError(f"Unknown target type: {targets_type}. "
                           f"Supported types: 'point_target'")
    
    
    def clutter(self):
        
        return
    

    def simulate_data(self, data_representation="hrrp"):
        """
        Run end-to-end radar simulation pipeline.
        Args:
            data_representation (str): Output representation
                
        Return:
            dict: Simulation results containing targets and processed data
        """
        print(f"\n Simulation Started \n")
        # Transmit signal
        tx_signal = self.pipeline.transmit_signal(TX_PARAMETERS["type_tx_signal"])
        print(f"TX Signal type: {TX_PARAMETERS['type_tx_signal']}")
        
        # Build targets from configuration
        targets = self.build_targets(self.targets_type)
        print(f"Number of targets: {targets.num_targets()}")
             
        
        # Propagate signal through channel
        ...
        
        # Receive and process signal
        ...
        
        print(f"\n Simulation Complete \n")
        
        return  
        
        

if __name__ == "__main__":
    targets_type = "point_target"
    radar_sim = Simulator(targets_type)
    data = radar_sim.simulate_data(targets_type)
    
    
    