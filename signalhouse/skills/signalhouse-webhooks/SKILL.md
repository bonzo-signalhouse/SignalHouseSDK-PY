---
name: signalhouse-webhooks
description: >-
  Signal House webhooks: how delivery actually behaves, what a receiver can and cannot trust,
  and the retry window before an event is lost for good.
  TRIGGER when the user is setting up, debugging, or writing a receiver for Signal House
  webhooks; when webhook events appear to be missing, duplicated, or arriving late; when they
  ask how to verify a webhook is genuine; or when they are choosing an authType.
  SKIP for inbound message handling logic itself, for the SMS send path, and for questions about
  which events exist. That list is in the webhooks guide and changes independently of this.
---

# Signal House webhooks

## What cannot happen

**A receiver cannot verify that a webhook came from Signal House.** Payloads are **not signed**.
There is no HMAC, no signature header, and no request timestamp. This is verified in the
backend, not assumed.

The `authType` setting (`NONE`, `BASIC`, `API_KEY`, `OAUTH2`) authenticates *Signal House to the
receiver's endpoint*. It is the opposite direction from a signature and gives the receiver
nothing to check. Even with `BASIC` or `API_KEY`, the credential is a bearer secret sent *to*
the receiver: it proves nothing about payload integrity and any captured request can be replayed.

Practical consequences a receiver has to design around:

- **Do not treat an inbound webhook as authenticated.** Anyone who learns the URL can post to it.
  With `authType: NONE` there is nothing stopping them at all.
- **Never take a state-changing action on webhook content alone** where the action is
  irreversible or financial. Treat the webhook as a *hint that something changed*, then read the
  authoritative state back from the API before acting on it.
- **Do not put secrets in the webhook URL** as a substitute for verification. It ends up in
  proxy logs, browser history and support screenshots.

> ⚠️ Tracked as **SHGHL-2944**. Delete this section when signing ships. A workaround left in a
> skill becomes permanent.

## Retry behaviour, and when an event is gone

Delivery is a **direct HTTP POST with a 3-second timeout**, retried **3 times, 500 ms apart, with
no backoff and no jitter**. It is not queued, so there is no queue-level redelivery behind it.
Verified against the send path, which takes the retry defaults at every call site.

Two numbers matter, and they are different things:

- **A receiver has 3 seconds to respond.** Exceed it and the attempt is a failure, even if the
  work eventually succeeds on your side.
- **The whole delivery window is about 10 seconds** worst case, three attempts that can each
  burn the full timeout, plus 500 ms between them.

- A receiver that is down, restarting, or rate-limited for even a minute **loses the event
  permanently**. There is no dead-letter queue and no replay endpoint.
- **4xx responses are retried too.** The HTTP client throws on any non-2xx and the retry
  predicate accepts everything, so a receiver returning 400 gets the same doomed request three
  times.
- A slow endpoint that exceeds 3 seconds and *then* completes its work has been recorded as a
  failure and will be sent the **same event up to three times**, with no delivery id to key
  idempotency on. This is the most likely duplicate scenario in practice.

So a correct receiver:

1. **Responds inside 3 seconds, and does the work afterwards.** Acknowledge, enqueue, process out
   of band. Any processing done before responding is spending a budget you do not control, and
   blowing it converts a successful handler into a duplicate delivery.
2. **Is idempotent on the event's own identifiers** (message id, campaign id and status),
   because there is no delivery id to dedupe on.
3. **Reconciles against `GET /notification`.** This is the important one. Every event that would
   trigger a webhook also writes a **notification record, before endpoints are even looked up and
   regardless of whether delivery succeeds**. It carries the same `{timestamp, event, identifier,
   metaData}` shape and is filterable by group, status and event type.

   That makes it the durable record and the webhook merely the push. A receiver that must not
   miss anything polls it to catch up after any outage, which is the only reliable recovery,
   given there is no replay endpoint.

> ⚠️ Also tracked as **SHGHL-2944**. If the retry policy changes, these numbers are wrong and
> this section must be rewritten from the code, not adjusted from memory.

## Setting one up

Webhooks are created per group, and numbers can additionally carry their own inbound URL.
`authType` picks how Signal House authenticates to the endpoint, and `credentials` is
`{ key, secret }`, required whenever `authType` is not `NONE`.

| authType | What is sent |
|---|---|
| `NONE` | nothing. The endpoint is open to anyone who knows the URL |
| `BASIC` | HTTP Basic; `key` is the username, `secret` is the password |
| `API_KEY` | `key` holds the key; `secret` optional |
| `OAUTH2` | `secret` is the access token sent as the Authorization value; `key` is required at create but unused in outgoing headers |

`NONE` is the right default only for an endpoint that is already unreachable from the public
internet. For anything else, pick a real `authType`. It is not verification, but it stops
casual forgery.

**The table above does not cover per-number inbound URLs.** A number can carry
`primaryInboundWebhookUrl` and `secondaryInboundWebhookUrl`, and inbound messages are posted to
both. That path sends **no auth headers at all**, whatever `authType` is configured elsewhere,
it is always unauthenticated. Do not assume configuring auth on a group webhook protects the
per-number ones; it does not. Treat those URLs as fully public and put nothing behind them that
matters without an independent check.

## Where to look it up

- **Event types and payload shape:** the internal Webhooks Guide
  (`documentation/dev-documentation/04-webhooks-guide.md`). The event list changes independently
  of this skill; read it there rather than reciting it here. Note the guide does **not** document
  the per-number `primaryInboundWebhookUrl` / `secondaryInboundWebhookUrl` fields described above.
- **Whether an event actually happened:** `GET /notification`
  (`documentation/dev-documentation/03-api-reference/13-notifications.md`). The notification
  record is written independently of delivery, so it is the record and the webhook is the push.
- **Whether a delivery failed:** you largely cannot, from the outside or the inside. Failed group
  and per-number deliveries are swallowed without a server-side log, so support may have no trace
  of a delivery you never received. Do not design a process that depends on us being able to
  confirm one.
