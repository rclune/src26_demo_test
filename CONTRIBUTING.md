# Contributing to this Documentation Template

This repository is maintained by member of the [Open Molecular Software Foundation (OMSF)](https://playbooks.omsf.io/). Contributions from the community are welcome and encouraged. The process for creating a pull request (PR) depends on the type and scope of your contribution. Follow the guidelines below to make your contribution as smooth as possible.

## Branching and Pull Requests
**Small Changes:** Create a new branch in this repository, make your edits, and submit a PR to `main`.
**Large Changes:** Fork the repository, make your edits, and submit a PR to merge into `main`.

 A member of the OMSF team will review your changes and leave comments as necessary until your PR is ready to merge. 

## Documentation Templates

### Contributing a New Template
Templates are stored in `docs/doc_templates` even if the document would normally reside elsewhere (e.g., `README.md` is usually in the `root`).  Any new template should have a descriptive name followed by `_template.<extension>` (typically `.md`).

There is a companion 'Playbook' that goes with this repository, also created and maintained by members of the OMSF. The Documentation Playbook <!-- TODO: link documentation playbook --> has a section for each of the different templates here. If you contribute a new template, pleas also contribute to the Documentation Playbook by creating a PR to [OMSF's playbooks-website repository](https://github.com/omsf/playbooks-website).The linked repository has its own Contributing Guide to help you get started. Each section in the playbook follows this structure: 
1. **Introductory page:** Overview of the documentation type and highlights.
2. **Fundamentals page:** Explains the *who*, *what*, *when*, *where*, *why*, and *how*.
3. **Writing Guide:** Expands on templates with prompts and writing tips.
Any extra information can go in a separate page within the section.

When your template is ready please make a PR with a title containing `New Template:` and then a few words summarizing what type of documentation the template is for. In the longer description please add more details for why the template should be added and link to the matching PR to the Documentation Playbook. The PR should request to merge to `main`.

## Modifying an Existing Template
Changes and edits are welcome. If you would like to change the file type (for example `.md` instead of `.rst`) create a new file instead. Having multiple file types for the same piece of documentation allows for greater flexibility when developers are writing documentation. 

There is a 'Documentation Playbook' <!-- TODO: Link Playbook --> that goes along with this Documentation Template. If the modifications you make to a template would change, delete, or add text to the Playbook, we also ask that you create a PR to [OMSF's playbooks-website repository](https://github.com/omsf/playbooks-website) as well. See the Contributing Guide in the linked repository for how to get started. 

The title of your PR should start with `Template change:` and then have a short description of the modification. The longer description should provide more details on what was changed and why. The PR should request to merge to `main`. 

## Creating an Issue
If you notice a problem or want to request a new feature: 
- Use a concise title, for bugs it should start with `BUG:`.
- Include these details in the description: 
    - File paths and line numbers, if relevant. 
    - Example inputs/outputs/log files/screenshots if applicable.
    - Steps you have already tried to fix the issue.
    - Links to your project or any additional context.

## Modifying the Sphinx Architecture  
This category includes anything from adding an extension to the `docs/conf.py` to changing how the API docs are rendered. Avoid submitting PRs for purely stylistic choices (themes, colors, fonts, etc.). 

For these types of changes, please star the title of your PR with `Architecture_mod:` and then a short description of the change. In the description field please provide more details on the files you changed and why. If your change requires a new extension or introduces a new dependency when building the documentation, please make note of it here. The target of your PR should be `main`.

## Modifying the Example Module
If you would like to modify or add to the example module to provide a better reference for people learning how to automatically generate documentation from docstrings, we welcome your input! 

Please make sure the changes you are suggesting are as general as possible, as the scope of the projects using this resource is broad. 

Please start the title of your PR with `Module_mod:` and then a short description of the change. In the description field please provide more details about the files you changed or created and why. The target branch for the PR should be `main`.

## Code of Conduct
PRs, comments on PRs, and Issues should all use constructive language aimed at improving this resource. Report any unacceptable behavior by emailing <info@omsf.io>.


