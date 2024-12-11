from dataclasses import dataclass

@dataclass
class BusinessUnitCredentials:
    grant_type: str
    client_id: str
    client_secret: str

@dataclass
class BusinessUnit:
    name: str
    baseURL: str
    credentials: BusinessUnitCredentials
    data_extensions: list[str]
