#!/bin/sh

# Create Version label wtihn repo
curl \
    --data "name=v${RELEASE_TAG}&color=#eee600&description=Version%20that%20is%20affected" \
    --header "PRIVATE-TOKEN: $GIT_COMMIT_TOKEN" \
    "https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/labels"
