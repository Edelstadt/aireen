from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = {
            'queue1': ['user1', 'user2', 'user3'],
            'queue2': ['user4', 'user5', 'user6'],
            'queue3': ['user7', 'user8', 'user9'],
        }

        return self.render_to_response(context)

    @staticmethod
    def _process_queue(queue):
        return [x for x in queue.split(" ") if x]

    @staticmethod
    def logger(user, queue, message):
        pass

    def post(self, request, *args, **kwargs):
        queue_1 = self._process_queue(request.POST['queue1'])
        queue_2 = self._process_queue(request.POST['queue2'])
        queue_3 = self._process_queue(request.POST['queue3'])
        name = request.POST.get('name')

        if name and request.POST.get('add'):
            self.logger(name, 1, f"User {name} added to queue 1")
            queue_1.insert(0, name)

            context = {
                'queue1': queue_1,
                'queue2': queue_2,
                'queue3': queue_3,
            }
        
        elif request.POST.get('queue1-remove'):
            name = queue_1[-1]
            self.logger(name, 1, f"User {name} moved to queue 2")
            queue_2.insert(0, name)

            context = {
                'queue1': queue_1[:-1],
                'queue2': queue_2,
                'queue3': queue_3,
            }
        
        elif request.POST.get('queue2-remove'):
            name = queue_2[-1]
            self.logger(name, 1, f"User {name} moved to queue 2")
            queue_3.insert(0, name)

            context = {
                'queue1': queue_1,
                'queue2': queue_2[:-1],
                'queue3': queue_3,
            }

        elif request.POST.get('queue3-remove'):
            messages.info(request, 'User removed from queues.')
            context = {
                'queue1': queue_1,
                'queue2': queue_2,
                'queue3': queue_3[:-1],
            }

        return self.render_to_response(context)