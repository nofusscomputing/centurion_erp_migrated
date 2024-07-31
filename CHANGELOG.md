## 1.0.0-b5 (2024-07-31)

### Feat

- **api**: Add device config groups to devices
- **api**: Ability to fetch configgroups from api along with config

### Fix

- **api**: Ensure device groups is read only

## 1.0.0-b4 (2024-07-29)

### Feat

- **swagger**: remove `{format}` suffixed doc entries

### Fix

- **api**: cleanup team post/get
- **api**: confirm HTTP method is allowed before permission check
- **api**: Ensure that organizations can't be created via the API
- **access**: Team model class inheritance order corrected

## 1.0.0-b3 (2024-07-21)

### Fix

- **itam**: Limit os version count to devices user has access to

## 1.0.0-b2 (2024-07-19)

### Fix

- **itam**: only show os version once

## 1.0.0-b1 (2024-07-19)

### Fix

- **itam**: ensure installed operating system count is limited to users organizations
- **itam**: ensure installed software count is limited to users organizations

## 1.0.0-a4 (2024-07-18)

### Feat

- **api**: When processing uploaded inventory and name does not match, update name to one within inventory file
- **config_management**: Group name to be entire breadcrumb

## 1.0.0-a3 (2024-07-18)

### Feat

- **config_management**: Prevent a config group from being able to change organization
- **itam**: On device organization change remove config groups

### Fix

- **config_management**: dont attempt to do action during save if group being created
- **itam**: remove org filter for device so that user can see installations
- **itam**: remove org filter for operating systems so that user can see installations
- **itam**: remove org filter for software so that user can see installations
- **itam**: Device related items should not be global.
- **itam**: When changing device organization move related items too.

## 1.0.0-a2 (2024-07-17)

### Feat

- **api**: Inventory matching of device second by uuid
- **api**: Inventory matching of device first by serial number
- **base**: show warning bar if the user has not set a default organization

### Fix

- **base**: dont show user warning bar for non-authenticated user
- **api**: correct inventory operating system selection by name
- **api**: correct inventory operating system and it's linking to device
- **api**: correct inventory device search to be case insensitive

## 1.0.0-a1 (2024-07-16)

### BREAKING CHANGE

- squashed DB migrations in preparation for v1.0 release.

### Feat

- Administratively set global items org/is_global field now read-only
- **access**: Add multi-tennant manager

### Fix

- **core**: migrate manufacturer to use new form/view logic
- **settings**: correct the permission to view manufacturers
- **access**: Correct team form fields
- **config_management**: don't exclude parent from field, only self

### Refactor

- Squash database migrations

## 0.7.0 (2024-07-14)

### Bug Fixes

- **config_management**: [5ae487cd](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/5ae487cd3eac2f5273d3b2a9e7642e714bdbde68) - Don't allow a config group to assign itself as its parent [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#122](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/122) ]
- **config_management**: [3aab7b57](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/3aab7b57e80b48e1f4671413034c1c71dfad4c66) - correct permission for deleting a host from config group [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **config_management**: [931c9864](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/931c9864db8e14072a0a7e331d525aeedd19eb2a) - use parent group details to work out permissions when adding a host [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#120](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/120) ]
- **config_management**: [65bf9946](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/65bf994619949c4d42bfa92e06e8c63f67acabca) - use parent group details to work out permissions [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#121](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/121) ]
- **itam**: [77ff580f](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/77ff580f19e41a430cfa7d3bf1ba3870d7993cf9) - Add missing permissions to software categories index view [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) ]
- **itam**: [423ff11d](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/423ff11d4c30670cb8c7832b452af78cf54a5fd3) - Add missing permissions to device types index view [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) ]
- **itam**: [9e4b5185](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/9e4b5185b144ade67b98aeb6e909e1af39b62545) - Add missing permissions to device model index view [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) ]
- **settings**: [020441c4](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/020441c41aae4ccc3453becdf451918bc3a432f7) - Add missing permissions to app settings view [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) ]
- **itam**: [d0a3b7b4](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/d0a3b7b49dfa8c0468106652af723b824c7ecf89) - Add missing permissions to software index view [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) ]
- **itam**: [960fa548](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/960fa5485d3198c1e4868957e6d57f3c8bd65cf8) - Add missing permissions to operating system index view [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) ]
- **itam**: [26db4630](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/26db4630445ceff412a6d12f97f661e95c165a3b) - Add missing permissions to device index view [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) ]
- **config_management**: [1193f1d8](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/1193f1d86d247e5df77dc44bae36a5534c0f0c88) - Add missing permissions to group views [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) ]
- **navigation**: [ee8920a4](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/ee8920a464017e2ec7ef714530a105197eaae75b) - always show settings menu entry [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **itam**: [a62a36ba](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/a62a36ba82252257646325679180c68632971c52) - cater for fields that are prefixed [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#112](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/112) ]
- **itam**: [c00cf16b](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/c00cf16bc8ac85f5c5bf19d30cf78ae9a838d00f) - Ability to view software category [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **itam**: [7784dfed](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/7784dfede98f94bd1a5e4df5155130e91876fe67) - correct view permission [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **access**: [03d350e3](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/03d350e302c443ff53fc71e32bc32f489af1409a) - When adding a new team to org ensure parent model is fetched [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **access**: [1d5c86f1](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/1d5c86f13b2df36e0562e1fe3b6aca7dfa04a7ec) - enable org manager to view orgs [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#105](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/105) ]
- **settings**: [9e336d36](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/9e336d368d51381701b358287853f9ceab61b49f) - restrict user visible organizations to ones they are part of [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#99](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/99) ]
- **access**: [937e9359](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/937e9359498da9388fd730c69e591679458c331e) - enable org manager to view orgs [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#105](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/105) ]
- **access**: [860eaa67](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/860eaa674937dc9ff1690615bafcddaab38d890d) - fetch object if method exists [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#105](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/105) ]
- **docs**: [aab94431](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/aab94431a9d3864ace91af70e29b5dc59b61fd6f) - update docs link to new path [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#103](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/103) ]
- **access**: [524a70ba](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/524a70ba184c0af1125636f5923492ba65765f1e) - correctly set team user parent model to team [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#109](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/109) ]
- **access**: [29c4b4a0](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/29c4b4a0caaa37866774235d56312f2b9ede8148) - fallback to django permissions if org permissions check is false [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#109](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/109) [#101](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/101) ]
- **access**: [f5ae01b0](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/f5ae01b08d0ce91e4af86a042effff79db489d6a) - Correct logic so that org managers can see orgs they manage [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#100](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/100) ]
- **base**: [ee3dd68c](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/ee3dd68cfe78c71a4431e88f6d1f6429dd2af8c0) - add missing content_title to context [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) ]
- **access**: [25efa314](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/25efa31493f71eca5d553d46136d3a261a9d3612) - Enable Organization Manager to view organisations they are assigned to [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#100](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/100) ]
- **api**: [4a6ce353](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/4a6ce353325148f66e3216e61feee7ad96b45cbc) - correct logic for adding inventory UUID and serial number to device [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **ui**: [2d80f026](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/2d80f026341910eecd23560ef970323ac275b112) - navigation alignment and software icon [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **ui**: [abe1ce69](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/abe1ce69480de5c831d5183845987bc9a3264fc3) - display organization manager name instead of ID [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **access**: [86ed7318](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/86ed7318ecd43c15cfccdb344af4ea2ac05c8a87) - ensure name param exists before attempting to access [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **itam**: [90a01911](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/90a01911dacd698d0b7832a05e24eec6fe8310eb) - dont show none/nil for device fields containing no value [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **itam**: [de3ed3a8](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/de3ed3a881bd53e533b9b35f37ce17419c6d75f2) - show device model name instead of ID [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **api**: [f64be2ea](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/f64be2ea33ebf0ae1ba735a7259caf880bcddad5) - Ensure if serial number from inventory is `null` that it's not used [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#78](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/78) ]
- **api**: [ef9c596e](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/ef9c596ec79decec268ffb700e62d5bc35e49019) - ensure checked uuid and serial number is used for updating [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **itam**: [67f20ecb](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/67f20ecb661b039092ad34b491c3a8a7296534db) - only remove device software when not found during inventory upload [ [!38](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/38) [#75](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/75) ]
- **itam**: [3bceb666](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/3bceb66600404919ac32498ffa5cbb4f24fcced4) - only update software version if different [ [!38](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/38) [#75](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/75) ]
- **itam**: [241ba47c](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/241ba47c80805dbd648392ef0b6b26793d3f55ff) - correct device software pagination [ [!36](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/36) [#67](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/67) ]

### Code Refactor

- [367c4beb](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/367c4bebb67c24ffcc2ade19abfeac6089a1e702) - adjust views missing add/change form to now use forms [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#15](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/15) [#46](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/46) [#74](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/74) [#120](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/120) [#121](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/121) [#118](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/118) ]
- [0276f945](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/0276f9454b3999ec147314327b25945a69213250) - add navigation menu expand arrows [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#21](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/21) ]
- [7d172fb4](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/7d172fb4afa284e67231d3d24c7f1bdc533f922a) - migrate views to use new abstract model view classes [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#111](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/111) ]
- [f848d01b](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/f848d01b347af5615613e8bfdb0d9d7324e1daec) - migrate forms to use new abstract model form class [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **access**: [7cfede45](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/7cfede45b89dd5d5ce5b2d2fa8e4ef0c64d31ab3) - Rename Team Button "new user" -> "Assign User" [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#110](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/110) ]
- **access**: [65de9371](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/65de93715d505d5c71b150175e31471b5a07bb8f) - model pk and name not required context for adding a device [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- [fea7ea31](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/fea7ea31198190bf115dc89595b00d7e034aa991) - rename field "model notes" -> "Notes" [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#102](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/102) [#104](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/104) ]
- [f0bbd22c](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/f0bbd22cf441cb3c3f5b01c8108a7a0fd8357938) - remove settings model [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **ui**: [fb907283](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/fb907283b036454aa2afd41bbc658c8feb1a44d8) - increase indentation to sub-menu items [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **itam**: [c1a8ee65](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/c1a8ee65f2bc892c2ca8bfacc5f95094a0130b24) - rename old inventory status icon for use with security [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **api**: [7aeba347](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/7aeba347875cbefb6d5eae112804ae6f0097d264) - migrate inventory processing to background worker [ [!39](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/39) [#76](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/76) ]
- **itam**: [f47b97e2](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/f47b97e2a084e1acbfba733c910f3b8f4f764a36) - only perform actions on device inventory if DB matches inventory item [ [!38](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/38) [#75](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/75) ]

### Continious Integration

- [e25ec12c](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/e25ec12cb02f8f48853806d9cc97959d3e757115) - correct test report path [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- [a235aa7e](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/a235aa7ec37a6dda69bc96ab854df41eacba255b) - add submodule update job [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]

### Documentaton / Guides

- **development**: [935e10dc](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/935e10dc24d10c2d99b52a185730d676b4978908) - add initial forms [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **development**: [d4aaea4d](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/d4aaea4dbb250f23850d02d8c5cb9ecbc147a9da) - update views, models and index [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- [329049e8](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/329049e81dd50ca01512f75323669c7953be2199) - roadmap update [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- [c41c7ed1](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/c41c7ed1f09a7a13ac93043bee4e3f3ce0613245) - update mkdocs [ [!41](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/41) ]
- [c9190e9a](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/c9190e9a7dd12725df323811816ea603315331e9) - Update index [ [!41](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/41) ]
- **centurion**: [0294f5ed](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/0294f5ed65868fadd9f27a8a9c22ca861418061b) - replace Django ITSM -> Centurion ERP [ [!41](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/41) ]
- [7329a65a](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/7329a65ae7f30b6e89d0c284609aac2063c76ea6) - update roadmap [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- [9a529a64](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/9a529a64e2e5deaeebec872e3cbe91a6eccebcbe) - add bug count badge [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- [9b79c9d7](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/9b79c9d7ffaacc6ecd9a8d379bc26a303d2951c4) - update readme [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- [9dd2f6a3](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/9dd2f6a341c4e4c78de4e80769552914a4b23bc9) - fix mkdocs navigation [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- [23c640a4](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/23c640a4602948d1b6ec0d3a88473aa26d359997) - add roadmap [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **api**: [27eb54cc](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/27eb54cc3729bcf3ac4b74c84b2def8086685b34) - update swagger docs with inventory changes [ [!39](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/39) [#76](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/76) ]
- **administration**: [a8e2c687](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/a8e2c687b11186f922abd57bb46e98de9f9bf985) - notate rabbitMQ setup [ [!39](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/39) [#76](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/76) ]

### Features

- **core**: [4c42f776](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/4c42f776924dc2f8c52c237b9facd35f10e85e28) - Filter every form field if associated with an organization to users organizations only [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#119](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/119) ]
- **core**: [1cf15f73](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/1cf15f7339a50d9aa1a7940feb84a3128a573ea6) - add var `template_name` to common view template for all views that require it [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **core**: [c057ffdc](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/c057ffdc9c57b399206579f13c51bf4d28120e88) - add Display view to common forms abstract class [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **navigation**: [6837c383](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/6837c383034b962973248cbdd6ae6a5a8a758a41) - always show every menu for super admin [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **core**: [45cc3428](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/45cc34284a7b89aa3d61e61cfa3a12c73165127b) - only display navigation menu item if use can view model [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#114](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/114) ]
- **django**: [f2640df0](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/f2640df0d3737a5fc7a416cd692c37690786e7d1) - update 5.0.6 -> 5.0.7 [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **core**: [44f20b28](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/44f20b28be8c54978b53f00fac9664a5c403ed50) - add common forms abstract class [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **core**: [2e22a484](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/2e22a484a0f4416f41dffb49c68db703c177fe0d) - add common views abstract class [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- [332810ff](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/332810ffd6cf6024a0a917024eafed21ec8d2139) - add postgreSQL database support [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **ui**: [cb66b930](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/cb66b9303aa752ee131e3fd6edb9d670e37c3b0e) - add config groups navigation icon [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **ui**: [a2a8e120](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/a2a8e1204649a27481862e85f8292a229e85fa97) - add some navigation icons [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#21](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/21) [#22](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/22) [#23](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/23) ]
- **itam**: [6a14f78b](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/6a14f78bf7fcda8509d1b0c6b477711b4da59180) - update inventory status icon [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) ]
- **itam**: [656807e4](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/656807e410c4dcc0d049cc61ce67c07114313925) - ensure device software pagination links keep interface on software tab [ [!35](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/35) [#81](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/81) ]
- **access**: [b42bb3a3](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/b42bb3a30e613ed9701c95c6ad10fa1890d17dac) - enable non-organization django permission checks [ [!39](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/39) [#76](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/76) ]
- **settings**: [090c4a54](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/090c4a542544cb61356bc00ce2258463d5647f67) - Add celery task results index and view page [ [!39](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/39) [#76](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/76) ]
- **base**: [87a1f2aa](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/87a1f2aa20fdcbbff1863a751a0c5e7d91b269bb) - Add background worker [ [!39](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/39) [#76](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/76) ]
- **itam**: [7b4ed7b1](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/7b4ed7b13537de064680f3c19a703b37c9d2bb83) - Update Serial Number from inventory if present and Serial Number not set [ [!37](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/37) ]
- **itam**: [b801c9a4](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/commit/b801c9a49e70ca5640c65bafdd05c29daed40798) - Update UUID from inventory if present and UUID not set [ [!37](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/merge_requests/37) [#66](https://gitlab.com/nofusscomputing/projects/centurion_erp/-/issues/66) ]

## 0.6.0 (2024-06-30)

### Bug Fixes

- **user_token**: [6cfcf158](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6cfcf1580c669c046e4dd6d547b99c8b9814a078) - conduct user check on token view access [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) [#63](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/63) ]
- **itam**: [f6866912](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f6866912329fd2ea5f1bce6014db53605e1fee55) - use same form for edit and add [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) [#65](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/65) ]
- **itam**: [802f2c41](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/802f2c410da1d4810005991f6da27963621adc25) - dont add field inventorydate if adding new item [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) ]
- **api**: [4e428560](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4e428560274fc2a82d927338c66b4641a1c93986) - inventory upload requires sanitization [ [!33](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/33) ]

### Code Refactor

- **settings**: [66b8d936](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/66b8d9362d815e7f54ae402e4689c0a38f65c14d) - use seperate change/view views [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) ]
- **settings**: [37d277e1](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/37d277e1493ab708b8861fa8d0de3191da24d2f2) - use form for user settings [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) ]
- **tests**: [58b134ae](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/58b134ae30866b2ca207cef2cf17158d54517044) - move unit tests to unit test sub-directory [ [!33](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/33) [#15](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/15) ]

### Continious Integration

- **git_sync**: [a0874356](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/a0874356fd59978864664d4c25217dca527ee667) - sync on push ro feature branch 14-feat-project-management [ [!29](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/29) [!31](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/31) ]
- [5d8f5e3a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/5d8f5e3a518bea520a4b6159623c60a3eaade051) - remove dockerhub publish on bot push [ [!29](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/29) ]

### Documentaton / Guides

- [4d3a2385](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4d3a2385831c4db99bb9f3e70411b3d2d4d624f0) - Add user settings documentation [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) [#63](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/63) ]
- **api**: [47d6a3be](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/47d6a3beffa7bb3d5b822c54440fe8b31ad18e02) - API Token authentication [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) [#63](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/63) ]

### Features

- **api**: [11179143](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/111791438a45a8eb0cf4c175e4a1439cd56c84da) - API token authentication [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) [#63](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/63) ]
- **api**: [ce2c6f3b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ce2c6f3b135ec9110682db3b77c80d6dde26a3c2) - abilty for user to create/delete api token [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) [#63](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/63) ]
- **api**: [e655f22f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e655f22fac4d7de2ef42f16f33c8427528b63481) - create token model [ [!34](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/34) [#63](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/63) ]

## 0.5.0 (2024-06-17)

### Bug Fixes

- **itam**: [78216116](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/78216116dfdfca8542daa95e530bcb8855ec8cb6) - remove requirement that user needs change device to add notes [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) [#52](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/52) ]
- **core**: [54c34a95](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/54c34a95f59e32ca393c71ca2e579d9ee69f5eff) - dont attempt to access parent_object if 'None' during history save [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) ]
- **config_management**: [3b3ee9fc](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/3b3ee9fc3ddf1327207309cd860dc4ee9e2bf013) - Add missing parent item getter to model [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) ]
- **core**: [0a1aba7c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0a1aba7ca8e5c639fa56bede846c980ea0a5fb4e) - overridden save within SaveHistory to use default attributes [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) ]
- **access**: [eb8dca98](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/eb8dca980684cf6b7a1851a86c3eec71e71d07a3) - overridden save to use default attributes [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) ]
- **core**: [7239f572](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7239f572a35f576735b0a77832caebbe7a9df227) - on object delete remove history entries [ [!25](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/25) [#54](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/54) ]
- **api**: [505f4cfd](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/505f4cfdd9d6738d0f634508983412a1b736d3e3) - ensure proper permission checking [ [!24](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/24) [#55](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/55) ]
- [dc4968ee](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/dc4968ee7bc691b1537a7cc04a1da8b896f1c231) - dont throw an exception during settings load for an item django already checks [ [!23](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/23) ]
- **core**: [8d6826f7](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8d6826f7c0dd12e0f179d76dfac4e45215e7a4a6) - Add overrides for delete so delete history saved for items with parent model [ [!22](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/22) [#53](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/53) ]
- **config_management**: [23c43ed8](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/23c43ed8dc67d75301a9f27cbb901d596b0074d7) - correct delete success url [ [!22](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/22) [#43](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/43) ]
- **base**: [07e93243](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/07e93243a02602b4e3881e1aa4e13b8e6815720f) - remove social auth from nav menu [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **access**: [579e44f8](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/579e44f8344120b76f8c1f7580428da1e20a9419) - add a team user permissions to use team organization [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#51](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/51) ]

### Code Refactor

- **access**: [991ddc3d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/991ddc3d7f67f40e3d210025b6c38726e80ba460) - relocate permission check to own function [ [!28](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/28) [#39](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/39) ]
- **itam**: [e517c5fd](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e517c5fd761e9f84dc589468da96b26979f6b33f) - move device os tab to details tab [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) [#22](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/22) ]
- **itam**: [4a104095](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4a10409551e459d6a29a1c844d848759e05a25ad) - add device change form and adjust view to be non-form [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **itam**: [904234c5](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/904234c5818d893d63fc152e5f7b86d37226e122) - migrate device vie to use manual entered fields in two columns [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) [#22](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/22) ]
- **access**: [4016d4c2](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4016d4c20044053da7a9165723d0706fe8dabb7c) - migrate team users view to use forms [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **access**: [f36662ca](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f36662ca82b697ff2e6db286214ae1cac296d55b) - migrate teams view to use forms [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **access**: [3e340a47](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/3e340a47b844e955d9ba9d51bcb2fabbcfac6287) - migrate organization view to use form [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **base**: [3fb27063](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/3fb270632141d1b70a38e1edafec1e43dca9c18b) - cleanup form and prettyfy [ [!23](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/23) [#24](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/24) ]
- **config_management**: [ae81ee88](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ae81ee886334795d29298bbfdeb561f689b1409e) - relocate groups views to own directory [ [!22](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/22) ]
- [3b743a84](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/3b743a847c0b610de348718e392d417dd008e7b5) - login to use base template [ [!20](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/20) ]
- [95a08b2d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/95a08b2d2ca5915eb62abbcfe2acf45e85b578d3) - adjust template block names [ [!20](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/20) ]

### Continious Integration

- [fa28fd43](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/fa28fd436ef03b66c270ad460cadfd877434fd0d) - dont rebuild on dev on git tag [ [!19](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/19) ]

### Documentaton / Guides

- [a9485687](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/a94856879e740a261354f2fce8b1f213c5afcf86) - correct testing link [ [!28](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/28) ]
- [108398da](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/108398da4b2cd9280b65c6fef3bdc6cc0e9758e3) - rejig [ [!28](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/28) ]
- **access**: [8abbf2ff](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8abbf2ff9e33e1607be11be2c4757038334c0d11) - correct doc warnings [ [!28](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/28) ]
- **access**: [27b62d10](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/27b62d10180e0a299554fc72d2bd0faacf2e3b75) - add link to docs on team page [ [!28](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/28) [#39](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/39) ]
- **access**: [aef276b7](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/aef276b76c4636290d76735e7a390178e3bef12b) - add link to docs on organization page [ [!28](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/28) [#39](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/39) ]
- [afb5a709](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/afb5a709d7f19a042dcf451d227e29c26f3e04dc) - add badges to index [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) ]
- [ddead8eb](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ddead8eb56a06570926bc9aeeef877162a7d06fd) - restructure to sections administration, user and devlopment [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) [!62](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/62) ]
- **development**: [f861295b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f861295b1c48ea843cdaeef107e3652468328814) - add device model to api docs [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) ]
- [dbcb2825](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/dbcb2825487cd425fac6e60a3aeb9f02d18de96c) - docstrings show category headings [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) ]
- **development**: [5eec41fe](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/5eec41fe57f5cd26943cddae53623a74ad1ddc58) - Add test case documentation [ [!27](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/27) [#15](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/15) [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) [#57](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/57) [!83](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/83) ]
- **api**: [2eb50311](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/2eb50311b485094304f99cdd7d5fc1513896fabd) - document the inventory endpoint [ [!24](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/24) [#55](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/55) ]
- **api**: [36fa364d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/36fa364d04473c7a9de71890fed4eebf843954ed) - notate inventory permission [ [!24](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/24) [#55](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/55) ]
- [05bb6f8a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/05bb6f8a516edf9b61f6a3d3bdbb902b675b77b9) - update contributing with further test info [ [!22](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/22) ]
- **config_management**: [e62a570b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e62a570be3ca429e946b0d15b4865c9e71e9d4d1) - notate software group actions [ [!22](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/22) [#43](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/43) ]

### Features

- **access**: [84866185](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/848661856a44de31ee2116c1b5c4445fe6daf654) - add notes field to organization [ [!28](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/28) [#39](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/39) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **access**: [14acea31](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/14acea31f286541ef75358ee37062ee042ea8ca8) - add organization manger [ [!28](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/28) [#39](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/39) ]
- **config_management**: [8af59754](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8af5975428bb9d3aa18fe2126be702d894d7682e) - Use breadcrumbs for child group name display [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **config_management**: [ac707157](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ac70715752eeeeb9f01526989e145a79b3b3a92f) - ability to add host to global group [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **itam**: [8ccdf9a8](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8ccdf9a8f3815ae51a5005024021709b56601627) - add a status of "bad" for devices [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **itam**: [1200a879](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/1200a879136c52bcf63b8629a1ab8ca1d7edc0e5) - paginate device software tab [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **itam**: [e8cb685d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e8cb685da1bcfdec98da06fba77d076b0f9c096b) - status of device visible on device index page [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **core**: [8b47d956](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8b47d95614d81685edd277c300890e58fa7153ff) - add skeleton http browser [ [!26](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/26) [#58](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/58) ]
- **core**: [c570fb11](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c570fb114f70a2a1785fffe3ba627eee86c0c8d5) - Add a notes field to manufacturer/ publisher [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **itam**: [ea1727f2](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ea1727f2c796bd305b0e01c87f1db16c217b1b1e) - Add a notes field to software category [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **itam**: [36d7e545](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/36d7e54547bd5afc1270c02f6160b95eda5cc557) - Add a notes field to device types [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **itam**: [a02fda84](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/a02fda84137810d840168d214af471dac451887f) - Add a notes field to device models [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **itam**: [b5bc76b0](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b5bc76b0ab79dcec38d5c91a95c1a737b89c9f8b) - Add a notes field to software [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **itam**: [36c13e18](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/36c13e18c7f8f6e3354a2fb79c6a2240fdec431f) - Add a notes field to operating system [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **itam**: [6969b611](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6969b611644f025426cdb1f77c92f7a79d361859) - Add a notes field to devices [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **access**: [85bf1b99](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/85bf1b9907788f1e190c00827c096b00e25a8048) - Add a notes field to teams [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **base**: [ca8e0c07](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ca8e0c07ea6aff681e03ed966412403ba94c2d7c) - Add a notes field to `TenancyObjetcs` class [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) [#13](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/13) ]
- **settings**: [da93425c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/da93425c0b9eacb9d46233173c1cb99b79487103) - add docs icon to application settings page [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **itam**: [8a9899cf](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8a9899cf66bee3ac1f752ca38e4360aafa92be51) - add docs icon to software page [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **itam**: [38db558b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/38db558be2e330c7f9ebf6a1c70c70dc59ee1bd0) - add docs icon to operating system page [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **itam**: [67b204e4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/67b204e40cfbb1e078dac6aecc9835b08132c13c) - add docs icon to devices page [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **config_management**: [456fed80](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/456fed80a9fd6adc09cf8cb7e1be6ea0a4492c5e) - add docs icon to config groups page [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **base**: [87282ce4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/87282ce41cca9a750c7bc99ec8c1a78aa2b03dd7) - add dynamic docs icon [ [!21](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/21) ]
- **models**: [fe0696fe](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/fe0696fee6211236ac7f69e77dd0ec9c1516b25c) - add property parent_object to models that have a parent [ [!22](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/22) ]
- **config_management**: [1069211d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/1069211d1bde9362fdb6fd2f2f5d080bffd81a6e) - add config group software to group history [ [!22](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/22) [#43](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/43) ]
- **itam**: [460eff1f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/460eff1f71af6d75958c0eeb3dacb9b0169c6ca9) - render group software config within device rendered config [ [!22](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/22) [#43](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/43) ]
- **config_management**: [0c382a73](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0c382a73e5e0462b4bd598734159626f14f3a96e) - assign software action to config group [ [!22](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/22) [#43](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/43) ]
- [8b887575](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8b887575c921cdd6f5656e7e37ca8dab747081bf) - add configuration value 'SESSION_COOKIE_AGE' [ [!20](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/20) ]
- [d0e8e9a6](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/d0e8e9a674c24aff675ac73ba34dd20acca26b0c) - remove development SECRET_KEY and enforce checking for user configured one [ [!20](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/20) ]
- **base**: [d8d75c7d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/d8d75c7db09f7532665408299c9bf878e079f99a) - build CSRF trusted origins from configuration [ [!20](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/20) ]
- **base**: [b38984fc](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b38984fcb95ab121a610710b9df049ee7caa17cd) - Enforceable SSO ONLY [ [!20](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/20) [#1](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/1) ]
- **base**: [3040d4af](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/3040d4afe74c65ebf656329ea3cfe13e59409a61) - configurable SSO [ [!20](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/20) [#1](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/1) ]

## 0.4.0 (2024-06-05)

### Bug Fixes

- **itam**: [dd0c13a6](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/dd0c13a65f4cc55e2047f1b654dd228147eac183) - ensure device type saves history [ [!18](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/18) ]
- **core**: [4cafa34d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4cafa34d69332995307faf29eff42efd81e569d6) - correct history view permissions [ [!18](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/18) [#48](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/48) [#15](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/15) ]
- **config_management**: [2c1bbbfc](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/2c1bbbfc15babdc22d67285dae1c18a4b6f3cc96) - set config dict keys to be valid ansible variables [ [!18](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/18) [#47](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/47) ]
- **itam**: [dd30a57a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/dd30a57a9db7f5d6aa318651d9e252dae7f73b58) - correct logic for device add dynamic success url [ [!18](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/18) ]
- **itam**: [18e84db6](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/18e84db63c992c142f31f44fcc650561a16045fe) - correct config group link for device [ [!18](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/18) ]
- **config_management**: [c9098f5d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c9098f5d2fe1817d7d33b7ffd30aeffa4077cdd2) - correct model permissions [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **config_management**: [d422f2fe](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/d422f2feee4a5013ced153c43e0858098890d90b) - add config management to navigation [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **ui**: [8061b7c8](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8061b7c8e29b0f1ad12969a3d4e6a3e27cd85b2d) - remove api entries from navigation [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) ]
- **api**: [f41282d0](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f41282d08b6a417a12d22268a67b27425bed2361) - check for org must by by type None [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) ]
- **api**: [8dfb996b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8dfb996b24c26f3697a8d3c787faab4f190953eb) - correct software permissions [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) ]
- **api**: [95dc9794](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/95dc979419c7cb0f6bfeff71169201149c9341fb) - corrct device permissions [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) ]
- **api**: [09cc1db6](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/09cc1db665af30c32d043644806f65e56f80c510) - permissions for teams [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) ]
- **api**: [e7c535c4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e7c535c48d73f7f3dbde6a0c191afb134ba2dd72) - correct reverse url lookup to use NS API [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) ]
- **api**: [e9cd111a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e9cd111af6299dee24b7c917726c54f7e7be8fe2) - permissions for organization [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) ]

### Code Refactor

- **access**: [6650434c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6650434c63a7fc620f98ed79b32fe4bbd52b1ada) - cache object so it doesnt have to be called multiple times [ [!18](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/18) ]
- **config_management**: [58738971](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/5873897184e906ae1fd3419a018441de78c5741d) - move groups to nav menu [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **api**: [e257c114](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e257c1148808d6159bd6c8396a22168aa88c3b2f) - migrate devices and software to viewsets [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) ]
- **api**: [33b1a6c9](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/33b1a6c91dc6d7f47738b96f7ce08b616e0749bb) - move permission check to mixin [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) ]
- **access**: [5f3b48ea](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/5f3b48ea982588e39137a3e695a2bbe65fd4c0a2) - add team option to org permission check [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) ]

### Continious Integration

- [8e338c7c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8e338c7ca02057728089a8dabceae4348d3cb04a) - add pytest coverage report as environment [ [!15](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/15) [#37](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/37) ]
- [9b811ede](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/9b811ede266631a297bf84851b68f8b11a5d9f39) - run container build/publish on git tag [ [!15](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/15) ]

### Documentaton / Guides

- **config_management**: [0a17329a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0a17329a710e7f94ea3054857975467236130d1c) - notate future feature [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- [0d18e974](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0d18e974dda10490f0b2b95f416fd8af8351a58a) - correct liniting errors [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) ]
- **config_management**: [62e605d4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/62e605d4172c114d9d14a6aebf2bc122cee21866) - document module [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **api**: [fbdbede4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/fbdbede4295005ab861b1ef3c0fe552c516b8738) - add team/org paths [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) [#41](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/41) ]

### Features

- **database**: [adeffff4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/adeffff42c666243ce7e3b84ca2de3140bb350ca) - add mysql support [ [!19](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/19) [#16](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/16) ]
- **api**: [c0173d6f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c0173d6feb22e1dae42d596c8e916d3083e63c4d) - move invneotry api endpoint to '/api/device/inventory' [ [!18](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/18) ]
- **core**: [eb6ae13c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/eb6ae13c58d45240c0ad99fcde2bc1c3fbaef035) - support more history types [ [!18](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/18) ]
- **core**: [46bdd488](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/46bdd488ecedde9aeac97947caf96a5efb8c437f) - function to fetch history entry item [ [!18](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/18) [#48](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/48) [#15](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/15) ]
- **config_management**: [55f0db22](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/55f0db2217e247d7f76edd1c2e81bfd9b7570698) - Add button to groups ui for adding child group [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **access**: [7fe12603](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7fe12603080d649bedb5d29f7084083271c9c982) - throw error if no organization added [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) ]
- **itam**: [df27a7df](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/df27a7dfd365faed6ee1194433e0d8da9499600b) - add delete button to config group within ui [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **itam**: [5cb155e0](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/5cb155e01f72680c8249690be885f386679d458a) - Config groups rendered configuration now part of devices rendered configuration [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **config_management**: [39bfbd25](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/39bfbd25cbc2f936f54600d508cfd8c67a4e023b) - Ability to delete a host from a config group [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **config_management**: [fff51e38](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/fff51e38d2503bf4741b3734bfffad6d537fd862) - Ability to add a host to a config group [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **config_management**: [746b7ac7](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/746b7ac747fbb39657912225135dc1d4d4178c8c) - ensure config doesn't use reserved config keys [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **config_management**: [a7d195df](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/a7d195dfcbd38d14e04b1f45faeba09baca21696) - Config groups rendered config [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **config_management**: [fdeae217](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/fdeae217fa8883031b67df12c1f0f8b06ff92bbd) - add configuration groups [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#42](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/42) ]
- **api**: [3f68d67b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/3f68d67ba581e11cfe8ec88d2a1cdb7c6ba63e46) - add swagger ui for documentation [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) ]
- **api**: [4151e0af](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4151e0afdc6cbc9a253f41441ab0074fe947db01) - filter software to users organizations [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#45](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/45) ]
- **api**: [89a5e0f4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/89a5e0f4cc1336e042f242dfeef9a88c37b1d9f4) - filter devices to users organizations [ [!17](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/17) [#45](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/45) ]
- **api**: [3fef74e7](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/3fef74e7000bcd7e90a15d40e68f667c4a882114) - add org team view page [ [!16](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/16) [#41](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/41) ]
- **api**: [c0a09d5d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c0a09d5d505dedc5562be08844ccd3e7fc5b589a) - configure team permissions [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) [#36](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/36) ]

## 0.3.0 (2024-05-29)

### Bug Fixes

- **settings**: [d379205b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/d379205bffcc808031e8227d08220ef5d6c4e130) - Add correct permissions for team user delete [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [ebf4cb7a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ebf4cb7a5daf6fcf2f39f912203ac9ed31d7fca6) - Add correct permissions for team user view/change [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [b5669c83](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b5669c83869b38463f7c99008eb9e2b29b59faf2) - Add correct permissions for team view/change [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [58e688e0](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/58e688e0a5f44a63d1526b1a73f6ce63d67d3e07) - Add correct permissions for team add [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [e3c2f712](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e3c2f712c19bd1040c311891bd766311e302be6f) - Add correct permissions for team delete [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **access**: [0abcb462](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0abcb4628e5c5fac3d7997b457df7589772b929f) - correct back link within team view [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **access**: [b9a2d2ac](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b9a2d2ac59d8e31c99a268375b51d866186dc8bf) - correct url name to be within naming conventions [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [8bfc952f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8bfc952f2eaac67bb1c40a40fdfd8046b8580eed) - Add correct permissions for manufacturer / publisher delete [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [6e6bd107](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6e6bd1070e5c0b63f8b97c6617098b21823f609c) - Add correct permissions for manufacturer / publisher add [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [42fd648e](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/42fd648e4c6817af88248343312a1232bbfa22d3) - Add correct permissions for manufacturer / publisher view/update [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [9893e5f9](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/9893e5f95270ebc3476a5c7c070080399304afab) - Add correct permissions for software category delete [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [e35a2300](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e35a2300e261586be5aa209e5cc70ad190d8d00c) - Add correct permissions for software category add [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [0aa78a4c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0aa78a4c514faaddeb7501c1824ccdedc896c39c) - Add correct permissions for software category view/update [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [84d895c2](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/84d895c214c8109b70b3bb764c26bcc488e0a85d) - Add correct permissions for device type delete [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [cba28108](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/cba28108e04f3e9007f904c8038fa07edbf5d0ea) - Add correct permissions for device type add [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [18339547](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/18339547ba8450d7ba25872085a7efda39049a87) - Add correct permissions for device type view/update [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [d2e9e107](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/d2e9e1070e72e0aaf9dacb2cfff5d4d5c0bfb679) - Add correct permissions for device model delete [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [6880c5e9](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6880c5e90b8dbd8969b00b6571bb38f004f2db13) - Add correct permissions for device model add [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **settings**: [608a3838](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/608a38384db6415162d155b951abad743e03a10d) - Add correct permissions for device model view/update [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **access**: [cb7987f8](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/cb7987f841626687c8ec5b1ad17df3fcf2698257) - Add correct permissions for organization view/update [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **access**: [98885a32](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/98885a32e71463403f1bb9c535cb6cab39d09733) - use established view naming [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [6b37c952](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6b37c952f82367e5178ed926757e47c07436ebd5) - Add correct permissions for operating system delete [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [d81d1ba3](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/d81d1ba32a51a592193f013b0a2eb45178e9fa49) - Add correct permissions for operating system add [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [01c6cd4b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/01c6cd4bdf3a167179be4a7e07ed59751ccf44ed) - Add correct permissions for operating system view/update [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [88058234](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/880582340561060a8466c619b191d01cff261f65) - Add correct permissions for software delete [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [7dd2634f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7dd2634facf6708b5aef5c22413b2fb7f5b5da44) - Add correct permissions for software add [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [b1cfb9fa](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b1cfb9fa59d009a0dfba6a64184264166ace5a11) - for non-admin user use correct order by fields  for software view/update [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [550e6f40](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/550e6f40801071b8c5222e809d9e922de0cb0c74) - Add correct permissions for software view/update [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [94116fa1](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/94116fa173c8ed05d84d84aa09467d10fe02cd4c) - ensure permission_required parameter for view is a list [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **core**: [0e726684](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0e7266845402d07d0cd289f268ae22e4a977362a) - dont save history when no user information available [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **access**: [37ceffcb](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/37ceffcb3bd196557d3fe0cc90b7c6722113e092) - during organization permission check, check the entire list of permissions [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **core**: [c656f5bc](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c656f5bce597fc333a6549a2159b847a7338de29) - dont save history for anonymous user [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **access**: [6cb69c62](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6cb69c627ff54eb1b5bfa11da2b60d4bb0b45b19) - during permission check use post request params for an add action [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **user**: [80c3af32](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/80c3af32d533995679854d7a20984c8dd4904fd0) - on new-user signal create settings row if not exist [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [9d6bd6db](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/9d6bd6db83c56b8904d86829ef1134d689c5fb3e) - ensure only user with change permission can change a device [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **user**: [2750750a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/2750750a0c3f384ab384d409d90f00afc44cc619) - if user settings row doesn't exist on access create [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **access**: [664ad0ec](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/664ad0ec7d220fd20aea1ad405b27546ac62b57f) - adding/deleting team group actions moved to model save/delete method override [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **api**: [1c9d8b1c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/1c9d8b1c7e72a15e6186aa6d95a30e4ba3fbfac4) - add teams and permissions to org and teams respectively [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **ui**: [a3716b01](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/a3716b01584cb7842b782b0e9dd986c5542d8b6c) - correct repo url used [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **api**: [752770ec](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/752770ec32b6330ddd6060dc71dcbf3e60aacd83) - device inventory date set to read only [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **software**: [46af675f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/46af675f3c87d975a8dab3da70090fa3ab3f7033) - ensure management command query correct for migration [ [!12](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/12) [#32](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/32) ]
- **device**: [7f4a036a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7f4a036a32630599ef95bbe801d24e6204c61fcf) - OS form trying to add last inventory date when empty [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) ]
- [249b9cba](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/249b9cbab9e8f917e0e1ecd97fbcc5300c1c832f) - add static files path to urls [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) ]
- **inventory**: [f5d5529c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f5d5529c173d64ef839e9db638600e963ec6a0aa) - Dont select device_type, use 'null' [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) [#17](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/17) ]
- **base**: [d2dba2f7](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/d2dba2f7b8b38370da0dae18cab752789ac2e5e8) - show "content_title - SITE_TITLE" as site title [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) [#18](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/18) ]
- **device**: [2689c35d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/2689c35db36455982e57b08fd418ab2244280af0) - Read Only field set as required=false [ [!9](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/9) ]
- [7ae7ffae](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7ae7ffaef46cc27a2bae9acdcfa70dff80a05f7a) - correct typo in notes templates [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#7](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/7) ]
- **ui**: [5273b58a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/5273b58afb383843de6da3faca552fe143fff8eb) - Ensure navigation menu entry highlighted for sub items [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) ]

### Code Refactor

- **access**: [dd0eaae6](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/dd0eaae6b3c112bf9746b7ab37b996ba693650fc) - add to models a get_organization function [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **access**: [e34d2998](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e34d29987e128190cefd1af9cd1c504123c59170) - remove change view [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [668e871e](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/668e871e4fd52abb20426b8dafa988c423d3d3a7) - relocation item delete from list to inside device [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#23](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/23) ]
- **context_processor**: [900412b3](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/900412b31706fbba0040139dd5a04b76aeb32af2) - relocate as base [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) ]
- **itam**: [23e661ce](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/23e661cef04627912363492955b004920748edb6) - software index does not require created and modified date [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) ]
- **organizations**: [a6a0da72](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/a6a0da72b223ca64b6e7361db6e250ebbceedddb) - set org field to null if not set [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) ]
- **itam**: [66e8b290](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/66e8b290146cb241455792cb70d5de184b59819a) - move software categories to settings app [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) ]
- **itam**: [c83b8836](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c83b8836730babd497b185c3ccf28176cd298ba7) - move device types to settings app [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) ]
- **template**: [191244ed](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/191244ed40f8feacf8885f0eb9fff5b32ef91252) - content_title can be rendered in base [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) ]

### Continious Integration

- **docker**: [19d24b54](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/19d24b54a2cb9f4f81692b863260089caed12772) - build on any change [ [!12](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/12) ]
- **docker**: [2c81007c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/2c81007c0ae73586fdaabe9387cc625486dee8f4) - always build on dev branch [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) ]

### Documentaton / Guides

- [3af254d9](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/3af254d9e83093b91200a2b6ef9b6f92975a6ad8) - update software and os [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) [#12](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/12) ]
- **core**: [f7444892](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f7444892d06bb25c6a7de92ecf0410a2109ae0f5) - Add history docs [ [!9](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/9) [#5](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/5) ]
- **core**: [5dadc3fe](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/5dadc3fe98e3317c83305b73c1f9763617f486a8) - Add details about model notes [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#7](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/7) ]
- [6b5acc0d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6b5acc0d575706d30a41d26f51dfe7d6f7bdf945) - add inventory details [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#2](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/2) ]

### Features

- **access**: [7f7f7197](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7f7f719731ce1214582f69f55544a1059b874a80) - during organization permission check, check to ensure user is logged on [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **history**: [8d786d4d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8d786d4dea2ed3b290a83f90c863bbe46e53cefd) - always create an entry even if user=none [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [353117aa](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/353117aa74f0e0aac3ad687628cc7a21af690f0e) - device uuid must be unique [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **itam**: [c4fe2185](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c4fe218592fe25ebad842e8bb24ce1f2062debaa) - device serial number must be unique [ [!13](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/13) ]
- **setting**: [bf69a301](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/bf69a30163e6bafd0f951dde5fd058a31c327c09) - Enable super admin to set ALL manufacturer/publishers as global [ [!12](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/12) ]
- **setting**: [ece6b9e3](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ece6b9e354a149ff1aa73d147bedcb3c406603c0) - Enable super admin to set ALL device types as global [ [!12](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/12) [#31](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/31) ]
- **setting**: [abbda7b4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/abbda7b400d7c06fee5165157d2bf545c00d4bbe) - Enable super admin to set ALL device models as global [ [!12](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/12) [#29](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/29) ]
- **setting**: [935e119e](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/935e119e6418d561739fff4e8b1fdbb399588a18) - Enable super admin to set ALL software categories as global [ [!12](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/12) [#30](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/30) ]
- **UI**: [da0d3a81](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/da0d3a816d398d45d729ad9bcd5c0f2c625a3469) - show build details with page footer [ [!12](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/12) [#25](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/25) ]
- **software**: [51e52e69](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/51e52e69a48fefc792b8556aa20d84652a53afe7) - Add output to stdout to show what is and has occurred [ [!12](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/12) [#32](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/32) ]
- **base**: [b2f7c831](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b2f7c831551469445d091cd176ab6f210ec862e1) - Add delete icon to content header [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#23](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/23) ]
- **itam**: [e66e9b8d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e66e9b8dca740ffe411b74c8f50c53c732acef2f) - Populate initial organization value from user default organization for software category creation [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#28](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/28) ]
- **itam**: [4c002bc2](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4c002bc259062fc4926deda8a943d165496c8a25) - Populate initial organization value from user default organization for device type creation [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#28](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/28) ]
- **itam**: [90f95672](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/90f95672aa71c0a5358238f491949fb356503ff3) - Populate initial organization value from user default organization for device model creation [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#28](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/28) ]
- **api**: [7f3bf95b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7f3bf95b4627be434732b1045120e59fcae21cf3) - Populate initial organization value from user default organization inventory [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#28](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/28) ]
- **itam**: [9f5e5d25](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/9f5e5d25ec574caa0aeec91c5763f7f64c8b11c2) - Populate initial organization value from user default organization for Software creation [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#28](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/28) ]
- **itam**: [62c0bb77](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/62c0bb77fe5134669e77b198acc02c28ea073696) - Populate initial organization value from user default organization for operating system creation [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#28](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/28) ]
- **device**: [abbd6a49](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/abbd6a49d64fc24eb2c27191b594e8cefdb9042b) - Populate initial organization value from user default organization [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#28](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/28) ]
- [395f24f2](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/395f24f22c5418eed99d59659b7c60726c2ade53) - Add management command software [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#27](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/27) ]
- **setting**: [f36400db](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f36400dbb98d305e1ec54f62493f7f2cff0359b1) - Enable super admin to set ALL software as global [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#27](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/27) ]
- **user**: [ee7977fe](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ee7977fe4a5e78844e8652c313af49eda901bdad) - Add user settings panel [ [!11](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/11) [#28](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/28) ]
- **itam**: [2fcbb1ea](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/2fcbb1ead72cfa294ad26f63688b4344df56b0db) - Add publisher to software [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) [#12](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/12) ]
- **itam**: [53baeb59](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/53baeb59c9e0d0eff681ba36996e47c22bd7afe7) - Add publisher to operating system [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) [#12](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/12) ]
- **itam**: [99a559fe](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/99a559fe6dd8b234cf860c7a44fd65dc178c1bc7) - Add device model [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) [#12](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/12) ]
- **core**: [ef463b84](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ef463b845d1738a6067c786bf410f5109d832a5c) - Add manufacturers [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) [#12](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/12) ]
- **settings**: [bf0fa3f4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/bf0fa3f41dda11a02d6ae2c9b58a9e21900d2a9f) - add dummy model for permissions [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) ]
- **settings**: [ac233e43](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ac233e432f7222c59a0bb62a1cd85a6a7770c13c) - new module for whole of application settings/globals [ [!10](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/10) ]
- **access**: [724c52b7](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/724c52b777896600fc8ed5a71bb3e3f6429f9e56) - Save changes to history for organization and teams [ [!9](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/9) [#5](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/5) ]
- **software**: [b5470f2c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b5470f2cefeddac2dd154ef37975902fe511e9f6) - Save changes to history [ [!9](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/9) [#5](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/5) ]
- **operating_system**: [e16a4212](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e16a4212ccd8c7ed04d34a87bbef78a4f5565166) - Save changes to history [ [!9](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/9) [#5](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/5) ]
- **device**: [6cbcd4aa](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6cbcd4aa56441efce29c8dfe2489794716a72e8b) - Save changes to history [ [!9](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/9) [#5](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/5) ]
- **core**: [9b2abeca](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/9b2abecac37f9b2ea12a56ad2023afedc6dd78fc) - history model for saving model history [ [!9](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/9) [#5](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/5) ]
- **itam**: [dec29429](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/dec2942996073746f78463b69156e67c8d879b72) - Ability to add notes to software [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#7](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/7) ]
- **itam**: [4d5f229f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4d5f229fc737606bf272b0ccea6390ad2737dae1) - Ability to add notes to operating systems [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#7](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/7) ]
- **itam**: [725e6b8c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/725e6b8c922e0c1a6fd9d96a0f2581a8aad4a737) - Ability to add notes on devices [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#7](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/7) ]
- **core**: [8e0df948](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8e0df948d5006976981eb2ac3918c38fe74aff14) - notes model added to core [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#7](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/7) ]
- **device**: [fb041f77](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/fb041f77ebb9b9b44b0ebbed955252e22d3ee4dc) - Record inventory date and show as part of details [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#2](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/2) ]
- **ui**: [e93ce07d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/e93ce07d887b3d3151cb6714df27fd5cf9fdcd67) - Show inventory details if they exist [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#2](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/2) ]
- **api**: [c52fd080](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c52fd0802ed2395fa3a62ec41ec0297b0bca373e) - API accept computer inventory [ [!8](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/8) [#2](https://gitlab.com/nofusscomputing/projects/django_template/-/issues/2) ]

## 0.2.0 (2024-05-18)

### Bug Fixes

- **device**: [9e801fa9](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/9e801fa9eb0244d413d1555bff8e206b2ff6acd7) - correct software link [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]

### Continious Integration

- [ce18edaa](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ce18edaa398bfca5f38ae9320a6a98d6a6338318) - correct junit collection to use wildcard name [ [!6](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/6) ]
- [8b746bb9](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8b746bb9ff607950a73850d3cb0432f3d5538c63) - correct junit report name [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]

### Documentaton / Guides

- [fa97286d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/fa97286dc885dacbf2e56bab02cb42c67c70f9ab) - start to document features [ [!6](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/6) ]
- [7d007f72](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7d007f721af5e3a192c9a713069bec8c7a602d12) - update [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]

### Features

- **itam**: [a0b5a08f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/a0b5a08f0d27f8676998eaf818c449961ccc42dd) - Add Operating System to ITAM models [ [!6](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/6) ]
- **api**: [377c78d6](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/377c78d6b84398e2bbae01a91478a8ab8f94a0a2) - force content type to be JSON for req/resp [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **software**: [95405283](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/95405283b98ec6b39faedd509619dcdc39b82fc0) - view software [ [!6](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/6) ]
- **device**: [aade1e80](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/aade1e80d7d0b5bf5d45c7fe202a360d325bc396) - Prevent devices from being set global [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]
- **software**: [0e69a0ac](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0e69a0accc32ea1513394da38e78066b0e09a5ed) - if no installations found, denote [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]
- **device**: [b811eedb](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b811eedb338712e1e8ddfba3b032dbdd3513dda5) - configurable software version [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]
- **software_version**: [b0e69ee6](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b0e69ee64b929466a41d69b523641e17928188e7) - name does not need to be unique [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]
- **software_version**: [b1c4e570](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b1c4e570cfb92ce6c72bd6df28f4c9d6d9eb30e6) - set is_global to match software [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]
- **software**: [b2e1a460](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b2e1a460c853f57397c615707575f9b87b174e9c) - prettify device software action [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]
- **software**: [7f35292f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7f35292f64656830208b097388516b13e8b91613) - ability to add software versions [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]
- **base**: [7302f997](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7302f997530c9caba8e534877eba65dfa3659f9c) - add stylised action button/text [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]
- **software**: [6f6031fb](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/6f6031fb1eb789e86afb7c9cbb8c12e7f1563f56) - add pagination for index [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]
- **device**: [789b4a55](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/789b4a55d657c6c7a23af4c5d499b2be0a20481b) - add pagination for index [ [!5](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/5) ]

## 0.1.0 (2024-05-17)

### Bug Fixes

- **itam**: [d3cafe08](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/d3cafe08aa7e817d5511d8f455cbd8efe5294be2) - device software to come from device org or global not users orgs [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [5a3450f3](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/5a3450f3c0f84fc32781338ef0c644356072366e) - correct team required permissions [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **fields**: [2fe15778](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/2fe15778cb638eb420e5f3312ca24e33bfc601c5) - correct autoslug field so it works [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **docker**: [69aec7ba](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/69aec7ba6a5ea43fb3ec7f359744e30ac4a945ed) - build wheels then install [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]

### Code Refactor

- [761afb6f](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/761afb6f2bc592f29870a8eaac86c70a32086af3) - button to use same selection colour [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [30e7c8de](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/30e7c8de42eafeacba02c221ad855ca0fb68f50d) - remove inline form for org teams [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- [0edfba60](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0edfba604aba7f7810dbb038b836770b888f9d15) - rename app from itsm -> app [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [86046d6e](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/86046d6e923a32145869c1cb6cc0661eec9bd1d6) - dont use inline formset [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **views**: [c7986328](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c7986328f7c36ae6a817c4e7321d41daaa9423bd) - move views to own directory [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [c9f147d8](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c9f147d805d7d2e94cb9177b61fcb608efd5deb8) - addjust org and teams to use different view per action [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]

### Continious Integration

- [de83d749](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/de83d7490b9e6118beaf2eec303d38ac49332d16) - sync project to github [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- [8e2542f9](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8e2542f9a50e64a2bc966d85a96d561cc1de8e67) - correct test path [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **coverage**: [eb9eeff4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/eb9eeff4ed63e09a4670c3b3ac07f98f2575694b) - add test coverage to ci [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]

### Documentaton / Guides

- [f59ffa58](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f59ffa581c5711fcb414aa4aa3ae9a3695ce4786) - add base itam pages [ [!2](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/2) ]
- [c43f41d9](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c43f41d9587e060ea7f3c4e51a72f5c928c9384b) - notate global object [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- [db5d7e18](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/db5d7e18ad77c7402a8d73495ddaa9bbe626754b) - update and include permissions [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]

### Features

- **api**: [962ae2b8](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/962ae2b8dfaf7cccdfd449e2a7db087f9b3542c9) - initial token authentication implementation [ [!3](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/3) ]
- **docker**: [4b77e2e6](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4b77e2e63dcc57534e821386584c3b6896d44173) - add settings to store data in separate volume [ [!2](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/2) ]
- **django**: [a96fc062](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/a96fc062f209e86bf4a8f40dd4a738ad8d889cf2) - add split settings for specifying additional settings paths [ [!2](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/2) ]
- **api**: [0c38155c](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0c38155c4453d89c552eaf16aaf7d7e2092b2431) - Add device config to device [ [!2](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/2) ]
- **itam**: [2d67f93d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/2d67f93d882d1ebe7782d9425c915e31f3a16453) - add organization to device installs [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **itam**: [195bb5e4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/195bb5e4ab29540647cf30d22fcbb6e6c06e6db6) - migrate app from own repo [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- [f98e3bc9](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f98e3bc9c2ff5f3627dc2f49df6eb7e6afdc974c) - Enable API by default [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **admin**: [4b214d0b](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/4b214d0b8cc10f43c708ef45ce5e20225f9b6c21) - remove team management [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **admin**: [736d3930](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/736d3930dff9705c3d27f853ed9a5f0000108164) - remove group management [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [50371267](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/50371267c1fb02e066d9a4ac066f54128ce957ea) - adjustable team permissions [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **api**: [102aa981](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/102aa981ce0a72fa263016139076e87778255226) - initial work on API [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **template**: [50cc050a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/50cc050adf4cfcf43303350850caa56bf649874b) - add header content icon block [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **tenancy**: [857aa7af](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/857aa7af72f9e92be04d9cc258fc5875e4223ffd) - Add is_ global field [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [070ba47d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/070ba47de284d912fc86aabb323a1639e4328d4a) - when modifying a team ad/remove user from linked group [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **auth**: [a0f4940a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/a0f4940a09fb00486ed8280eb17ec35811839947) - include python social auth django application [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- [b3b12638](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/b3b12638ad85fe1b3744561a2220d255cf9e105c) - Build docker container for release [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [ca68c258](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/ca68c2589a8cabdc11fbe7e95b0a5d58f5fd8a0e) - add permissions to team and user [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **style**: [9d507d82](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/9d507d82df745a057f7903d76bf439b142e71494) - format check boxes [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [7445d880](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7445d8807ce7e995fdb2f7443e59b407e1cf92dd) - delete team user form [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **view**: [fa5703cb](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/fa5703cb794b010d46dfdce1bd03243ca260cde1) - new user [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- [8a62c3f6](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/8a62c3f6ee061add16ae165857735a44cb0bb085) - user who is 'is_superuser' to view everything and not be denied access [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [af858dcc](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/af858dcc43c414f6c523a757345537149eb4178e) - add org mixin to current views [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [2b5047db](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/2b5047db2db18bfb10ccaadbf9adce12802b9c11) - add views for each action for teams [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [d715038a](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/d715038a884cad87fba0a55f0d30ea66fda322b0) - add mixin to check organization permissions against user and object [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **account**: [0446d391](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/0446d39190406fb54baf85bc031708a03473e020) - show admin site link if user is staff [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **development**: [c0212178](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/c0212178111f000c20b0b60426d3542dd704e8ce) - added the debug django app [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **access**: [af5175c4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/af5175c4e198f5431d3f7b0d5b94f78818366053) - rename structure to access and remove organization app in favour of own implementation [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **account**: [f7bbb122](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/f7bbb122e6651635a4cb8e74246a8e155be6dcd1) - Add user password change form [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **urls**: [789777a2](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/789777a270bbd46e0a3126026e7236222f38da35) - provide option to exclude navigation items [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **structure**: [dae7f3c4](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/dae7f3c47a3c511ac30decb647461902e0dc248f) - unregister admin pages from organization app not required [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **auth**: [96a99c9d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/96a99c9df181367498e3f8d8031a0c1e4304a312) - Custom Login Page [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **auth**: [65bd32df](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/65bd32dfad3d7f8f867aea84dd4ad31133aa8fc1) - Add User Account Menu [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **auth**: [283ef9a7](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/283ef9a7145d424bca2c898935e08cdc83038fff) - Setup Login required [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- [71bcd192](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/71bcd192b3e9d6616ff8dca5d8b5745ad371de92) - Dyno-magic build navigation from application urls.py [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **structure**: [7cdfdab1](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/7cdfdab1fc966f3c92e69baf1162033c7d2e9bc4) - Select and View an individual Organization [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **structure**: [dd54eae8](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/dd54eae8d747ab0a17e71797d675a45eeaaae813) - View Organizations [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **app**: [9092445d](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/9092445d0bcbe3215f675eb5e4794cfefb710913) - Add new app structure for organizations and teams [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **template**: [1a886184](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/1a8861846bb16255c204729438057e42b3c81d7a) - add base template [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]
- **django**: [81b170ca](https://gitlab.com/nofusscomputing/projects/django_template/-/commit/81b170cabf2398304861fa5b68fadb962630d4cb) - add organizations app [ [!1](https://gitlab.com/nofusscomputing/projects/django_template/-/merge_requests/1) ]

## 0.0.1 (2024-05-06)
