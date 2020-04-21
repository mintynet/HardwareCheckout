from .models import DeviceQueue, DeviceType
from .webutil import Blueprint, noself, UserBaseHandler

main = Blueprint()


@main.route('/', name="main")
class MainHandler(UserBaseHandler):
    def get(self):
        """
        Home path for the site

        :return:
        """
        with self.make_session() as session:
            if self.current_user and self.current_user.has_roles('Admin'):
                terminals = DeviceQueue.get_all_web_urls(session)
                show_streams = False
            else:
                terminals = DeviceQueue.get_all_ro_urls(session)
                show_streams = True
            if self.current_user:
                devices = self.current_user.get_owned_devices(session)
            else:
                devices = []
            queues = [{'id': id, 'name': name, 'size': count} for id, name, count in DeviceType.get_queues(session)]
        self.render('index.html', **noself(locals()))
