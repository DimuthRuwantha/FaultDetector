from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import RegisterForm, LoginForm
from .models import TrainingLog
from .models import PreFault
from channels.channel import Group
from notifications import utils
from notifications.models import Room
import json
from . import neural
from ArtificialNeuralNetwork import NeuralNets as staticnn
from ArtificialNeuralNetwork.NeuralNets import NeuralNets
from ArtificialNeuralNetwork.NeuralNetwork import NeuralNetObject
import datetime

neural_object = staticnn.css


class IndexView(View):
    template_name = 'aibased/index.html'

    def get(self, request):
        return render(request, 'aibased/index.html', context=None)

    def post(self, request):
        return render(request, 'aibased/index.html', context=None)


class Monitor(generic.ListView):
    template_name = 'aibased/monitor.html'
    user = None

    def get(self, request):
        self.user = request.user
        self.form_class = LoginForm
        if self.user.is_authenticated():
            object_list = PreFault.objects.all().order_by('-id')[:3]  # limit t8o 3
            room = Room.objects.get(title="Room1")
            return render(request, self.template_name, {'faults': object_list, 'room': room})
        else:
            return redirect('aibased:user-login')

    def get_queryset(self):
        return PreFault.objects.all()


# aibased/monitor/fault
class Fault(View):
    def get(self, request):
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

        neural_object = NeuralNets.clf

        result = neural_object.predict([lst])
        faults = NeuralNets.process_fault(result)

        time = datetime.datetime.now()
        time_str = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')

        message = "A Fault has been occurred in {0} which is identified as a {1} fault at {2}".format(location,
                                                                                                      faults[0],
                                                                                                      time_str)

        r_message = {'message': message, 'position': location, 'fault': faults[0]}
        user = request.user
        room = utils.get_room_or_error(1, user)
        room.send_message(r_message, user)

        # save data to the database
        fault = PreFault(date=time, location=location, fault=faults[0], i_a=i1, i_b=i2, i_c=i3, v_a=v1, v_b=v2, v_c=v3)
        fault.save()

        return HttpResponse("Message Received")


class NeuralNetwork(View):
    user = None
    model = TrainingLog
    template_name = 'aibased/ann.html'

    def get(self, request):
        self.user = request.user
        if self.user.is_authenticated():
            recent_log = TrainingLog.objects.order_by('-id')[0]

            return render(request, self.template_name, {'log': recent_log})
        else:
            return render(request, 'aibased/index.html', context=None)

    def post(self, request):
        user = request.user
        check_tests = False
        algorithm = request.POST.get('algorithm')
        ratio = request.POST.get('ratio')
        ratio = int(ratio)
        h_l_nodes = request.POST.get('nodes')
        h_l_nodes = int(h_l_nodes)
        test_accuracy = request.POST.get('accuracy')
        if test_accuracy == 'on':
            check_tests = True

        ann = NeuralNets(algorithm=algorithm, h_l_size=h_l_nodes, ratio=ratio / 100)

        tr, tst, pred, acc = ann.run(test_accuracy=check_tests)

        traing_log = TrainingLog(trained_by=user, time=datetime.datetime.now(), train_ratio=ratio,
                                 algorithm_name=algorithm, hidden_layer_nodes=h_l_nodes, accuracy_tested=check_tests,
                                 trained_inputs=tr, tested_inputs=tst, accuracy=acc)
        traing_log.save()

        neural_object = ann.get_ann_classifier()
        recent_log = TrainingLog.objects.order_by('-id')[0]

        context = {'log': recent_log, 'trained': tr, 'tested': tst, 'correct': pred, 'accuracy': acc}
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

            # cleaned (Normalized) data
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
