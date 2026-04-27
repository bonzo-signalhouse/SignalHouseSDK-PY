"""Auth domain for the SignalHouse SDK."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class Auth:
    """Authentication operations including login, password reset, and auth history."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def login(
        self,
        email: str,
        password: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Login with email and password.

        Args:
            email: The user's email address.
            password: The user's password.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        return self._sdk._request(
            "/auth",
            method="POST",
            body={"email": email, "password": password},
            token=token,
            headers=headers,
        )

    def reset_password(
        self,
        user_id: str,
        new_password: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Reset a user's password.

        Args:
            user_id: The id of the user.
            new_password: The new password to set for the user.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If user_id or new_password is missing.
        """
        self._sdk._require({"userId": user_id, "newPassword": new_password})
        safe_user_id = quote(str(user_id), safe="")
        return self._sdk._request(
            f"/auth/resetpassword/{safe_user_id}",
            method="PUT",
            body={"newPassword": new_password},
            token=token,
            headers=headers,
        )

    def get_auth_history(
        self,
        *,
        group_id: str | None = None,
        user_id: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get token login history for a group or user.

        Args:
            group_id: Returns history for all users in the group (one of group_id/user_id required).
            user_id: Returns history for a specific user (one of group_id/user_id required).
            page: Page number (min 1, default 1).
            limit: Results per page (min 1, max 100, default 20).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If neither group_id nor user_id is provided.
        """
        self._sdk._require({"groupId or userId": group_id or user_id})
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
            "userId": user_id,
            "page": page,
            "limit": limit,
        })
        return self._sdk._request(
            f"/auth/history{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )
