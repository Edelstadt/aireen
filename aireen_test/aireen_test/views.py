from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
import logging


logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "index.html"
    queue1 = 'queue1'
    queue2 = 'queue2'
    queue3 = 'queue3'

    test_initial_data = {
            queue1: ['user1', 'user2', 'user3'],
            queue2: ['user4', 'user5', 'user6'],
            queue3: ['user7', 'user8', 'user9'],
        }

    queues = [
        queue1,
        queue2,
        queue3,
    ]

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.test_initial_data)

    def _clean_queue(self, request):
        return (
            [x for x in request.POST[queue].split(" ") if x]
            for queue in self.queues
        )

    @staticmethod
    def _logger(user, queue, message):
        logger.info(message)

    def get_context_data(self, queues, **kwargs):
        context = super().get_context_data(**kwargs)

        if len(self.queues) == len(queues):
            context = dict(zip(self.queues, queues))
        return context

    def post(self, request, *args, **kwargs):
        queue_1, queue_2, queue_3 = self._clean_queue(request)
        name = request.POST.get('name')

        if name and request.POST.get('add'):
            self._logger(name, 1, f"User {name} added to queue 1")
            queue_1.insert(0, name)
        
        elif request.POST.get('queue1-remove'):
            name = queue_1[-1]
            self._logger(name, 1, f"User {name} moved to queue 2")
            queue_2.insert(0, name)
            del queue_1[-1]
        
        elif request.POST.get('queue2-remove'):
            name = queue_2[-1]
            self._logger(name, 1, f"User {name} moved to queue 2")
            queue_3.insert(0, name)
            del queue_2[-1]

        elif request.POST.get('queue3-remove'):
            name = queue_3[-1]
            del queue_3[-1]
            messages.info(request, f'User {name} removed from queues.')
            self._logger(name, 1, f'User {name}removed from queues.')

        return self.render_to_response(self.get_context_data([queue_1, queue_2, queue_3]))