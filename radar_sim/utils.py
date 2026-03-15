
"""Physical constants and utility functions for radar signal processing."""

import torch

# Physical constants
C = 3e8  # Speed of light in vacuum (m/s)
K_BOLTZMANN = 1.380649e-23  # Boltzmann constant (J/K)
T_NOISE = 290.0  # Standard noise temperature (K)


def db_to_linear(value_db):
    """Convert decibel (power) value to linear scale.

    Args:
        value_db: Value in decibels (dB).

    Returns:
        Equivalent linear-scale value.
    """
    return 10.0 ** (value_db / 10.0)


def linear_to_db(value_linear):
    """Convert linear-scale value to decibels (power).

    Args:
        value_linear: Value in linear scale (must be > 0).

    Returns:
        Equivalent value in decibels (dB).
    """
    return 10.0 * torch.log10(value_linear)


def amplitude_to_db(amplitude):
    """Convert amplitude (voltage) to decibels.

    Args:
        amplitude: Amplitude value (must be > 0).

    Returns:
        Value in decibels (dB), computed as 20·log10(amplitude).
    """
    return 20.0 * torch.log10(amplitude)


def db_to_amplitude(value_db):
    """Convert decibels to amplitude (voltage) scale.

    Args:
        value_db: Value in decibels (dB).

    Returns:
        Equivalent amplitude value.
    """
    return 10.0 ** (value_db / 20.0)
