import operator
import itertools


class UnsupportedCriterionError(NotImplementedError):
    """Raise when a filter criterion is unsupported."""


class AttributeFilter:
    """Filter on comparable attributes of close approaches and attached NEOs.

    Represents search criteria comparing a close approach's attribute or its
    attached NEO's attribute to a reference value. Functions as a callable
    predicate for whether a CloseApproach object satisfies the encoded criterion.
    """

    def __init__(self, op, value):
        """Initialize with a comparator operator and a reference value."""
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Check if the approach satisfies the criterion."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get the desired attribute from approach. To be overridden by subclasses."""
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


class DateFilter(AttributeFilter):
    """Filter close approaches based on their approach date."""

    @classmethod
    def get(cls, approach):
        return approach.time.date()


class DistanceFilter(AttributeFilter):
    """Filter close approaches based on their approach distance."""

    @classmethod
    def get(cls, approach):
        return approach.distance


class VelocityFilter(AttributeFilter):
    """Filter close approaches based on their relative velocity."""

    @classmethod
    def get(cls, approach):
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """Filter close approaches based on the diameter of their NEO."""

    @classmethod
    def get(cls, approach):
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    """Filter close approaches based on whether their NEO is hazardous."""

    @classmethod
    def get(cls, approach):
        return approach.neo.hazardous


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create filters for querying close approaches.

    Based on provided criteria, return a collection of filters that determine
    whether a close approach or its NEO match the criteria.
    """

    filters = []

    # Adding filters to the list based on the non-None criteria provided.
    # For each criterion, creating an appropriate AttributeFilter and add to the filters list.
    if date is not None:
        filters.append(DateFilter(operator.eq, date))
    if start_date is not None:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date is not None:
        filters.append(DateFilter(operator.le, end_date))
    if distance_min is not None:
        filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max is not None:
        filters.append(DistanceFilter(operator.le, distance_max))
    if velocity_min is not None:
        filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max is not None:
        filters.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min is not None:
        filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max is not None:
        filters.append(DiameterFilter(operator.le, diameter_max))
    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, hazardous))

    # Return the filters as a tuple.
    return tuple(filters)


def limit(iterator, n=None):
    """Limit the number of items produced by an iterator.

    If n is None or <= 0, the iterator is unchanged. Otherwise, at most n items are produced.
    """
    if n is None or n <= 0:
        return iterator
    else:
        return itertools.islice(iterator, (None if n == 0 else n))
