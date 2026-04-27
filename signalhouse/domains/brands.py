"""Brands domain for the SignalHouse SDK."""

from __future__ import annotations

import json
from typing import Any, BinaryIO, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class Brands:
    """10DLC Brand registration operations."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def get_brands(
        self,
        *,
        id: str | None = None,
        subgroup_id: str | None = None,
        group_id: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        status: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a list of brands with optional filters.

        Args:
            id: The ID of the brand to filter by.
            subgroup_id: The ID of the subgroup to filter by.
            group_id: The ID of the group to filter by.
            page: The page number for pagination.
            limit: The number of items per page.
            status: The status of the brand to filter by (PENDING_CREATION, PENDING_APPROVAL,
                    UNVERIFIED, VERIFIED, VETTED_VERIFIED, PENDING_DELETE, DELETED).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({
            "id": id,
            "subgroupId": subgroup_id,
            "groupId": group_id,
            "page": page,
            "limit": limit,
            "status": status,
        })
        return self._sdk._request(
            f"/brand{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_external_vetting(
        self,
        brand_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get external vetting information for a brand.

        Args:
            brand_id: The ID of the brand to get the external vetting information for.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If brand_id is missing.
        """
        self._sdk._require({"brandId": brand_id})
        safe_brand_id = quote(str(brand_id), safe="")
        return self._sdk._request(
            f"/brand/externalvetting/{safe_brand_id}",
            method="GET",
            token=token,
            headers=headers,
        )

    def create_brand(
        self,
        brand_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a new brand.

        Args:
            brand_data: The data for the brand to be created. Required fields include
                        subgroupId, entityType, displayName, companyName, ein, phone,
                        street, city, state, postalCode, country, email, vertical.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If brand_data is missing.
        """
        self._sdk._require({"brandData": brand_data})
        return self._sdk._request(
            "/brand",
            method="POST",
            body=brand_data,
            token=token,
            headers=headers,
        )

    def transfer_brand(
        self,
        subgroup_id: str,
        brand_ids: list[str],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Transfer one or more brands to a different subgroup.

        Args:
            subgroup_id: The ID of the subgroup to transfer the brands to.
            brand_ids: The IDs of the brands to be transferred.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If subgroup_id or brand_ids is missing.
        """
        self._sdk._require({"subgroupId": subgroup_id, "brandIds": brand_ids})
        safe_subgroup_id = quote(str(subgroup_id), safe="")
        return self._sdk._request(
            f"/brand/transfer/{safe_subgroup_id}",
            method="POST",
            body={"brandIds": brand_ids},
            token=token,
            headers=headers,
        )

    def create_external_vetting(
        self,
        brand_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create external vetting for a brand.

        Args:
            brand_id: The ID of the brand to create external vetting for.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If brand_id is missing.
        """
        self._sdk._require({"brandId": brand_id})
        safe_brand_id = quote(str(brand_id), safe="")
        return self._sdk._request(
            f"/brand/externalvetting/{safe_brand_id}",
            method="POST",
            token=token,
            headers=headers,
        )

    def update_brand(
        self,
        brand_id: str,
        brand_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update a brand's information.

        Args:
            brand_id: The ID of the brand to update.
            brand_data: The data for the brand to be updated.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If brand_id is missing.
        """
        self._sdk._require({"brandId": brand_id})
        safe_brand_id = quote(str(brand_id), safe="")
        return self._sdk._request(
            f"/brand/{safe_brand_id}",
            method="PUT",
            body=brand_data,
            token=token,
            headers=headers,
        )

    def revet_brand(
        self,
        brand_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Revet a brand that is in UNVERIFIED status due to an update after it was previously VERIFIED or VETTED_VERIFIED.

        Args:
            brand_id: The ID of the brand to revert.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If brand_id is missing.
        """
        self._sdk._require({"brandId": brand_id})
        safe_brand_id = quote(str(brand_id), safe="")
        return self._sdk._request(
            f"/brand/revet/{safe_brand_id}",
            method="PUT",
            token=token,
            headers=headers,
        )

    def delete_brand(
        self,
        brand_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete a brand (mark it as DELETED). The brand will still be retrievable.

        Args:
            brand_id: The ID of the brand to delete.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If brand_id is missing.
        """
        self._sdk._require({"brandId": brand_id})
        safe_brand_id = quote(str(brand_id), safe="")
        return self._sdk._request(
            f"/brand/{safe_brand_id}",
            method="DELETE",
            token=token,
            headers=headers,
        )

    def get_appeal_history(
        self,
        brand_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get the appeal history for a brand.

        Args:
            brand_id: The ID of the brand to get the appeal history for.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict containing an array of BrandAppeal objects.

        Raises:
            SignalHouseValidationError: If brand_id is missing.
        """
        self._sdk._require({"brandId": brand_id})
        safe_brand_id = quote(str(brand_id), safe="")
        return self._sdk._request(
            f"/brand/appeal/{safe_brand_id}",
            method="GET",
            token=token,
            headers=headers,
        )

    def submit_appeal(
        self,
        brand_id: str,
        appeal_categories: list[str],
        explanation: str,
        file: BinaryIO | tuple,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Submit an appeal for a brand.

        Args:
            brand_id: The ID of the brand to submit the appeal for.
            appeal_categories: A list of appeal category strings.
            explanation: The explanation for the appeal.
            file: The file to attach to the appeal. Can be a file-like object or
                  a tuple of (filename, file_object, content_type).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If required parameters are missing.
        """
        self._sdk._require({
            "brandId": brand_id,
            "appealCategories": appeal_categories,
            "explanation": explanation,
            "file": file,
        })
        safe_brand_id = quote(str(brand_id), safe="")

        form_data: dict[str, Any] = {
            "appealCategories": json.dumps(appeal_categories),
            "explanation": explanation,
        }

        files_list: list[tuple[str, Any]] = []
        if isinstance(file, tuple):
            files_list.append(("file", file))
        else:
            files_list.append(("file", file))

        return self._sdk._multipart_request(
            f"/brand/appeal/{safe_brand_id}",
            method="POST",
            form_data=form_data,
            files=files_list,
            token=token,
            headers=headers,
        )
