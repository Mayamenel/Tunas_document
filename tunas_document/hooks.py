# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "tunas_document"
app_title = "Tunas Document"
app_publisher = "DAS"
app_description = "New Document for Tunas"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "digitalasiasolusindo@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tunas_document/css/tunas_document.css"
# app_include_js = "/assets/tunas_document/js/tunas_document.js"

# include js, css files in header of web template
# web_include_css = "/assets/tunas_document/css/tunas_document.css"
# web_include_js = "/assets/tunas_document/js/tunas_document.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "tunas_document.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "tunas_document.install.before_install"
# after_install = "tunas_document.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tunas_document.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Salary Slip": {
		"after_insert": "tunas_document.custom_salary.calculate_pph"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tunas_document.tasks.all"
# 	],
# 	"daily": [
# 		"tunas_document.tasks.daily"
# 	],
# 	"hourly": [
# 		"tunas_document.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tunas_document.tasks.weekly"
# 	]
# 	"monthly": [
# 		"tunas_document.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "tunas_document.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tunas_document.event.get_events"
# }

