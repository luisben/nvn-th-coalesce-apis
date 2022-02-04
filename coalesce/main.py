import math
from typing import Optional, Callable, List
from dataclasses import fields
import logging
from http import HTTPStatus

import requests

from models import MemberRecord, APIConfig
from config import API_LIST, FUNCTIONS

logger = logging.getLogger(__name__)
AggregateFunction = Callable[[List[int]], int]


def coalesce_member_data(member_id: int,
                         coalesce_function_name: Optional[str] = "mean",
                         coalesce_function: Optional[AggregateFunction] = None
                         ):
    # gather data from all APIs
    member_data_results = _get_member_data(member_id)
    # apply coalesce function
    if not coalesce_function:
        if coalesce_function_name not in FUNCTIONS:
            return {"error": "Invalid coalesce function."}
        coalesce_function = FUNCTIONS[coalesce_function_name]
    # return w/count of failed  about missing data
    agg_data: MemberRecord = _apply_agg_function(member_data_results["data"], coalesce_function)
    return {"member_data": agg_data,
            "aggregated_sources": len(member_data_results),
            "failed_sources": member_data_results["failure_count"]}


def _apply_agg_function(member_records: List[MemberRecord], agg_function: AggregateFunction) -> MemberRecord:
    agg_values = {}
    for attr_name in [field.name for field in fields(MemberRecord)]:
        attr_values = [member_record.__getattribute__(attr_name) for member_record in member_records]
        agg_values[attr_name] = math.floor(agg_function(attr_values))
    return MemberRecord(**agg_values)


def _get_member_data(member_id):
    member_data = []
    failed_invocations = 0
    for api_config in API_LIST:
        api_member_data = _invoke_api(api_config, member_id)
        if api_member_data:
            member_data.append(api_member_data)
        else:
            failed_invocations += 1
    return {"data": member_data, "failure_count": failed_invocations}


def _invoke_api(api_config: APIConfig, member_id: int) -> MemberRecord:
    request_params = {"member_id": member_id}
    response: requests.Response = requests.get(api_config.hostname, headers=api_config.headers, params=request_params)
    if response.status_code != HTTPStatus.OK:
        logger.error("Error invoking API %s: %s", api_config.id, response.status_code)
        return
    return MemberRecord(**response.json())
