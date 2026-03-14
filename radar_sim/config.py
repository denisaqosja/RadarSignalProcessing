"""
Config loader for radar simulation parameters.
Loads parameters from YAML file and computes derived values.
"""
import yaml
import os


def load_config(config_path='configs/config.yaml'):
    """
    Load configuration from YAML file and compute derived parameters.
    
    Args:
        config_path: Path to the YAML config file
        
    Returns:
        Dictionary containing all configuration parameters
    """
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct absolute path to config file
    full_path = os.path.join(current_dir, '..', config_path)
    
    with open(full_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Calculate derived parameters
    config['global_parameters']['fs'] = 1.2 * config['global_parameters']['bandwidth']
    config['global_parameters']['wavelength'] = config['global_parameters']['c'] / config['tx_parameters']['fc']
    
    return config


# Load configuration
_CONFIG = load_config()

# Export configuration dictionaries for backward compatibility
GLOBAL_PARAMETERS = _CONFIG['global_parameters']
TX_PARAMETERS = _CONFIG['tx_parameters']
ANTENNA_PARAMETERS = _CONFIG['antenna_parameters']
RX_PARAMETERS = _CONFIG['rx_parameters']