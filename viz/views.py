import pandas as pd

from django.shortcuts import render

from .BGGClient import BGGClient
from .Grapher import Grapher
from .forms import BGGForm
from .models import User
from .utils import cleanup_old_charts, cleanup_old_collections

from datetime import datetime

def form(request):
    if request.method == 'POST':
        form = BGGForm(request.POST)

        if form.is_valid():
            cleanup_old_charts()
            cleanup_old_collections()

            username = form.cleaned_data['username']

            try:
                user = User.objects.get(username=username)
            except:
                user = False

            if user:
                df = pd.read_json(user.xml_data)
            else:
                try:
                    client = BGGClient(form.cleaned_data['username'])
                    df = client.yield_dataframe()
        
                    user = User()
                    user.username = client.username
                    user.creation_time = datetime.now()
                    user.xml_data = df.to_json()
                    user.save()

                except:
                    return render(request, 'viz/error.html', {'form':form})
                    
            grapher = Grapher(df)

            chart_type = form.cleaned_data['chart_type']
            x_axis = form.cleaned_data['x_axis']
            y_axis = form.cleaned_data['y_axis']
            grapher.render_input(chart_type, x_axis, y_axis)
            fp = grapher.chart_filepath.split('/', 2)[2]
            return render(request, 'viz/chart.html', {'form':form, 'chart_filepath':fp})

        else:
            form = BGGForm()

    else:
        form = BGGForm()

    return render(request, 'viz/form.html', {'form':form})

def chart(request):
    return render(request, 'viz/chart.html')
