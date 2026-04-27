"""Numbers domain for the SignalHouse SDK."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class NumbersAdmin:
    """Admin-only number operations (SignalHouse staff)."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def change_porting_status(
        self,
        porting_id: str,
        status: str,
        description: str | None = None,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Change the status of a port-in request.

        Args:
            porting_id: The ID of the port-in request.
            status: The new status to set.
            description: Optional description for the status change.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If porting_id or status is missing.
        """
        self._sdk._require({"portingId": porting_id, "status": status})
        safe_porting_id = quote(str(porting_id), safe="")
        body: dict[str, Any] = {"status": status}
        if description is not None:
            body["description"] = description
        return self._sdk._request(
            f"/number/portin/{safe_porting_id}/status",
            method="PUT",
            body=body,
            token=token,
            headers=headers,
        )

    def approve_port_request(
        self,
        porting_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Approve a port-in request.

        Args:
            porting_id: The ID of the port-in request to approve.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If porting_id is missing.
        """
        self._sdk._require({"portingId": porting_id})
        safe_porting_id = quote(str(porting_id), safe="")
        return self._sdk._request(
            f"/number/portin/{safe_porting_id}/approve",
            method="POST",
            token=token,
            headers=headers,
        )


class Numbers:
    """Phone number management operations including purchase, assignment, transfer, and lookup."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk
        self.admin: NumbersAdmin | None = None
        if sdk.enable_admin:
            self.admin = NumbersAdmin(sdk)

    def get_phone_numbers(
        self,
        *,
        phone_number: str | None = None,
        campaign_id: str | None = None,
        brand_id: str | None = None,
        subgroup_id: str | None = None,
        group_id: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a list of phone numbers with optional filters.

        Args:
            phone_number: Filter by phone number (partial match).
            campaign_id: Filter by campaign ID.
            brand_id: Filter by brand ID.
            subgroup_id: Filter by subgroup ID.
            group_id: Filter by group ID.
            page: The page number for pagination (default: 1).
            limit: The number of items per page (default: 20).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({
            "phoneNumber": phone_number,
            "campaignId": campaign_id,
            "brandId": brand_id,
            "subgroupId": subgroup_id,
            "groupId": group_id,
            "page": page,
            "limit": limit,
        })
        return self._sdk._request(
            f"/number{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_available_phone_numbers(
        self,
        *,
        sms_enabled: bool | None = None,
        mms_enabled: bool | None = None,
        voice_enabled: bool | None = None,
        country: str | None = None,
        state: str | None = None,
        npa: str | None = None,
        nxx: str | None = None,
        phone_number: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a list of available phone numbers for purchase with optional filters.

        Args:
            sms_enabled: Filter for SMS enabled numbers.
            mms_enabled: Filter for MMS enabled numbers.
            voice_enabled: Filter for voice enabled numbers.
            country: Filter by country code (e.g., "US").
            state: Filter by state code (e.g., "CA").
            npa: Filter by NPA (area code).
            nxx: Filter by NXX (central office code).
            phone_number: Filter by phone number.
            limit: The number of items per page.
            page: The page number for pagination.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({
            "smsEnabled": sms_enabled,
            "mmsEnabled": mms_enabled,
            "voiceEnabled": voice_enabled,
            "country": country,
            "state": state,
            "npa": npa,
            "nxx": nxx,
            "phoneNumber": phone_number,
            "limit": limit,
            "page": page,
        })
        return self._sdk._request(
            f"/number/available{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def purchase_phone_number(
        self,
        phone_numbers: list[str],
        subgroup_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Purchase phone numbers and assign them to a subgroup.

        Each requested number is queued and processed independently. Per-number success or
        failure is delivered via ``NUMBER_PURCHASE_SUCCESSFUL`` / ``NUMBER_PURCHASE_FAILED``
        webhooks — not in this response.

        Args:
            phone_numbers: The list of phone numbers to purchase.
            subgroup_id: The ID of the subgroup to assign the purchased numbers to.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with a ``message`` field confirming the request was queued.

        Raises:
            SignalHouseValidationError: If phone_numbers or subgroup_id is missing.
        """
        self._sdk._require({"phoneNumbers": phone_numbers, "subgroupId": subgroup_id})
        return self._sdk._request(
            "/number",
            method="POST",
            body={"phoneNumbers": phone_numbers, "subgroupId": subgroup_id},
            token=token,
            headers=headers,
        )

    def update_phone_number(
        self,
        phone_number: str,
        update_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update an existing phone number's details (e.g., setting a friendly name).

        Args:
            phone_number: The phone number to update.
            update_data: The data to update for the phone number (e.g., friendlyName).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If phone_number or update_data is missing.
        """
        self._sdk._require({"phoneNumber": phone_number, "updateData": update_data})
        safe_phone_number = quote(str(phone_number), safe="")
        return self._sdk._request(
            f"/number/{safe_phone_number}",
            method="PUT",
            body=update_data,
            token=token,
            headers=headers,
        )

    def port_in_phone_number(
        self,
        number_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Submit a port-in request for one or more phone numbers from another provider.

        Args:
            number_data: The port-in request data including owner info, address, phone numbers, and signature.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with the created port-in request.

        Raises:
            SignalHouseValidationError: If number_data is missing.
        """
        self._sdk._require({"numberData": number_data})
        return self._sdk._request(
            "/number/portin",
            method="POST",
            body=number_data,
            token=token,
            headers=headers,
        )

    def get_port_requests(
        self,
        *,
        group_id: str | None = None,
        phone_number: str | None = None,
        status: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get port-in requests with optional filters.

        Signal House staff can view all requests; regular users see only their group's requests.

        Args:
            group_id: Filter by group ID.
            phone_number: Filter by phone number.
            status: Filter by status (PENDING, IN_PROGRESS, COMPLETED, REJECTED, CANCELLED).
            page: The page number for pagination (default: 1).
            limit: The number of items per page (default: 20).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with paginated port-in requests.
        """
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
            "phoneNumber": phone_number,
            "status": status,
            "page": page,
            "limit": limit,
        })
        return self._sdk._request(
            f"/number/portin{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_port_request_by_id(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a single port-in request by its ID.

        Args:
            id: The ID of the port-in request to retrieve.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with the port-in request.

        Raises:
            SignalHouseValidationError: If id is missing.
        """
        self._sdk._require({"id": id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/number/portin/{safe_id}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_porting_requests(
        self,
        porting_id: str | None = None,
        *,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get porting requests. If porting_id is provided, returns a single request; otherwise returns all.

        Args:
            porting_id: Optional ID of a specific port-in request. When provided, fetches that single request.
            page: The page number for pagination (only used when porting_id is not provided).
            limit: The number of items per page (only used when porting_id is not provided).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        if porting_id is not None:
            return self.get_port_request_by_id(id=porting_id, token=token, headers=headers)
        return self.get_port_requests(page=page, limit=limit, token=token, headers=headers)

    def assign_phone_number_to_campaign(
        self,
        campaign_id: str,
        phone_numbers: list[str],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Assign phone numbers to a campaign.

        Args:
            campaign_id: The ID of the campaign to assign phone numbers to.
            phone_numbers: The list of phone numbers to assign.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If campaign_id or phone_numbers is missing.
        """
        self._sdk._require({"campaignId": campaign_id, "phoneNumbers": phone_numbers})
        safe_campaign_id = quote(str(campaign_id), safe="")
        return self._sdk._request(
            f"/number/assign/{safe_campaign_id}",
            method="POST",
            body={"phoneNumbers": phone_numbers},
            token=token,
            headers=headers,
        )

    def unassign_phone_numbers_from_campaigns(
        self,
        phone_numbers: list[str],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Unassign phone numbers from any campaign they are currently assigned to.

        Args:
            phone_numbers: The list of phone numbers to unassign.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If phone_numbers is missing.
        """
        self._sdk._require({"phoneNumbers": phone_numbers})
        return self._sdk._request(
            "/number/unassign",
            method="POST",
            body={"phoneNumbers": phone_numbers},
            token=token,
            headers=headers,
        )

    def delete_phone_numbers(
        self,
        phone_numbers: list[str],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete (release) phone numbers. This operation is irreversible.

        The phone numbers will no longer be active but will still be visible with status "RELEASED".

        Args:
            phone_numbers: The list of phone numbers to delete.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If phone_numbers is missing.
        """
        self._sdk._require({"phoneNumbers": phone_numbers})
        return self._sdk._request(
            "/number",
            method="DELETE",
            body={"phoneNumbers": phone_numbers},
            token=token,
            headers=headers,
        )

    def deactivate_phone_numbers(
        self,
        phone_numbers: list[str],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Deactivate one or more phone numbers. Numbers must be in READY status.

        Deactivated numbers will not be able to send or receive messages but will
        remain assigned to their subgroup and campaign.

        Args:
            phone_numbers: The list of phone numbers to deactivate.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with an array of updated number objects.

        Raises:
            SignalHouseValidationError: If phone_numbers is missing.
        """
        self._sdk._require({"phoneNumbers": phone_numbers})
        return self._sdk._request(
            "/number/deactivate",
            method="POST",
            body={"phoneNumbers": phone_numbers},
            token=token,
            headers=headers,
        )

    def reactivate_phone_numbers(
        self,
        phone_numbers: list[str],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Reactivate one or more previously deactivated phone numbers.

        Numbers must be in DEACTIVATED status. Reactivated numbers will return to
        PENDING or IN_PROGRESS status depending on their campaign assignment.

        Args:
            phone_numbers: The list of phone numbers to reactivate.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with an array of updated number objects.

        Raises:
            SignalHouseValidationError: If phone_numbers is missing.
        """
        self._sdk._require({"phoneNumbers": phone_numbers})
        return self._sdk._request(
            "/number/reactivate",
            method="POST",
            body={"phoneNumbers": phone_numbers},
            token=token,
            headers=headers,
        )

    def transfer_phone_numbers(
        self,
        phone_numbers: list[str],
        new_subgroup_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Transfer unassigned phone numbers from one subgroup to another.

        Args:
            phone_numbers: The list of phone numbers to transfer.
            new_subgroup_id: The ID of the new subgroup to transfer the numbers to.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        self._sdk._require({"phoneNumbers": phone_numbers, "newSubgroupId": new_subgroup_id})
        return self._sdk._request(
            "/number/transfer",
            method="POST",
            body={"phoneNumbers": phone_numbers, "newSubgroupId": new_subgroup_id},
            token=token,
            headers=headers,
        )

    def search_npa_nxx(
        self,
        *,
        country: str | None = None,
        state: str | None = None,
        city: str | None = None,
        npa: str | None = None,
        nxx: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Search NPA/NXX lookup data with optional filters.

        At least one search parameter is required.
        Location filters (country, state, city) cannot be combined with NPA/NXX filters.

        Args:
            country: Filter by country code.
            state: Filter by state code (2 characters).
            city: Filter by city name (prefix match, case-insensitive; requires country and state).
            npa: Area code filter (1-3 digits; cannot combine with location filters).
            nxx: Central office code filter (1-3 digits; cannot combine with location filters).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({
            "country": country,
            "state": state,
            "city": city,
            "npa": npa,
            "nxx": nxx,
        })
        return self._sdk._request(
            f"/number/lookup{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def lookup_locations(
        self,
        entries: list[dict[str, str]],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Batch lookup city/state for NPA/NXX pairs.

        Args:
            entries: NPA/NXX pairs to look up (max 50), each with 'npa' and 'nxx' keys.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with an array of {npa, nxx, city, state} objects.
        """
        return self._sdk._request(
            "/number/lookup/location",
            method="POST",
            body={"entries": entries},
            token=token,
            headers=headers,
        )

    def migrate_phone_number_to_v2(
        self,
        phone_number: str | None = None,
        campaign_id: str | None = None,
        group_id: str | None = None,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Migrate a phone number (or all numbers in a group) from v1 to v2.

        Args:
            phone_number: Phone number to migrate. If provided, group_id is ignored.
            campaign_id: Campaign ID to migrate all numbers for.
            group_id: Group ID to migrate all non-released numbers for.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with migration queue confirmation.
        """
        return self._sdk._request(
            "/number/migrate",
            method="POST",
            body={"phoneNumber": phone_number, "campaignId": campaign_id, "groupId": group_id},
            token=token,
            headers=headers,
        )
