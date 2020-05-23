from releasedatehub import create_app
app = create_app()
app.app_context().push()

from releasedatehub.users.utils import send_notification_email

send_notification_email()







