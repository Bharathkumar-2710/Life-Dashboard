// ---------------- 🌗 THEME TOGGLE ----------------
function toggleTheme() {
    document.body.classList.toggle("light");

    // save preference
    localStorage.setItem("theme", document.body.classList.contains("light") ? "light" : "dark");
}

// load saved theme
window.onload = function () {
    if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light");
    }
};


// ---------------- 📈 WEEKLY CHART ----------------
function loadWeeklyChart(labels, data) {
    const ctx = document.getElementById('weeklyChart');

    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Completed Tasks',
                data: data,
                borderColor: '#22c55e',
                backgroundColor: 'rgba(34,197,94,0.2)',
                tension: 0.4,
                fill: true
            }]
        }
    });
}


// ---------------- 📊 CATEGORY CHART ----------------
function loadCategoryChart(categoryData) {
    const ctx = document.getElementById('categoryChart');

    if (!ctx) return;

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(categoryData),
            datasets: [{
                data: Object.values(categoryData),
                backgroundColor: [
                    '#3b82f6',
                    '#22c55e',
                    '#f59e0b',
                    '#ef4444',
                    '#a855f7'
                ]
            }]
        }
    });
}


// ---------------- 🧲 DRAG & DROP ----------------
function enableDragAndDrop() {
    const list = document.getElementById('taskList');

    if (!list) return;

    new Sortable(list, {
        animation: 150,

        onEnd: function () {
            let order = [];

            document.querySelectorAll('.task').forEach(el => {
                order.push(el.dataset.id);
            });

            fetch('/reorder/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(order)
            })
            .then(res => res.json())
            .then(data => console.log("Order saved"))
            .catch(err => console.error(err));
        }
    });
}


// ---------------- 🔐 CSRF TOKEN ----------------
function getCSRFToken() {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();

            if (cookie.substring(0, 10) === ('csrftoken=')) {
                cookieValue = cookie.substring(10);
                break;
            }
        }
    }

    return cookieValue;
}


// ---------------- 🚀 INIT ----------------
document.addEventListener("DOMContentLoaded", function () {

    // parse data from HTML
    let weeklyLabels = window.weeklyLabels || [];
    let weeklyValues = window.weeklyValues || [];
    let categoryData = window.categoryData || {};

    // load features
    loadWeeklyChart(weeklyLabels, weeklyValues);
    loadCategoryChart(categoryData);
    enableDragAndDrop();

});