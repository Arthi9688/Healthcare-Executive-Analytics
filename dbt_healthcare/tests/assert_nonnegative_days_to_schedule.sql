select *
from {{ ref('int_request_to_appointment') }}
where days_to_schedule < 0