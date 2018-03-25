from bokeh.plotting import figure, curdoc
from bokeh.layouts import *
from bokeh.models import *
from bokeh.models.widgets import *
from bokeh.core.json_encoder import serialize_json

import geopandas as gpd
import tweepy
from os.path import dirname, join
time_intervals = ["8-10AM", "10-12PM", "12-3PM", "3-6PM", "6-10PM", "10-12AM"]

gmap_key = 'AIzaSyCMPGzkf5CjZ3Ro7p1C9k9ePh7S_rjXxJk'

map_style = [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#444444"}]},
            {"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},
            {"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},
            {"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},
            {"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},
            {"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},
            {"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},
            {"featureType":"transit.station","elementType":"all","stylers":[{"visibility":"on"}]},
            {"featureType":"water","elementType":"all","stylers":[{"color":"#a1c6d7"},{"visibility":"on"}]}]

# Default location on gmap
syd_lat = -33.8688
syd_lon = 151.2093

# Factors
# suburbs = ["Sydney", "Bankstown", "Paramatta", "Mosman"]
events = ["Vivid", "Glebe Markets", "NRL"]
events_coord = [(syd_lat,syd_lon), (-33.8833071,151.1889673), (-33.898311, 151.233274)]
weathers = ["Sunny", "Rainy"]
consumer_key = 'ZMZMXG9rKVAvHRH4S8xNWX64m'
consumer_secret = '3DalURFRaIcNWhrjz9CYzkIOOETSGkI0QXqUW09fSU3f4j3Dzt'
access_token = '977379028045774848-lBEfQ48W6WbPJNm0jwt9nc7QsmJU5Y3'
access_secret = 'YaCDJstV4GtuQ2lFEbX4IbXRwldYagzVmkAv5Q3HEWs2m'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)



# Sample points for our demo
picked_lat = [-33.802760, -33.879839, -33.882803, -33.887729, -33.889036]
picked_lon = [151.246176 ,151.187066, 151.204140, 151.193322 ,151.201495]
picked_ints = ['10' for i in range(0,5)]

# Sample 2
sample2_lat = [-33.890224,-33.908710, -33.883431, -33.882650, -33.891092, -33.891092, -33.895748, -33.894525,
                -33.884825, -33.882226, -33.908213, -33.878588, -33.902721]

sample2_lon = [151.246964, 151.223275, 151.221419, 151.231823, 151.210923, 151.210923, 151.215982, 151.240749,
                151.238965, 151.228214, 151.234141, 151.237397,151.207410]


def plot_gmap():
    """Return a google maps plot centered at sydney cbd"""
    map_options = GMapOptions(lat=syd_lat, lng=syd_lon, zoom=14, map_type="roadmap", styles=serialize_json(map_style))
    plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), api_key=gmap_key, map_options=map_options,
                    plot_height=1000, plot_width=1300, toolbar_location="left")
    plot.add_tools(PanTool(), ZoomInTool(), ZoomOutTool())

    return plot


####################
## START PlOTTING ##
####################

days_options = RadioButtonGroup(name="Day", labels=["Weekdays", "Weekend"], active=0)
event_options = RadioButtonGroup(name="Events", labels=events)
weather_options = RadioButtonGroup(name="Weather", labels=weathers, active=0)
# suburb_options = RadioButtonGroup(name="Suburb", labels=suburbs)
time_options = RadioButtonGroup(name="Time", labels=time_intervals, active=0)

# Alert button
alert = Button(label="ALERT", button_type="danger", width=500)

gplot = plot_gmap()

# Add sample points 1
source = ColumnDataSource(data=dict(lat=picked_lat,lon=picked_lon, label=picked_ints, level=[10 for i in range(0,5)]))
sample_points = Circle(x="lon", y="lat", radius=50, fill_color="green", fill_alpha=0.5, line_color=None)
gplot.add_glyph(source, sample_points)
hover = HoverTool(tooltips=[("Intensity Level %: ","@level")], toggleable=False)
gplot.add_tools(hover)

# Add sample points 2
source2 = ColumnDataSource(data=dict(lat=sample2_lat,lon=sample2_lon, level=[5 for i in range(0,13)]))
sample2_points = Circle(x="lon", y="lat", radius=50, fill_color="green", fill_alpha=0.5, line_color=None)
gplot.add_glyph(source2, sample2_points)
# hover = HoverTool(tooltips=[("Intensity Level %: ","@level")], toggleable=False)
# gplot.add_tools(hover)



dashboard = layout([[gplot, column(days_options, event_options, weather_options, time_options, alert)]])


event_renderers = [0,0,0]

def event_callback(active):

    current_plot = dashboard.children[0].children[0]

    if active == 0:
        if event_renderers[1] != 0 and event_renderers[1].visible is True:
            event_renderers[1].visible = False

            sp_data = current_plot.renderers[0].data_source.data
            sp_data['level'] = [l-70 for l in sp_data['level']]
            # current_plot.renderers[0].data_source

            for i, level in enumerate(sp_data['level']):
                if level <= 50:
                    current_plot.renderers[0].glyph.fill_color="green"

                if level <= 80:
                    current_plot.renderers[0].glyph.fill_color="yellow"

        if event_renderers[2] != 0 and event_renderers[2].visible is True:
            event_renderers[2].visible = False

        source = ColumnDataSource(data=dict(lat=[events_coord[0][0]], lon=[events_coord[0][1]], label=["100%"], level=[100]))
        circle = Circle(x="lon", y="lat", radius=3000, fill_color="red", fill_alpha=0.3, line_color=None)

        # current_plot = dashboard.children[0].children[0]
        event_renderers[0] = current_plot.add_glyph(source, circle)
        hover = HoverTool(tooltips=[("Intensity Level %","@level")], toggleable=False)
        current_plot.add_tools(hover)



    elif active == 1:

        if event_renderers[0] != 0 and event_renderers[0].visible is True:
            event_renderers[0].visible = False

        if event_renderers[2] != 0 and event_renderers[2].visible is True:
            event_renderers[2].visible = False
            # sp_data = current_plot.renderers[0].data_source.data
            # sp_data['level'] = [l-70 for l in sp_data['level']]
            # # current_plot.renderers[0].data_source

            # for i, level in enumerate(sp_data['level']):

            #     if level <= 80:
            #         current_plot.renderers[0].glyph.fill_color="yellow"

            #     if level <= 50:
            #         current_plot.renderers[0].glyph.fill_color="green"



        source = ColumnDataSource(data=dict(lat=[events_coord[1][0]], lon=[events_coord[1][1]], label=["100%"], level=[100]))
        circle = Circle(x="lon", y="lat", radius=1800, fill_color="red", fill_alpha=0.3, line_color=None)

        # current_plot = dashboard.children[0].children[0]
        event_renderers[1] = current_plot.add_glyph(source, circle)
        hover = HoverTool(tooltips=[("Intensity Level %","@level")], toggleable=False)
        current_plot.add_tools(hover)

        sp_data = current_plot.renderers[0].data_source.data
        sp_data['level'] = [l+70 for l in sp_data['level']]
        # current_plot.renderers[0].data_source

        for i, level in enumerate(sp_data['level']):
            if level > 50:
                current_plot.renderers[0].glyph.fill_color="yellow"

            if level > 80:
                current_plot.renderers[0].glyph.fill_color="red"

    else:
        if event_renderers[0] != 0 and event_renderers[0].visible == True:
            event_renderers[0].visible = False

        if event_renderers[1] != 0 and event_renderers[1].visible == True:
            event_renderers[1].visible = False

            sp_data = current_plot.renderers[0].data_source.data
            sp_data['level'] = [l-70 for l in sp_data['level']]
            # current_plot.renderers[0].data_source

            for i, level in enumerate(sp_data['level']):

                if level <= 80:
                    current_plot.renderers[0].glyph.fill_color="yellow"

                if level <= 50:
                    current_plot.renderers[0].glyph.fill_color="green"



        source = ColumnDataSource(data=dict(lat=[events_coord[2][0]], lon=[events_coord[2][1]], label=["100%"], level=[100]))
        circle = Circle(x="lon", y="lat", radius=1800, fill_color="red", fill_alpha=0.3, line_color=None)

        # current_plot = dashboard.children[0].children[0]
        event_renderers[2] = current_plot.add_glyph(source, circle)
        hover = HoverTool(tooltips=[("Intensity Level %","@level")], toggleable=False)
        current_plot.add_tools(hover)





def time_callback(active):

    if active in [0, 2, 3]:
        current_plot = dashboard.children[0].children[0]
        sp_data = current_plot.renderers[0].data_source.data
        sp_data['level'] = [l+5 for l in sp_data['level']]
        # current_plot.renderers[0].data_source

        for i, level in enumerate(sp_data['level']):
            if level > 50:
                current_plot.renderers[0].glyph.fill_color="yellow"
            if level > 80:
                current_plot.renderers[0].glyph.fill_color="red"

    else:
        current_plot = dashboard.children[0].children[0]
        sp_data = current_plot.renderers[0].data_source.data
        sp_data['level'] = [l-5 for l in sp_data['level']]
        # current_plot.renderers[0].data_source

        for i, level in enumerate(sp_data['level']):
            if level <= 80:
                current_plot.renderers[0].glyph.fill_color="yellow"
            if level <= 50:
                current_plot.renderers[0].glyph.fill_color="green"


def weather_callback(active):
    # Rainy
    if active == 1:
        current_plot = dashboard.children[0].children[0]
        sp_data = current_plot.renderers[0].data_source.data
        sp_data['level'] = [l+10 for l in sp_data['level']]

        for i, level in enumerate(sp_data['level']):
            if level > 50:
                current_plot.renderers[0].glyph.fill_color="yellow"
            if level > 80:
                current_plot.renderers[0].glyph.fill_color="red"

    else:
        current_plot = dashboard.children[0].children[0]
        sp_data = current_plot.renderers[0].data_source.data
        sp_data['level'] = [l-10 for l in sp_data['level']]

        for i, level in enumerate(sp_data['level']):
            if level <= 80:
                current_plot.renderers[0].glyph.fill_color="yellow"
            if level <= 50:
                current_plot.renderers[0].glyph.fill_color="green"

# Call back to put tweet bot
############################
#### TWEET TWEET TWEET #####
############################
def alert_callback():
    api.update_status("GLEBE: 1 lane closed at Glebe Point Road due to a 2 car crash. Exercise caution")



# Listening
event_options.on_click(event_callback)
time_options.on_click(time_callback)
weather_options.on_click(weather_callback)
alert.on_click(alert_callback)

curdoc().add_root(dashboard)
