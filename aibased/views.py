from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import RegisterForm, LoginForm
from .models import TrainingLog
from .models import PreFaults
from channels.channel import Group
from notifications import utils
from notifications.models import Room
import json
from . import neural
from ArtificialNeuralNetwork.NeuralNets import NeuralNets

neural_object = None

class IndexView(View):
    template_name = 'aibased/index.html'

    def get(self, request):
        return render(request, 'aibased/index.html', context=None)

    def post(self, request):
        return render(request, 'aibased/index.html', context=None)


class Monitor(generic.ListView):
    template_name = 'aibased/monitor.html'

    def get(self, request):
        # pre_faults = PreFaults.objects.all().order_by('-id')[:3]  # limit to 3
        object_list = PreFaults.objects.all().order_by('-id')[:3]  # limit to 3
        # faults = reversed(pre_faults)
        rooms = Room.objects.order_by("title")

        return render(request, self.template_name, {'faults': object_list, 'rooms': rooms})

    def get_queryset(self):
        return PreFaults.objects.all()


# aibased/monitor/fault
class Fault(View):
    # template_name = 'aibased/monitor.html'

    def get(self):
        return HttpResponse("OK")

    def post(self, request):

        received_json_data = json.loads(request.body.decode('utf-8'))

        location = received_json_data.get('location')
        v1 = received_json_data.get('v1')
        v2 = received_json_data.get('v2')
        v3 = received_json_data.get('v3')
        i1 = received_json_data.get('i1')
        i2 = received_json_data.get('i2')
        i3 = received_json_data.get('i3')
        lst = [v1, v2, v3, i1, i2, i3]

        result = neural_object.predict(lst)



        user = request.user
        room = utils.get_room_or_error(1, user)
        room.send_message("message", user)


        return HttpResponse("Message Received")


class NeuralNetwork(View):
    model = TrainingLog
    template_name = 'aibased/ann.html'

    def get(self, request):
        # form = self.form_class(None)
        # text = '5'
        # return render(request, self.template_name, {'text': text})
        return render(request, self.template_name, {})

    def post(self, request):
        check_tests = False

        algorithm = request.POST.get('algorithm')
        ratio = request.POST.get('ratio')
        ratio = int(ratio)
        h_l_nodes = request.POST.get('nodes')
        h_l_nodes = int(h_l_nodes)
        test_accuracy = request.POST.get('accuracy')
        if test_accuracy == 'on':
            check_tests = True

        ann = NeuralNets()

        tr, tst, pred, acc = ann.run(algorithm=algorithm, h_l_size=h_l_nodes, ratio=ratio / 100,
                                        test_accuracy=check_tests)

        neural_object = ann.get_ann_classifier()
        # neural_object = NeuralNets.get_ann_classifier()

        context = {'trained': tr, 'tested': tst, 'correct': pred, 'accuracy': acc}
        return render(request, self.template_name, context)


class UserRegistrationView(View):
    form_class = RegisterForm
    template_name = 'aibased/user_form.html'

    # Display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            #
            # # cleaned (Normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns user object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('aibased:index')

        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'aibased/user_form.html'

    # Display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        username = form.data.get('username')
        password = form.data.get('password')

        # returns user object if credentials are correct
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('aibased:index')

        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
    form_class = RegisterForm

    def get(self, request):
        logout(request)
        return redirect('aibased:index')
