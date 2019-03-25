from param_parser.core import services, exceptions


class ParamParser(object):

    DATA_TYPE = None
    CALL_FUNC_IDENTIFIER = 'return_func__'
    EXCEPTIONS = {
        'incorrect_data_type': exceptions.IncorrectParserObjectDataType
    }

    def __init__(self, name, data_source_prop, source_key, return_func):
        self.name = name
        self.source_key = source_key

        self._data_source = self._get_data_source(data_source_prop)
        self._return_func = self._get_return_func(return_func)

    def _validated_getattr(self, _prop):
        if not hasattr(self, _prop):
            raise NotImplementedError(_prop)
        return getattr(self, _prop)

    def _get_data_source(self, data_source_prop):
        return self._validated_getattr(data_source_prop)

    def _get_return_func(self, _return_func):
        return self._validated_getattr(self.CALL_FUNC_IDENTIFIER + _return_func)

    @property
    def parsed_value(self):
        return self._return_func(self._parse_value(self._data_source, self.source_key))

    @classmethod
    def _parse_value(cls, data_source, source_key):
        if cls.DATA_TYPE == 'XPATH':
            return data_source.xpath(source_key)
        if cls.DATA_TYPE == 'JSON':
            return cls._read_multi_level(data_source, source_key)
        raise cls.EXCEPTIONS['incorrect_data_type']

    @classmethod
    def _read_multi_level(cls, data_source, source_key):
        deep_source_keys = source_key.split('.') if source_key else list()
        response = data_source
        for k in deep_source_keys:
            response = response[k]
        return response

    @classmethod
    def return_func__empty_if_None(cls, response):
        return response or ''

    @classmethod
    def return_func__single_obj_array(cls, response, stripped=True):
        response = cls.return_func__empty_if_None(response)

        if not isinstance(response, list):
            response = [response]

        if len(response) > 1:
            if stripped:
                return response[0].strip()
            return response[0]


class ParserBase(object):

    TRL = None
    CONFIG_FILE = None
    PARSED_PARAM_IDENTIFIER = 'parsed__'
    PROPERTIES = list()
    EXCEPTIONS = {
        'missing_field': exceptions.MissingFieldInParser,
    }
    SERVICE_CALLS = {
        'save_in_mongo': services.API.SaveDataInMongoDB,
        'get_field_mapping': services.API.GetFieldMapping,
    }

    def __init__(self, parser_data):
        self.parser_data = parser_data
        self.request_id = parser_data['requestId']
        for param_parser in self.PROPERTIES:
            setattr(self, self.PARSED_PARAM_IDENTIFIER + param_parser.name, param_parser.parsed_value)

    def _get_parsed_value(self, param_name):
        return 'value of %s' % param_name
        # return getattr(self, self.PARSED_PARAM_IDENTIFIER + param_name)

    @property
    def complete_parsed_values(self):
        """
        save in mongo db the return value
        :return: parsed_data with all the source_key related fields in key 'payload' with meta details attached to it
        """
        defined_fields = [parser_param.name for parser_param in self.PROPERTIES]
        required_fields = self.SERVICE_CALLS['get_field_mapping'](self.request_id)
        if not set(required_fields).issubset(set(defined_fields)):
            raise self.EXCEPTIONS['missing_field']

        payload = {param: self._get_parsed_value(param)
                   for param in required_fields
                   if param in defined_fields}

        meta_data = self.parser_data['meta']
        meta_data.update({'payload': payload})
        return meta_data

    @classmethod
    def save_parsed_data(cls, parsed_data):
        return cls.SERVICE_CALLS['save_in_mongo'](parsed_data)
