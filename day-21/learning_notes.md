# Day 21 learning notes

A contact record and a company record are distinct CRM objects. An association
connects them; it does not create either object. Association labels and type
IDs can vary by portal, so this project requires an explicit value obtained
from the current HubSpot schema instead of assuming an ID.

The default operation only prints a plan. Live mode uses the configured
association type, sends an idempotent `PUT`, and reads associations back to
verify that the company ID is present. Tests use a fake client and never call
HubSpot.
