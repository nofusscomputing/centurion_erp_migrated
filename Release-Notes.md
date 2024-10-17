## Version 1.3

API redesign in preparation for moving the UI out of centurion to it's [own project](https://github.com/nofusscomputing/centurion_erp_ui). This release introduces a **Feature freeze** to the current UI. Only bug fixes will be done for the current UI.

- A large emphasis is being placed upon API stability. This is being achieved by ensuring the following:

    - Actions can only be carried out by users whom have the correct permissions

    - fields are of the correct type and visible when required as part of the API response

    - Data validations work and notify the user of any issue

    We are make the above possible by ensuring a more stringent test policy.

- New API will be at path `api/v2` and will remain until v2.0.0 release of Centurion on which the `api/v2` path will be moved to `api`

- API v1 is now **Feature frozen** with only bug fixes being completed. It's recommended that you move to and start using API v2 as this has feature parity with API v1.

- Depreciation of **ALL** API urls. API v1 Will be [removed in v2.0.0](https://github.com/nofusscomputing/centurion_erp/issues/343) release of Centurion.


## Version 1.0.0

Initial Release of Centurion ERP.


### Breaking changes

- Nil
