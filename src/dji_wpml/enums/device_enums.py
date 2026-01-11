from enum import Enum

class DeviceDomainEnum(Enum):
    DRONE = 0
    PAYLOAD = 1
    REMOTER_CONTROL = 2
    DOCK = 3

    @property
    def domain(self) -> int:
        """Equivalent to Java's getDomain() @JsonValue"""
        return self.value

    @classmethod
    def find(cls, domain_id: int):
        """Equivalent to Java's find(int domain) @JsonCreator"""
        for member in cls:
            if member.value == domain_id:
                return member
        # Custom error handling to match CloudSDKException
        raise ValueError(f"DeviceDomainEnum not found for domain ID: {domain_id}")

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}({self.value})"

class DeviceTypeEnum(Enum):
    M350 = 89
    M300 = 60
    M30_OR_M3T_CAMERA = 67
    M3E = 77
    Z30 = 20
    XT2 = 26
    FPV = 39
    XTS = 41
    H20 = 42
    H20T = 43
    P1 = 50
    M30_CAMERA = 52
    M30T_CAMERA = 53
    H20N = 61
    DOCK_CAMERA = 165
    L1 = 90742
    M3E_CAMERA = 66
    M3M_CAMERA = 68
    RC = 56
    RC_PLUS = 119
    RC_PRO = 144
    DOCK = 1
    DOCK2 = 2
    DOCK3 = 3
    M3D = 90
    M3TD = 91
    M3D_CAMERA = 80
    M3TD_CAMERA = 81
    M4E = 99        # DJI Matrice 4 Series (E)
    M4T = 99        # DJI Matrice 4 Series (T)
    M4D = 100       # Matrice 4D
    M4TD = 101      # Matrice 4TD
    M4E_CAMERA = 99 # Payload ID for M4 series
    M4T_CAMERA = 99 # Payload ID for M4 series
    M4D_CAMERA = 98
    M4TD_CAMERA = 99
    RC_PLUS_2 = 174 # RC for M4 Series

    @property
    def type(self) -> int:
        """Equivalent to Java's getType() @JsonValue"""
        return self.value

    @classmethod
    def find(cls, type_id: int):
        """Equivalent to Java's find(int type) @JsonCreator"""
        for member in cls:
            if member.value == type_id:
                return member
        # In Python, we usually raise a ValueError or a custom Exception 
        # to match CloudSDKException behavior.
        raise ValueError(f"DeviceTypeEnum not found for type: {type_id}")

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}({self.value})"

class DeviceSubTypeEnum(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    _65535 = 65535

    @property
    def sub_type(self) -> int:
        """Equivalent to Java's getSubType() @JsonValue"""
        return self.value

    @classmethod
    def find(cls, sub_type_id: int):
        """Equivalent to Java's find(int subType) @JsonCreator"""
        for member in cls:
            if member.value == sub_type_id:
                return member
        raise ValueError(f"DeviceSubTypeEnum not found for sub-type: {sub_type_id}")

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}({self.value})"
    
class DeviceEnum(Enum):
    # Drones
    M350 = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M350, DeviceSubTypeEnum.ZERO)
    M300 = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M300, DeviceSubTypeEnum.ZERO)
    M30 = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M30_OR_M3T_CAMERA, DeviceSubTypeEnum.ZERO)
    M30T = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M30_OR_M3T_CAMERA, DeviceSubTypeEnum.ONE)
    M3E = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M3E, DeviceSubTypeEnum.ZERO)
    M3T = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M3E, DeviceSubTypeEnum.ONE)
    M3M = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M3E, DeviceSubTypeEnum.TWO)
    M3D = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M3D, DeviceSubTypeEnum.ZERO)
    M3TD = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M3TD, DeviceSubTypeEnum.ONE)
    M4E = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M4E, DeviceSubTypeEnum.ZERO)
    M4T = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M4T, DeviceSubTypeEnum.ONE)
    M4D = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M4D, DeviceSubTypeEnum.ZERO)
    M4TD = (DeviceDomainEnum.DRONE, DeviceTypeEnum.M4TD, DeviceSubTypeEnum.ONE)
    
    # Payloads
    M3E_CAMERA = (DeviceDomainEnum.PAYLOAD, DeviceTypeEnum.M3E_CAMERA, DeviceSubTypeEnum.ZERO)
    M3T_CAMERA = (DeviceDomainEnum.PAYLOAD, DeviceTypeEnum.M30_OR_M3T_CAMERA, DeviceSubTypeEnum.ZERO)
    M4E_CAMERA = (DeviceDomainEnum.PAYLOAD, DeviceTypeEnum.M4E_CAMERA, DeviceSubTypeEnum.ZERO)
    M4T_CAMERA = (DeviceDomainEnum.PAYLOAD, DeviceTypeEnum.M4T_CAMERA, DeviceSubTypeEnum.ZERO)
    M3D_CAMERA = (DeviceDomainEnum.PAYLOAD, DeviceTypeEnum.M3D_CAMERA, DeviceSubTypeEnum.ZERO)
    M3TD_CAMERA = (DeviceDomainEnum.PAYLOAD, DeviceTypeEnum.M3TD_CAMERA, DeviceSubTypeEnum.ZERO)
    M4D_CAMERA = (DeviceDomainEnum.PAYLOAD, DeviceTypeEnum.M4D_CAMERA, DeviceSubTypeEnum.ZERO)
    M4TD_CAMERA = (DeviceDomainEnum.PAYLOAD, DeviceTypeEnum.M4TD_CAMERA, DeviceSubTypeEnum.ZERO)

    # Docks
    DOCK = (DeviceDomainEnum.DOCK, DeviceTypeEnum.DOCK, DeviceSubTypeEnum.ZERO)
    DOCK2 = (DeviceDomainEnum.DOCK, DeviceTypeEnum.DOCK2, DeviceSubTypeEnum.ZERO)
    DOCK3 = (DeviceDomainEnum.DOCK, DeviceTypeEnum.DOCK3, DeviceSubTypeEnum.ZERO)

    # RC
    RC_PLUS_2 = (DeviceDomainEnum.REMOTER_CONTROL, DeviceTypeEnum.RC_PLUS_2, DeviceSubTypeEnum.ZERO)

    def __init__(self, domain, device_type, sub_type):
        self._domain = domain
        self._device_type = device_type
        self._sub_type = sub_type

    # Getters
    @property
    def domain(self):
        return self._domain

    @property
    def type(self):
        return self._device_type

    @property
    def sub_type(self):
        return self._sub_type

    def get_device(self) -> str:
        """Equivalent to Java getDevice() @JsonValue"""
        return f"{self.domain.domain}-{self.type.type}-{self.sub_type.sub_type}"

    @classmethod
    def find_by_key(cls, key: str):
        """Equivalent to Java find(String key) @JsonCreator"""
        for member in cls:
            if member.get_device() == key:
                return member
        raise ValueError(f"DeviceEnum not found for key: {key}")

    @classmethod
    def find_by_values(cls, domain: int, device_type: int, sub_type: int):
        """Equivalent to Java find(int, int, int)"""
        for member in cls:
            if (member.domain.domain == domain and 
                member.type.type == device_type and 
                member.sub_type.sub_type == sub_type):
                return member
        raise ValueError(f"DeviceEnum not found for: {domain}-{device_type}-{sub_type}")
    



def get_device_enum(enum_value, sub_enum_value, domain_enum):
    # Uses the find logic we built earlier
    return DeviceEnum.find_by_values(
        domain=domain_enum.domain, 
        device_type=enum_value, 
        sub_type=sub_enum_value
    )