# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#   Copyright 2018 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
from typing import List

from oef.schema import DataModel, AttributeSchema, Location

class TRANSPORT_DATAMODEL(DataModel):
    PRICE_PER_KM = AttributeSchema("price_per_km",
                                   int,
                                   is_attribute_required=True,
                                   attribute_description="Provides the price per kilometer.")

    STATE = AttributeSchema("state",
                            str,
                            is_attribute_required=True,
                            attribute_description="Current state of transport.")

    DRIVER_ID = AttributeSchema("driver_id",
                                str,
                                is_attribute_required=False,
                                attribute_description="Driver.")

    PASSENGERS = AttributeSchema("passengers_ids",
                                 str,
                                 is_attribute_required=False,
                                 attribute_description="All passangers.")

    POSITION = AttributeSchema("position",
                               Location,
                               is_attribute_required=True,
                               attribute_description="Latitude of transport.")

    def __init__(self):
        super().__init__("transport_datamodel", [self.PRICE_PER_KM,
                                            self.STATE,
                                            self.DRIVER_ID,
                                            self.PASSENGERS,
                                            self.POSITION],
                         "Transport create fully.")
