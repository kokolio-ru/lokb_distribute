from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.contrib import auth
from django.views import View
from .models import Patient, Room, Status, Position
from .form import PatientForm


class Auth(View):

    def get(self, request):
        template = loader.get_template('distr/auth.html')
        return HttpResponse(template.render({}, request))

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            template = loader.get_template('distr/auth.html')
            return HttpResponse(template.render({'error': True}, request))


class PatientView(View):

    def get(self, request, patient_id=0):

        template = loader.get_template('distr/create-patient.html')
        if patient_id > 0:
            try:
                patient = Patient.objects.get(id=patient_id)
            except ObjectDoesNotExist:
                return HttpResponseRedirect("/patient/0/")
        else:
            patient = None

        context = {
            'patient_id': patient_id,
            'statuses': Status.objects.all(),
            'patient': patient
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, patient_id=0):

        if patient_id > 0:

            patient = Patient.objects.get(id=patient_id)

            data = PatientForm(request.POST or None, instance=patient)
            if data.is_valid():
                data.save()
                return HttpResponseRedirect("/")

        else:
            data = PatientForm(request.POST or None)
            if data.is_valid():
                data.save()
                return HttpResponseRedirect("/")

        template = loader.get_template('distr/create-patient.html')
        context = {
            'patient_id': patient_id,
            'statuses': Status.objects.all()
        }
        return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


@login_required(login_url='/login/')
def index(request):

    patients = Patient.objects.filter(distributed=False).order_by('created_at').order_by('-important')
    rooms = Room.objects.all()

    template = loader.get_template('distr/index.html')
    context = {
        'patients': patients,
        'rooms': rooms
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def modal(request):

    if not ('position_id' in request.GET):
        return HttpResponse('position_id parameter is not found')

    patients = Patient.objects.filter(distributed=False).order_by('created_at').order_by('-important')
    rooms = Room.objects.all()

    position_id = request.GET['position_id']
    try:
        position = Position.objects.get(id=position_id)
    except ObjectDoesNotExist:
        return HttpResponse('position is not found')

    context = {
        'patients': patients,
        'rooms': rooms,
        'position': position
    }

    template = loader.get_template('distr/modal.html')

    return HttpResponse(template.render(context, request))


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("auth/")


@login_required(login_url='/login/')
def get_room(request, room_id):
    template = loader.get_template('distr/room.html')

    room = Room.objects.get(id=room_id)
    positions = room.position_set.all()

    context = {
        'room': room,
        'positions': positions
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def distribute_patient(request):

    patient_id = request.POST['patient_id']
    position_id = request.POST['position_id']
    patient = Patient.objects.get(id=patient_id)
    position = Position.objects.get(id=position_id)

    if not patient.distributed:
        position.patient = patient
        position.save()

        patient.distributed = True
        patient.save()

    return HttpResponseRedirect("/room/{}".format(position.room.id))


@login_required(login_url='/login/')
def save_position_comment(request, position_id):
    comment = request.POST['comment']

    position = Position.objects.get(id=position_id)
    patient = position.patient
    patient.doctor_comment = comment
    patient.save()
    return HttpResponse()


@login_required(login_url='/login/')
def delete_patient(request, position_id):

    position = Position.objects.get(id=position_id)

    if position.patient:
        position.patient.delete()

    return HttpResponseRedirect("/room/{}".format(position.room.id))


def page_not_found(request, exception):

    response = render(
        request,
        'distr/404.html'
    )

    response.status_code = 400
    return response
