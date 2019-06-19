from oef.schema import DataModel, AttributeSchema, Location


class TRIP_DATAMODEL(DataModel):
    PERSON_ID = AttributeSchema("account_id",
                                str,
                                is_attribute_required=True,
                                attribute_description="Person ID.")

    CAN_BE_DRIVER = AttributeSchema("can_be_driver",
                                    bool,
                                    is_attribute_required=True,
                                    attribute_description="Can person be driver?")

    TRIP_ID = AttributeSchema("trip_id",
                              str,
                              is_attribute_required=True,
                              attribute_description="Person ID.")

    FROM_LOCATION_LATITUDE = AttributeSchema("from_location_latitude",
                                             Location,
                                             is_attribute_required=True,
                                             attribute_description="Latitude of FROM point.")

    FROM_LOCATION_LONGITUDE = AttributeSchema("from_location_longitude",
                                              Location,
                                              is_attribute_required=True,
                                              attribute_description="Longitude of FROM point.")

    TO_LOCATION_LATITUDE = AttributeSchema("to_location_latitude",
                                           Location,
                                           is_attribute_required=True,
                                           attribute_description="Latitude of TO point.")

    TO_LOCATION_LONGITUDE = AttributeSchema("to_location_longitude",
                                            Location,
                                            is_attribute_required=True,
                                            attribute_description="Longitude of TO point.")

    DISTANCE_AREA = AttributeSchema("distance_area",
                                    float,
                                    is_attribute_required=False,
                                    attribute_description="Allowed distance of area from center of way-point.")

    def __init__(self):
        super().__init__("trip_datamodel", [self.PERSON_ID,
                                            self.CAN_BE_DRIVER,
                                            self.TRIP_ID,
                                            self.FROM_LOCATION_LATITUDE,
                                            self.FROM_LOCATION_LONGITUDE,
                                            self.TO_LOCATION_LATITUDE,
                                            self.TO_LOCATION_LONGITUDE,
                                            self.DISTANCE_AREA],
                         "Trip create fully.")
