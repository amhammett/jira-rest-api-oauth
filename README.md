Jira Rest Api OAuth
===================

Sample code demonstrating how to integrate with Jira Rest Api using OAuth.

## Workflow

The basic process for getting up and running with Jira Rest Api OAuth:

0. Prerequisites
1. Register link applications
2. Do the oauth dance
3. Make jira rest api requests

## 0. Prerequisites

Generate rsa keys to be registered in jira and used when configuring rsa tokens.

```
    make generate-rsa
```


## 1. Register link applications

Instructions available via https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-oauth-authentication/

### Navigate to Configure Application Links

Jira Administration > Applications > Configure Application Links


### Create new link

(url not important)


### Skip Outgoing Authentication

This is not required for this example


### Configure Incoming Authentication

Consumer Key `hardcoded-consumer`
Public Key `contents of rsa.pub` generated in prerequisites


## 2. Do the oauth dance

Generate OAuth tokens with pre-configured keys and user interactions

```
    make oauth-dance jira-server='https://jira.url/jira'
```

Keep track of generated oauth tokens


## 3. Make jira rest api requests

Wtih generated oauth tokens, make rest api requests

```
    make oauth-jira-projects jira-server='https://jira.url/jira' token=<token> token-secrets=<token-secret>
```

In the above example, a list of all accessible/available projects will be listed.
