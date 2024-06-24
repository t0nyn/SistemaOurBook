const sidebarCollapsible = document.querySelectorAll("li > .collapse");

sidebarCollapsible.forEach((collapsible) => {
	const liParent = collapsible.parentElement;
	const collapseBtn = liParent.querySelector(".sidebar-collapse-button");
	const collapseChevron = collapseBtn.querySelector(".collapse-chevron");

	collapsible.addEventListener(
		"show.bs.collapse",
		() => {
			liParent.classList.remove("bg-white");
			liParent.classList.add("bg-collapsed-show");

			collapseBtn.classList.remove("bg-white");
			collapseBtn.classList.add("bg-collapsed-show");

			collapseChevron.classList.add("rotate-180");
		},
		false
	);

	collapsible.addEventListener(
		"hide.bs.collapse",
		() => {
			liParent.classList.remove("bg-collapsed-show");
			liParent.classList.add("bg-white");

			collapseBtn.classList.remove("bg-collapsed-show");
			collapseBtn.classList.add("bg-white");

			collapseChevron.classList.remove("rotate-180");
		},
		false
	);
});
