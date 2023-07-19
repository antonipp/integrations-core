# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# This file is autogenerated.
# To change this file you should edit assets/configuration/spec.yaml and then run the following commands:
#     ddev -x validate config -s <INTEGRATION_NAME>
#     ddev -x validate models -s <INTEGRATION_NAME>

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from datadog_checks.base.utils.functions import identity
from datadog_checks.base.utils.models import validation

from . import defaults, validators


class MetricPatterns(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    exclude: Optional[Sequence[str]] = None
    include: Optional[Sequence[str]] = None


class InstanceConfig(BaseModel):
    model_config = ConfigDict(
        validate_default=True,
        frozen=True,
    )
    auto_discover_channels: Optional[bool] = None
    auto_discover_queues: Optional[bool] = None
    channel: str = Field(..., min_length=1)
    channel_status_mapping: Optional[Mapping[str, Any]] = None
    channels: Optional[Sequence[str]] = None
    collect_reset_queue_metrics: Optional[bool] = None
    collect_statistics_metrics: Optional[bool] = None
    connection_name: Optional[str] = Field(None, min_length=1)
    convert_endianness: Optional[bool] = None
    disable_generic_tags: Optional[bool] = None
    empty_default_hostname: Optional[bool] = None
    host: Optional[str] = Field(None, min_length=1)
    metric_patterns: Optional[MetricPatterns] = None
    min_collection_interval: Optional[float] = None
    mqcd_version: Optional[float] = Field(None, ge=1.0)
    override_hostname: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=1)
    port: Optional[int] = None
    queue_manager: str = Field(..., min_length=1)
    queue_manager_process: Optional[str] = None
    queue_manager_timezone: Optional[str] = Field(None, min_length=1)
    queue_patterns: Optional[Sequence[str]] = None
    queue_regex: Optional[Sequence[str]] = None
    queue_tag_re: Optional[Mapping[str, Any]] = None
    queues: Optional[Sequence[str]] = None
    service: Optional[str] = None
    ssl_auth: Optional[bool] = None
    ssl_certificate_label: Optional[str] = None
    ssl_cipher_spec: Optional[str] = None
    ssl_key_repository_location: Optional[str] = Field(None, min_length=1)
    tags: Optional[Sequence[str]] = None
    timeout: Optional[int] = None
    try_basic_auth: Optional[bool] = None
    username: Optional[str] = Field(None, min_length=1)

    @model_validator(mode='before')
    def _initial_validation(cls, values):
        return validation.core.initialize_config(getattr(validators, 'initialize_instance', identity)(values))

    @field_validator('*', mode='before')
    def _ensure_defaults(cls, value, info):
        field = cls.model_fields[info.field_name]
        field_name = field.alias or info.field_name
        if field_name in info.context['configured_fields']:
            return value

        return getattr(defaults, f'instance_{info.field_name}', lambda: value)()

    @field_validator('*')
    def _run_validations(cls, value, info):
        field = cls.model_fields[info.field_name]
        field_name = field.alias or info.field_name
        if field_name not in info.context['configured_fields']:
            return value

        return getattr(validators, f'instance_{info.field_name}', identity)(value, field=field)

    @field_validator('*', mode='after')
    def _make_immutable(cls, value):
        return validation.utils.make_immutable(value)

    @model_validator(mode='after')
    def _final_validation(cls, model):
        return validation.core.check_model(getattr(validators, 'check_instance', identity)(model))
