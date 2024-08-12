## 1.0.0-b14 (2024-08-12)

### Fixes

- **api**: ensure model_notes is an available field

### Tests

- **access**: test field model_notes

## 1.0.0-b13 (2024-08-11)

### Fixes

- Audit models for validations
- **itam**: Ensure device name is formatted according to RFC1035 2.3.1
- **itam**: Ensure device UUID is correctly formatted
- **config_management**: Ensure that config group can't set self as parent
- **settings**: ensure that the api token cant be saved to notes field

### Tests

- api field checks
- **software**: api field checks

## 1.0.0-b12 (2024-08-10)

### Fixes

- **api**: ensure org mixin is inherited by software view
- **base**: correct project links to github

### Tests

- api field checks

#128 #162
- **teams**: api field checks
- **organization**: api field checks

## 1.0.0-b11 (2024-08-10)

## 1.0.0-b10 (2024-08-09)

## 1.0.0-b9 (2024-08-09)

## 1.0.0-b8 (2024-08-09)

## 1.0.0-b7 (2024-08-09)

## 1.0.0-b6 (2024-08-09)

## 1.0.0-b5 (2024-07-31)

### feat

- add Config groups to API
- **api**: Add device config groups to devices
- **api**: Ability to fetch configgroups from api along with config

### Fixes

- **api**: Ensure device groups is read only

### Tests

- **api**: Field existence and type checks for device
- **api**: test configgroups API fields

## 1.0.0-b4 (2024-07-29)

### feat

- **swagger**: remove `{format}` suffixed doc entries

### Fixes

- release-b3 fixes
- **api**: cleanup team post/get
- **api**: confirm HTTP method is allowed before permission check
- **api**: Ensure that organizations can't be created via the API
- **access**: Team model class inheritance order corrected

### Tests

- confirm that the tenancymanager is called

## 1.0.0-b3 (2024-07-21)

### Fixes

- **itam**: Limit os version count to devices user has access to

## 1.0.0-b2 (2024-07-19)

### Fixes

- **itam**: only show os version once

## 1.0.0-b1 (2024-07-19)

### Fixes

- **itam**: ensure installed operating system count is limited to users organizations
- **itam**: ensure installed software count is limited to users organizations

## 1.0.0-a4 (2024-07-18)

### feat

- **api**: When processing uploaded inventory and name does not match, update name to one within inventory file
- **config_management**: Group name to be entire breadcrumb

### Tests

- ensure inventory upload matches by both serial number and uuid if device name different
- placeholder for moving organization

## 1.0.0-a3 (2024-07-18)

### feat

- **config_management**: Prevent a config group from being able to change organization
- **itam**: On device organization change remove config groups

### Fixes

- **config_management**: dont attempt to do action during save if group being created
- **itam**: remove org filter for device so that user can see installations
- **itam**: remove org filter for operating systems so that user can see installations
- **itam**: remove org filter for software so that user can see installations
- **itam**: Device related items should not be global.
- **itam**: When changing device organization move related items too.

## 1.0.0-a2 (2024-07-17)

### feat

- **api**: Inventory matching of device second by uuid
- **api**: Inventory matching of device first by serial number
- **base**: show warning bar if the user has not set a default organization

### Fixes

- **base**: dont show user warning bar for non-authenticated user
- **api**: correct inventory operating system selection by name
- **api**: correct inventory operating system and it's linking to device
- **api**: correct inventory device search to be case insensitive

## 1.0.0-a1 (2024-07-16)

### BREAKING CHANGE

- squashed DB migrations in preparation for v1.0 release.

### feat

- Administratively set global items org/is_global field now read-only
- **access**: Add multi-tennant manager

### Fixes

- **core**: migrate manufacturer to use new form/view logic
- **settings**: correct the permission to view manufacturers
- **access**: Correct team form fields
- **config_management**: don't exclude parent from field, only self

### Refactoring

- repo preperation for v1.0.0-Alpha-1
- Squash database migrations

### Tests

- tenancy objects
- refactor to single abstract model for inclusion.

## 0.7.0 (2024-07-14)

### feat

- **core**: Filter every form field if associated with an organization to users organizations only
- **core**: add var `template_name` to common view template for all views that require it
- **core**: add Display view to common forms abstract class
- **navigation**: always show every menu for super admin
- **core**: only display navigation menu item if use can view model
- **django**: update 5.0.6 -> 5.0.7
- **core**: add common forms abstract class
- **core**: add common views abstract class
- add postgreSQL database support
- **ui**: add config groups navigation icon
- **ui**: add some navigation icons
- **itam**: update inventory status icon
- **itam**: ensure device software pagination links keep interface on software tab
- "Migrate inventory processing to background worker"
- **access**: enable non-organization django permission checks
- **settings**: Add celery task results index and view page
- **base**: Add background worker
- **itam**: Update Serial Number from inventory if present and Serial Number not set
- **itam**: Update UUID from inventory if present and UUID not set

### Fixes

- **config_management**: Don't allow a config group to assign itself as its parent
- **config_management**: correct permission for deleting a host from config group
- **config_management**: use parent group details to work out permissions when adding a host
- **config_management**: use parent group details to work out permissions
- **itam**: Add missing permissions to software categories index view
- **itam**: Add missing permissions to device types index view
- **itam**: Add missing permissions to device model index view
- **settings**: Add missing permissions to app settings view
- **itam**: Add missing permissions to software index view
- **itam**: Add missing permissions to operating system index view
- **itam**: Add missing permissions to device index view
- **config_management**: Add missing permissions to group views
- **navigation**: always show settings menu entry
- **itam**: cater for fields that are prefixed
- **itam**: Ability to view software category
- **itam**: correct view permission
- **access**: When adding a new team to org ensure parent model is fetched
- **access**: enable org manager to view orgs
- **settings**: restrict user visible organizations to ones they are part of
- **access**: enable org manager to view orgs
- **access**: fetch object if method exists
- **docs**: update docs link to new path
- **access**: correctly set team user parent model to team
- **access**: fallback to django permissions if org permissions check is false
- **access**: Correct logic so that org managers can see orgs they manage
- **base**: add missing content_title to context
- **access**: Enable Organization Manager to view organisations they are assigned to
- **api**: correct logic for adding inventory UUID and serial number to device
- **ui**: navigation alignment and software icon
- **ui**: display organization manager name instead of ID
- **access**: ensure name param exists before attempting to access
- **itam**: dont show none/nil for device fields containing no value
- **itam**: show device model name instead of ID
- **api**: Ensure if serial number from inventory is `null` that it's not used
- **api**: ensure checked uuid and serial number is used for updating
- inventory
- **itam**: only remove device software when not found during inventory upload
- **itam**: only update software version if different
- existing device without uuid not updated when uploading an inventory
- Device Software tab pagination does not work
- **itam**: correct device software pagination

### Refactoring

- adjust views missing add/change form to now use forms
- add navigation menu expand arrows
- migrate views to use new abstract model view classes
- migrate forms to use new abstract model form class
- **access**: Rename Team Button "new user" -> "Assign User"
- **access**: model pk and name not required context for adding a device
- rename field "model notes" -> "Notes"
- remove settings model
- **ui**: increase indentation to sub-menu items
- **itam**: rename old inventory status icon for use with security
- **api**: migrate inventory processing to background worker
- **itam**: only perform actions on device inventory if DB matches inventory item

### Tests

- add test test_view_*_attribute_not_exists_fields for add and change views
- fix test_view_change_attribute_type_form_class to test if type class
- **views**: add test cases for model views
- Add Test case abstract classes to models
- **inventory**: add mocks?? for calling background worker
- **view**: view permission checks
- **inventory**: update tests for background worker changes

## 0.6.0 (2024-06-30)

### feat

- user api token
- **api**: API token authentication
- **api**: abilty for user to create/delete api token
- **api**: create token model

### Fixes

- **user_token**: conduct user check on token view access
- **itam**: use same form for edit and add
- **itam**: dont add field inventorydate if adding new item
- **api**: inventory upload requires sanitization

### Refactoring

- **settings**: use seperate change/view views
- **settings**: use form for user settings
- **tests**: move unit tests to unit test sub-directory

### Tests

- **token_auth**: test authentication method token
- more tests
- add .coveragerc to remove non-code files from coverage report
- Unit Tests TenancyObjects
- Test Cases for TenancyObjects
- tests for checking links from rendered templetes
- **core**: test cases for notes permissions
- **config_management**: config groups history permissions
- **api**: Majority of Inventory upload tests
- **access**: TenancyObject field tests
- **access**: remove skipped api tests for team users

## 0.5.0 (2024-06-17)

### feat

- Setup Organization Managers
- **access**: add notes field to organization
- **access**: add organization manger
- **config_management**: Use breadcrumbs for child group name display
- **config_management**: ability to add host to global group
- **itam**: add a status of "bad" for devices
- **itam**: paginate device software tab
- **itam**: status of device visible on device index page
- API Browser
- **core**: add skeleton http browser
- **core**: Add a notes field to manufacturer/ publisher
- **itam**: Add a notes field to software category
- **itam**: Add a notes field to device types
- **itam**: Add a notes field to device models
- **itam**: Add a notes field to software
- **itam**: Add a notes field to operating system
- **itam**: Add a notes field to devices
- **access**: Add a notes field to teams
- **base**: Add a notes field to `TenancyObjetcs` class
- **settings**: add docs icon to application settings page
- **itam**: add docs icon to software page
- **itam**: add docs icon to operating system page
- **itam**: add docs icon to devices page
- **config_management**: add docs icon to config groups page
- **base**: add dynamic docs icon
- config group software
- **models**: add property parent_object to models that have a parent
- **config_management**: add config group software to group history
- **itam**: render group software config within device rendered config
- **config_management**: assign software action to config group
- sso
- add configuration value 'SESSION_COOKIE_AGE'
- remove development SECRET_KEY and enforce checking for user configured one
- **base**: build CSRF trusted origins from configuration
- **base**: Enforceable SSO ONLY
- **base**: configurable SSO

### Fixes

- **itam**: remove requirement that user needs change device to add notes
- **core**: dont attempt to access parent_object if 'None' during history save
- **config_management**: Add missing parent item getter to model
- **core**: overridden save within SaveHistory to use default attributes
- **access**: overridden save to use default attributes
- History does not delete when item deleted
- **core**: on object delete remove history entries
- inventory upload cant determin object organization
- **api**: ensure proper permission checking
- dont throw an exception during settings load for an item django already checks
- **core**: Add overrides for delete so delete history saved for items with parent model
- **config_management**: correct delete success url
- **base**: remove social auth from nav menu
- **access**: add a team user permissions to use team organization

### Refactoring

- **access**: relocate permission check to own function
- **itam**: move device os tab to details tab
- **itam**: add device change form and adjust view to be non-form
- **itam**: migrate device vie to use manual entered fields in two columns
- **access**: migrate team users view to use forms
- **access**: migrate teams view to use forms
- **access**: migrate organization view to use form
- **base**: cleanup form and prettyfy
- **config_management**: relocate groups views to own directory
- login to use base template
- adjust template block names

### Tests

- **access**: team user model permission check for organization manager
- **access**: team model permission check for organization manager
- **access**: organization model permission check for organization manager
- **access**: add test cases for model delete as organization manager
- **access**: add test cases for model addd as organization manager
- **access**: add test cases for model change as organization manager
- **access**: add test cases for model view as organization manager
- write some more
- **core**: skip invalid tests
- **itam**: tests for device type history entries
- **core**: tests for manufacturer history entries
- move manufacturer to it's parent
- refactor api model permission tests to use an abstract class of test cases
- move tests to the module they belong to
- refactor history permission tests to use an abstract class of test cases
- refactor model permission tests to use an abstract class of test cases
- refactor history entry to have test cases in abstract classes
- **itam**: history entry tests for software category
- **itam**: history entry tests for device operating system version
- **itam**: history entry tests for device operating system
- **itam**: history entry tests for device software
- **itam**: ensure child history is removed on config group software delete
- add placeholder tests
- **itam**: ensure history is removed on software delete
- **itam**: ensure history is removed on operating system delete
- **itam**: ensure history is removed on device model delete
- **config_management**: test history on delete for config groups
- **itam**: ensure history is removed on device delete
- **access**: test team history
- **access**: ensure team user history is created and removed as required
- **access**: ensure history is removed on team delete
- **access**: ensure history is removed on item delete
- **api**: Inventory upload permission checks
- **config_management**: testing of config_groups rendered config
- **config_management**: history save tests for config groups software
- **config_management**: config group software permission for add, change and delete
- **base**: placeholder tests for config groups software
- **base**: basic test for merge_software helper
- during unit tests add SECRET_KEY

## 0.4.0 (2024-06-05)

### feat

- 2024 06 05
- **database**: add mysql support
- **api**: move invneotry api endpoint to '/api/device/inventory'
- **core**: support more history types
- **core**: function to fetch history entry item
- 2024 06 02
- **config_management**: Add button to groups ui for adding child group
- **access**: throw error if no organization added
- **itam**: add delete button to config group within ui
- **itam**: Config groups rendered configuration now part of devices rendered configuration
- **config_management**: Ability to delete a host from a config group
- **config_management**: Ability to add a host to a config group
- **config_management**: ensure config doesn't use reserved config keys
- **config_management**: Config groups rendered config
- **config_management**: add configuration groups
- **api**: add swagger ui for documentation
- **api**: filter software to users organizations
- **api**: filter devices to users organizations
- randomz
- **api**: add org team view page
- API configuration of permissions
- **api**: configure team permissions

### Fixes

- **itam**: ensure device type saves history
- **core**: correct history view permissions
- **config_management**: set config dict keys to be valid ansible variables
- **itam**: correct logic for device add dynamic success url
- **itam**: correct config group link for device
- **config_management**: correct model permissions
- **config_management**: add config management to navigation
- **ui**: remove api entries from navigation
- **api**: check for org must by by type None
- **api**: correct software permissions
- **api**: corrct device permissions
- **api**: permissions for teams
- **api**: correct reverse url lookup to use NS API
- **api**: permissions for organization

### Refactoring

- **access**: cache object so it doesnt have to be called multiple times
- **config_management**: move groups to nav menu
- **api**: migrate devices and software to viewsets
- **api**: move permission check to mixin
- **access**: add team option to org permission check

### Tests

- **api**: placeholder test for inventory
- **settings**: access permission check for app settings
- **settings**: history view permission check for software category
- **settings**: history view permission check for manufacturer
- **settings**: history view permission check for device type
- **settings**: user settings
- **settings**: view permission check for user settings
- refactor core test layout
- **itam**: view permission check for software
- **itam**: view permission check for operating system
- **itam**: view permission check for device model
- **itam**: view permission check for device
- **config_management**: view permission check for config_groups
- **access**: view permission check for team
- **access**: view permission check for organization
- add history entry creation tests for most models
- **config_management**: when adding a host to config group filter out host that are already members of the group
- **config_management**: unit test for config groups model to ensure permissions are working
- **api**: remove tests for os and manufacturer as they are not used in api
- **api**: check model permissions for software
- **api**: check model permissions for devices
- **api**: check model permissions for teams
- **api**: check model permissions for organizations

## 0.3.0 (2024-05-29)

### feat

- Randomz
- **access**: during organization permission check, check to ensure user is logged on
- **history**: always create an entry even if user=none
- **itam**: device uuid must be unique
- **itam**: device serial number must be unique
- 2024 05 26
- **setting**: Enable super admin to set ALL manufacturer/publishers as global
- **setting**: Enable super admin to set ALL device types as global
- **setting**: Enable super admin to set ALL device models as global
- **setting**: Enable super admin to set ALL software categories as global
- **UI**: show build details with page footer
- **software**: Add output to stdout to show what is and has occurred
- 2024 05 25
- **base**: Add delete icon to content header
- **itam**: Populate initial organization value from user default organization for software category creation
- **itam**: Populate initial organization value from user default organization for device type creation
- **itam**: Populate initial organization value from user default organization for device model creation
- **api**: Populate initial organization value from user default organization inventory
- **itam**: Populate initial organization value from user default organization for Software creation
- **itam**: Populate initial organization value from user default organization for operating system creation
- **device**: Populate initial organization value from user default organization
- Add management command software
- **setting**: Enable super admin to set ALL software as global
- **user**: Add user settings panel
- Manufacturer and Model Information
- **itam**: Add publisher to software
- **itam**: Add publisher to operating system
- **itam**: Add device model
- **core**: Add manufacturers
- **settings**: add dummy model for permissions
- **settings**: new module for whole of application settings/globals
- 2024 05 21-23
- **access**: Save changes to history for organization and teams
- **software**: Save changes to history
- **operating_system**: Save changes to history
- **device**: Save changes to history
- **core**: history model for saving model history
- 2024 05 19/20
- **itam**: Ability to add notes to software
- **itam**: Ability to add notes to operating systems
- **itam**: Ability to add notes on devices
- **core**: notes model added to core
- **device**: Record inventory date and show as part of details
- **ui**: Show inventory details if they exist
- **api**: API accept computer inventory

### Fixes

- **settings**: Add correct permissions for team user delete
- **settings**: Add correct permissions for team user view/change
- **settings**: Add correct permissions for team view/change
- **settings**: Add correct permissions for team add
- **settings**: Add correct permissions for team delete
- **access**: correct back link within team view
- **access**: correct url name to be within naming conventions
- **settings**: Add correct permissions for manufacturer / publisher delete
- **settings**: Add correct permissions for manufacturer / publisher add
- **settings**: Add correct permissions for manufacturer / publisher view/update
- **settings**: Add correct permissions for software category delete
- **settings**: Add correct permissions for software category add
- **settings**: Add correct permissions for software category view/update
- **settings**: Add correct permissions for device type delete
- **settings**: Add correct permissions for device type add
- **settings**: Add correct permissions for device type view/update
- **settings**: Add correct permissions for device model delete
- **settings**: Add correct permissions for device model add
- **settings**: Add correct permissions for device model view/update
- **access**: Add correct permissions for organization view/update
- **access**: use established view naming
- **itam**: Add correct permissions for operating system delete
- **itam**: Add correct permissions for operating system add
- **itam**: Add correct permissions for operating system view/update
- **itam**: Add correct permissions for software delete
- **itam**: Add correct permissions for software add
- **itam**: for non-admin user use correct order by fields  for software view/update
- **itam**: Add correct permissions for software view/update
- **itam**: ensure permission_required parameter for view is a list
- **core**: dont save history when no user information available
- **access**: during organization permission check, check the entire list of permissions
- **core**: dont save history for anonymous user
- **access**: during permission check use post request params for an add action
- **user**: on new-user signal create settings row if not exist
- **itam**: ensure only user with change permission can change a device
- **user**: if user settings row doesn't exist on access create
- **access**: adding/deleting team group actions moved to model save/delete method override
- **api**: add teams and permissions to org and teams respectively
- **ui**: correct repo url used
- **api**: device inventory date set to read only
- **software**: ensure management command query correct for migration
- **device**: OS form trying to add last inventory date when empty
- add static files path to urls
- **inventory**: Dont select device_type, use 'null'
- **base**: show "content_title - SITE_TITLE" as site title
- **device**: Read Only field set as required=false
- correct typo in notes templates
- **ui**: Ensure navigation menu entry highlighted for sub items

### Refactoring

- **access**: add to models a get_organization function
- **access**: remove change view
- **itam**: relocation item delete from list to inside device
- **context_processor**: relocate as base
- **itam**: software index does not require created and modified date
- **organizations**: set org field to null if not set
- **itam**: move software categories to settings app
- **itam**: move device types to settings app
- **template**: content_title can be rendered in base

### Tests

- cleanup duplicate tests and minor reshuffle
- **access**: unit testing team user permissions
- **access**: unit testing team permissions
- **settings**: unit testing manufacturer permissions
- **settings**: unit testing software category permissions
- **device_model**: unit testing device type permissions
- **device_model**: unit testing device model permissions
- **organization**: unit testing organization permissions
- **operating_system**: unit testing operating system permissions
- **software**: unit testing software permissions
- **device**: unit testing device permissions
- adjust test layout and update contributing
- **core**: placeholder tests for history component
- **core**: place holder tests for notes model
- **api**: add placeholder tests for inventory

## 0.2.0 (2024-05-18)

### feat

- 2024 05 18
- **itam**: Add Operating System to ITAM models
- **api**: force content type to be JSON for req/resp
- **software**: view software
- 2024 05 17
- **device**: Prevent devices from being set global
- **software**: if no installations found, denote
- **device**: configurable software version
- **software_version**: name does not need to be unique
- **software_version**: set is_global to match software
- **software**: prettify device software action
- **software**: ability to add software versions
- **base**: add stylised action button/text
- **software**: add pagination for index
- **device**: add pagination for index

### Fixes

- **device**: correct software link

## 0.1.0 (2024-05-17)

### feat

- API token auth
- **api**: initial token authentication implementation
- itam and API setup
- **docker**: add settings to store data in separate volume
- **django**: add split settings for specifying additional settings paths
- **api**: Add device config to device
- **itam**: add organization to device installs
- **itam**: migrate app from own repo
- Enable API by default
- Genesis
- **admin**: remove team management
- **admin**: remove group management
- **access**: adjustable team permissions
- **api**: initial work on API
- **template**: add header content icon block
- **tenancy**: Add is_ global field
- **access**: when modifying a team ad/remove user from linked group
- **auth**: include python social auth django application
- Build docker container for release
- **access**: add permissions to team and user
- **style**: format check boxes
- **access**: delete team user form
- **view**: new user
- user who is 'is_superuser' to view everything and not be denied access
- **access**: add org mixin to current views
- **access**: add views for each action for teams
- **access**: add mixin to check organization permissions against user and object
- **account**: show admin site link if user is staff
- **development**: added the debug django app
- **access**: rename structure to access and remove organization app in favour of own implementation
- **account**: Add user password change form
- **urls**: provide option to exclude navigation items
- **structure**: unregister admin pages from organization app not required
- **auth**: Custom Login Page
- **auth**: Add User Account Menu
- **auth**: Setup Login required
- Dyno-magic build navigation from application urls.py
- **structure**: Select and View an individual Organization
- **structure**: View Organizations
- **app**: Add new app structure for organizations and teams
- **template**: add base template
- **django**: add organizations app

### Fixes

- **itam**: device software to come from device org or global not users orgs
- **access**: correct team required permissions
- **fields**: correct autoslug field so it works
- **docker**: build wheels then install

### Refactoring

- button to use same selection colour
- **access**: remove inline form for org teams
- rename app from itsm -> app
- **access**: dont use inline formset
- **views**: move views to own directory
- **access**: addjust org and teams to use different view per action

### Tests

- interim unit tests

## 0.0.1 (2024-05-06)
