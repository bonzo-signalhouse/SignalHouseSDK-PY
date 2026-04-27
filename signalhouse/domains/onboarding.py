"""Onboarding domain for the SignalHouse SDK (staff-only)."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class OnboardingAdmin:
    """Admin-only onboarding operations (SignalHouse staff)."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def get_onboardings(
        self,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get all onboarding records (one per group). Staff-only.

        Args:
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with a list of onboarding records.
        """
        return self._sdk._request(
            "/group/onboarding",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_onboarding(
        self,
        group_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a single onboarding record by group ID. Staff-only.

        Args:
            group_id: The ID of the group whose onboarding record to retrieve.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If group_id is missing.
        """
        self._sdk._require({"groupId": group_id})
        safe_group_id = quote(str(group_id), safe="")
        return self._sdk._request(
            f"/group/onboarding/{safe_group_id}",
            method="GET",
            token=token,
            headers=headers,
        )


class Onboarding:
    """Onboarding domain. Admin namespace only (staff-only data)."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk
        self.admin: OnboardingAdmin | None = None
        if sdk.enable_admin:
            self.admin = OnboardingAdmin(sdk)
