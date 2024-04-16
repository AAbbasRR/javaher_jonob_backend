import calendar
import random


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


def generate_random_number():
    length = random.randint(4, 10)  # Generate a random length between 4 and 10
    random_number = "".join(
        [str(random.randint(0, 9)) for _ in range(length)]
    )  # Generate a random number of that length
    return random_number
