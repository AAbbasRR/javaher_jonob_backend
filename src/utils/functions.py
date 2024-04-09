import calendar


def get_client_ip(request):
    # Attempt to get the real client IP address, considering proxies and load balancers
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_days_in_month(year, month):
    _, days_in_month = calendar.monthrange(year, month)
    return days_in_month
