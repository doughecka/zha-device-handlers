"""Module for Sengled quirks implementations."""
import asyncio
import binascii
import logging

from zigpy.quirks import CustomCluster, CustomDevice
from zigpy import types as t
from zigpy.zcl.clusters.general import Basic, PowerConfiguration
import zigpy.zcl.foundation as foundation

from zhaquirks import Bus, LocalDataCluster

SENGLED_ATTRIBUTE = 0x0100
_LOGGER = logging.getLogger(__name__)


class SengledCustomDevice(CustomDevice):
    """Custom device representing Sengled devices."""

    def __init__(self, *args, **kwargs):
        """Init."""
        
        super().__init__(*args, **kwargs)


class BasicCluster(CustomCluster, Basic):
    """Sengled basic cluster implementation."""

    cluster_id = Basic.cluster_id

    def deserialize(self, tsn, frame_type, is_reply, command_id, data):
        """Deserialize cluster data."""
        try:
            return super().deserialize(tsn, frame_type, is_reply, command_id,
                                       data)
        except ValueError:
            msg = "ValueError exception for: tsn=%s, frame_type=%s, is_repy=%s"
            msg += " cmd_id=%s, data=%s"
            self.debug(msg, tsn, frame_type, is_reply, command_id,
                       binascii.hexlify(data))
            newdata = b''
            while data:
                try:
                    attr, data = foundation.Attribute.deserialize(data)
                except ValueError:
                    attr_id, data = t.uint16_t.deserialize(data)
                    if attr_id not in (SENGLED_ATTRIBUTE):
                        raise
                    attr_type, data = t.uint8_t.deserialize(data)
                    val_len, data = t.uint8_t.deserialize(data)
                    val_len = t.uint8_t(val_len - 1)
                    val, data = data[:val_len], data[val_len:]
                    newdata += attr_id.serialize()
                    newdata += attr_type.serialize()
                    newdata += val_len.serialize() + val
                    continue
                newdata += attr.serialize()
            if frame_type != 1 and command_id == 0x0a:
                self.debug("new data: %s", binascii.hexlify(newdata))
                return super().deserialize(
                    tsn, frame_type, is_reply, command_id, newdata
                )
            raise

    def _update_attribute(self, attrid, value):
        if attrid == SENGLED_ATTRIBUTE :
            super()._update_attribute(attrid, value.raw)
        else:
            super()._update_attribute(attrid, value)
            return

        _LOGGER.debug(
            "%s - Attribute report. attribute_id: [%s] value: [%s]",
            self.endpoint.device.ieee,
            attrid,
            attributes
        )
