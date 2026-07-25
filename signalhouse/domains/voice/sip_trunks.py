"""SIP Trunks — peer-to-peer SIP connections to a customer PBX or carrier.

Routes are mounted under /voice/sip-trunks on the voice-backend service.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ...client import SignalHouseSDK


class SipTrunks:
    """SIP trunk management. Accessed via ``sdk.voice.sip_trunks``."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def list(
        self,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """List all SIP trunks for the current account. ``GET /voice/sip-trunks``."""
        return self._sdk._request(
            "/voice/sip-trunks", method="GET", token=token, headers=headers,
        )

    def get(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a single SIP trunk by ID. ``GET /voice/sip-trunks/:id``."""
        self._sdk._require({"id": id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-trunks/{safe_id}", method="GET", token=token, headers=headers,
        )

    def create(
        self,
        trunk_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a SIP trunk. ``POST /voice/sip-trunks``.

        ``trunk_data`` keys: ``name``, ``region``, ``connectionType``
        (``"IP_AUTH"`` or ``"REGISTRATION"``), optional ``allowedIps``,
        ``transport``, ``maxSpendPerMinute``, ``destinationHosts``, ``sourceHosts``.
        Registration trunks return a one-time password on the response.
        """
        self._sdk._require({"trunkData": trunk_data})
        return self._sdk._request(
            "/voice/sip-trunks", method="POST", body=trunk_data, token=token, headers=headers,
        )

    def update(
        self,
        id: str,
        update_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update a SIP trunk. ``PATCH /voice/sip-trunks/:id``."""
        self._sdk._require({"id": id, "updateData": update_data})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-trunks/{safe_id}", method="PATCH", body=update_data, token=token, headers=headers,
        )

    def delete(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete a SIP trunk. ``DELETE /voice/sip-trunks/:id``."""
        self._sdk._require({"id": id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-trunks/{safe_id}", method="DELETE", token=token, headers=headers,
        )

    def toggle_active(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Toggle a trunk's active/inactive status. ``POST /voice/sip-trunks/:id/toggle-active``."""
        self._sdk._require({"id": id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-trunks/{safe_id}/toggle-active", method="POST", token=token, headers=headers,
        )

    def regenerate_password(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Regenerate the SIP password for a REGISTRATION-type trunk.

        Returns ``{ "password": "..." }``. The old password stops working immediately.
        ``POST /voice/sip-trunks/:id/regenerate-password``.
        """
        self._sdk._require({"id": id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-trunks/{safe_id}/regenerate-password", method="POST", token=token, headers=headers,
        )

    def assign_numbers(
        self,
        id: str,
        phone_numbers: list[str],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Assign phone numbers to a SIP trunk for outbound caller ID / inbound routing.

        Returns ``{ "assigned": [...], "skipped": [...] }``.
        ``POST /voice/sip-trunks/:id/assign-numbers``.
        """
        self._sdk._require({"id": id, "phoneNumbers": phone_numbers})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-trunks/{safe_id}/assign-numbers",
            method="POST",
            body={"phoneNumbers": phone_numbers},
            token=token,
            headers=headers,
        )

    def unassign_numbers(
        self,
        id: str,
        phone_numbers: list[str],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Unassign phone numbers from a SIP trunk.

        Returns ``{ "unassigned": [...] }``.
        ``POST /voice/sip-trunks/:id/unassign-numbers``.
        """
        self._sdk._require({"id": id, "phoneNumbers": phone_numbers})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-trunks/{safe_id}/unassign-numbers",
            method="POST",
            body={"phoneNumbers": phone_numbers},
            token=token,
            headers=headers,
        )

    def get_pops(
        self,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """List available SIP POPs (Points of Presence). ``GET /voice/sip-trunks/pops``."""
        return self._sdk._request(
            "/voice/sip-trunks/pops", method="GET", token=token, headers=headers,
        )
