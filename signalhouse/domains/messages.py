"""Messages domain for the SignalHouse SDK."""

from __future__ import annotations

import json
from typing import Any, BinaryIO, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class Messages:
    """SMS/MMS messaging operations with multipart file upload support."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def get_messages(
        self,
        *,
        id: str | None = None,
        campaign_id: str | None = None,
        brand_id: str | None = None,
        subgroup_id: str | None = None,
        group_id: str | None = None,
        phone_number: str | None = None,
        sender_phone_number: str | None = None,
        recipient_phone_number: str | None = None,
        status: str | None = None,
        direction: str | None = None,
        message_type: str | list[str] | None = None,
        carrier: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        sort_field: str | None = None,
        sort_order: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a list of messages with optional filters and pagination.

        Args:
            id: Filter messages by their unique ID.
            campaign_id: Filter messages by the ID of the associated campaign.
            brand_id: Filter messages by the ID of the associated brand.
            subgroup_id: Filter messages by the ID of the associated subgroup.
            group_id: Filter messages by the ID of the associated group.
            status: Filter by status (ENQUEUED, DEQUEUED, SENT, FAILED, DELIVERED).
            direction: Filter by direction (INBOUND, OUTBOUND).
            message_type: Filter by type (SMS, MMS).
            carrier: Filter by carrier used for sending.
            sender_phone_number: Filter by sender phone number.
            recipient_phone_number: Filter by recipient phone number.
            start_date: ISO-8601 date or timestamp; normalized to start-of-UTC-day (inclusive).
            end_date: ISO-8601 date or timestamp; normalized to end-of-UTC-day (inclusive). Hourly resolution is not supported.
            sort_field: The field to sort by.
            sort_order: The sort order (asc, desc).
            page: The page number for pagination.
            limit: The number of messages per page.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({
            "id": id,
            "campaignId": campaign_id,
            "brandId": brand_id,
            "subgroupId": subgroup_id,
            "groupId": group_id,
            "phoneNumber": phone_number,
            "senderPhoneNumber": sender_phone_number,
            "recipientPhoneNumber": recipient_phone_number,
            "status": status,
            "direction": direction,
            "messageType": message_type,
            "carrier": carrier,
            "startDate": start_date,
            "endDate": end_date,
            "sortField": sort_field,
            "sortOrder": sort_order,
            "page": page,
            "limit": limit,
        })
        return self._sdk._request(
            f"/message{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_analytics(
        self,
        *,
        group_id: str | None = None,
        subgroup_id: str | None = None,
        brand_id: str | None = None,
        campaign_id: str | None = None,
        phone_number: str | None = None,
        carrier: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get aggregated analytics for messages with optional filters.

        Args:
            group_id: Filter analytics by group ID.
            subgroup_id: Filter analytics by subgroup ID.
            brand_id: Filter analytics by brand ID.
            campaign_id: Filter analytics by campaign ID.
            phone_number: Filter analytics by phone number.
            carrier: Filter analytics by carrier.
            start_date: ISO-8601 date or timestamp; normalized to start-of-UTC-day (inclusive).
            end_date: ISO-8601 date or timestamp; normalized to end-of-UTC-day (inclusive). Hourly resolution is not supported.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.
        """
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
            "subgroupId": subgroup_id,
            "brandId": brand_id,
            "campaignId": campaign_id,
            "phoneNumber": phone_number,
            "carrier": carrier,
            "startDate": start_date,
            "endDate": end_date,
        })
        return self._sdk._request(
            f"/message/analytics{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_analytics_detail(
        self,
        *,
        group_id: str | None = None,
        subgroup_id: str | None = None,
        brand_id: str | None = None,
        campaign_id: str | None = None,
        phone_number: str | None = None,
        carrier: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get detailed analytics snapshot records for charting and aggregation.

        Args:
            group_id: Filter analytics by group ID.
            subgroup_id: Filter analytics by subgroup ID.
            brand_id: Filter analytics by brand ID.
            campaign_id: Filter analytics by campaign ID.
            phone_number: Filter analytics by phone number.
            carrier: Filter analytics by carrier.
            start_date: ISO-8601 date or timestamp; normalized to start-of-UTC-day (inclusive).
            end_date: ISO-8601 date or timestamp; normalized to end-of-UTC-day (inclusive). Hourly resolution is not supported.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with array of analytics snapshot records.
        """
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
            "subgroupId": subgroup_id,
            "brandId": brand_id,
            "campaignId": campaign_id,
            "phoneNumber": phone_number,
            "carrier": carrier,
            "startDate": start_date,
            "endDate": end_date,
        })
        return self._sdk._request(
            f"/message/analytics/detail{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_analytics_filter_options(
        self,
        *,
        group_id: str,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get filter dropdown options (subgroups, brands, campaigns, phone numbers) for the
        Analytics page, scoped to a single group. Sourced from ClickHouse — only items with
        at least one message are returned.

        Args:
            group_id: The ID of the group whose filter options to load.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with subgroups, brands, campaigns, and phoneNumbers arrays.
        """
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
        })
        return self._sdk._request(
            f"/message/analytics/filter-options{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_analytics_by_subgroup(
        self,
        *,
        group_id: str,
        subgroup_id: str | list[str] | None = None,
        brand_id: str | list[str] | None = None,
        campaign_id: str | list[str] | None = None,
        phone_number: str | list[str] | None = None,
        carrier: str | list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        channel: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a paginated breakdown of message metrics grouped by subgroup. Each row
        carries the full set of sms/mms/p2p metric columns plus ``smsOptOuts`` and
        ``mmsOptOuts`` (sourced from the DNC analytics MV — P2P has no opt-outs) so
        callers can apply channel toggles client-side.

        Args:
            page: Page number (default 1).
            limit: Rows per page, max 50.
            channel: "tenDLC" | "p2p" | "both" (default "both"). Scopes the ORDER BY +
                row inclusion so a P2P-only caller doesn't get pages dominated by
                10DLC-heavy subgroups with no visible activity.

        Returns:
            Standardized response dict with rows, totalCount, page, and limit.
        """
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
            "subgroupId": subgroup_id,
            "brandId": brand_id,
            "campaignId": campaign_id,
            "phoneNumber": phone_number,
            "carrier": carrier,
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "limit": limit,
            "channel": channel,
        })
        return self._sdk._request(
            f"/message/analytics/by-subgroup{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_analytics_by_error_code(
        self,
        *,
        group_id: str,
        subgroup_id: str | list[str] | None = None,
        brand_id: str | list[str] | None = None,
        campaign_id: str | list[str] | None = None,
        phone_number: str | list[str] | None = None,
        carrier: str | list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        channel: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a paginated breakdown of failed messages grouped by error code. Each row
        contains per-channel (sms/mms/p2p) error counts plus an enriched description.

        Args:
            page: Page number (default 1).
            limit: Rows per page, max 50.
            channel: "tenDLC" | "p2p" | "both" (default "both"). Scopes the ORDER BY +
                totalCount so a P2P-only caller doesn't get pages dominated by codes
                with only 10DLC errors.

        Returns:
            Standardized response dict with rows, totalCount, totalErrors, page, and limit.
        """
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
            "subgroupId": subgroup_id,
            "brandId": brand_id,
            "campaignId": campaign_id,
            "phoneNumber": phone_number,
            "carrier": carrier,
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "limit": limit,
            "channel": channel,
        })
        return self._sdk._request(
            f"/message/analytics/by-error-code{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_dnc_analytics(
        self,
        *,
        group_id: str | None = None,
        subgroup_id: str | None = None,
        brand_id: str | None = None,
        campaign_id: str | None = None,
        phone_number: str | None = None,
        carrier: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get aggregated DNC (Do Not Contact) opt-out analytics with optional filters.

        Args:
            group_id: Filter by group ID.
            subgroup_id: Filter by subgroup ID.
            brand_id: Filter by brand ID.
            campaign_id: Filter by campaign ID.
            phone_number: Filter by phone number.
            carrier: Filter by carrier.
            start_date: ISO-8601 date or timestamp; normalized to start-of-UTC-day (inclusive).
            end_date: ISO-8601 date or timestamp; normalized to end-of-UTC-day (inclusive). Hourly resolution is not supported.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with totals, byDate, byPhoneNumber, byCarrier.
        """
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
            "subgroupId": subgroup_id,
            "brandId": brand_id,
            "campaignId": campaign_id,
            "phoneNumber": phone_number,
            "carrier": carrier,
            "startDate": start_date,
            "endDate": end_date,
        })
        return self._sdk._request(
            f"/message/dnc/analytics{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_dnc_records(
        self,
        *,
        group_id: str | None = None,
        subgroup_id: str | None = None,
        brand_id: str | None = None,
        campaign_id: str | None = None,
        phone_number: str | None = None,
        carrier: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        sort_field: str | None = None,
        sort_order: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get paginated Do Not Call records with optional filters.

        Args:
            group_id: Filter by group ID.
            subgroup_id: Filter by subgroup ID.
            brand_id: Filter by brand ID.
            campaign_id: Filter by campaign ID.
            phone_number: Filter by phone number.
            carrier: Filter by carrier.
            start_date: ISO-8601 date or timestamp; normalized to start-of-UTC-day (inclusive).
            end_date: ISO-8601 date or timestamp; normalized to end-of-UTC-day (inclusive). Hourly resolution is not supported.
            page: Page number for pagination.
            limit: Number of records per page.
            sort_field: Field to sort by.
            sort_order: Sort direction (asc, desc).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with paginated DNC records.
        """
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
            "subgroupId": subgroup_id,
            "brandId": brand_id,
            "campaignId": campaign_id,
            "phoneNumber": phone_number,
            "carrier": carrier,
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "limit": limit,
            "sortField": sort_field,
            "sortOrder": sort_order,
        })
        return self._sdk._request(
            f"/message/dnc{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def send_sms(
        self,
        sender_phone_number: str,
        recipient_phone_numbers: str | list[str],
        message_body: str,
        *,
        status_callback_url: str | None = None,
        enable_shortlink: bool = False,
        filter_landlines_and_inactive_numbers: bool = False,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send an SMS message to one or more recipient phone numbers.

        Args:
            sender_phone_number: The phone number to send the message from.
            recipient_phone_numbers: The phone number(s) to send the message to.
            message_body: The body of the SMS message.
            status_callback_url: The URL to receive status callbacks.
            enable_shortlink: Whether to enable shortlink in the message.
            filter_landlines_and_inactive_numbers: Whether to filter out landline and inactive numbers before sending.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If required parameters are missing.
        """
        self._sdk._require({
            "senderPhoneNumber": sender_phone_number,
            "recipientPhoneNumbers": recipient_phone_numbers,
            "messageBody": message_body,
        })
        body: dict[str, Any] = {
            "senderPhoneNumber": sender_phone_number,
            "recipientPhoneNumber": recipient_phone_numbers,
            "messageBody": message_body,
            "enableShortlink": enable_shortlink,
        }
        if filter_landlines_and_inactive_numbers:
            body["filterLandlinesAndInactiveNumbers"] = True
        if status_callback_url is not None:
            body["statusCallbackUrl"] = status_callback_url
        return self._sdk._request(
            "/message/sms",
            method="POST",
            body=body,
            token=token,
            headers=headers,
        )

    def send_p2p(
        self,
        recipient_phone_numbers: str | list[str],
        message_body: str,
        *,
        status_callback_url: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a P2P message via Rogue Mobile SMPP.

        Args:
            recipient_phone_numbers: The phone number(s) to send the message to.
            message_body: The body of the P2P message.
            status_callback_url: The URL to receive status callbacks.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If required parameters are missing.
        """
        self._sdk._require({
            "recipientPhoneNumbers": recipient_phone_numbers,
            "messageBody": message_body,
        })
        body: dict[str, Any] = {
            "recipientPhoneNumber": recipient_phone_numbers,
            "messageBody": message_body,
        }
        if status_callback_url is not None:
            body["statusCallbackUrl"] = status_callback_url
        return self._sdk._request(
            "/message/p2p",
            method="POST",
            body=body,
            token=token,
            headers=headers,
        )

    def send_mms(
        self,
        sender_phone_number: str,
        recipient_phone_numbers: str | list[str],
        message_body: str,
        *,
        media_urls: list[str] | None = None,
        status_callback_url: str | None = None,
        enable_shortlink: bool = False,
        enable_compression: bool = True,
        filter_landlines_and_inactive_numbers: bool = False,
        images: list[BinaryIO | tuple] | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send an MMS message to one or more recipients, with optional media attachments.

        Args:
            sender_phone_number: The phone number to send the message from.
            recipient_phone_numbers: The phone number(s) to send the message to.
            message_body: The body of the MMS message.
            media_urls: The URLs of the media attachments.
            status_callback_url: The URL to receive status callbacks.
            enable_shortlink: Whether to enable shortlink in the message.
            enable_compression: Whether to enable image compression for attachments.
            filter_landlines_and_inactive_numbers: Whether to filter out landline and inactive numbers before sending.
            images: Image files to attach to the MMS message. Each can be a file-like object
                    or a tuple of (filename, file_object, content_type).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If required parameters are missing.
        """
        self._sdk._require({
            "senderPhoneNumber": sender_phone_number,
            "recipientPhoneNumbers": recipient_phone_numbers,
        })

        form_data: dict[str, Any] = {
            "senderPhoneNumber": sender_phone_number,
            "messageBody": message_body,
            "enableShortlink": str(enable_shortlink).lower(),
            "enableCompression": str(enable_compression).lower(),
        }

        if filter_landlines_and_inactive_numbers:
            form_data["filterLandlinesAndInactiveNumbers"] = "true"

        if isinstance(recipient_phone_numbers, list):
            form_data["recipientPhoneNumber"] = json.dumps(recipient_phone_numbers)
        else:
            form_data["recipientPhoneNumber"] = recipient_phone_numbers

        if media_urls:
            form_data["mediaUrls"] = json.dumps(media_urls)

        if status_callback_url:
            form_data["statusCallbackUrl"] = status_callback_url

        files_list: list[tuple[str, Any]] = []
        if images:
            for image in images:
                if isinstance(image, tuple):
                    files_list.append(("images", image))
                else:
                    files_list.append(("images", image))

        return self._sdk._multipart_request(
            "/message/mms",
            method="POST",
            form_data=form_data,
            files=files_list if files_list else None,
            token=token,
            headers=headers,
        )

    def send_group_message(
        self,
        sender_phone_number: str,
        recipient_phone_numbers: str | list[str],
        message_body: str,
        *,
        media_urls: list[str] | None = None,
        status_callback_url: str | None = None,
        enable_shortlink: bool = False,
        enable_compression: bool = True,
        filter_landlines_and_inactive_numbers: bool = False,
        images: list[BinaryIO | tuple] | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a group MMS message to one or more recipients, with optional media attachments.

        Args:
            sender_phone_number: The phone number to send the message from.
            recipient_phone_numbers: The phone number(s) to send the message to.
            message_body: The body of the MMS message.
            media_urls: The URLs of the media attachments.
            status_callback_url: The URL to receive status callbacks.
            enable_shortlink: Whether to enable shortlink in the message.
            enable_compression: Whether to enable image compression for attachments.
            filter_landlines_and_inactive_numbers: Whether to filter out landline and inactive numbers before sending.
            images: Image files to attach to the MMS message. Each can be a file-like object
                    or a tuple of (filename, file_object, content_type).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If required parameters are missing.
        """
        self._sdk._require({
            "senderPhoneNumber": sender_phone_number,
            "recipientPhoneNumbers": recipient_phone_numbers,
        })

        form_data: dict[str, Any] = {
            "senderPhoneNumber": sender_phone_number,
            "messageBody": message_body,
            "enableShortlink": str(enable_shortlink).lower(),
            "enableCompression": str(enable_compression).lower(),
        }

        if filter_landlines_and_inactive_numbers:
            form_data["filterLandlinesAndInactiveNumbers"] = "true"

        if isinstance(recipient_phone_numbers, list):
            form_data["recipientPhoneNumber"] = json.dumps(recipient_phone_numbers)
        else:
            form_data["recipientPhoneNumber"] = recipient_phone_numbers

        if media_urls:
            form_data["mediaUrls"] = json.dumps(media_urls)

        if status_callback_url:
            form_data["statusCallbackUrl"] = status_callback_url

        files_list: list[tuple[str, Any]] = []
        if images:
            for image in images:
                if isinstance(image, tuple):
                    files_list.append(("images", image))
                else:
                    files_list.append(("images", image))

        return self._sdk._multipart_request(
            "/message/groupMessage",
            method="POST",
            form_data=form_data,
            files=files_list if files_list else None,
            token=token,
            headers=headers,
        )

    def carrier_id_lookup(
        self,
        phone_number: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Look up the carrier for a phone number. Always fresh (not cached). Billed per request.

        Args:
            phone_number: The phone number to look up (10+ digits, no + prefix).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with carrier information.

        Raises:
            SignalHouseValidationError: If required parameters are missing.
        """
        self._sdk._require({"phoneNumber": phone_number})
        return self._sdk._request(
            "/message/carrier-id",
            method="POST",
            body={"phoneNumber": phone_number},
            token=token,
            headers=headers,
        )
