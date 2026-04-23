// ---------- CHECK JS LOADED ----------
console.log("✅ JS Loaded");

// ---------- PAGE LOAD ----------
window.onload = function () {
    console.log("🚀 Page fully loaded");
};

// ---------- DELETE CONFIRM ----------
document.addEventListener("DOMContentLoaded", function () {
    const deleteLinks = document.querySelectorAll("a[href*='delete']");

    deleteLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            const confirmDelete = confirm("Are you sure you want to delete this task?");
            if (!confirmDelete) {
                e.preventDefault();
            }
        });
    });
});

// ---------- TASK HOVER EFFECT ----------
document.addEventListener("DOMContentLoaded", function () {
    const tasks = document.querySelectorAll(".task");

    tasks.forEach(task => {
        task.addEventListener("mouseenter", () => {
            task.style.transform = "scale(1.03)";
        });

        task.addEventListener("mouseleave", () => {
            task.style.transform = "scale(1)";
        });
    });
});

// ---------- SUCCESS ALERT ON ADD ----------
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function () {
            console.log("📝 Task added");
        });
    }
});

// ---------- SIMPLE FADE-IN EFFECT ----------
document.addEventListener("DOMContentLoaded", function () {
    const tasks = document.querySelectorAll(".task");

    tasks.forEach((task, index) => {
        task.style.opacity = 0;
        task.style.transition = "opacity 0.5s ease";

        setTimeout(() => {
            task.style.opacity = 1;
        }, index * 100);
    });
});