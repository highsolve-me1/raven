
export interface RavenSettings{
	name: string
	creation: string
	modified: string
	owner: string
	modified_by: string
	docstatus: 0 | 1 | 2
	parent?: string
	parentfield?: string
	parenttype?: string
	idx?: number
	/**	Automatically add system users to Raven : Check	*/
	auto_add_system_users?: 0 | 1
	/**	Show Raven on Desk : Check	*/
	show_raven_on_desk?: 0 | 1
	/**	Tenor API Key : Data	*/
	tenor_api_key?: string
	/**	Automatically Create a Channel for each Department : Check - If checked, a channel will be created in Raven for each department and employees will be synced with Raven Users.	*/
	auto_create_department_channel?: 0 | 1
	/**	Department Channel Type : Select	*/
	department_channel_type?: "Public" | "Private"
	/**	Show if a user is on leave : Check	*/
	show_if_a_user_is_on_leave?: 0 | 1
}