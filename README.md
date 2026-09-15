# SignalHouse Python SDK

Python SDK for the SignalHouse API. Manage SMS/MMS messaging, phone numbers, 10DLC brands & campaigns, billing, and more.

## Installation

```bash
pip install signalhouse
```

## Agent skills

The package bundles the Signal House agent skills, which teach a coding agent the order the
platform enforces, what carriers require, and what a send cannot do before a campaign is approved.

A Python wheel cannot run anything at install time, so place them with one command:

```bash
signalhouse-skills            # install into this project
signalhouse-skills --list     # show what is bundled and which release it came from
signalhouse-skills --force    # create the agent directory if the project has none yet
```

It only ever writes inside the project, never your home directory, and never overwrites a skill you
have edited.

Or install from source:

```bash
pip install -e .
```

## Quick Start

```python
from signalhouse import SignalHouseSDK

# Initialize the SDK
sdk = SignalHouseSDK(
    api_key="your-api-key",
    base_url="https://v2.signalhouse.io",
)

# Send an SMS
response = sdk.messages.send_sms(
    sender_phone_number="15551234567",
    recipient_phone_numbers="15559876543",
    message_body="Hello from SignalHouse!",
)

if response["success"]:
    print("Message sent!", response["data"])
else:
    print("Error:", response["error"])
```

## Authentication

All methods accept an optional `token` parameter to override the default API key per-request:

```python
response = sdk.billing.get_wallet("G12345678", token="user-jwt-token")
```

## Domains

The SDK is organized into domain modules matching the SignalHouse API:

| Domain | Description |
|--------|-------------|
| `sdk.auth` | Login, password reset, auth history |
| `sdk.billing` | Wallets, payment methods, funds, invoices, fees |
| `sdk.brands` | 10DLC brand registration and management |
| `sdk.campaigns` | 10DLC campaign management |
| `sdk.groups` | Group management |
| `sdk.landings` | Landing page management (with file uploads) |
| `sdk.messages` | Send SMS/MMS/Group MMS, message logs, analytics |
| `sdk.notifications` | Notification management |
| `sdk.numbers` | Phone number purchase, assignment, transfer, lookup |
| `sdk.shortlinks` | URL shortlink operations |
| `sdk.subgroups` | Subgroup management |
| `sdk.subscriptions` | Subscription management |
| `sdk.users` | User and service user management |
| `sdk.webhooks` | Webhook management |

## Admin Methods

Some domains have admin-only methods accessible via the `.admin` sub-object. Enable them by passing `enable_admin=True`:

```python
sdk = SignalHouseSDK(
    api_key="your-api-key",
    base_url="https://v2.signalhouse.io",
    enable_admin=True,
)

# Admin-only: approve a campaign
response = sdk.campaigns.admin.approve_campaign("campaign-id", token="admin-token")

# Admin-only: list all groups
response = sdk.groups.admin.get_groups(page=1, limit=20, token="admin-token")
```

Domains with admin sub-objects: `campaigns`, `groups`, `subscriptions`, `users`.

## Response Format

All methods return a standardized dictionary:

**Success:**
```python
{"success": True, "data": {...}, "status": 200}
```

**Error:**
```python
{"success": False, "error": "Error message", "status": 400}
```

## File Uploads

The `landings` and `messages` domains support multipart file uploads:

```python
# Create a landing page with a logo
with open("logo.png", "rb") as f:
    response = sdk.landings.create_landing(
        landing_data={
            "brandId": "brand-id",
            "description": "My landing page",
            "primaryBackgroundColor": "#FFFFFF",
            "secondaryBackgroundColor": "#F0F0F0",
            "primaryTextColor": "#000000",
            "secondaryTextColor": "#333333",
        },
        file=("logo.png", f, "image/png"),
    )

# Send an MMS with images
with open("photo.jpg", "rb") as img:
    response = sdk.messages.send_mms(
        sender_phone_number="15551234567",
        recipient_phone_numbers=["15559876543"],
        message_body="Check this out!",
        images=[("photo.jpg", img, "image/jpeg")],
    )
```

## Error Handling

```python
from signalhouse import SignalHouseSDK, SignalHouseValidationError

sdk = SignalHouseSDK(api_key="your-key", base_url="https://v2.signalhouse.io")

try:
    # This will raise SignalHouseValidationError because group_id is required
    sdk.billing.get_wallet("")
except SignalHouseValidationError as e:
    print(f"Validation error: {e.message}")  # "Missing required parameter: groupId"
```

## Requirements

- Python 3.10+
- `requests` >= 2.28.0


## Canada (SHGHL-3190)

The number purchase methods accept optional ISO-2 `country` (US by default, CA for Canada). For example, `numbers.purchase_phone_number(phone_numbers, subgroup_id, country="CA")`. Toll-Free quantity purchases accept the same country. A 202 purchase response means queued; use existing status polling/webhooks. Canadian Virtual Long Codes become READY on successful provisioning without a brand or campaign. Canadian Toll-Free uses the shared approved brand/campaign records.

Estimate without sending or charging: `messages.estimate_message(sender, recipients, body, message_type="MMS")`. Estimates accept 1–100 Canadian recipients, return per-recipient rates and totals in microdollars, and use the same retail rate function as dispatch. SMS is the default type; MMS/group-MMS bill one segment per recipient. Standard carrier rates are 75,500; Ice Wireless/Iristel and unknown or unpriced carriers use 81,000. Carrier cache misses or disabled lookup use the upper fallback. Estimates return pricing fields only (phoneNumber, rate, amount, fallback); carrier names are not exposed. Estimates can change when carrier information changes. Canadian sends reject US +1 numbers based on the NANP country assignment. Uploaded media must be an image under 1 MiB; existing media URL support remains available.

Available-number searches return `{ numbers, numberCount? }`. `numberCount` is omitted when the total is unknown, including Canadian geographic and US city searches; do not treat the page length as a total. These filtered searches have a 20-second discovery deadline and return HTTP 503 when incomplete. Narrow the location/NPA/NXX or retry later; an error does not mean no stock. Successful Infobip discovery samples may be reused for 15 seconds across pages. Availability is rechecked during purchase.


Brand, campaign, phone-number, message and opt-out records carry `region` (ISO-2). Treat absent, null or blank historical regions as US. Canadian Virtual Long Code messages use `channel: virtualLongCode` and nullable `brandId`/`campaignId`; consumers must tolerate these values. STOP/START consent for these numbers is scoped to the owning group and sender number. Existing US calls remain compatible.


### Geographic availability search

The availability path supports optional `city` as a case-insensitive prefix within an explicit `country` (`CA` or `US`) and `state` (province/state code). City must be supplied with both country and state. Example: `get_available_phone_numbers(country="CA", state="QC", city="Charny", npa="367", nxx="883", limit=10)`. Canadian province, city, NPA and NXX matches are checked before the result limit; unrelated substring matches are excluded. Availability may change before purchase.
