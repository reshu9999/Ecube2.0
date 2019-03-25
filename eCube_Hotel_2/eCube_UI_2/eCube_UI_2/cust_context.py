import json
from django.urls import reverse
from django.conf import settings


class SessionPermissionReader(object):

    SESSION_KEY = 'UserMenuAccess'

    def __init__(self, request):
        self._request = request

    @property
    def is_user_logged_in(self):
        return self._request.user.is_authenticated

    @property
    def session_permissions(self):
        if self.is_user_logged_in and self.SESSION_KEY in self._request.session:
            return self._request.session[self.SESSION_KEY]

    def permission(self, menu_key):
        if self.session_permissions and menu_key in self.session_permissions:
            return self.session_permissions[menu_key]


class BasePermission(object):

    SESSION_PERM_READER = SessionPermissionReader

    def __init__(self, name, key=None, limit=None, link=None, children=None):
        if link and children:
            raise Exception('cannot have both link and children')

        if children:
            if not isinstance(children, list):
                children = [children]

            for child in children:
                if type(child) != type(self):
                    raise Exception('children should be "%s" type' % type(self))

        self.verbose = name
        self.key = key or "_".join(self.verbose.lower().split(' '))
        self._default_limit = limit
        self.link = link
        self.children = children

    @classmethod
    def _user_perm(cls, request, menu_key):
        return cls.SESSION_PERM_READER(request).permission(menu_key)

    def _is_visible(self, request):
        raise NotImplementedError

    def _get_limit(self, request):
        raise NotImplementedError

    def _permission_type(self, request):
        raise NotImplementedError

    def to_context(self, request):
        raise NotImplementedError

    def to_role(self, request):
        return {'limits': self._get_limit(request) or self._default_limit,
                'permission_type': self._permission_type(request),
                'accessitems': self.key}


class MenuPermission(BasePermission):

    CREATE_REQUEST_BUSINESS_MAP = {
        'Hotel': 'hotel_create_request_index',
        'Hotel+Flight': 'hotel_plus_flight_request',
    }

    def _is_visible(self, request):
        user_perm = self._user_perm(request, self.key)
        if user_perm and 'limits' in user_perm:
            return bool(user_perm['limits'])

    def _get_limit(self, request):
        return 1

    def _permission_type(self, request):
        return 'view'

    def to_create_request_context(self, request):
        business = request.session.get('business')
        # business = 'Hotel + Flight'
        if business in self.CREATE_REQUEST_BUSINESS_MAP:
            create_request_link = self.CREATE_REQUEST_BUSINESS_MAP[business]
            return {'show': self._is_visible(request), 'name': self.verbose, 'link': reverse(create_request_link)}

    def to_context(self, request):

        if hasattr(self, 'to_%s_context' % self.key):
            custom_context = getattr(self, 'to_%s_context' % self.key)(request)
            if custom_context:
                return custom_context

        if self.children:
            return {'show': self._is_visible(request), 'name': self.verbose, 'list': [child.to_context(request)
                                                                                      for child in self.children]}
        if self.link:
            return {'show': self._is_visible(request), 'name': self.verbose, 'link': self.link}


class LimitPermission(BasePermission):

    def _is_visible(self, request):
        return True

    def _get_limit(self, request):
        user_perm = self._user_perm(request, self.key)
        if user_perm and 'limits' in user_perm:
            return user_perm['limits']

    def _permission_type(self, request):
        return 'limit'

    def to_context(self, request):
        return {'show': self._is_visible(request), 'name': self.verbose, 'limit': self._get_limit(request)}


class OPSPermission(BasePermission):

    def _is_visible(self, request):
        return True

    def _get_limit(self, request):
        return 1

    def _permission_type(self, request):
        return 'ops'

    def to_context(self, request):
        return {'show': self._is_visible(request), 'name': self.verbose}


class RolePermissions(object):
    MENU_CLASS = MenuPermission
    LIMIT_CLASS = LimitPermission
    OPS_CLASS = OPSPermission

    def __init__(self, menu_perms, limit_perms, ops_perms):
        self.menu_perms = menu_perms
        self.limit_perms = limit_perms
        self.ops_perms = ops_perms

    @staticmethod
    def _make_permissions_list(perm_class, perm_list):
        return [perm_class(**perm) for perm in perm_list]

    @property
    def _menu_permissions_list(self):
        return self._make_permissions_list(self.MENU_CLASS, self.menu_perms)

    @property
    def _limit_permissions_list(self):
        return self._make_permissions_list(self.LIMIT_CLASS, self.limit_perms)

    @property
    def _ops_permissions_list(self):
        return self._make_permissions_list(self.OPS_CLASS, self.ops_perms)

    @property
    def permissions(self):
        return self._menu_permissions_list + self._limit_permissions_list + self._ops_permissions_list


eclerx_user = RolePermissions(
    menu_perms=[
        {'name': 'Dashboard'},

        {'name': 'Create Request'},

        {'name': 'Management'},
        {'name': 'Request Management'},
        {'name': 'Lead Time Upload'},
        {'name': 'Push To Staging'},
        {'name': 'Script Uploader'},
        {'name': 'Proxy Mapping'},

        {'name': 'eMatch'},
        {'name': 'Hotel Matching'},
        {'name': 'Hotel Matching Download'},
    ],
    limit_perms=[
        {'name': 'Request Limit', 'limit': 1000},
    ],
    ops_perms=[
        {'name': 'Resume'},
        {'name': 'Pause'},
        {'name': 'Stop'},
        {'name': 'Reparse'},
        {'name': 'Recrawl'},
        {'name': 'PNFRecrawl'},
    ]
)

client_user = RolePermissions(
    menu_perms=[
        {'name': 'Dashboard'},

        {'name': 'Create Request'},

        {'name': 'Management'},
        {'name': 'Request Management'},

        {'name': 'eMatch'},
        {'name': 'Hotel Matching'},
        {'name': 'Hotel Matching Download'},
    ],
    limit_perms=[
        {'name': 'Request Limit', 'limit': 1000},
    ],
    ops_perms=[
        {'name': 'Resume'},
        {'name': 'Pause'},
        {'name': 'Stop'},
        {'name': 'Reparse'},
        {'name': 'Recrawl'},
        {'name': 'PNFRecrawl'},
    ]
)

ops_admin = RolePermissions(
    menu_perms=[
        {'name': 'Dashboard'},

        {'name': 'Create Request'},

        {'name': 'Management'},
        {'name': 'Login Management'},
        {'name': 'Request Management'},
        {'name': 'Lead Time Upload'},
        {'name': 'Push To Staging'},
        {'name': 'Script Uploader'},
        {'name': 'Proxy Mapping'},

        {'name': 'eMatch'},
        {'name': 'Hotel Matching'},
        {'name': 'Hotel Matching Download'},

        {'name': 'Masters'},
        {'name': 'City Beach'},
        {'name': 'Keyword'},
        {'name': 'Group Mapping Domain'},
        {'name': 'Country'},
        {'name': 'City'},
        {'name': 'Airport'},
        {'name': 'Board Type'},
        {'name': 'POS'},
        {'name': 'Hotel Master'},
    ],
    limit_perms=[
        {'name': 'Request Limit', 'limit': 1000},
    ],
    ops_perms=[
        {'name': 'Resume'},
        {'name': 'Pause'},
        {'name': 'Stop'},
        {'name': 'Reparse'},
        {'name': 'Recrawl'},
        {'name': 'PNFRecrawl'},
    ]
)

super_admin = RolePermissions(
    menu_perms=[
        {'name': 'Dashboard'},

        {'name': 'Create Request'},

        {'name': 'Management'},
        {'name': 'Login Management'},
        {'name': 'Request Management'},
        {'name': 'Lead Time Upload'},
        {'name': 'Push To Staging'},
        {'name': 'Script Uploader'},
        {'name': 'Proxy Mapping'},

        {'name': 'eMatch'},
        {'name': 'Hotel Matching'},
        {'name': 'Hotel Matching Download'},

        {'name': 'Masters'},
        {'name': 'City Beach'},
        {'name': 'Keyword'},
        {'name': 'Group Mapping Domain'},
        {'name': 'Country'},
        {'name': 'City'},
        {'name': 'Airport'},
        {'name': 'Board Type'},
        {'name': 'POS'},
        {'name': 'Hotel Master'},
    ],
    limit_perms=[
        {'name': 'Request Limit', 'limit': 1000},
    ],
    ops_perms=[
        {'name': 'Resume'},
        {'name': 'Pause'},
        {'name': 'Stop'},
        {'name': 'Reparse'},
        {'name': 'Recrawl'},
        {'name': 'PNFRecrawl'},
    ]
)


def get_role_master(request):
    return { 
        'ROLES_DATA': json.dumps({
            "eclerx_user": {
                'verbose': 'eClerx User',
                'list': [permission.to_role(request) for permission in eclerx_user.permissions]
            },
            "client_user": {
                'verbose': 'Client User',
                'list': [permission.to_role(request) for permission in client_user.permissions]
            },
            "admin": {
                'verbose': 'Admin',
                'list': [permission.to_role(request) for permission in ops_admin.permissions]
            },
            # "super_admin": {
            #     'verbose': 'Super Admin',
            #     'list': [permission.to_role(request) for permission in super_admin.permissions]
            # },
        })
    }


def get_menu_items(request):
    return {
        'MENU_DATA': [
            MenuPermission('Dashboard', link=reverse('hotel_dashboard_index')).to_context(request),

            MenuPermission('Create Request', children=[
                MenuPermission('Hotel', link=reverse('hotel_create_request_index')),
                MenuPermission('Hotel + Flight', link=reverse('hotel_plus_flight_request')),
            ]).to_context(request),

            MenuPermission('Management', children=[
                MenuPermission('Login Management', link=reverse('hotel_user_management_index')),
                MenuPermission('Request Management', link=reverse('hotel_request_management_index')),
                MenuPermission('Lead Time Upload', link=reverse('lead_time_upload')),
                MenuPermission('Push To Staging', link=reverse('push_to_staging')),
                MenuPermission('Script Uploader', link=reverse('domain_mapping')),
                MenuPermission('Proxy Mapping', link=reverse('proxy_mapping')),
                # MenuPermission('IMS', link="https://ims.eclerx.com"),
            ]).to_context(request),

            MenuPermission('eMatch', children=[
                MenuPermission('Hotel Matching', link=reverse('match_n_unmatch')),
                MenuPermission('Hotel Matching Download', link=reverse('match_n_unmatch_download')),
            ]).to_context(request),

            MenuPermission('Masters', children=[
                MenuPermission('Keyword', link=reverse('Keyword_n_rule')),
                MenuPermission('Group Mapping Domain', link=reverse('map_group_domain')),
                MenuPermission('City Beach', link=reverse('group_creation')),
                MenuPermission('Country', link=reverse('master_country')),
                MenuPermission('City', link=reverse('master_cities')),
                MenuPermission('Airport', link=reverse('master_airport')),
                MenuPermission('Board Type', link=reverse('master_board')),
                # MenuPermission('Hotel Group', link=reverse('master_hotelgrp')),
                MenuPermission('POS', link=reverse('master_pos')),
                MenuPermission('Hotel Master', link=reverse('master_hotel')),
            ]).to_context(request),
        ],

        'LIMIT_DATA': [
            # LimitPermission('SKU Limit').to_context(request),
            LimitPermission('Request Limit').to_context(request),
            LimitPermission('Request Schedule Limit').to_context(request),
            LimitPermission('User Limit').to_context(request),
        ],

        'OPS_DATA': [
            OPSPermission('Resume').to_context(request),
            OPSPermission('Pause').to_context(request),
            OPSPermission('Stop').to_context(request),
            OPSPermission('Reparse').to_context(request),
            OPSPermission('Recrawl').to_context(request),
            OPSPermission('PNFRecrawl').to_context(request),
        ],

        'SERVICES_IP': settings.SERVICES_IP,
        'DJANGO_BASEURL': settings.DJANGO_BASEURL,
        'POST_LOGIN_URL': settings.POST_LOGIN_URL
    }