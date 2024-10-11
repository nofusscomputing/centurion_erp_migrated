


class TicketValues:

    
    _DRAFT_INT    = '1'
    _NEW_INT      = '2'

    _ASSIGNED_INT = '3'
    _CLOSED_INT   = '4'
    _INVALID_INT  = '5'

    #
    # ITSM statuses
    #

    # Requests / Incidents / Problems / Changed
    _ASSIGNED_PLANNING_INT = '6'
    _PENDING_INT           = '7'

    # Requests / Incidents / Problems
    _SOLVED_INT            = '8'

    # Problem

    _OBSERVATION_INT = '9'

    # Problems / Changes

    _ACCEPTED_INT = '10'

    # Changes

    _EVALUATION_INT    = '11'
    _APPROVALS_INT     = '12'
    _TESTING_INT       = '13'
    _QUALIFICATION_INT = '14'
    _APPLIED_INT       = '15'
    _REVIEW_INT        = '16'
    _CANCELLED_INT     = '17'
    _REFUSED_INT       = '18'




    _DRAFT_STR    = 'Draft'
    _NEW_STR      = 'New'

    _ASSIGNED_STR = 'Assigned'
    _CLOSED_STR   = 'Closed'
    _INVALID_STR  = 'Invalid'

    #
    # ITSM statuses
    #

    # Requests / Incidents / Problems / Changed
    _ASSIGNED_PLANNING_STR = 'Assigned (Planning)'
    _PENDING_STR           = 'Pending'

    # Requests / Incidents / Problems
    _SOLVED_STR            = 'Solved'

    # Problem

    _OBSERVATION_STR = 'Under Observation'

    # Problems / Changes

    _ACCEPTED_STR = 'Accepted'

    # Changes

    _EVALUATION_STR    = 'Evaluation'
    _APPROVALS_STR     = 'Approvals'
    _TESTING_STR       = 'Testing'
    _QUALIFICATION_STR = 'Qualification'
    _APPLIED_STR       = 'Applied'
    _REVIEW_STR        = 'Review'
    _CANCELLED_STR     = 'Cancelled'
    _REFUSED_STR       = 'Refused'


    class ExternalSystem:

        _GITHUB_INT   = '1'
        _GITHUB_VALUE = 'Github'
        _GITLAB_INT   = '2'
        _GITLAB_VALUE = 'Gitlab'

        _CUSTOM_1_INT   = '9999'
        _CUSTOM_1_VALUE = 'Custom #1 (Imported)'
        _CUSTOM_2_INT   = '9998'
        _CUSTOM_2_VALUE = 'Custom #2 (Imported)'
        _CUSTOM_3_INT   = '9997'
        _CUSTOM_3_VALUE = 'Custom #3 (Imported)'
        _CUSTOM_4_INT   = '9996'
        _CUSTOM_4_VALUE = 'Custom #4 (Imported)'
        _CUSTOM_5_INT   = '9995'
        _CUSTOM_5_VALUE = 'Custom #5 (Imported)'
        _CUSTOM_6_INT   = '9994'
        _CUSTOM_6_VALUE = 'Custom #6 (Imported)'
        _CUSTOM_7_INT   = '9993'
        _CUSTOM_7_VALUE = 'Custom #7 (Imported)'
        _CUSTOM_8_INT   = '9992'
        _CUSTOM_8_VALUE = 'Custom #8 (Imported)'
        _CUSTOM_9_INT   = '9991'
        _CUSTOM_9_VALUE = 'Custom #9 (Imported)'



    class Priority:

        _VERY_LOW_INT    = '1'
        _VERY_LOW_VALUE  = 'Very Low'
        _LOW_INT         = '2'
        _LOW_VALUE       = 'Low'
        _MEDIUM_INT      = '3'
        _MEDIUM_VALUE    = 'Medium'
        _HIGH_INT        = '4'
        _HIGH_VALUE      = 'High'
        _VERY_HIGH_INT   = '5'
        _VERY_HIGH_VALUE = 'Very High'
        _MAJOR_INT       = '6'
        _MAJOR_VALUE     = 'Major'
