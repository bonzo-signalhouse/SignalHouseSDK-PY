"""Subgroups domain for the SignalHouse SDK."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class Subgroups:
    """Subgroup management operations."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def get_subgroups(
        self,
        *,
        id: str | None = None,
        group_id: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a list of subgroups with optional filters.

        Args:
            id: Filter by subgroup ID.
            group_id: Filter by parent group ID.
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
            "page": page,
            "limit": limit,
        })
        return self._sdk._request(
            f"/subgroup{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def create_subgroup(
        self,
        subgroup_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a new subgroup with the specified subgroup data.

        Args:
            subgroup_data: The data for the subgroup. Required fields include groupId and subgroupName.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If subgroup_data is missing.
        """
        self._sdk._require({"subgroupData": subgroup_data})
        return self._sdk._request(
            "/subgroup",
            method="POST",
            body=subgroup_data,
            token=token,
            headers=headers,
        )

    def update_subgroup(
        self,
        id: str,
        update_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update an existing subgroup with the specified data.

        Args:
            id: The ID of the subgroup to update.
            update_data: The data for the subgroup to be updated.
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
            f"/subgroup/{safe_id}",
            method="PUT",
            body=update_data,
            token=token,
            headers=headers,
        )

    def delete_subgroup(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete a subgroup by its ID (mark as inactive).

        Args:
            id: The ID of the subgroup to delete.
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
            f"/subgroup/{safe_id}",
            method="DELETE",
            token=token,
            headers=headers,
        )
