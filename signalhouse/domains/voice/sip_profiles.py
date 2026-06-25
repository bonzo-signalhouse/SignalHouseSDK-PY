"""SIP Profiles / endpoints — single registerable SIP UAs.

A SIP profile represents one device (desk phone, softphone, SIP app) that
registers to Signal House with a username + password. Distinct from a SIP
trunk, which is a peer-to-peer link to a PBX or carrier.

Routes are mounted under /voice/sip-profiles on the voice-backend service.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ...client import SignalHouseSDK


class SipProfiles:
    """SIP profile / endpoint management. Accessed via ``sdk.voice.sip_profiles``."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def list(
        self,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """List all SIP profiles. ``GET /voice/sip-profiles``."""
        return self._sdk._request(
            "/voice/sip-profiles", method="GET", token=token, headers=headers,
        )

    def get(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a single SIP profile by ID. Response does NOT include the password —
        use :py:meth:`get_password` to retrieve it. ``GET /voice/sip-profiles/:id``."""
        self._sdk._require({"id": id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-profiles/{safe_id}", method="GET", token=token, headers=headers,
        )

    def get_password(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Fetch the SIP password for this profile. Returns ``{ "password": "..." }``.
        ``GET /voice/sip-profiles/:id/password``."""
        self._sdk._require({"id": id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-profiles/{safe_id}/password", method="GET", token=token, headers=headers,
        )

    def get_transports(
        self,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """List valid SIP transports (UDP/TCP/TLS) with their address and port.
        ``GET /voice/sip-profiles/transports``."""
        return self._sdk._request(
            "/voice/sip-profiles/transports", method="GET", token=token, headers=headers,
        )

    def create(
        self,
        profile_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a SIP profile. ``POST /voice/sip-profiles``.

        ``profile_data`` keys: ``name`` (required), optional ``recordingAllowed``,
        ``transcriptionEnabled``, ``sentimentFlag``. The server generates the SIP
        username and password; the password is returned at the TOP LEVEL of the
        response (not nested in ``sipProfile``) and is the only chance to surface
        it without an explicit ``get_password`` call.
        """
        self._sdk._require({"profileData": profile_data})
        return self._sdk._request(
            "/voice/sip-profiles", method="POST", body=profile_data, token=token, headers=headers,
        )

    def update(
        self,
        id: str,
        update_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update a SIP profile. ``PATCH /voice/sip-profiles/:id``.

        To rotate the password, pass a new ``password`` value — there is no
        dedicated regenerate endpoint.
        """
        self._sdk._require({"id": id, "updateData": update_data})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-profiles/{safe_id}", method="PATCH", body=update_data, token=token, headers=headers,
        )

    def delete(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete a SIP profile. Unassigns any linked numbers as a side effect.
        ``DELETE /voice/sip-profiles/:id``."""
        self._sdk._require({"id": id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-profiles/{safe_id}", method="DELETE", token=token, headers=headers,
        )

    def assign_number(
        self,
        id: str,
        phone_number_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Assign a phone number to this SIP profile (routes inbound calls on
        that number to the endpoint). ``POST /voice/sip-profiles/:id/assign-number``."""
        self._sdk._require({"id": id, "phoneNumberId": phone_number_id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-profiles/{safe_id}/assign-number",
            method="POST",
            body={"phoneNumberId": phone_number_id},
            token=token,
            headers=headers,
        )

    def unassign_number(
        self,
        id: str,
        phone_number_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Unassign a phone number from this SIP profile.
        ``POST /voice/sip-profiles/:id/unassign-number``."""
        self._sdk._require({"id": id, "phoneNumberId": phone_number_id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/voice/sip-profiles/{safe_id}/unassign-number",
            method="POST",
            body={"phoneNumberId": phone_number_id},
            token=token,
            headers=headers,
        )
