from typing import Any, Dict, Optional


class bidict(dict):
    """
    A bidirectional dictionary implementation.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the bidict by calling the parent class's constructor
        and creates a reverse dictionary for efficient reverse lookups.
        """
        super().__init__(*args, **kwargs)
        self.reverse_dict: Dict[Any, Any] = {}
        for k, v in self.items():
            if v in self.reverse_dict:
                raise ValueError(
                    f"Duplicate value detected during initialization: {v}")
            self.reverse_dict[v] = k

    def __getitem__(self, key: Any) -> Any:
        """
        Overrides the __getitem__ method to allow accessing values
        by key as well as keys by value.
        """
        if key in self:
            return super().__getitem__(key)
        return self.reverse_dict[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Overrides the __setitem__ method to allow setting key-value pairs
        and updating the reverse dictionary accordingly.
        """
        super().__setitem__(key, value)
        self.reverse_dict[value] = key

    def __delitem__(self, key: Any) -> None:
        """
        Overrides the __delitem__ method to allow deleting key-value pairs
        and updating the reverse dictionary accordingly.
        """
        value = self[key]
        super().__delitem__(key)
        del self.reverse_dict[value]

    def __hash__(self) -> int:
        """
        Overrides the __hash__ method to allow using the bidict as a key
        in hash-based collections.
        """
        return hash(frozenset(self.items()))

    def getr(self, value: Any, default: Optional[Any] = None) -> Optional[Any]:
        """
        Returns the key associated with the given value, or a default
        value if the given value is not present in the reverse dictionary.
        """
        return self.reverse_dict.get(value, default)
