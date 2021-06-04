from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Union

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Contact:
    organization: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    telephone: Optional[str] = None


@dataclass_json
@dataclass
class Tech(Contact):
    pass


@dataclass_json
@dataclass
class Registrant(Contact):
    pass


@dataclass_json
@dataclass
class Admin(Contact):
    pass


@dataclass_json
@dataclass
class Abuse:
    email: Optional[str] = None
    telephone: Optional[str] = None


@dataclass_json
@dataclass
class WhoisRecord:
    raw_text: str

    registrant: Registrant
    admin: Admin
    tech: Tech
    abuse: Abuse

    statuses: List[str] = field(default_factory=list)
    name_servers: List[str] = field(default_factory=list)

    domain: Optional[str] = None
    registrar: Optional[str] = None

    expires_at: Optional[Union[datetime, str]] = None
    registered_at: Optional[Union[datetime, str]] = None
    updated_at: Optional[Union[datetime, str]] = None
