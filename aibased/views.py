from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import RegisterForm, LoginForm
from .models import TrainingLog

from . import neural


class IndexView(generic.ListView):
    template_name = 'aibased/index.html'

    def get_queryset(self):
        return None


class Monitor(generic.ListView):
    template_name = 'aibased/monitor.html'

    def get_queryset(self):
        return None


class NeuralNetwork(View):
    model = TrainingLog
    template_name = 'aibased/ann.html'

    def get(self, request):
        # form = self.form_class(None)
        text = '5'
        return render(request, self.template_name, {'text': text})

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

        tr, tst, pred, acc = neural.run(algorithm=algorithm, h_l_size=h_l_nodes, ratio=ratio / 100,
                                        test_accuracy=check_tests)

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
