from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)


from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from groups.models import Group,GroupMember
from . import models

import json
from common.utils import *

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Group
    
    def get_context_data(self, **kwargs):
        print("===this is a Create Group ===")
        context = super().get_context_data(**kwargs)    
     
        return context

class SingleGroup(generic.DetailView):
    model = Group
    template_name = "groups/group_detail.html"   
    context_object_name = "group"
    
    def get_context_data(self, **kwargs):
        print("===this is a single Group ===")
        context = super().get_context_data(**kwargs)    
        context["group_info"] = self.show_model_fields(self.object)
        return context
    def show_model_fields(self, obj):
        field_dict = {}
        for field in obj._meta.fields:
            field_name = field.name
            field_value = getattr(obj, field_name, None)
            field_dict[field_name] = field_value
        return field_dict


class ListGroups(generic.ListView):
    template_name = "groups/group_list.html"
    model = Group

    context_object_name = "group_list"
    print("=== List of Group INFO ===")
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("=== List of Group INFO2 ===")
        array = [ ]
        for group in self.object_list:
            array.append(self.show_model_fields(group))
        context["group_array"] = array
        return context
    
    def show_model_fields(self, obj):
        field_dict = {}
        for field in obj._meta.fields:
            field_name = field.name
            field_value = getattr(obj, field_name, None)
            field_dict[field_name] = field_value
        return field_dict

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))
            messages.success(self.request,"You are now a member of the tony join the group.")

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:
            
            
            debug_info = {
              'method': request.method,
              'path': request.path,
              'GET': dict(request.GET),
               'POST': dict(request.POST),
        'user': str(request.user),
        'kwargs': kwargs
                 }
            print("=== REQUEST DEBUG INFO ===")
            print(json.dumps(debug_info, indent=2, default=str))
            print("=" * 30)

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()
            
          

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
            messages.success(self.request, self.request)
        return super().get(request, *args, **kwargs)
