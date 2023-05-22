from abc import ABC, abstractmethod
from typing import List

from satellite_determination.custom_dataclasses.overhead_window import OverheadWindow


class EventFinder(ABC):
    @abstractmethod
    def get_overhead_windows(self) -> List[OverheadWindow]:
        pass

    @abstractmethod
    def get_overhead_windows_slew(self) -> List[OverheadWindow]:
        pass
