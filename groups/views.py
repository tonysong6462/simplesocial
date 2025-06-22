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
import pprint
from common.utils import *

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Group
    template_name = "groups/group_form.html" 
    def get_context_data(self, **kwargs):     
        context = super().get_context_data(**kwargs)       
        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import Group

class GroupUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Group
    fields = ("name", "description")
    template_name = "groups/group_form.html"

    def get_queryset(self):
        """
        Optionally restrict who can edit the group, e.g., only group creator.
        """
        return Group.objects.all()  # You can filter based on user if needed

    def get_success_url(self):
        """
        Redirect after successful update.
        """
        return reverse_lazy("groups:single", kwargs={"slug": self.object.slug})


class SingleGroup(generic.DetailView):
    model = Group
    template_name = "groups/group_detail.html"   
    context_object_name = "group"
    
    def get_context_data(self, **kwargs):
       
        context = super().get_context_data(**kwargs) 
       
        logger.info("kwargs with pprint:")
        logger.info(pprint.pformat(self.kwargs))
        # show_model_dic = debug_request(self.request)
        # show_model_dic1 = show_model_deep_fields(self.object)
        # context["group_info"] = show_model_dic
        
        # members_info = []
        # for member in self.object.members.all():
        #         members_info.append({
        #         'id': member.id,
        #         'username': member.username,
        #         'email': member.email,
        #         'full_name': f"{member.first_name} {member.last_name}".strip(),
        #     # Add any other User model fields you want to include
        #         })
        
        # # Add the members key-value pair to the dictionary
        # show_model_dic1.append({
        #     'name': 'members',
        #     'value': members_info
        # })
        # logger.info(json.dumps(show_model_dic, indent=2, default=str, ensure_ascii=False))
        # logger.info(json.dumps(show_model_dic1, indent=2, default=str, ensure_ascii=False))
        # logger.info("=== 记录请求 SingleGroup ===")
        # logger.info(json.dumps(show_model_dic, indent=2, default=str, ensure_ascii=False))
        # logger.info("=== 记录 请求 SingleGroup  完毕 ===")
        return context
    


class ListGroups(generic.ListView):
    template_name = "groups/group_list.html"
    model = Group

    context_object_name = "group_list"
    
    def get_context_data(self, **kwargs):
      
        context = super().get_context_data(**kwargs)
     
        array = [ ]
        for group in self.object_list:
            group: Group = group          
            array.append(show_model_dic_fields(group))
                
        context["group_array"] = array
        
       
        return context
    
  

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
         
        return super().get(request, *args, **kwargs)
