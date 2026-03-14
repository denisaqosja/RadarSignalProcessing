# Radar Simulation Pipeline

An end-to-end simulation of a pulse radar system implemented in PyTorch. The pipeline covers chirp waveform generation, free-space propagation, receiver and signal processing.

## Project Structure

```
RadarSignalProcessing/
├── README.md                           # Project documentation
├── config.yaml                         # (in configs/ folder)
│
├── radar_sim/                          # Main package
│   ├── __pycache__/                   # Python cache
│   ├── config.py                      # YAML configuration loader
│   ├── channel.py                     # Propagation models 
│   ├── waveform.py                    # PulseRadar & CWRadar waveform generators
│   ├── transmitter.py                 # TX chain (baseband → RF → PA)
│   ├── receiver.py                    # RX chain framework
│   ├── signal_processor.py            # Range/Doppler processing
│   ├── helpers.py                     # Helper functions
│   ├── visualization.py               # Plotting utilities 
│   └── pipeline.py                    # End-to-end simulation pipeline 
│
├── configs/                            # Configuration files
│   ├── config.yaml                    # Main system parameters
│   └── scenario1.yaml                 # Alternative scenario configuration
│
├── notebooks/                          # Jupyter notebooks for exploration
│   ├── tx_waveform.ipynb              # Waveform generation examples
│   └── filtering.ipynb                # Signal filtering examples
│
└── results/                            # Output and results directory
```


## Getting Started

### Prerequisites

Before running the simulation, ensure you have the following installed:

- **Python 3.8 or higher**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/RadarSignalProcessing.git
   cd RadarSignalProcessing
   ```


2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt  (TODO: add env file)
   ```


### Run Simulation
```bash
python radar_sim/pipeline.py
```

### Configuration

All simulation parameters are located in `configs/config.yaml`. 

Edit these values to customize your simulation:

```yaml
global_parameters:
  bandwidth: 200e6          # Bandwidth in Hz

tx_parameters:
  fc: 10e9                  # Carrier frequency
  pulse:
    pulse_width: 20e-6      # Pulse width in seconds
    prf: 2000               # Pulse repetition frequency
    n_pulses: 128           # Number of pulses
```


## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)



## License
This project is provided for educational and research purposes.


