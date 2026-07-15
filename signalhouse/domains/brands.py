"""Brands domain for the SignalHouse SDK.

Brand lookup id: carrier Brand ID (B… or TFNB…), Mongo _id, or internal reference UUID.
Read/create responses return ``brandId: null`` for pending brands — poll ``GET /brand?id=<Mongo _id>``.
"""

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
        registration_type: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a list of brands with optional filters.

        Args:
            id: Brand lookup id (carrier Brand ID, Mongo _id, or internal reference).
            subgroup_id: The ID of the subgroup to filter by.
            group_id: The ID of the group to filter by.
            page: The page number for pagination.
            limit: The number of items per page.
            status: The status of the brand to filter by (PENDING_CREATION, PENDING_APPROVAL,
                    UNVERIFIED, VERIFIED, VETTED_VERIFIED, PENDING_DELETE, DELETED).
            registration_type: Optional registration-type filter ("TEN_DLC" or "TOLL_FREE").
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict. Each brand may have ``brandId: null`` until a carrier
            Brand ID is assigned — use ``_id`` for polling.
        """
        query_string = self._sdk._get_query_string({
            "id": id,
            "subgroupId": subgroup_id,
            "groupId": group_id,
            "page": page,
            "limit": limit,
            "status": status,
            "registrationType": registration_type,
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
            brand_id: Brand lookup id (carrier Brand ID, Mongo _id, or internal reference).
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
            Standardized response dict. ``brandId`` may be ``null`` until carrier assignment — use ``_id`` to poll.

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

    def create_toll_free_brand(
        self,
        brand_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a new Toll-Free (TFN) brand.

        registrationType is forced to TOLL_FREE server-side; TFN-specific fields live under
        ``brand_data["tollFree"]`` (businessRegistrationType, legalEntityType, taxId, countryCode,
        supportPhone, and optional taxIdIssuingCountry / businessDBA).

        Args:
            brand_data: The data for the toll-free brand to be created (see API docs for required
                        fields, including the ``tollFree`` sub-object).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict. For Toll-Free, ``brandId`` is a ``TFNB``-prefixed id when
            assigned; otherwise ``null`` — use ``_id`` to poll.

        Raises:
            SignalHouseValidationError: If brand_data is missing.
        """
        self._sdk._require({"brandData": brand_data})
        return self._sdk._request(
            "/brand/toll-free",
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
            brand_ids: Brand lookup ids to transfer (carrier id, Mongo _id, or internal reference).
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
            brand_id: Brand lookup id (carrier Brand ID, Mongo _id, or internal reference).
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

    def import_external_vetting(
        self,
        brand_id: str,
        vetting_provider_id: str,
        vetting_id: str,
        vetting_token: str | None = None,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Import an existing external vetting record for a brand.

        Unlike create_external_vetting (which orders a new, billable vetting), this attaches a
        vetting the brand already completed directly with the provider, using the provider-issued
        vettingId and vettingToken. It is synchronous and not billable.

        Args:
            brand_id: Brand lookup id (carrier Brand ID, Mongo _id, or internal reference).
            vetting_provider_id: The external vetting provider (AEGIS, WMC, CV).
            vetting_id: The provider-issued vetting / transaction ID to import.
            vetting_token: The provider-issued vetting token (required by some providers, e.g. AEGIS).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If brand_id, vetting_provider_id, or vetting_id is missing.
        """
        self._sdk._require(
            {"brandId": brand_id, "vettingProviderId": vetting_provider_id, "vettingId": vetting_id}
        )
        safe_brand_id = quote(str(brand_id), safe="")
        body: dict[str, Any] = {"vettingProviderId": vetting_provider_id, "vettingId": vetting_id}
        if vetting_token is not None:
            body["vettingToken"] = vetting_token
        return self._sdk._request(
            f"/brand/externalvetting/import/{safe_brand_id}",
            method="POST",
            body=body,
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
            brand_id: Brand lookup id (carrier Brand ID, Mongo _id, or internal reference).
            brand_data: The data for the brand to be updated. For a Toll-Free brand, pass the
                        editable Toll-Free fields under a ``tollFree`` sub-object (legalEntityType,
                        businessRegistrationType, taxId, countryCode, supportPhone,
                        taxIdIssuingCountry, businessDBA); subgroupId is immutable.
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
            brand_id: Brand lookup id (carrier Brand ID, Mongo _id, or internal reference).
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
            brand_id: Brand lookup id (carrier Brand ID, Mongo _id, or internal reference).
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
            brand_id: Brand lookup id (carrier Brand ID, Mongo _id, or internal reference).
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
            brand_id: Brand lookup id (carrier Brand ID, Mongo _id, or internal reference).
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
