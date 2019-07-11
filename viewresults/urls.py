from django.conf.urls import url

from django.views.generic.base import TemplateView

from . import views


urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name="result_index.html"), name="resultindex"),
	url(r'^bymusicians/$', views.by_musicians, name="bymusicians"),
	url(r'^bymusicians/(\d*)/$', views.show_musician_contests, name="showmusiciancontests"),
	url(r'^bymusicianlevel/$', views.by_musicians_level, name="bymusicianslevel"),
	url(r'^bysolouse/$', views.by_solo_use, name="bysolouse"),
	url(r'^playcontest/(\d*)/$', views.get_playcontest, name="playcontest"),
	url(r'^playrandsolo/(\d*)/$', views.get_randsolo, name="playrandsolo"),
	url(r'^playallrulesolo/(\d*)/$', views.get_allrulesolo, name="playallrulesolo"),
	url(r'^musiciansevaluations/$', views.show_musicians_evaluations, name="allusersevaluations"),
	url(r'^musiciansevaluations/(\d*)/$', views.show_single_musician_evaluations, name="singlemusicianevaluations"),
	url(r'^begevals/$', views.show_begevals, name="begevals"),
	url(r'^interevals/$', views.show_interevals, name="interevals"),
	url(r'^profevals/$', views.show_profevals, name="profevals"),
	url(r'^statistics/$', views.show_statistics, name="showstatistics"),
	url(r'^solouse/$', views.show_solouse_general, name="showsolouse"),
	url(r'^solouse/beginner/$', views.show_solouse_beginner, name="showsolousebeginner"),
	url(r'^solouse/intermed/$', views.show_solouse_intermed, name="showsolouseintermed"),
	url(r'^solouse/prof/$', views.show_solouse_prof, name="showsolouseprof"),
	url(r'^solosdetails/$', views.show_solosdetails, name="showsolosdetails"),
	url(r'^generaluse/$', views.show_general_use, name="showgeneraluse"),
]