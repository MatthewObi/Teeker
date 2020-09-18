# Manage the URL paths

from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("homefeed", views.index_posts, name="index_posts"),
	path("trending", views.trending, name="trending"),
	path("world", views.world, name="world"),
	path("worldfeed", views.world_posts, name="world_posts"),
	path("upload", views.upload, name="upload"),
	path("upload=<slug:content_type>", views.upload, name="upload"),
	path("inbox", views.inbox_page, name="inbox_page"),
	path("recommend_sys", views.recommend_system, name="recommend_system"),
	path("view=<slug:content_id>", views.view_page, name="view_page"),
	path("comment", views.comment_posts, name="comment_posts"),
	path("votesystem", views.vote_system, name="vote_system"),
	path("account", views.account_page, name="account_page"),
	path("editcontent", views.editcontent, name="editcontent"),
	path("TK/view=<slug:user_id>", views.view_teeker_page, name="view_teeker_page"),
	path("TK/viewposts", views.view_teeker_page_posts, name="view_teeker_page_posts"),
	path("login", views.login_page, name="login_page"),
	path("logout", views.logout_page, name="logout_page"),
	path("register", views.register, name="register"),
	path("forgot_pwd/<slug:option>", views.forgot_pwd, name="forgot_pwd"),
	path("emailcode", views.emailcode, name="emailcode"),
	path("support", views.support_page, name="support_page"),
	path("settings", views.settings_page, name="settings_page"),
	path("settings=<slug:option>", views.settings_page, name="settings_page"),
	path("termsandconditions", views.termsandconditions, name="termsandconditions"),
	path("level0/users", views.level0_users, name="level0_users"),
	path("level0/users/viewuser", views.level0_users_view, name="level0_users_view"),
	path("level0/users/viewuser=<slug:option>", views.level0_users_view, name="level0_users_view"),
	path("level0/content", views.level0_users_content, name="level0_users_content")
]
