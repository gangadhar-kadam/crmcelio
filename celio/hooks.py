app_name = "celio"
app_title = "Celio"
app_publisher = "indictrans"
app_description = "celio CRM"
app_icon = "icon-star-empty"
app_color = "#CC99FF"
app_email = "priya.s@indictranstech.com"
app_url = "www.indictranstech.com"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/celio/css/celio.css"
# app_include_js = "/assets/celio/js/celio.js"

# include js, css files in header of web template
# web_include_css = "/assets/celio/css/celio.css"
# web_include_js = "/assets/celio/js/celio.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "celio.install.before_install"
# after_install = "celio.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "celio.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.core.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.core.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"celio.celio.page.support_dashboard.support_dashboard.get_escalation_for_supportticket"
	]
	# "daily": [
	# 	"celio.tasks.daily"
	# ],
	# "hourly": [
	# 	"celio.page.support_dashboard.support_dashboard.get_escalation_for_supportticket"
	# ],
	# "weekly": [
	# 	"celio.tasks.weekly"
	# ]
	# "monthly": [
	# 	"celio.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "celio.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.core.doctype.event.event.get_events": "celio.event.get_events"
# }

