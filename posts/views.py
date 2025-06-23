import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from common.utils import *

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()

import logging
logger = logging.getLogger(__name__)


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")
    context_object_name = "List_posts"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # return  User.objects.prefetch_related("posts").get(
        #         username__iexact=self.request.user.username
        #     ).posts.all()
        # return queryset.filter(user__username__iexact=self.request.user.username)
        return queryset.filter()





class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group')
    model = models.Post
    
          
    def get(self, request, *args, **kwargs):
        self.object = None
        debug_request(self.request)
        return super().get(request, *args, **kwargs)

   

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        debug_request(self.request)
        messages.success(self.request, "Post Created Successfully")
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
      model = models.Post
      template_name = "posts/post_confirm_delete.html"
      context_object_name = "post"
      select_related = ("user", "group")
      success_url = reverse_lazy("posts:all")
      
    
      
      
      def get_context_data(self, **kwargs):
            logger.info("=== add dev branch ===")       
            logger.info("=== 记录请求调试信息的便捷函数 ===")
            debug_info = request_to_dict(self.request)
            logger.info(json.dumps(debug_info, indent=2, default=str, ensure_ascii=False))
            logger.info("=== 记录请求调试信息的便捷函数  完毕 ===")            
            context = super().get_context_data(**kwargs)            
            context["post_user"] = show_model_deep_fields(self.object,0,2,None)    
            return context
     
      def get_queryset(self): 
       
          queryset = super().get_queryset()
          return queryset.filter(user_id=self.request.user.id)
      
      def form_valid(self, form):
            logger.info("=== 记录请求删除 ===")
            debug_info = request_to_dict(self.request)
            logger.info(json.dumps(debug_info, indent=2, default=str, ensure_ascii=False))
            logger.info("=== 记录请求删除   完毕 ===")
            messages.success(self.request, "Post Deleted")         
            return super().form_valid(form)
    
     
    

    #   def delete(self, *args, **kwargs):
    #         logger.info("=== 删除帖子视图.删除() 开始 ===")
    #         messages.success(self.request, "Post Deleted") 
    #         # return super().delete(*args, **kwargs)
    #         response = super().delete(self.request, *args, **kwargs)
    #         logger.info("=== 删除帖子视图.删除() 完成 ===")
    #         return response
      
