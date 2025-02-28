"""Device handler for centralite 3305."""
from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import Basic, Identify, Ota, PollControl
from zigpy.zcl.clusters.measurement import (
    OccupancySensing, TemperatureMeasurement)
from zigpy.zcl.clusters.security import IasZone

from zhaquirks.centralite import PowerConfigurationCluster

DIAGNOSTICS_CLUSTER_ID = 0x0B05  # decimal = 2821


class CentraLite3305S(CustomDevice):
    """Custom device representing centralite 3305."""

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=1026
        #  device_version=0
        #  input_clusters=[0, 1, 3, 1026, 1280, 32, 2821]
        #  output_clusters=[25]>
        'models_info': [
            ('CentraLite', '3305-S'),
            ('CentraLite', '3325-S'),
            ('CentraLite', '3305'),
            ('CentraLite', '3325'),
            ('CentraLite', '3326'),
            ('CentraLite', '3326-L'),
            ('CentraLite', '3328-G'),
            ('CentraLite', 'Motion Sensor-A')
        ],
        'endpoints': {
            1: {
                'profile_id': zha.PROFILE_ID,
                'device_type': zha.DeviceType.IAS_ZONE,
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfigurationCluster.cluster_id,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    IasZone.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID
                ],
                'output_clusters': [
                    Ota.cluster_id
                ],
            },
            #  <SimpleDescriptor endpoint=2 profile=260 device_type=263
            #  device_version=0
            #  input_clusters=[0, 1, 3, 1030, 2821]
            #  output_clusters=[3]>
            2: {
                'profile_id': zha.PROFILE_ID,
                'device_type': zha.DeviceType.OCCUPANCY_SENSOR,
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfigurationCluster.cluster_id,
                    Identify.cluster_id,
                    OccupancySensing.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID
                ],
                'output_clusters': [
                    Identify.cluster_id
                ],
            },
        }
    }

    replacement = {
        'endpoints': {
            1: {
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfigurationCluster,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    IasZone.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID
                ],
                'output_clusters': [
                    Ota.cluster_id
                ],
            },
            2: {
                'input_clusters': [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    OccupancySensing.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID
                ],
                'output_clusters': [
                    Identify.cluster_id
                ],
            }
        },
    }


class CentraLite3305S2(CentraLite3305S):
    """Custom device representing centralite 3305 with one endpoint."""

    signature = {
        'models_info': [
            ('CentraLite', '3305'),
        ],
        'endpoints': {
            1: {
                **CentraLite3305S.signature['endpoints'][1]
            }
        }
    }

    replacement = {
        'endpoints': {
            1: {
                **CentraLite3305S.replacement['endpoints'][1]
            }
        }
    }
