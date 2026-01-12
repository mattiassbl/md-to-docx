# Technical Guide: Implementing GCP Workload Identity Federation for Apache NiFi with Azure AD On-Prem

## 1. Executive Summary

This document details the configuration required to enable Apache NiFi (running on-premise or Azure) to authenticate with Google Cloud Platform (GCP) without managing static Service Account keys.

By adopting Workload Identity Federation, we replace long-lived .json credential files with a trust relationship. NiFi exchanges its local external identity (Azure AD token) for short-lived GCP access tokens automatically. This eliminates the need for key rotation, reduces the attack surface, and aligns with modern Zero Trust security practices.

## 2. Architecture Overview

Instead of a static secret, the authentication flow works as follows:

Trust Establishment
 Configure GCP to trust an external Identity Provider (IdP), such as Azure AD (Entra ID) for on-prem environments.

Token Exchange

NiFi presents its external credential (Azure AD JWT) to Google Security Token Service (STS).

Google STS verifies the credential against the configured trust policy.

If valid, Google returns a temporary Federated Access Token.

Impersonation
 NiFi uses this federated token to impersonate a specific GCP Service Account to access resources (GCS, BigQuery, Pub/Sub).

## 3. Implementation Prerequisites

GCP Permissions:
 roles/iam.workloadIdentityPoolAdmin and roles/iam.serviceAccountAdmin.

NiFi Version:
 NiFi 1.15+ (recommended for updated GCP client libraries).

External Environment:

Azure AD (On-Prem):

Enterprise Application registered in Entra ID.

NiFi obtains a JWT from Azure AD using Client Credentials Flow or Managed Identity (if running on Azure VM).

## 4. Configuration Steps

# Phase 1: GCP Identity Configuration

Run these commands in the Google Cloud SDK (gcloud CLI).

## 1.1 Create the Workload Identity Pool

```bash

gcloud iam workload-identity-pools create "nifi-external-pool" \

--location="global" \

--display-name="NiFi External Pool" \

--description="Trust pool for external NiFi clusters"

```

## 1.2 Create the Identity Provider for Azure AD

```bash
gcloud iam workload-identity-pools providers create-oidc "nifi-azuread-provider" \

--location="global" \

--workload-identity-pool="nifi-external-pool" \

--issuer-uri="https://login.microsoftonline.com/<TENANT_ID>/v2.0" \

--allowed-audiences="<APPLICATION_ID_URI>" \

--attribute-mapping="google.subject=assertion.sub"

```


Notes:

issuer-uri is the Azure AD OpenID Connect endpoint for your tenant.

allowed-audiences should match the Application ID URI of your registered app in Entra ID.

Ensure NiFi can request tokens from Azure AD using Client Credentials Flow.

## 1.3 Bind the Pool to a Service Account

```bash

PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format="value(projectNumber)")

POOL_ID="nifi-external-pool"

SA_EMAIL="your-service-account@your-project.iam.gserviceaccount.com"

gcloud iam service-accounts add-iam-policy-binding $SA_EMAIL \

--role="roles/iam.workloadIdentityUser" \

--member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$POOL_ID/*"

```

For production, restrict this to specific Azure AD app IDs.

# Phase 2: Generate Credential Configuration

Instead of a private key, generate a Client Configuration File:

```bash

gcloud iam workload-identity-pools create-cred-config \

projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/$POOL_ID/providers/YOUR_PROVIDER_ID \

--service-account="$SA_EMAIL" \

--output-file="nifi-credential-config.json"

```

Securely copy this file to NiFi servers (e.g., /opt/nifi/conf/keys/).

# Phase 3: NiFi Component Configuration

Log in to NiFi Canvas.

Navigate to Controller Services.

Add or edit GCPCredentialsControllerService.

Configure:

Service Account JSON File: /opt/nifi/conf/keys/nifi-credential-config.json

Use Compute Engine Credentials: false

Test with a processor like ListGCSBucket.

## 5. Summary of Benefits

Feature | Old Method (Static Keys) | New Method (Workload Identity)

--- | --- | ---

Secret Management | Requires storing high-risk .json private keys | No secrets; only config files

Rotation | Manual rotation required | Automatic; tokens expire in 1 hour

Security Risk | Leaked key grants permanent access | Leaked config is useless without Azure AD context