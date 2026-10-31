# Security Policy

## Supported Versions

Only the latest release of `devspeed` receives active security updates and vulnerability patches.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

## Reporting a Vulnerability

We take the security of `devspeed` and our users' developer workstations seriously.

If you believe you have discovered a vulnerability (such as insecure credential handling, container escape vector, shell injection, or unsafe socket binding):

1. **Do not disclose the issue publicly** on GitHub Issues, Discussions, or social media.
2. Please submit a confidential advisory report via GitHub's [Private Vulnerability Reporting](https://github.com/ZitouniNidhal/devspeed/security/advisories/new).
3. If GitHub Private Vulnerability Reporting is unavailable, send an email to the maintainer directly at `zitouninidhal@gmail.com` with:
   - A description of the issue and potential impact
   - Minimal steps or a proof-of-concept configuration (`devspeed.yaml`) to reproduce the behavior
   - Any suggested mitigations or patches

### Response Timeline

- **Initial Acknowledgement**: Within 48 hours.
- **Triage & Assessment**: Within 5 business days.
- **Patch Release & Disclosure**: We will collaborate with you to release a fix and coordinate disclosure.
