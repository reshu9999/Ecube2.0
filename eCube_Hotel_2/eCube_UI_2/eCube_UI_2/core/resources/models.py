import json
from .custom_exceptions import FieldHTMLMapDoesNotExist
from hotel.master.models import UserMaster

from django.db.models import *
from django.urls import reverse
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


class ModelHandler(object):
    MODELS_MAP = {}
    REQUIRED_MODELS = list()

    @classmethod
    def check_required_models(cls):
        for name in cls.REQUIRED_MODELS:
            if not (name in cls.MODELS_MAP or cls.MODELS_MAP[name]):
                raise MissingRequiredModel('"%s" Missing' % name)
        return True

class AetosModel(Model):
    active = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    modified_at = DateTimeField(auto_now=True)
    _extra = TextField(default=json.dumps(dict()))

    class Meta:
        abstract = True

    @property
    def extra_details(self):
        return json.loads(self._extra or self.get_meta_field(self._extra).default)

    @classmethod
    def get_meta_field(cls, field):
        if isinstance(field, query_utils.DeferredAttribute):
            field = field.field_name
        if not isinstance(field, str):
            raise TypeError('field param should be of type %s' % str)
        field_name = field

        for meta_field in cls._meta.fields:
            if field_name == meta_field.attname:
                return meta_field

    def set_extra_details(self, extra_details, commit=False):
        old_extra_details = self.extra_details
        old_extra_details.update(extra_details)
        self._extra = json.dumps(old_extra_details)
        if commit:
            self.save()
        return self.extra_details


class HTMLModel(object):
    FIELD_HTML_DEFAULT_MAP = {
        CharField: {
            'template': 'hotel/master/html_model/components/fields/char-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                            'display_name': f.verbose_name},
        },
        BooleanField: {
            'template': 'hotel/master/html_model/components/fields/bool-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                            'display_name': f.verbose_name},
        },
        IntegerField: {
            'template': 'hotel/master/html_model/components/fields/char-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                            'display_name': f.verbose_name},
        },
        PositiveIntegerField: {
            'template': 'hotel/master/html_model/components/fields/char-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                            'display_name': f.verbose_name},
        },
        PositiveSmallIntegerField: {
            'template': 'hotel/master/html_model/components/fields/char-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                            'display_name': f.verbose_name},
        },
        ForeignKey: {
            'template': 'hotel/master/html_model/components/fields/select-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.name), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name, 'readonly': True,
                                           'options': f.related_model.objects.all()},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'options': f.related_model.objects.all(),
                                            'field_name': f.name, 'display_name': f.verbose_name},
            'insert_function': lambda i, f: f.related_model.objects.get(id=i)
        },
        ManyToManyField: {
            'template': 'hotel/master/html_model/components/fields/multi-select-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.name), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name, 'readonly': True,
                                           'options': f.related_model.objects.all()},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'options': f.related_model.objects.all(),
                                            'field_name': f.name, 'display_name': f.verbose_name},
        },
        DateField: {
            'template': 'hotel/master/html_model/components/fields/date-time-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                            'display_name': f.verbose_name},
        },
        DateTimeField: {
            'template': 'hotel/master/html_model/components/fields/date-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                            'display_name': f.verbose_name},
        },
        TextField: {
            'template': 'hotel/master/html_model/components/fields/text-field.html',
            'view_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                          'display_name': f.verbose_name, 'readonly': True},
            'input_context': lambda o, f: {'field_name': f.name, 'display_name': f.verbose_name},
            'update_context': lambda o, f: {'input_val': getattr(o, f.attname), 'field_name': f.name,
                                            'display_name': f.verbose_name},
        },
    }
    FIELD_HTML_CUSTOM_MAP = {}
    DEFAULT_IGNORE_FIELDS = [
        AutoField,
        'created_at',
        'modified_at',
        'created_date',
        'createddate',
        'modified_date',
        'modifieddate',
        'created_by_id',
        'createdby_id',
        'modified_by_id',
        'modifiedby_id',
        '_extra',
    ]
    CUSTOM_IGNORE_FIELDS = []
    IGNORE_FIELDS = DEFAULT_IGNORE_FIELDS + CUSTOM_IGNORE_FIELDS
    HTML_VIEW_TEMPLATE_MAP = {'template': 'hotel/master/html_model/components/view-tr.html'}
    HTML_INPUT_TEMPLATE_MAP = {'template': 'hotel/master/html_model/components/input-modal.html'}
    HTML_UPDATE_TEMPLATE_MAP = {'template': 'hotel/master/html_model/components/update-modal.html'}

    @classmethod
    def _get_field_map(cls, field):
        FIELD_HTML_MAP = cls.FIELD_HTML_CUSTOM_MAP
        FIELD_HTML_MAP.update(cls.FIELD_HTML_DEFAULT_MAP)

        if field in FIELD_HTML_MAP:
            return FIELD_HTML_MAP[field.attname]
        elif field.attname in FIELD_HTML_MAP:
            return FIELD_HTML_MAP[field]
        elif type(field) in FIELD_HTML_MAP:
            return FIELD_HTML_MAP[type(field)]
        else:
            raise FieldHTMLMapDoesNotExist('Field: "%s" Does not exist in Field Mappings' % field)

    @classmethod
    def _get_field(cls, model_cls, field_name):
        for field in model_cls._meta.fields:
            if field.name == field_name:
                return field
        raise Exception('Field: "%s" Does not exist in Model: "%s"' % (field_name, model_cls))

    @classmethod
    def _prep_params(cls, model_cls, params):
        for field_name, value in params.items():
            field = cls._get_field(model_cls, field_name)
            field_map = cls._get_field_map(field)
            insert_function = field_map.get('insert_function')
            if insert_function:
                params[field_name] = insert_function(value, field)
        return params

    @classmethod
    def add_object(cls, model_cls, params):
        prepped_params = cls._prep_params(model_cls, params)
        prepped_params.update({
            'created_by': UserMaster.objects.get(User_ID=1),
            'modified_by': UserMaster.objects.get(User_ID=1),
        })

        model_obj = model_cls(**prepped_params)
        model_obj.save()
        return model_obj

    @classmethod
    def update_object(cls, model_obj, params):
        prepped_params = cls._prep_params(model_obj, params)
        prepped_params.update({
            'created_by': UserMaster.objects.get(User_ID=1),
            'modified_by': UserMaster.objects.get(User_ID=1),
        })

        for key, value in prepped_params.items():
            setattr(model_obj, key, value)
        model_obj.save()
        return model_obj

    @classmethod
    def delete_object(cls, model_obj):
        model_obj._active=0
        model_obj.save()
        return None

    def __init__(self, model_object, add_url, update_url):
        self._instance = model_object
        self.add_url = reverse(add_url)
        self.update_url = reverse(update_url)

    def _get_fields_html(self, field, html_type):
        field_map = self._get_field_map(field)
        field_context = field_map['%s_context' % html_type](self._instance, field)
        field_template = get_template(field_map['template'])
        return field_template.render(field_context)

    @property
    def _model_fields(self):
        return [field for field in self._instance._meta.fields
                if not (field.attname in self.IGNORE_FIELDS
                        or field in self.IGNORE_FIELDS
                        or type(field) in self.IGNORE_FIELDS)]

    @property
    def get_view_context(self):
        return {'view_fields': [self._get_fields_html(field, 'view') for field in self._model_fields],
                'model_title': self._instance._meta.verbose_name.title, 'object': self._instance,}

    @property
    def get_input_context(self):
        return {'input_fields': [self._get_fields_html(field, 'input') for field in self._model_fields],
                'model_title': self._instance._meta.verbose_name.title, 'add_url': self.add_url}

    @property
    def get_update_context(self):
        return {'update_fields': [self._get_fields_html(field, 'update') for field in self._model_fields],
                'model_title': self._instance._meta.verbose_name.title, 'object': self._instance,
                'update_url': self.update_url}

    @property
    def render_view(self):
        return get_template(self.HTML_VIEW_TEMPLATE_MAP['template']).render(self.get_view_context)

    @property
    def render_input(self):
        return get_template(self.HTML_INPUT_TEMPLATE_MAP['template']).render(self.get_input_context)

    @property
    def render_update(self):
        return get_template(self.HTML_UPDATE_TEMPLATE_MAP['template']).render(self.get_update_context)


class MasterViews(object):

    HTML_MODEL = HTMLModel

    @classmethod
    def _clean_request_value(cls, value):
        if isinstance(value, list):
            pass

    def __init__(self, model, ops_urls):
        self.model = model
        self.ops_urls = ops_urls

    def index(self, request):
        ops_urls = self.ops_urls
        context = {
            'view_list': [self.HTML_MODEL(obj, **ops_urls).render_view for obj in self.model.objects.all()],
            'update_modals': [self.HTML_MODEL(obj, **ops_urls).render_update for obj in self.model.objects.all()],
            'input_modal': self.HTML_MODEL(self.model, **ops_urls).render_input,
            'ops_urls': ops_urls,
        }
        return render(request, 'hotel/master/ui.html', context)

    @csrf_exempt
    def add(self, request):
        post_data = {k: v for k, v in request.POST.items()}
        self.HTML_MODEL.add_object(self.model, post_data)
        return redirect('master_index')

    @csrf_exempt
    def update(self, request, obj_id):
        post_data = {k: v for k, v in request.POST.items()}
        country_object = self.model.objects.get(id=obj_id)
        self.HTML_MODEL.update_object(country_object, post_data)
        return redirect('master_index')

    @csrf_exempt
    def delete(self, request, obj_id):
        country_object = self.model.objects.get(id=obj_id)
        self.HTML_MODEL.delete_object(country_object)
        return redirect('master_index')
