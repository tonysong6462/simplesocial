from asyncio.log import logger
import json
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from common.utils import request_to_dict

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        
        # logger.info("=== 主页请求 ===")
        # debug_info = request_to_dict(self.request)
        # logger.info(json.dumps(debug_info, indent=2, default=str, ensure_ascii=False))
        # logger.info("=== 主页请求  完毕 ===")
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("test"))
        return super().get(request, *args, **kwargs)
