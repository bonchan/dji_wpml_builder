
from dataclasses import dataclass, field

from dji_wpml.enums.general_enums import *

@dataclass
class PayloadParam:
    payload_position_index: int
    focus_mode: PayloadFocusMode
    metering_mode: PayloadMeteringMode
    dewarping_enable: bool
    return_mode: LiDARReturnMode
    sampling_rate: SamplingRate
    scanning_mode: ScanningMode
    model_coloring_enable: bool
    image_format: ImageFormat
