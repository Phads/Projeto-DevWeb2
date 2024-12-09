from .models import Tarefa
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

class TarefasListView(ListView) :
    model = Tarefa

class TarefaCreateView(CreateView) :
    model = Tarefa
    fields = ["titulo", "data_entrega"]
    success_url = reverse_lazy("tarefa_lista")

class TarefaUpdateView(UpdateView):
    model = Tarefa
    fields = ["titulo", "data_entrega"]
    success_url = reverse_lazy("tarefa_lista")

class TarefaDeleteView(DeleteView):
    model = Tarefa
    success_url = reverse_lazy("tarefa_lista")