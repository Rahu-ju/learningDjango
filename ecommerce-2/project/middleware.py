from joins.models import Join


def refer_middleware(get_response):
    # One-time configuration and initialization.
    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            # get thr ref value from the browser url
            # and check the ref id exist or not
            ref_id = request.GET.get('ref', '')
            obj = Join.objects.get(ref_id=ref_id)
        except:
            obj = None

        if obj:
            # Add the ref obj id to the request.session dict
            # to get it from view.
            request.session['ref_obj_id'] = obj.id
            print('i am from middleware ', obj.id)

        response = get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        # remove the ref id from the request.session dict
        request.session['ref_obj_id'] = None

        return response

    return middleware
