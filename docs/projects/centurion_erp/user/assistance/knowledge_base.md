---
title: Knowledge Base
description: Knowledge Base user documentation for Centurion ERP by No Fuss Computing
date: 2024-07-19
template: project.html
about: https://gitlab.com/nofusscomputing/infrastructure/configuration-management/centurion_erp
---

A Knowledge Base forms part of the ITSM, specifically Information Management. Information Management is intended to capture all available data within an organization, not just the IT department. This information is then categorised and presented to the users that require it.


## Article

Article content is intended to be written in markdown, which provides for a richer user experience. To create an article the following fields are are available:

- Title _Article title_

- Summary _Short summary of the article_

- Content _article content_

- Category _article category_

- Release Date _date to publish the article_

    !!! info
        If no release date is set, the article will be published immediately.

- Expiry Date _date the article expires_

    !!! info
        Not specifying an expiry date means that the article will remain published indefinitely.

- Target Team(s) _team(s) to make the article available for_

- Target User _user to target the article for_

- Responsible User _the user who is considered the owner_

- Responsible Team(s) _the team or teams who is considered the owner_

- Public _if the article is to be made available to public user (users who are not logged in)_ _[See #144](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/144)_

!!! info
    An article must either have a target user or target group. Not both.

!!! info
    An article can have a responsible user or responsible team(s). Not both.


### Notes

Notes can be added to an article that is intended to be article owner notes. these notes are not made available as part of the article.


## Categories

Categories are available to offer an ability to filter/sort articles. Fields available as part of Knowledge Base Categories are:

- Name _Category Name_

- Parent _Parent Category for nesting categories_

- Target Team _Team the categories articles should be made available for_

- Target User _User the categories articles should be made available for_

!!! info
    A KB Category must either have a target user or target group. Not both.
