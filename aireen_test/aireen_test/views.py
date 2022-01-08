from django.views.generic import TemplateView
from django.contrib import messages
import logging


logger = logging.getLogger(__name__)


class Queues:
    def __init__(self, queues, request):
        self.queues = queues
        self.request = request

    @staticmethod
    def _logger(user, queue, message):
        logger.info(message)

    def add(self, element):
        self.queues[0].insert(0, element)
        self._logger(element, 1, f"Element {element} added to queue 1")

    def move(self, queue_index):
        name = self.queues[queue_index][-1]

        try:
            self._logger(
                name, 1, f"User {name} moved to queue {self.queues[queue_index + 1]}"
            )
            self.queues[queue_index + 1].insert(0, name)
        except IndexError:
            messages.info(self.request, f"User {name} removed from queues.")
            self._logger(name, 1, f"User {name}removed from queues.")
        finally:
            del self.queues[queue_index][-1]


class IndexView(TemplateView):
    template_name = "index.html"
    queue1 = "queue1"
    queue2 = "queue2"
    queue3 = "queue3"

    test_initial_data = {
        queue1: ["user1", "user2", "user3"],
        queue2: ["user4", "user5", "user6"],
        queue3: ["user7", "user8", "user9"],
    }

    queues = [
        queue1,
        queue2,
        queue3,
    ]

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.test_initial_data)

    def _clean_queue(self, request):
        return tuple(
            [x for x in request.POST[queue].split(" ") if x] for queue in self.queues
        )

    def get_context_data(self, queues, **kwargs):
        context = super().get_context_data(**kwargs)

        if len(self.queues) == len(queues):
            context = dict(zip(self.queues, queues))

        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        queues = Queues(self._clean_queue(request), request)

        if name and request.POST.get("add"):
            queues.add(name)
        else:
            for queue_index, _ in enumerate(self.queues):
                if request.POST.get(f"queue{queue_index+1}-remove"):
                    queues.move(queue_index)

        return self.render_to_response(self.get_context_data(list(queues.queues)))
