from datetime import datetime
from typing import List, Optional, Union

from .. import dataclasses
from .abstract import AbstractParser


class BaseParser(AbstractParser):
    def _find_domain(self) -> Optional[str]:
        value = self._find_by_keywords(["Domain Name", "domain"])
        if value is not None:
            value = value.lower()

        return value

    def _find_registered_at(self) -> Optional[Union[str, datetime]]:
        return self._find_datetime_by_keywords(
            [
                "Creation Date",
                "registered",
                "created",
                "activated",
                "Registration Time",
                "Registered Date",
                "Registration Date",
                "Record created on",
                "Created On",
                "registered on",
            ],
            is_line_start_sensitive=False,
        )

    def _find_updated_at(self) -> Optional[Union[str, datetime]]:
        return self._find_datetime_by_keywords(
            [
                "Updated Date",
                "registered",
                "updated",
                "changed",
                "modified",
                "Last Updated On",
                "Last Updated Date",
                "domain_datelastmodified",
                "Last Update",
            ],
            is_line_start_sensitive=False,
        )

    def _find_expires_at(self) -> Optional[Union[str, datetime]]:
        return self._find_datetime_by_keywords(
            [
                "Expiry Date",
                "Expiration Date",
                "expire",
                "expires",
                "Expires On",
                "Expiration Time",
                "Renewal Date",
                "Record expires on",
                "paid-till",
                "expire-date",
                "domain_datebilleduntil",
                "Valid Until",
                "validity",
            ],
            is_line_start_sensitive=False,
        )

    def _find_registrar(self) -> Optional[str]:
        return self._find_by_keywords(
            [
                "Registrar",
                "Registrar Name",
                "Sponsoring Registrar",
                "registrar-name",
                "Registration Service Provider",
                "Domain Support",
                "Sponsoring Registrar Organization",
                "Registration Service Provider",
                "Account Name",
            ]
        )

    def _find_abuse_email(self) -> Optional[str]:
        return self._find_by_keywords(["Registrar Abuse Contact Email", "AC E-Mail"])

    def _find_abuse_telephone(self) -> Optional[str]:
        return self._find_by_keywords(
            ["Registrar Abuse Contact Phone", "AC Phone Number"]
        )

    def _find_abuse(self) -> dataclasses.Abuse:
        return dataclasses.Abuse(
            email=self._find_abuse_email(), telephone=self._find_abuse_telephone()
        )

    def _find_registrant_name(self) -> Optional[str]:
        return self._find_by_keywords(
            [
                "Registrant Name",
                "Registrant",
                "Registrant Contact Name",
                "Person",
                "registrant_contact_name",
                "Domain Holder",
                "personname",
                "responsible",
            ]
        )

    def _find_registrant_email(self) -> Optional[str]:
        return self._find_by_keywords(["Registrant Email", "Registrant Contact Email"])

    def _find_registrant_telephone(self) -> Optional[str]:
        return self._find_by_keywords(
            [
                "Registrant Phone",
            ]
        )

    def _find_registrant_organization(self) -> Optional[str]:
        return self._find_by_keywords(
            [
                "Registrant Organization",
                "org",
                "org-name",
                "Registrant Contact Organisation",
            ]
        )

    def _find_registrant(self) -> dataclasses.Registrant:
        return dataclasses.Registrant(
            name=self._find_registrant_name(),
            email=self._find_registrant_email(),
            telephone=self._find_registrant_telephone(),
            organization=self._find_registrant_organization(),
        )

    def _find_admin_name(self) -> Optional[str]:
        return self._find_by_keywords(
            [
                "Admin Name",
            ]
        )

    def _find_admin_email(self) -> Optional[str]:
        return self._find_by_keywords(
            [
                "Admin Email",
            ]
        )

    def _find_admin_telephone(self) -> Optional[str]:
        return self._find_by_keywords(
            [
                "Admin Phone",
            ]
        )

    def _find_admin_organization(self) -> Optional[str]:
        return self._find_by_keywords(
            [
                "Admin Organization",
            ]
        )

    def _find_admin(self) -> dataclasses.Admin:
        return dataclasses.Admin(
            name=self._find_admin_name(),
            email=self._find_admin_email(),
            telephone=self._find_admin_telephone(),
            organization=self._find_admin_organization(),
        )

    def _find_tech_name(self) -> Optional[str]:
        return self._find_by_keywords(["Tech Name", "Tech Contact Name"])

    def _find_tech_email(self) -> Optional[str]:
        return self._find_by_keywords(["Tech Email", "Tech Contact Email"])

    def _find_tech_telephone(self) -> Optional[str]:
        return self._find_by_keywords(
            [
                "Tech Phone",
            ]
        )

    def _find_tech_organization(self) -> Optional[str]:
        return self._find_by_keywords(
            ["Tech Organization", "Tech Contact Organisation"]
        )

    def _find_tech(self) -> dataclasses.Tech:
        return dataclasses.Tech(
            name=self._find_tech_name(),
            email=self._find_tech_email(),
            telephone=self._find_tech_telephone(),
            organization=self._find_tech_organization(),
        )

    def _find_statuses(self) -> List[str]:
        return self._find_all_by_keywords(["Domain Status", "domaintype"])

    def _find_name_servers(self) -> List[str]:
        values = self._find_all_by_keywords(["Name server", "Nserver", "Host Name"])
        return [value.lower() for value in values]
