"""Voice domain — wraps the voice-backend service (mounted under /voice).

Groups all voice-service sub-resources under a single namespace, accessed via
``sdk.voice.*``:

* ``sdk.voice.sip_trunks``   — SIP trunk (peer-to-peer connections to PBX/carrier).
* ``sdk.voice.sip_profiles`` — SIP profile / endpoint (single registerable UA).
* ``sdk.voice.calls``        — Outbound call origination + call log queries.
* ``sdk.voice.tokens``       — Mint ephemeral SIP credentials for the browser voice SDK.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .sip_trunks import SipTrunks
from .sip_profiles import SipProfiles
from .calls import Calls
from .tokens import Tokens

if TYPE_CHECKING:
    from ...client import SignalHouseSDK


class Voice:
    """Voice domain namespace. Accessed via ``sdk.voice``."""

    def __init__(self, sdk: SignalHouseSDK) -> None:
        self._sdk = sdk
        self.sip_trunks = SipTrunks(sdk)
        self.sip_profiles = SipProfiles(sdk)
        self.calls = Calls(sdk)
        self.tokens = Tokens(sdk)


__all__ = ["Voice", "SipTrunks", "SipProfiles", "Calls", "Tokens"]
