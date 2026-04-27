"""Groups domain for the SignalHouse SDK."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class GroupsAdmin:
    """Admin-only group operations (SignalHouse staff)."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def get_groups(
        self,
        *,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a list of all groups with optional pagination.

        Args:
            page: The page number for pagination.
            limit: The number of items per page.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({"page": page, "limit": limit})
        return self._sdk._request(
            f"/group{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def create_group(
        self,
        group_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a new group with the specified group data.

        Args:
            group_data: The data for the new group, including required fields such as groupName.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If group_data is missing.
        """
        self._sdk._require({"groupData": group_data})
        return self._sdk._request(
            "/group",
            method="POST",
            body=group_data,
            token=token,
            headers=headers,
        )

    def delete_group(
        self,
        group_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete a group with the specified group ID.

        Args:
            group_id: The ID of the group to delete.
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
            f"/group/{safe_group_id}",
            method="DELETE",
            token=token,
            headers=headers,
        )


class Groups:
    """Group management operations."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk
        self.admin: GroupsAdmin | None = None
        if sdk.enable_admin:
            self.admin = GroupsAdmin(sdk)

    def get_group(
        self,
        *,
        id: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get details of a group by its ID.

        Args:
            id: The ID of the group to retrieve.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({"id": id})
        return self._sdk._request(
            f"/group{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def update_group(
        self,
        id: str,
        group_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update a group with the specified group data.

        Args:
            id: The ID of the group to update.
            group_data: The data for the group, including required fields such as groupName.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If id or group_data is missing.
        """
        self._sdk._require({"id": id, "groupData": group_data})
        safe_id = quote(str(id), safe="")
        return self._sdk._request(
            f"/group/{safe_id}",
            method="PUT",
            body=group_data,
            token=token,
            headers=headers,
        )
