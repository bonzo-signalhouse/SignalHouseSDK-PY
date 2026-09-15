"""Webhooks domain for the SignalHouse SDK."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class Webhooks:
    """Webhook management operations."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def get_webhooks(
        self,
        *,
        id: str | None = None,
        group_id: str | None = None,
        endpoint_type: str | None = None,
        phone_number: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a list of webhooks with optional filters.

        Each returned endpoint carries `hasSigningSecret` (bool) instead of the signing secret
        itself — see `create_webhook`.

        Args:
            id: Filter by webhook ID.
            group_id: Filter by associated group ID.
            endpoint_type: Filter by endpoint type (Global, Number).
            phone_number: Filter by associated phone number.
            page: The page number for pagination.
            limit: The number of items per page.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({
            "id": id,
            "groupId": group_id,
            "endpointType": endpoint_type,
            "phoneNumber": phone_number,
            "page": page,
            "limit": limit,
        })
        return self._sdk._request(
            f"/webhook{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def create_webhook(
        self,
        webhook_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a new webhook with the specified data.

        The response includes a `signingSecret` (plaintext HMAC-SHA256 secret) used to sign every
        delivery to this endpoint via the `X-SignalHouse-Signature` header. It is returned exactly
        once, here — store it now, it is never exposed again by any read.

        Args:
            webhook_data: The data for the new webhook, including endpoint URL and event types.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict, including the plaintext `signingSecret` (this one time only).

        Raises:
            SignalHouseValidationError: If webhook_data is missing.
        """
        self._sdk._require({"webhookData": webhook_data})
        return self._sdk._request(
            "/webhook",
            method="POST",
            body=webhook_data,
            token=token,
            headers=headers,
        )

    def update_webhook(
        self,
        id: str,
        update_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update an existing webhook with the specified data.

        Like every other read of a webhook, the response carries `hasSigningSecret` (bool), never
        the signing secret itself — see `create_webhook`.

        Args:
            id: The ID of the webhook to update.
            update_data: The data for the webhook to be updated.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If id or update_data is missing.
        """
        self._sdk._require({"id": id, "updateData": update_data})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/webhook/{safe_id}",
            method="PUT",
            body=update_data,
            token=token,
            headers=headers,
        )

    def delete_webhook(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete a webhook by its ID (mark as inactive).

        Args:
            id: The ID of the webhook to delete.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If id is missing.
        """
        self._sdk._require({"id": id})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/webhook/{safe_id}",
            method="DELETE",
            token=token,
            headers=headers,
        )
