# common/utils.py
from asyncio.log import logger
import json


def debug_request(request):
    """Shared function to debug request information"""
    request_dict = request_to_dict(request)
    logger.info("=== REQUEST DEBUG INFO ===")
    logger.info(json.dumps(request_dict, indent=2, default=str))
    logger.info("=" * 30)


def request_to_dict(request):
    """将Django request对象转换为可序列化的字典"""
    request_data = {
        'method': request.method,
        'path': request.path,
        'path_info': request.path_info,
        'content_type': request.content_type,
        'encoding': request.encoding,
        'GET': dict(request.GET),
        'POST': dict(request.POST),
        'COOKIES': dict(request.COOKIES),
        'user': {
            'id': request.user.id if hasattr(request.user, 'id') else None,
            'username': request.user.username if hasattr(request.user, 'username') else str(request.user),
            'is_authenticated': request.user.is_authenticated,
        },
        'session_key': request.session.session_key if hasattr(request, 'session') else None,
        'META': {
            'REMOTE_ADDR': request.META.get('REMOTE_ADDR'),
            'HTTP_USER_AGENT': request.META.get('HTTP_USER_AGENT'),
            'HTTP_REFERER': request.META.get('HTTP_REFERER'),
            'CONTENT_TYPE': request.META.get('CONTENT_TYPE'),
            'CONTENT_LENGTH': request.META.get('CONTENT_LENGTH'),
            'HTTP_HOST': request.META.get('HTTP_HOST'),
            'REQUEST_METHOD': request.META.get('REQUEST_METHOD'),
        }
    }
    return request_data

def log_request_debug(request, logger, extra_info=None):
    """记录请求调试信息的便捷函数"""
    debug_info = request_to_dict(request)
    
    if extra_info:
        debug_info.update(extra_info)
    
    logger.info("=== REQUEST DEBUG INFO ===")
    logger.info(json.dumps(debug_info, indent=2, default=str, ensure_ascii=False))
    logger.info("=" * 30)
    
    return debug_info

def get_client_ip(request):
    """获取客户端真实IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_ajax_request(request):
    """判断是否为AJAX请求"""
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'