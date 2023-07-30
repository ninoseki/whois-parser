from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union


@dataclass
class Contact:
    organization: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    telephone: Optional[str] = None


@dataclass
class Tech(Contact):
    pass


@dataclass
class Registrant(Contact):
    pass


@dataclass
class Admin(Contact):
    pass


@dataclass
class Abuse:
    email: Optional[str] = None
    telephone: Optional[str] = None


@dataclass
class WhoisRecord:
    raw_text: str

    registrant: Registrant
    admin: Admin
    tech: Tech
    abuse: Abuse

    statuses: list[str] = field(default_factory=list)
    name_servers: list[str] = field(default_factory=list)

    domain: Optional[str] = None
    registrar: Optional[str] = None

    expires_at: Optional[Union[datetime, str]] = None
    registered_at: Optional[Union[datetime, str]] = None
    updated_at: Optional[Union[datetime, str]] = None

    is_rate_limited: bool = False
