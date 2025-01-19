from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _

def send_booking_confirmation_email(booking):
    """
    发送预订确认邮件给用户
    """
    subject = _('您的用车预订已确认')
    message = _('''尊敬的 %(name)s：

您的预订已确认！以下是预订详情：

预订编号：#%(booking_id)s
上车地点：%(pickup_location)s
目的地：%(destination)s
上车时间：%(pickup_time)s
车型：%(vehicle)s
司机：%(driver)s
价格：￥%(price)s

如有任何问题，请随时联系我们的客服。

祝您用车愉快！
''') % {
        'name': booking.user.get_full_name() or booking.user.username,
        'booking_id': booking.id,
        'pickup_location': booking.pickup_location,
        'destination': booking.destination,
        'pickup_time': booking.pickup_time.strftime('%Y-%m-%d %H:%M'),
        'vehicle': f'{booking.vehicle.brand} {booking.vehicle.model}',
        'driver': booking.driver.user.get_full_name(),
        'price': booking.price
    }
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.user.email]
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=True
    ) 