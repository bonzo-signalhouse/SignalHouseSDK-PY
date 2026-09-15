---
name: signalhouse-setup
description: >-
  Getting a Signal House integration authenticated and wired: login vs service-user tokens, what a
  token is scoped to, SDK initialization, and why webhooks come before the first write.
  TRIGGER when the user is starting a Signal House integration, asks how to authenticate, asks for
  an API key or token, is choosing a base URL, is installing or initializing the SDK, is getting a
  401 or 403, or asks why their token stopped working.
  SKIP for message sending, 10DLC registration, number purchase and webhook event semantics, which
  have their own skills. This one ends at "the first authenticated call succeeds".
---

# Signal House setup

## What cannot happen

**A login token cannot carry a server integration.** `POST /auth` returns a **short-lived session
JWT**, measured in hours. It is the right token for a user acting in a session and the wrong token
for anything that runs unattended. A cron job built on a login token works all afternoon and fails
overnight.

Both lifetimes are set per environment (`JWT_USER_EXPIRES_IN`, `JWT_SYSTEM_EXPIRES_IN`), so treat
the session token as short and the service token as long, and read the exact values from the
Authentication guide or the environment rather than quoting a number to a customer.

**A service user cannot be bootstrapped from nothing.** `POST /user/serviceuser` needs an existing
group and a token that is already privileged enough to mint one. The first credential in a new
integration comes from a human logging in or from Signal House provisioning it, not from an API call
made with no credential.

**`role: "signalhouse_api"` is not available to customers.** The two roles `POST /user/serviceuser`
accepts are `api` (customer key, scoped to one `groupId`) and `signalhouse_api` (internal, requires
`signalhouse_admin` credentials). A customer caller asking for the internal role gets a **403**. If
an integration seems to need it, the requirement is wrong.

**The API key is shown once.** The token is signed and returned at creation and never stored on the
user record, so no endpoint can hand it back. Losing it means creating another service user, not
recovering the old key.

**A group under compliance rejection cannot create API keys at all.** Service-user creation is gated
on the group's compliance state and fails with a group-rejected error rather than a validation error.
Staff roles are exempt. When key creation fails for one group and works for another, check the
account's standing before debugging the request.

**Being authenticated does not mean being able to send.** Setup ends with a working credential.
Sending additionally requires a verified brand, an `ACTIVE` campaign, and a number in `READY` status
on it. See `signalhouse-10dlc`.

## Order of operations

1. **Get a token.** Human session → `POST /auth`, short-lived. Server integration → a service user,
   long-lived. Do not build a server integration on a login token and plan to "refresh it later".
2. **Know the group.** A customer service user (`role: "api"`) is bound to one `groupId`, an
   8-character id beginning with `G`. That scoping is what limits the damage of a leaked
   key, so one key per group is the design, not an inconvenience to work around.
3. **Initialize the SDK** with `apiKey` and `baseUrl`. The `apiKey` is the default credential on
   every request; `options: { token }` overrides it per call, which is how an app acting for many
   users should work rather than reinitializing the SDK per user.
4. **Make one read call** and check the envelope before writing anything.
5. **Register webhooks before the first write.** Brand registration, campaign registration, number
   purchase and message delivery all resolve out of band, minutes to days later. An integration
   without webhooks discovers outcomes by polling, burns rate limit doing it, and still finds out
   late. See `signalhouse-webhooks`.

## Reading the response

The SDK returns an **envelope**, and most failures arrive inside it rather than as an exception:

```
{ success: true|false, data: <payload>, error: <body>, status: <http status> }
```

- Branch on `response.success` and `response.status`, not on a try/catch alone.
- **Rate limiting is a `429` in the envelope**, not a throw. Detect it as `response.status === 429`
  and back off; matching on the error string is brittle.
- Client-side validation failures DO throw (`SignalHouseValidationError`). Those are not retryable,
  and retrying an invalid payload just spends the retry budget.
- A `401` means the token expired or was revoked. Re-authenticate; do not retry the same token.

Response shapes are nested differently per endpoint and the nesting is not guessable. Read the
current shape from the API reference rather than assuming it matches a sibling endpoint.

## Where to look it up

- **Auth flows, service users, the full role table, token practice:** the internal Authentication
  guide (`documentation/dev-documentation/02-authentication.md`).
- **First working call end to end:** the Quickstart (`01-quickstart.md`).
- **Envelope shapes, error classes and status codes:** the Error Handling guide (`08-error-handling.md`).
- **Backoff, batching and pagination:** the Rate Limits guide (`09-rate-limits.md`).
- **What a role is allowed to do:** the role table in the Authentication guide. Roles are checked
  server-side, so a plan that assumes more access than the token has fails at the call, not earlier.
