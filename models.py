"""
This module defines two primary classes, NearEarthObject and CloseApproach.

NearEarthObject encapsulates the information about a single NEO (Near-Earth Object),
while CloseApproach encapsulates details of the NEO's close approach to Earth.
The module also imports helper functions `cd_to_datetime` and `datetime_to_str` for date-time conversions.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """Represent a near-Earth object with its characteristics.

    Each NEO has a unique primary designation, an optional name, diameter,
    and a flag to denote if it's hazardous.
    """

    def __init__(self, **info):
        """
        Initialize a new NearEarthObject.

        :param info: A dictionary containing data about the NEO.
        """
        self.designation = info.get('pdes', '')
        self.name = info.get('name', None)
        try:
            self.diameter = float(info.get('diameter', 'nan'))
        except ValueError:
            # Defaulting to NaN (Not a Number) if conversion fails
            self.diameter = float('nan')
        self.hazardous = bool(info.get('pha', False))
        self.approaches = []

    @property
    def fullname(self):
        """Return the full name of the NEO, combining its designation and optional name."""
        if self.name:
            return f"{self.designation} ({self.name})"
        return self.designation

    def __str__(self):
        """Return a string representation of the NEO."""
        return f"Near-Earth Object: {self.fullname}, Diameter: {self.diameter} km, Hazardous: {self.hazardous}"

    def __repr__(self):
        """Return the official string representation of the NEO."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """Represent a close approach of an NEO to Earth.

    A CloseApproach captures the time of approach, its distance to Earth,
    the relative velocity of the NEO, and a reference to the associated NEO.
    """

    def __init__(self, **info):
        """
        Initialize a new CloseApproach.

        :param info: A dictionary containing data about the close approach.
        """
        self._designation = info.get('des', '')  # Designation of the NEO
        self.time = cd_to_datetime(info.get('cd', ''))  # Use the 'cd_to_datetime' function
        try:
            self.distance = float(info.get('dist', 0.0))  # Convert to float
        except ValueError:
            # Defaulting to 0.0 if conversion fails
            self.distance = 0.0
        self.velocity = float(info.get('v_rel', 0.0))  # Convert to float
        self.neo = None  # Reference to the associated NEO, to be set later

        self.velocity = float(info.get('v_rel', 0.0))  # Convert to float
        self.neo = None  # Reference to the associated NEO, to be set later

    @property
    def time_str(self):
        """Return the approach time in a human-readable format."""
        return datetime_to_str(self.time)

    @property
    def full_description(self):
        """Return a full description of the close approach, combining time and NEO's full name."""
        time_str = self.time_str
        full_name = f"NEO {self.neo.designation} ({self.neo.name})" if self.neo.name else f"NEO {self.neo.designation}"
        return f"{time_str} - {full_name}"

    def __str__(self):
        """Return a string representation of the close approach."""
        return f"Close Approach: NEO {self._designation}, Time: {self.time_str}, " \
               f"Distance: {self.distance} AU, Velocity: {self.velocity} km/s"

    def __repr__(self):
        """Return the official string representation of the close approach."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
