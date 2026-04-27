"""Landings domain for the SignalHouse SDK."""

from __future__ import annotations

import json
from typing import Any, BinaryIO, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class Landings:
    """Landing page management operations with multipart file upload support."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def get_landings(
        self,
        landing_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get details of a landing page by its ID.

        Args:
            landing_id: The ID of the landing page to retrieve.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If landing_id is missing.
        """
        self._sdk._require({"landingId": landing_id})
        safe_landing_id = quote(str(landing_id), safe="")
        return self._sdk._request(
            f"/landing/{safe_landing_id}",
            method="GET",
            token=token,
            headers=headers,
        )

    def create_landing(
        self,
        landing_data: dict[str, Any],
        *,
        file: BinaryIO | tuple | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a new landing page with the specified landing data and optional logo file.

        Args:
            landing_data: The data for the new landing page. Required fields include
                         brandId, description, primaryBackgroundColor, secondaryBackgroundColor,
                         primaryTextColor, secondaryTextColor.
            file: A logo image file for the landing page. Can be a file-like object or
                  a tuple of (filename, file_object, content_type).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        form_data: dict[str, Any] = {}
        files_list: list[tuple[str, Any]] = []

        if file is not None:
            if isinstance(file, tuple):
                files_list.append(("file", file))
            else:
                files_list.append(("file", file))

        for key, value in landing_data.items():
            if value is not None:
                if isinstance(value, (dict, list)):
                    form_data[key] = json.dumps(value)
                else:
                    form_data[key] = value

        return self._sdk._multipart_request(
            "/landing",
            method="POST",
            form_data=form_data,
            files=files_list if files_list else None,
            token=token,
            headers=headers,
        )

    def update_landing(
        self,
        landing_id: str,
        landing_data: dict[str, Any],
        *,
        file: BinaryIO | tuple | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update an existing landing page with the specified landing data and optional logo file.

        Args:
            landing_id: The ID of the landing page to update.
            landing_data: The data for the landing page to be updated.
            file: A logo image file for the landing page. Can be a file-like object or
                  a tuple of (filename, file_object, content_type).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If landing_id is missing.
        """
        self._sdk._require({"landingId": landing_id})
        safe_landing_id = quote(str(landing_id), safe="")

        form_data: dict[str, Any] = {}
        files_list: list[tuple[str, Any]] = []

        if file is not None:
            if isinstance(file, tuple):
                files_list.append(("file", file))
            else:
                files_list.append(("file", file))

        for key, value in landing_data.items():
            if value is not None:
                if isinstance(value, (dict, list)):
                    form_data[key] = json.dumps(value)
                else:
                    form_data[key] = value

        return self._sdk._multipart_request(
            f"/landing/{safe_landing_id}",
            method="PUT",
            form_data=form_data,
            files=files_list if files_list else None,
            token=token,
            headers=headers,
        )

    def get_landing_by_brand_id(
        self,
        brand_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a landing page by its associated brand ID.

        Args:
            brand_id: The brand ID to look up the landing page for.
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
            f"/landing/brand/{safe_brand_id}",
            method="GET",
            token=token,
            headers=headers,
        )

    def delete_landing(
        self,
        landing_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete a landing page by its ID.

        Args:
            landing_id: The ID of the landing page to delete.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If landing_id is missing.
        """
        self._sdk._require({"landingId": landing_id})
        safe_landing_id = quote(str(landing_id), safe="")
        return self._sdk._request(
            f"/landing/{safe_landing_id}",
            method="DELETE",
            token=token,
            headers=headers,
        )
