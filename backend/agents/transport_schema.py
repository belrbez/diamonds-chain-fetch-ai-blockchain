from oef.schema import DataModel, AttributeSchema, Location


class TRANSPORT_DATAMODEL(DataModel):
    PRICE_PER_KM = AttributeSchema("price_per_km",
                                   float,
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

    LOCATION_LATITUDE = AttributeSchema("location_latitude",
                                        float,
                                        is_attribute_required=True,
                                        attribute_description="Latitude of transport.")

    LOCATION_LONGITUDE = AttributeSchema("location_longitude",
                                         float,
                                         is_attribute_required=True,
                                         attribute_description="Longitude of transport.")

    def __init__(self):
        super().__init__("transport_datamodel", [self.PRICE_PER_KM,
                                                 self.STATE,
                                                 self.DRIVER_ID,
                                                 self.PASSENGERS,
                                                 self.LOCATION_LATITUDE,
                                                 self.LOCATION_LONGITUDE],
                         "Transport create fully.")
