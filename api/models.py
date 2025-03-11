# -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import format_html

from bridge.models import Minera, BridgeResponse


GRAPH_TYPE = (
    ("LineChart", "LineChart"),
    ("BarChart", "BarChart"),
    ("PieChart", "PieChart"),
    ("Table", "Table"),
    ("CustomJson", "CustomJson"),
    ("MineData", "MineData"),
)

ENDPOINT_ICONS = (
    ("generic", "generic"),
    ("overview", "overview"),
    ("clock", "clock"),
    ("stats", "stats"),
    ("truck", "truck"),
    ("pin", "pin"),
    ("building", "building"),
    ("logout", "logout"),
)


class DynamicGraph(models.Model):
    ''' Define what to show and how in a graph.

    graph supported:
    LineChart: required two fields x and y.
    BarChart: required two fields x and y.
    Table: required two fields x and y.
    '''
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150, blank=True, default='')
    order = models.SmallIntegerField(blank=True, null=True, default=0)
    type = models.CharField('Graphic type', max_length=50, choices=GRAPH_TYPE, blank=True,)
    data = models.ForeignKey(BridgeResponse, on_delete=models.SET_NULL, blank=True, null=True)
    decimals = models.SmallIntegerField('Numero de decimales', blank=True, null=True, default=2)
    min_x = models.SmallIntegerField(blank=True, null=True, default=0)
    max_x = models.SmallIntegerField(blank=True, null=True, default=0)
    min_y = models.SmallIntegerField(blank=True, null=True, default=0)
    max_y = models.SmallIntegerField(blank=True, null=True, default=0)
    extra = models.TextField(blank=True, null=True,
                             default="""
                                        {
                                            "zoom": "14",
                                            "series": {"y":"", "y2": ""}
                                        }
                                        """,
                             help_text="""<strong>Format:</strong> JSON</br>
                                          <strong>Options:</strong> series, table_headers, shovels, label_x, zoom</br>
                                          </br>
                                          ie:<br>{<br>&nbsp;&nbsp;&nbsp;&nbsp;\"label_x\": \"hours\",
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;\"table_headers\": {
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\"header1\": [\"Movimientos (kt)\", \"Real (kt)\"]
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;},
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;\"shovels\": {
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\"S01\": {\"lat\": -22.124124, \"lon\": -69.01120}
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;},
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;\"series\": {
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\"y\": \"Movimiento Mina\",
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\"y2\": \"Extraccion Mina\"
                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;}</br>}
                                          </br></br><strong>Important:</strong> Properties must to be enclosed in double quotes.
                                          """)

    def __str__(self):
        return u'{}{}-{}'.format(u'{}-'.format(self.description) if self.description else '', self.title, self.type)

    def __unicode__(self):
        return u'{}{}-{}'.format(u'{}-'.format(self.description) if self.description else '', self.title, self.type)


class DynamicEndpoint(models.Model):
    ''' DynamicEndpoint will create one new endpoint for the app.

        and here is where we can define dynamically what data to show, how to display it, and to whom.
    '''
    id = models.AutoField(primary_key=True, editable=False)
    slug = models.SlugField(max_length=150, help_text="Esta será la url")
    bridge = models.ForeignKey(Minera, blank=True, null=True, on_delete=models.SET_NULL)
    graphs = models.ManyToManyField(DynamicGraph, verbose_name="list of graphs")
    title = models.CharField(max_length=150, default="", help_text="Texto que aparece en el menu de la aplicación")
    icon = models.CharField('Icon', max_length=30, choices=ENDPOINT_ICONS, blank=True)

    @property
    def url(self):
        return '/api/v1/data/{}/'.format(self.slug)

    def endpoint_url(self):
        return format_html(
            '<a href="{}?bridge={}">{}</a>',
            self.url,
            self.bridge.id if self.bridge else 0,
            self.slug,
        )
