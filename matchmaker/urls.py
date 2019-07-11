from django.conf.urls import url

from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
	# url(r'^$', views.index_render, name="index"),
	url(r'^$', views.single_evaluate_index_render, name="index"),
	url(r'^login/$', views.login_view, name="login_view"),
	url(r'^login_error/$', views.login_view, {'login_error': True}, name="login_error_view"),
	url(r'^logout/$', views.logout_view, name="logout"),
	url(r'^vote/$', views.ajax_vote, name="ajax_vote"),
	url(r'^user/changepassword/$', views.changepassword, name="changepassword"),
	url(r'^passwordchanged/$', views.login_view, {'passwordchanged': True}, name="passwordchanged"),
	url(r'^levelchoose/$', TemplateView.as_view(template_name="levelchoose.html")),
	url(r'^addmlevel/$', views.addmlevel, name="addmlevel" ),
	url(r'^allvoted/$', TemplateView.as_view(template_name="allvoted.html"), name="thanks" ),
	url(r'^addmusician/$', views.add_musician, name="addmusician" ),
	url(r'^evaluate/$', views.solo_evaluation, name="evaluate" ),
	url(r'^firstaccess/$', views.mark_firstaccess, name="firstaccess" ),
]