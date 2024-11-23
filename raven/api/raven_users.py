import json

import frappe
from frappe import _
from frappe.utils.caching import redis_cache


@frappe.whitelist(methods=["GET"])
def get_current_raven_user():
	"""
	Fetches the current user's Raven User profile
	"""

	# Check if the user is a Raven User and has he "Raven User" role
	# If not, then throw an error
	if not frappe.has_permission("Raven User"):
		frappe.throw(
			_(
				"You do not have a <b>Raven User</b> role. Please contact your administrator to add your user profile as a <b>Raven User</b>."
			),
			title=_("Insufficient permissions. Please contact your administrator."),
		)

	return frappe.get_cached_doc("Raven User", {"user": frappe.session.user})


@frappe.whitelist()
@frappe.read_only()
def get_list():
	"""
	Fetches list of all users who have the role: Raven User
	"""

	# Check if the user is a Raven User and has he "Raven User" role
	# If not, then throw an error
	if not frappe.has_permission("Raven User"):
		frappe.throw(
			_(
				"You do not have a <b>Raven User</b> role. Please contact your administrator to add your user profile as a <b>Raven User</b>."
			),
			title=_("Insufficient permissions. Please contact your administrator."),
		)

	# Get users is cached since this won't change frequently
	return get_users()


@redis_cache()
def get_users():
	users = frappe.db.get_all(
		"Raven User",
		fields=[
			"full_name",
			"user_image",
			"name",
			"first_name",
			"enabled",
			"type",
			"availability_status",
			"custom_status",
		],
		order_by="full_name",
	)
	return users


@frappe.whitelist()
def is_user_on_leave(user: str):
	"""
	If the user is on leave, return True
	"""
	# Check if FrappeHR is installed
	if not "hrms" in frappe.get_installed_apps():
		return False

	employee = frappe.db.exists("Employee", {"user_id": user})

	if employee:
		# Check if attendance today is marked as "On Leave"
		attendance = frappe.db.exists(
			"Attendance",
			{
				"employee": employee,
				"status": "On Leave",
				"attendance_date": frappe.utils.today(),
				"docstatus": 1,
			},
		)

		if attendance:
			return True

	return False


@frappe.whitelist(methods=["POST"])
def add_users_to_raven(users):

	if isinstance(users, str):
		users = json.loads(users)

	failed_users = []
	success_users = []

	for user in users:
		user_doc = frappe.get_doc("User", user)

		if user_doc.role_profile_name:
			failed_users.append(user_doc)

		elif hasattr(user_doc, "role_profiles") and len(user_doc.role_profiles) > 0:
			failed_users.append(user_doc)
		else:
			user_doc.append("roles", {"role": "Raven User"})
			user_doc.save()
			success_users.append(user_doc)

	return {"success_users": success_users, "failed_users": failed_users}
