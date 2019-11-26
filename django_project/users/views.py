from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, PerfilUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(request.POST.get('id_first_name', False))
        print(form)
        if form.is_valid():
            print('foi')
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            return redirect('login')
        else:
            messages.error(request, f'Algo deu ruim nessa porr')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        perfil_form = PerfilUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, f'Sua conta foi atualizado!')
            return redirect('perfil')
        else:
            messages.error(request, f'DEU RUIM')
            return redirect('perfil')
    else:
        user_form = UserUpdateForm(instance=request.user)
        perfil_form = PerfilUpdateForm(instance=request.user.perfil)

    context = {
        'user_form': user_form,
        'perfil_form': perfil_form
    }

    return render(request, 'users/profile.html', context)