class NEODatabase:
    """A database of Near Earth Objects and their close approaches.

    The database encapsulates information about NEOs and can be queried to produce filtered lists
    of close approaches that match certain criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase` from provided NEOs and approaches.

        :param neos: A list of `NearEarthObject`s.
        :param approaches: A list of `CloseApproach` objects.
        """
        self._neos = neos
        self._approaches = approaches

        self._neos_by_designation = {neo.designation: neo for neo in self._neos}
        self._neos_by_name = {neo.name: neo for neo in self._neos if neo.name}

        self._link_neos_and_approaches()

    def _link_neos_and_approaches(self):
        """Link NEOs and close approaches.

        Populate the approaches attribute of each NEO with its associated close approaches.
        Also set the neo attribute of each close approach to its associated NEO.
        """
        for approach in self._approaches:
            neo = self._neos_by_designation.get(approach._designation)
            if neo:
                neo.approaches.append(approach)
                approach.neo = neo

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        :param designation: The primary designation of the NEO.
        :return: The `NearEarthObject` with the given primary designation, or `None`.
        """
        return self._neos_by_designation.get(designation)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        :param name: The name of the NEO.
        :return: The `NearEarthObject` with the given name, or `None`.
        """
        return self._neos_by_name.get(name)

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of `CloseApproach` objects.
        """
        # Applying filters to the list of approaches.
        filtered_approaches = self._apply_filters(filters)

        # Sorting the filtered approaches by time.
        sorted_approaches = sorted(filtered_approaches, key=lambda approach: approach.time)

        # Generating and yielding the sorted approaches.
        for approach in sorted_approaches:
            yield approach

    def _apply_filters(self, filters):
        """Apply a collection of filters to the database's close approaches.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A list of `CloseApproach` objects.
        """
        filtered_approaches = self._approaches

        for filter_func in filters:
            filtered_approaches = filter(filter_func, filtered_approaches)

        return filtered_approaches
