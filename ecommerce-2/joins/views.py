import uuid

from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .forms import JoinForm
from .models import Join


#Generate random reference id of 10 digit
def get_ref_id():
    ref_id = str(uuid.uuid4())[:11].replace('-', '').lower()
    try:
        # If the ref id is matched with another obj,
        # then its call the function again to genetrate unique id
        exists_id = Join.objects.get(ref_id=ref_id)
        get_ref_id()
    except:
        return ref_id

#Get user ip address
def get_ip(request):
    try:
        x_forward = request.META.get("Http_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.spilt(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""

    return ip

def join_view(request):
    # Getting the referal id if it exist in the url
    # middleware taking care of this
    try:
        # get ref obj id from request.session as itis set from the middleware
        obj_id = request.session['ref_obj_id']
        obj = Join.objects.get(id=obj_id)
    except:
        obj = None

    # Call the form obj
    form = JoinForm(request.POST or None)
    if form.is_valid():
        data = form.save(commit=False)
        #Better approach to save only one unique field value:
        email = form.cleaned_data['email']
        new_join, created = Join.objects.get_or_create(email=email)
        if created:
            new_join.ip_address = get_ip(request)
            new_join.friend = obj
            new_join.ref_id = get_ref_id()
            new_join.save()
            return HttpResponseRedirect(reverse('share', kwargs={'ref_id': new_join.ref_id}))

    context = {'form': form}
    template_name = 'joins/home.html'
    return render(request, template_name, context)


def share_view(request, ref_id):
    # In this view you will see your shareable url,
    # This page url for future visit and you number of friends
    # who joined, using your url.
    try:
        obj = Join.objects.get(ref_id=ref_id)
        friends_count = obj.referal.all().count()
    except:
        friends_count = None
    share_url = 'http://127.0.0.1:8000/?ref=%s' %(ref_id)
    page_url = 'http://127.0.0.1:8000/share/%s' % ref_id
    context = {'share_url': share_url, 'friends_count': friends_count, 'page_url': page_url}
    template_name = 'joins/share.html'
    return render(request, template_name, context)
