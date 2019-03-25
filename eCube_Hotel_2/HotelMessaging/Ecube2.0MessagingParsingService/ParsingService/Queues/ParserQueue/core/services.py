from param_parser.core.utils import save_parsed_data, get_field_mapping


class API(object):

    @classmethod
    def SaveDataInMongoDB(cls, mongo_data):
        return save_parsed_data(mongo_data)

    @classmethod
    def GetFieldMapping(cls, request_id):
        return get_field_mapping(request_id)
