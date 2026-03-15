import torch 
from dataclasses import dataclass


@dataclass
class ScatteringCenter:
    """A single scattering center representing a target at a given instant.
    
    Attributes:
        range_m: Instantaneous range from the radar (m).
        velocity_mps: Instantaneous radial velocity (m/s, positive = receding).
        rcs_linear: Radar cross-section in linear scale (m²).
        rcs_dbsm: Radar cross-section in dBsm scale (dB re m²).
    """
    range_m: float
    velocity_mps: float
    rcs_linear: float
    rcs_dbsm: float


class PointTarget:
    """Represents a single point target with constant radial velocity.
    
    The instantaneous range evolves as:
        R(t) = R₀ + v · t
    
    where R₀ is the initial range and v is the radial velocity.
    """
    
    def __init__(self, range_m: float, velocity_mps: float, rcs_dbsm: float, target_id: int = 0):
        """
        Initialize a point target.
        
        Args:
            range_m: Initial range from radar (meters).
            velocity_mps: Radial velocity (m/s, positive = moving away).
            rcs_dbsm: Radar cross-section (dBsm = dB re m²).
            target_id: Unique identifier for this target.
        """
        self.range_m = range_m
        self.velocity_mps = velocity_mps
        self.rcs_dbsm = rcs_dbsm
        self.target_id = target_id
        
        # Convert RCS from dBsm to linear scale
        self.rcs_linear = 10 ** (rcs_dbsm / 10)
    
    
    def get_instantaneous_range(self, time_s):
        """
        Compute the instantaneous range at a given time.
        Args:
            time_s: Simulation time (seconds).

        Return:
            Instantaneous range (meters).
        """
        return self.range_m + self.velocity_mps * time_s
    
    
    def get_scattering_center(self, time_s):
        """
        Return the scattering center at a given time.
        Args:
            time_s: Simulation time (seconds).

        Return:
            ScatteringCenter object with current target parameters.
        """
        current_range = self.get_instantaneous_range(time_s)
        return ScatteringCenter(
            range_m=current_range,
            velocity_mps=self.velocity_mps,
            rcs_linear=self.rcs_linear,
            rcs_dbsm=self.rcs_dbsm
        )
    
    
    def get_doppler_shift(self, fc, c=3e8):
        """
        Compute the Doppler frequency shift.
        Args:
            fc: Carrier frequency (Hz).
            c: Speed of light (m/s).

        Return:
            Doppler frequency shift (Hz): f_d = 2 * f_c * v / c
        """

        return 2 * fc * self.velocity_mps / c
    
    
    def __repr__(self) -> str:
        """String representation of the target."""
        return (f"PointTarget(id={self.target_id}, "
                f"range={self.range_m:.1f}m, "
                f"velocity={self.velocity_mps:.1f}m/s, "
                f"RCS={self.rcs_dbsm:.1f}dBsm)")
    


class PointTargets:
    """Collection of point targets loaded from configuration parameters."""
    
    def __init__(self, target_parameters):
        """
        Initialize collection of point targets from config.
        Args:
            target_parameters: Target parameters dictionary from config.yaml
        """
        self.targets = []
        
        if target_parameters is not None:
            self._load_from_config(target_parameters)
    
    
    def _load_from_config(self, target_parameters, t=0.0):
        """
        Load targets from configuration dictionary.
        
        Args:
            target_parameters: Configuration dictionary with 'point_target' key.
        """
        targets_list = target_parameters.get('point_target', [])
        for idx, target_data in enumerate(targets_list):
            target = PointTarget(
                range_m=target_data.get('range_m', t), 
                velocity_mps=target_data.get('velocity_mps', t),
                rcs_dbsm=target_data.get('rcs_dbsm', t),
                target_id=idx
            )
            self.targets.append(target)
    
    
    def add_target(self, range_m, velocity_mps, rcs_dbsm):
        """
        Add a new target to the collection.
        
        Args:
            range_m: Initial range (meters).
            velocity_mps: Radial velocity (m/s).
            rcs_dbsm: Radar cross-section (dBsm).
        """
        target_id = len(self.targets)
        target = PointTarget(range_m, velocity_mps, rcs_dbsm, target_id)
        self.targets.append(target)
        return
    
    
    def remove_target(self, target_id):
        """
        Remove a target by its ID.
        Args:
            target_id: ID of the target to remove.
        """
        self.targets = [t for t in self.targets if t.target_id != target_id]
        return
    
    
    def get_target(self, target_id):
        """
        Get a specific target by ID.
        Args:
            target_id: Target ID.
            
        Return:
            PointTarget object or None if not found.
        """
        for target in self.targets:
            if target.target_id == target_id:
                return target
        return None
    
    
    def get_ranges(self, time_s=0.0):
        """
        Get ranges of all targets as tensor.
        Args:
            time_s: Simulation time for range calculation (seconds).
            
        Returns:
            Tensor of shape (N,) with ranges in meters.
        """
        ranges = [t.get_instantaneous_range(time_s) for t in self.targets]
        return torch.tensor(ranges, dtype=torch.float32) if ranges else torch.tensor([], dtype=torch.float32)
    
    
    def get_velocities(self):
        """
        Get velocities of all targets as tensor.
        
        Returns:
            Tensor of shape (N,) with velocities in m/s.
        """
        velocities = [t.velocity_mps for t in self.targets]
        return torch.tensor(velocities, dtype=torch.float32) if velocities else torch.tensor([], dtype=torch.float32)
    
    
    def get_rcs_linear(self):
        """
        Get RCS values in linear scale of all targets as tensor.
        
        Returns:
            Tensor of shape (N,) with RCS in m².
        """
        rcs = [t.rcs_linear for t in self.targets]
        return torch.tensor(rcs, dtype=torch.float32) if rcs else torch.tensor([], dtype=torch.float32)
    
    
    def get_rcs_dbsm(self):
        """
        Get RCS values in dBsm of all targets as tensor.
        
        Returns:
            Tensor of shape (N,) with RCS in dBsm.
        """
        rcs = [t.rcs_dbsm for t in self.targets]
        return torch.tensor(rcs, dtype=torch.float32) if rcs else torch.tensor([], dtype=torch.float32)
    
    
    def get_doppler_shifts(self, fc, c=3e8):
        """
        Get Doppler frequency shifts for all targets.
        
        Args:
            fc: Carrier frequency (Hz).
            c: Speed of light (m/s).
            
        Returns:
            Tensor of shape (N,) with Doppler shifts in Hz.
        """
        doppler_shifts = [t.get_doppler_shift(fc, c) for t in self.targets]
        return torch.tensor(doppler_shifts, dtype=torch.float32) if doppler_shifts else torch.tensor([], dtype=torch.float32)
    
    
    def get_scattering_centers(self, time_s):
        """
        Get scattering centers for all targets at given time.
        Args:
            time_s: Simulation time (seconds).
            
        Returns:
            List of ScatteringCenter objects.
        """
        return [t.get_scattering_center(time_s) for t in self.targets]
    
    
    def num_targets(self):
        """Get the number of targets."""
        return len(self.targets)
    
    
    def __iter__(self):
        """Enable iteration over targets."""
        return iter(self.targets)
    
    
    def __getitem__(self, idx: int):
        """Enable indexing access to targets."""
        return self.targets[idx]