// Javascript for Popover (Used for the Popover on the Sidebar)

document.addEventListener("DOMContentLoaded", () => {

	// popovers Initialization
	$(() => {
		$('.popover-btn').popover({
			animation: true,
			container: 'body',
			trigger: 'focus', // Dismiss the popover
			html: true // Enable the content to be HTML
			//template: ''
		})
	})
});
