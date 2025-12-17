# PROCESSING TOOLS

This repository and its counterpart living in GitLab contain scripts, utilities and automations used by the ObsInt processing team.

The [GitLab - processing-tools](https://gitlab.cee.redhat.com/ccx/processing-team/processing-tools) repository is used only for scripts that need to run behind VPN - directly in GitLab - such as gathering open GitLab Merge requests. 

**You should always use this GitHub repository, unless the workload needs to be behind VPN and you ensure synchronisation with this repositry**

## Structure
- Generation and sending of test archives (local and ephemeral version)
- Open PRs for GitHub repositories action running once per day
- Open MRs for GitLab repositories commited from GitLab CICD once per day
- GlitchTip <-> Jira integration tool action running once per day (and a separate action to close issues to possibly be run manually)

## Related
- [GitLab processing-tools](https://gitlab.cee.redhat.com/ccx/processing-team/processing-tools) - running scraping from GL repositiories such as open MRs
- [Molodec](https://gitlab.cee.redhat.com/ccx/molodec) - archive generation, sending
- [Local deployment of processing services](https://github.com/RedHatInsights/obsint-processing-local-deploy) - local deployment of processing services
- [Juan's utils](https://github.com/juandspy/utils) - Juan's repo full of automations and scripts
- [GlitchTip <-> Jira Integration](https://gitlab.cee.redhat.com/jdiazsua/jira-glitchtip-issues-closer) - source for Juan's automation (included in this repo)
