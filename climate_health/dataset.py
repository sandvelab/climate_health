from typing import Protocol, Union, Iterable, TypeVar, Generic

from climate_health.datatypes import Location
from climate_health.time_period.dataclasses import Period

spatial_index_type = Union[str, Location]
temporal_index_type = Union[Period, Iterable[Period], slice]

T = TypeVar('T')
class SpatioTemporalDataSet(Protocol, Generic[T]):
    dataclass = ...
    def get_locations(self, location: Iterable[Location])-> SpatioTemporalDataSet[T]:
        ...

    def get_data_for_location(self, location: Location) -> T
        ...
        
    def restrict_time_period(self, period_range: slice[Period])->SpatioTemporalDataSet[T]:
        ...
        
    # def __getitem__(self, index: spatial_index_type|Tuple[spatial_index_type, temporal_index_type] ) -> Union['SpatioTemporalDataSet', 'dataclass']:
    #     ...
