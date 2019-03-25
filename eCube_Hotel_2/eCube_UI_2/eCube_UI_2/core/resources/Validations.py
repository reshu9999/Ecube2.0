from eCube_UI_2.core.resources.models import MasterViews
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


class CountryValidations(MasterViews):

    REQUIRED = ['name', 'timezone']

    def __init__(self, model, ops_urls):
        super().__init__(model, ops_urls)

    @csrf_exempt
    def add(self, request):
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().add(request)

    @csrf_exempt
    def update(self, request,obj_id):
        print ('update Entered-----',obj_id)
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().update(request,obj_id)

class CityValidations(MasterViews):

    REQUIRED = ['name', 'country']

    def __init__(self, model, ops_urls):
        super().__init__(model, ops_urls)

    @csrf_exempt
    def add(self, request):
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().add(request)

    @csrf_exempt
    def update(self, request,obj_id):
        print ('update Entered-----',obj_id)
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().update(request,obj_id)

class AirportCodeValidations(MasterViews):

    REQUIRED = ['name', 'country','city']

    def __init__(self, model, ops_urls):
        super().__init__(model, ops_urls)

    @csrf_exempt
    def add(self, request):
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().add(request)

    

    @csrf_exempt
    def update(self, request,obj_id):
        print ('update Entered-----',obj_id)
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().update(request,obj_id)

class BoardTypeValidations(MasterViews):

    REQUIRED = ['code', 'description']

    def __init__(self, model, ops_urls):
        super().__init__(model, ops_urls)

    @csrf_exempt
    def add(self, request):
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().add(request)

    @csrf_exempt
    def update(self, request,obj_id):
        print ('update Entered-----',obj_id)
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().update(request,obj_id)

class HotelGroupValidations(MasterViews):

    REQUIRED = ['code', 'description']

    def __init__(self, model, ops_urls):
        super().__init__(model, ops_urls)

    @csrf_exempt
    def add(self, request):
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().add(request)

    @csrf_exempt
    def update(self, request,obj_id):
        print ('update Entered-----',obj_id)
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().update(request,obj_id)

class PointOfSaleValidations(MasterViews):

    REQUIRED = ['pointofsale']

    def __init__(self, model, ops_urls):
        super().__init__(model, ops_urls)

    @csrf_exempt
    def add(self, request):
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().add(request)

    @csrf_exempt
    def update(self, request,obj_id):
        print ('update Entered-----',obj_id)
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().update(request,obj_id)


class HotelValidations(MasterViews):

    REQUIRED = ['WebsiteHotelId', 'Address1','Name','City','StarRating']

    def __init__(self, model, ops_urls):
        super().__init__(model, ops_urls)

    @csrf_exempt
    def add(self, request):
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().add(request)

    @csrf_exempt
    def update(self, request,obj_id):
        print ('update Entered-----',obj_id)
        errors = list()
        post_data = {k: v for k, v in request.POST.items()}
        for key, value in post_data.items():
            if key in self.REQUIRED and value == "":
                errors.append({'name': key, 'html': key + ' is Required'})
        if errors:
            return JsonResponse({
                'errors': errors
            })
        else:
            return super().update(request,obj_id)
