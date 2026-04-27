"""Campaigns domain for the SignalHouse SDK."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class CampaignsAdmin:
    """Admin-only campaign operations (SignalHouse staff)."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def approve_campaign(
        self,
        campaign_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Approve a campaign that is pending approval.

        Args:
            campaign_id: The ID of the campaign to approve.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If campaign_id is missing.
        """
        self._sdk._require({"campaignId": campaign_id})
        safe_campaign_id = quote(str(campaign_id), safe="")
        return self._sdk._request(
            f"/campaign/approve/{safe_campaign_id}",
            method="POST",
            token=token,
            headers=headers,
        )

    def reject_campaign(
        self,
        campaign_id: str,
        *,
        rejection_reason: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Reject a campaign that is pending approval.

        Args:
            campaign_id: The ID of the campaign to reject.
            rejection_reason: Optional rejection reason (10-256 characters).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If campaign_id is missing.
        """
        self._sdk._require({"campaignId": campaign_id})
        safe_campaign_id = quote(str(campaign_id), safe="")
        body = {"rejectionReason": rejection_reason} if rejection_reason else None
        return self._sdk._request(
            f"/campaign/reject/{safe_campaign_id}",
            method="POST",
            body=body,
            token=token,
            headers=headers,
        )


class Campaigns:
    """10DLC Campaign management operations."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk
        self.admin: CampaignsAdmin | None = None
        if sdk.enable_admin:
            self.admin = CampaignsAdmin(sdk)

    def get_campaigns(
        self,
        *,
        id: str | None = None,
        brand_id: str | None = None,
        subgroup_id: str | None = None,
        group_id: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        status: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a list of campaigns with optional filters.

        Args:
            id: The ID of the campaign to filter by.
            brand_id: The ID of the brand to filter by.
            subgroup_id: The ID of the subgroup to filter by.
            group_id: The ID of the group to filter by.
            page: The page number for pagination.
            limit: The number of items per page.
            status: The status of the campaign to filter by.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({
            "id": id,
            "brandId": brand_id,
            "subgroupId": subgroup_id,
            "groupId": group_id,
            "page": page,
            "limit": limit,
            "status": status,
        })
        return self._sdk._request(
            f"/campaign{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def create_campaign(
        self,
        campaign_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a new campaign.

        Args:
            campaign_data: The data for the campaign to be created. Required fields include
                          brandId, usecase, description, messageFlow, privacyPolicyLink,
                          termsAndConditionsLink, phoneNumbers.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If campaign_data is missing.
        """
        self._sdk._require({"campaignData": campaign_data})
        return self._sdk._request(
            "/campaign",
            method="POST",
            body=campaign_data,
            token=token,
            headers=headers,
        )

    def update_campaign(
        self,
        campaign_id: str,
        campaign_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update an existing campaign.

        Args:
            campaign_id: The ID of the campaign to update.
            campaign_data: The data for the campaign to be updated.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If campaign_id is missing.
        """
        self._sdk._require({"campaignId": campaign_id})
        safe_campaign_id = quote(str(campaign_id), safe="")
        return self._sdk._request(
            f"/campaign/{safe_campaign_id}",
            method="PUT",
            body=campaign_data,
            token=token,
            headers=headers,
        )

    def delete_campaign(
        self,
        campaign_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete an existing campaign (mark it as EXPIRED). The campaign will still be retrievable.

        Args:
            campaign_id: The ID of the campaign to delete.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If campaign_id is missing.
        """
        self._sdk._require({"campaignId": campaign_id})
        safe_campaign_id = quote(str(campaign_id), safe="")
        return self._sdk._request(
            f"/campaign/{safe_campaign_id}",
            method="DELETE",
            token=token,
            headers=headers,
        )

    def appeal_dca_rejection(
        self,
        campaign_id: str,
        appeal_data: dict[str, Any] | None = None,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Appeal a DCA-rejected campaign.

        Args:
            campaign_id: The ID of the campaign to appeal.
            appeal_data: Optional request body (e.g., {"reason": "..."}).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If campaign_id is missing.
        """
        self._sdk._require({"campaignId": campaign_id})
        safe_campaign_id = quote(str(campaign_id), safe="")
        return self._sdk._request(
            f"/campaign/appealDcaRejection/{safe_campaign_id}",
            method="POST",
            body=appeal_data,
            token=token,
            headers=headers,
        )

    def nudge_dca_for_campaign(
        self,
        campaign_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Nudge a connectivity partner to prioritize review of a campaign.

        The campaign must be in PENDING_DCA_APPROVAL status.

        Args:
            campaign_id: The ID of the campaign to nudge.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If campaign_id is missing.
        """
        self._sdk._require({"campaignId": campaign_id})
        safe_campaign_id = quote(str(campaign_id), safe="")
        return self._sdk._request(
            f"/campaign/nudge/{safe_campaign_id}",
            method="POST",
            token=token,
            headers=headers,
        )
