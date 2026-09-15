"""AI Agents domain for the SignalHouse SDK."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from urllib.parse import quote

if TYPE_CHECKING:
    from ..client import SignalHouseSDK


class Agents:
    """AI Agent profile management operations (customer-facing /agent domain).

    Agent profiles hold the configuration for an AI agent: its name, prompts,
    guardrails, voice, and LLM backend. Profiles are scoped to a group (and
    optionally a subgroup); that scope is immutable after creation.
    """

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk

    def get_agent_profiles(
        self,
        *,
        group_id: str,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """List the agent profiles under a group.

        Allowed roles: api, admin, developer, billing, user.

        Args:
            group_id: The group whose profiles to list (required).
            page: The page number for pagination.
            limit: The number of items per page.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If group_id is missing.
        """
        self._sdk._require({"groupId": group_id})
        query_string = self._sdk._get_query_string({
            "groupId": group_id,
            "page": page,
            "limit": limit,
        })
        return self._sdk._request(
            f"/agent/profiles{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_agent_profile(
        self,
        agent_profile_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a single agent profile by ID.

        Allowed roles: api, admin, developer, billing, user.

        Args:
            agent_profile_id: The ID of the agent profile to fetch.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If agent_profile_id is missing.
        """
        self._sdk._require({"agentProfileId": agent_profile_id})
        safe_id = quote(str(agent_profile_id), safe="")
        return self._sdk._request(
            f"/agent/profiles/{safe_id}",
            method="GET",
            token=token,
            headers=headers,
        )

    def create_agent_profile(
        self,
        profile_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a new agent profile.

        Allowed roles: api, admin, developer.

        Args:
            profile_data: The data for the agent profile to create. Required fields:
                groupId (str, starts with 'G') and name (str). Optional fields:
                subgroupId (str, starts with 'S', null = group-level agent),
                status ("active" | "inactive", defaults to "active"), systemPrompt,
                greeting, guardrails, voiceId (str, nullable), llmProvider
                ("bedrock" | "openai" | "anthropic" | "groq", defaults to "bedrock"),
                llmModel (str, nullable), and temperature (number 0-2).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If profile_data is missing.
        """
        self._sdk._require({"profileData": profile_data})
        return self._sdk._request(
            "/agent/profiles",
            method="POST",
            body=profile_data,
            token=token,
            headers=headers,
        )

    def update_agent_profile(
        self,
        id: str,
        update_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update an existing agent profile.

        Allowed roles: api, admin, developer.

        Args:
            id: The ID of the agent profile to update.
            update_data: The fields to update. All create fields are accepted except
                groupId and subgroupId — the agent's scope is immutable. Updatable
                fields: name, status ("active" | "inactive"), systemPrompt, greeting,
                guardrails, voiceId (str, nullable), llmProvider ("bedrock" | "openai"
                | "anthropic" | "groq"), llmModel (str, nullable), temperature (0-2).
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
            f"/agent/profiles/{safe_id}",
            method="PUT",
            body=update_data,
            token=token,
            headers=headers,
        )

    def delete_agent_profile(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete (inactivate) an agent profile by its ID.

        Allowed roles: api, admin, developer.

        Args:
            id: The ID of the agent profile to delete.
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
            f"/agent/profiles/{safe_id}",
            method="DELETE",
            token=token,
            headers=headers,
        )

    def send_agent_message(
        self,
        *,
        agent_profile_id: str,
        channel: str,
        message: str,
        conversation_id: str | None = None,
        contact_identifier: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a message to an agent and get its reply (webchat / SMS).

        Omit conversation_id to start a new conversation, or pass one to continue an
        existing one. Runs the agent's LLM tool loop server-side and returns the
        assistant's reply along with any tools it invoked.

        Allowed roles: api, admin, developer, billing, user.

        Args:
            agent_profile_id: The agent to talk to (required).
            channel: The channel: "webchat", "sms", or "voice" (required).
            message: The user's message (required).
            conversation_id: Continue this conversation; omit to start a new one.
            contact_identifier: The far-end identifier (webchat visitor id, sender number).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict with conversationId, conversationSessionId,
            reply, toolInvocations, and ok.

        Raises:
            SignalHouseValidationError: If agent_profile_id, channel, or message is missing.
        """
        self._sdk._require({
            "agentProfileId": agent_profile_id,
            "channel": channel,
            "message": message,
        })
        body: dict[str, Any] = {
            "agentProfileId": agent_profile_id,
            "channel": channel,
            "message": message,
        }
        if conversation_id is not None:
            body["conversationId"] = conversation_id
        if contact_identifier is not None:
            body["contactIdentifier"] = contact_identifier
        return self._sdk._request(
            "/agent/messages",
            method="POST",
            body=body,
            token=token,
            headers=headers,
        )

    def get_agent_channel_settings(
        self,
        agent_profile_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """List an agent's per-channel settings.

        Allowed roles: api, admin, developer, billing, user.

        Args:
            agent_profile_id: The agent whose channel settings to list.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If agent_profile_id is missing.
        """
        self._sdk._require({"agentProfileId": agent_profile_id})
        safe_id = quote(str(agent_profile_id), safe="")
        return self._sdk._request(
            f"/agent/profiles/{safe_id}/channels",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_agent_channel_setting(
        self,
        agent_profile_id: str,
        channel: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a single per-channel setting for an agent.

        Allowed roles: api, admin, developer, billing, user.

        Args:
            agent_profile_id: The agent the setting belongs to.
            channel: The channel — "webchat", "sms", or "voice".
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If agent_profile_id or channel is missing.
        """
        self._sdk._require({"agentProfileId": agent_profile_id, "channel": channel})
        safe_id = quote(str(agent_profile_id), safe="")
        safe_channel = quote(str(channel), safe="")
        return self._sdk._request(
            f"/agent/profiles/{safe_id}/channels/{safe_channel}",
            method="GET",
            token=token,
            headers=headers,
        )

    def upsert_agent_channel_setting(
        self,
        agent_profile_id: str,
        channel: str,
        setting_data: dict[str, Any] | None = None,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create or update (upsert) an agent's per-channel setting.

        One row per (agent, channel); the channel comes from the path.

        Allowed roles: api, admin, developer.

        Args:
            agent_profile_id: The agent the setting belongs to.
            channel: The channel — "webchat", "sms", or "voice".
            setting_data: Fields to set: allowedTools (list[str]), enabled (bool),
                channelPrompt (str), greeting (str | None).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If agent_profile_id or channel is missing.
        """
        self._sdk._require({"agentProfileId": agent_profile_id, "channel": channel})
        safe_id = quote(str(agent_profile_id), safe="")
        safe_channel = quote(str(channel), safe="")
        return self._sdk._request(
            f"/agent/profiles/{safe_id}/channels/{safe_channel}",
            method="PUT",
            body=setting_data or {},
            token=token,
            headers=headers,
        )

    def delete_agent_channel_setting(
        self,
        agent_profile_id: str,
        channel: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete an agent's per-channel setting.

        Allowed roles: api, admin, developer.

        Args:
            agent_profile_id: The agent the setting belongs to.
            channel: The channel — "webchat", "sms", or "voice".
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If agent_profile_id or channel is missing.
        """
        self._sdk._require({"agentProfileId": agent_profile_id, "channel": channel})
        safe_id = quote(str(agent_profile_id), safe="")
        safe_channel = quote(str(channel), safe="")
        return self._sdk._request(
            f"/agent/profiles/{safe_id}/channels/{safe_channel}",
            method="DELETE",
            token=token,
            headers=headers,
        )

    def get_tenant_ai_settings(
        self,
        *,
        group_id: str,
        subgroup_id: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Read the tenant AI settings for a scope (group, or a subgroup within it).

        Returns the scope's own row only — no group-level fallback.

        Allowed roles: api, admin, developer, billing, user.

        Args:
            group_id: The group (required).
            subgroup_id: The subgroup; omit for the group-level settings.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If group_id is missing.
        """
        self._sdk._require({"groupId": group_id})
        query_string = self._sdk._get_query_string({"groupId": group_id, "subgroupId": subgroup_id})
        return self._sdk._request(
            f"/agent/tenant-settings{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def upsert_tenant_ai_settings(
        self,
        *,
        group_id: str,
        subgroup_id: str | None = None,
        settings_data: dict[str, Any] | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create or update (upsert) the tenant AI settings for a scope.

        The scope is identified by the query params; the body carries the fields.

        Allowed roles: api, admin, developer.

        Args:
            group_id: The group (required).
            subgroup_id: The subgroup; omit for the group-level settings.
            settings_data: Fields to set: brandName (str), tone (str), timezone (IANA str),
                businessHours (list of {day, closed, open, close}), afterHoursMessage (str).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If group_id is missing.
        """
        self._sdk._require({"groupId": group_id})
        query_string = self._sdk._get_query_string({"groupId": group_id, "subgroupId": subgroup_id})
        return self._sdk._request(
            f"/agent/tenant-settings{query_string}",
            method="PUT",
            body=settings_data or {},
            token=token,
            headers=headers,
        )

    def delete_tenant_ai_settings(
        self,
        *,
        group_id: str,
        subgroup_id: str | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete the tenant AI settings for a scope.

        Allowed roles: api, admin, developer.

        Args:
            group_id: The group (required).
            subgroup_id: The subgroup; omit for the group-level settings.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If group_id is missing.
        """
        self._sdk._require({"groupId": group_id})
        query_string = self._sdk._get_query_string({"groupId": group_id, "subgroupId": subgroup_id})
        return self._sdk._request(
            f"/agent/tenant-settings{query_string}",
            method="DELETE",
            token=token,
            headers=headers,
        )

    def get_knowledge_items(
        self,
        *,
        group_id: str,
        subgroup_id: str | None = None,
        agent_profile_id: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """List the knowledge-base items an agent can answer from (RAG).

        Scoped to a group, optionally narrowed to a subgroup and/or a single agent.
        Paginated: results are bounded (server default 25 per page, max 100).

        Allowed roles: api, admin, developer, billing, user.

        Args:
            group_id: The group whose knowledge to list (required).
            subgroup_id: Narrow to a subgroup.
            agent_profile_id: Narrow to one agent.
            page: Page number (1-based) for pagination.
            limit: Items per page (max 100; server default 25).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If group_id is missing.
        """
        self._sdk._require({"groupId": group_id})
        query_string = self._sdk._get_query_string({"groupId": group_id, "subgroupId": subgroup_id, "agentProfileId": agent_profile_id, "page": page, "limit": limit})
        return self._sdk._request(
            f"/agent/knowledge{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_knowledge_item(
        self,
        knowledge_item_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a single knowledge item by ID.

        Allowed roles: api, admin, developer, billing, user.

        Args:
            knowledge_item_id: The ID of the knowledge item to fetch.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If knowledge_item_id is missing.
        """
        self._sdk._require({"knowledgeItemId": knowledge_item_id})
        safe_id = quote(str(knowledge_item_id), safe="")
        return self._sdk._request(
            f"/agent/knowledge/{safe_id}",
            method="GET",
            token=token,
            headers=headers,
        )

    def create_knowledge_item(
        self,
        item_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create a knowledge item. The raw text is stored; Atlas Vector Search owns the embedding.

        Allowed roles: api, admin, developer.

        Args:
            item_data: The knowledge fields. Required: groupId (starts with 'G'), text.
                Optional: subgroupId (starts with 'S', nullable), agentProfileId (nullable =
                shared across the tenant's agents), title, source ("manual" | "url" |
                "document" | "import"), enabled (bool), metadata (dict | None).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If item_data is missing.
        """
        self._sdk._require({"itemData": item_data})
        return self._sdk._request(
            "/agent/knowledge",
            method="POST",
            body=item_data,
            token=token,
            headers=headers,
        )

    def update_knowledge_item(
        self,
        id: str,
        update_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update a knowledge item. The scope (group/subgroup/agent) is immutable.

        Allowed roles: api, admin, developer.

        Args:
            id: The ID of the knowledge item to update.
            update_data: The fields to update: title, text, source, enabled, metadata.
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
            f"/agent/knowledge/{safe_id}",
            method="PUT",
            body=update_data,
            token=token,
            headers=headers,
        )

    def delete_knowledge_item(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete a knowledge item by its ID.

        Allowed roles: api, admin, developer.

        Args:
            id: The ID of the knowledge item to delete.
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
            f"/agent/knowledge/{safe_id}",
            method="DELETE",
            token=token,
            headers=headers,
        )

    def get_agent_tools(
        self,
        *,
        group_id: str,
        subgroup_id: str | None = None,
        agent_profile_id: str | None = None,
        type: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """List the tools defined under a group (webhook, configured builtin, mcp).

        webhookAuth secrets are redacted in the response. Paginated (default 25, max 100).

        Allowed roles: api, admin, developer, billing, user.

        Args:
            group_id: The group whose tools to list (required).
            subgroup_id: Narrow to a subgroup.
            agent_profile_id: Narrow to one agent.
            type: Narrow to a tool type — "builtin", "webhook", or "mcp".
            page: Page number (1-based) for pagination.
            limit: Items per page (max 100; server default 25).
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If group_id is missing.
        """
        self._sdk._require({"groupId": group_id})
        query_string = self._sdk._get_query_string({"groupId": group_id, "subgroupId": subgroup_id, "agentProfileId": agent_profile_id, "type": type, "page": page, "limit": limit})
        return self._sdk._request(
            f"/agent/tools{query_string}",
            method="GET",
            token=token,
            headers=headers,
        )

    def get_agent_tool(
        self,
        agent_tool_id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Get a single agent tool by ID. webhookAuth secrets are redacted.

        Allowed roles: api, admin, developer, billing, user.

        Args:
            agent_tool_id: The ID of the tool to fetch.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If agent_tool_id is missing.
        """
        self._sdk._require({"agentToolId": agent_tool_id})
        safe_id = quote(str(agent_tool_id), safe="")
        return self._sdk._request(
            f"/agent/tools/{safe_id}",
            method="GET",
            token=token,
            headers=headers,
        )

    def create_agent_tool(
        self,
        tool_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Create an agent tool. A webhook tool's webhookUrl must be an https URL that does not
        target a private/internal address. webhookAuth is stored and never echoed back.

        Allowed roles: api, admin, developer.

        Args:
            tool_data: The tool fields. Required: groupId (starts with 'G'), name, description.
                Type-specific: type ("builtin" | "webhook" | "mcp"); webhook -> webhookUrl,
                builtin -> builtinKey, mcp -> mcpServerUrl. Optional: subgroupId, agentProfileId
                (nullable), parametersSchema, config, channels, enabled, and webhookAuth — which
                MUST be {"headers"?: {name: value}, "signingSecret"?: str} (any other shape, e.g.
                {"header", "value"}, is rejected with a 400). headers are sent verbatim on every
                call (reserved/framing and x-signalhouse-* names are rejected); signingSecret makes
                us send X-SignalHouse-Signature: sha256=HMAC-SHA256(f"{X-SignalHouse-Timestamp}.{rawBody}")
                so you can verify the call and reject replays. Stored, never returned.
            token: Optional bearer token for authentication.
            headers: Additional headers to include in the request.

        Returns:
            Standardized response dict.

        Raises:
            SignalHouseValidationError: If tool_data is missing.
        """
        self._sdk._require({"toolData": tool_data})
        return self._sdk._request(
            "/agent/tools",
            method="POST",
            body=tool_data,
            token=token,
            headers=headers,
        )

    def update_agent_tool(
        self,
        id: str,
        update_data: dict[str, Any],
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Update an agent tool. The scope is immutable; a supplied webhookUrl is SSRF-checked.

        Allowed roles: api, admin, developer.

        Args:
            id: The ID of the tool to update.
            update_data: The fields to update: name, description, type, builtinKey,
                parametersSchema, config, webhookUrl, webhookAuth, mcpServerUrl, channels, enabled.
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
            f"/agent/tools/{safe_id}",
            method="PUT",
            body=update_data,
            token=token,
            headers=headers,
        )

    def delete_agent_tool(
        self,
        id: str,
        *,
        token: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Delete an agent tool by its ID.

        Allowed roles: api, admin, developer.

        Args:
            id: The ID of the tool to delete.
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
            f"/agent/tools/{safe_id}",
            method="DELETE",
            token=token,
            headers=headers,
        )
