from viktor import ViktorController
from viktor.geometry import SquareBeam
from viktor.views import GeometryView, GeometryResult, PlotlyView, PlotlyResult
from viktor.parametrization import ViktorParametrization, NumberField

import numpy as np
import plotly.graph_objects as go

hotel_average_load = 400
hotel_profile = [1] * 7 + [1]* 3 + [1.5] * 7 + [1] * 7

residential_average_load = 230
residential_profile = [0.4] * 7 + [1]* 3 + [1.5] * 7 + [1] * 7

shop_average_load = 300
shop_profile = [0.4] * 7 + [1]* 3 + [1.5] * 7 + [0.5] * 7


class Parameterization(ViktorParametrization):
    residents = NumberField("Residents", default=10, step=1, suffix="# residents")
    shops = NumberField("Shops", default=5, step=1, suffix="# shops")
    hotels = NumberField("Hotels", default=5, step=1, suffix="# hotels")

result_profile_residential = [item * hotel_average_load * params.hotels for item in residential_profile]
result_profile_shop
result_profile_hotel

class Controller(ViktorController):
    label = "Weekly Load Profile [kW]"
    parametrization = Parameterization
    
    @PlotlyView("Total Load Profile", duration_guess=1)
    def total_plot(self, params, **kwargs):
        # Some engineering math, for a simply supported beam

        result_profile_residential = [item * residential_average_load * params.residents for item in residential_profile]
        
        # Create a plot with Plotly
        fig = go.Figure(go.Scatter(x=list(range(0,24)), y=result_profile_residential))
        fig.update_layout(xaxis_title="Hours of the Day", yaxis_title="Residential Load (W)")
        
        return PlotlyResult(fig.to_json())
    
    @PlotlyView("Standard Residential Load Profile", duration_guess=1)
    def residential_plot(self, params, **kwargs):
        # Some engineering math, for a simply supported beam
        residential_average_load = 230
        residential_profile = [0.4] * 7 + [1]* 3 + [1.5] * 7 + [1] * 7
        result_profile_residential = [item * residential_average_load for item in residential_profile]
        
        # Create a plot with Plotly
        fig = go.Figure(go.Scatter(x=list(range(0,24)), y=result_profile_residential))
        fig.update_layout(xaxis_title="Hours of the Day", yaxis_title="Residential Load (W)")
        
        return PlotlyResult(fig.to_json())
    
    @PlotlyView("Standard Shop Load Profile", duration_guess=1)
    def shop_plot(self, params, **kwargs):
        # Some engineering math, for a simply supported beam
        shop_average_load = 230
        residential_profile = [0.4] * 7 + [1]* 3 + [1.5] * 7 + [0.5] * 7
        result_profile_residential = [item * shop_average_load * params.shops for item in residential_profile]
        
        # Create a plot with Plotly
        fig = go.Figure(go.Scatter(x=list(range(0,24)), y=result_profile_residential))
        fig.update_layout(xaxis_title="Hours of the Day", yaxis_title="Shop Load (W)")
        
        return PlotlyResult(fig.to_json())

    @PlotlyView("Standard Hotel Load Profile", duration_guess=1)
    def hotel_plot(self, params, **kwargs):
        # Some engineering math, for a simply supported beam
   
        
        # Create a plot with Plotly
        fig = go.Figure(go.Scatter(x=list(range(0,24)), y=result_profile_residential))
        fig.update_layout(xaxis_title="Hours of the Day", yaxis_title="Hotel Load (W)")
        
        return PlotlyResult(fig.to_json())
    

    
