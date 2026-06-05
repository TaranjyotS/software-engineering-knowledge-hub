# Security Policy

This repository may connect to Confluence through local environment variables or GitHub Secrets.

## Do not commit

- `.env`
- API tokens
- Passwords
- Personal access tokens
- Private workspace URLs if you do not want them public

## If a token is exposed

1. Revoke the token immediately in Atlassian/GitHub.
2. Generate a new token.
3. Update your local `.env` and GitHub Secrets.
4. Remove the exposed value from Git history if it was committed.
