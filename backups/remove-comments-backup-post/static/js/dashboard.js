// Dashboard JavaScript

// Global variables
let allExpenses = [];
let categoryChart = null;
let monthlyChart = null;

// Modal Elements
const expenseModal = document.getElementById('expenseModal');
const addExpenseBtn = document.getElementById('addExpenseBtn');
const closeModal = document.getElementById('closeModal');
const cancelBtn = document.getElementById('cancelBtn');
const expenseForm = document.getElementById('expenseForm');
const modalTitle = document.getElementById('modalTitle');

// Search and Filter
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadDashboardStats();
    loadExpenses();

    // Set today's date as default
    const expenseDateField = document.getElementById('expenseDate');
    if (expenseDateField) {
        expenseDateField.valueAsDate = new Date();
    }
});

// Setup Event Listeners
function setupEventListeners() {
    // Modal controls
    if (addExpenseBtn) {
        addExpenseBtn.addEventListener('click', () => openModal());
    }
    if (closeModal) {
        closeModal.addEventListener('click', () => closeModalFunc());
    }
    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => closeModalFunc());
    }

    // Form submission
    if (expenseForm) {
        expenseForm.addEventListener('submit', handleExpenseSubmit);
    }

    // Search and filter
    if (searchInput) {
        searchInput.addEventListener('input', filterExpenses);
    }
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterExpenses);
    }

    // Export PDF
    const exportPdfBtn = document.getElementById('exportPdfBtn');
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener('click', exportPDF);
    }

    // Close modal on outside click
    if (expenseModal) {
        expenseModal.addEventListener('click', (e) => {
            if (e.target === expenseModal) {
                closeModalFunc();
            }
        });
    }

    // Menu toggle (Sidebar)
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        const currentTheme = localStorage.getItem('theme') || 'light';

        if (currentTheme === 'dark') {
            document.body.classList.add('dark-theme');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }

        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            const isDark = document.body.classList.contains('dark-theme');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
    }
}

// Load Dashboard Statistics
async function loadDashboardStats() {
    try {
        const response = await fetch('/api/dashboard/stats');
        const data = await response.json();

        // Update stats cards
        document.getElementById('totalSpending').textContent = `${currency}${data.total_spending.toFixed(2)}`;
        document.getElementById('monthlySpending').textContent = `${currency}${data.monthly_spending.toFixed(2)}`;
        document.getElementById('todaySpending').textContent = `${currency}${data.today_spending.toFixed(2)}`;

        // Create charts
        createCategoryChart(data.category_totals);
        createMonthlyChart(data.chart_data);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load Expenses
async function loadExpenses() {
    try {
        const response = await fetch('/api/expenses');
        const data = await response.json();
        allExpenses = data.expenses;
        displayExpenses(allExpenses);
    } catch (error) {
        console.error('Error loading expenses:', error);
        document.getElementById('expensesTableBody').innerHTML = '<tr><td colspan="6" class="text-center">Error loading expenses</td></tr>';
    }
}

// Display Expenses in Table
function displayExpenses(expenses) {
    const tbody = document.getElementById('expensesTableBody');

    if (expenses.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No expenses found</td></tr>';
        return;
    }

    tbody.innerHTML = expenses.map(expense => `
        <tr>
            <td>${formatDate(expense.date)}</td>
            <td>${expense.title}</td>
            <td><span class="badge badge-${getCategoryColor(expense.category)}">${expense.category}</span></td>
            <td>${currency}${parseFloat(expense.amount).toFixed(2)}</td>
            <td>${expense.notes || '-'}</td>
            <td>
                <button class="action-btn edit-btn" onclick="editExpense(${expense.id})" title="Edit">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="action-btn delete-btn" onclick="deleteExpense(${expense.id})" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Filter Expenses
function filterExpenses() {
    const searchTerm = searchInput.value.toLowerCase();
    const category = categoryFilter.value;

    let filtered = allExpenses;

    if (searchTerm) {
        filtered = filtered.filter(exp =>
            exp.title.toLowerCase().includes(searchTerm) ||
            (exp.notes && exp.notes.toLowerCase().includes(searchTerm))
        );
    }

    if (category) {
        filtered = filtered.filter(exp => exp.category === category);
    }

    displayExpenses(filtered);
}

// Modal Functions
function openModal(expense = null) {
    if (expense) {
        modalTitle.textContent = 'Edit Expense';
        document.getElementById('expenseId').value = expense.id;
        document.getElementById('expenseTitle').value = expense.title;
        document.getElementById('expenseCategory').value = expense.category;
        document.getElementById('expenseAmount').value = expense.amount;
        document.getElementById('expenseDate').value = expense.date;
        document.getElementById('expenseNotes').value = expense.notes || '';
    } else {
        modalTitle.textContent = 'Add Expense';
        expenseForm.reset();
        document.getElementById('expenseId').value = '';
        document.getElementById('expenseDate').valueAsDate = new Date();
    }
    expenseModal.classList.add('active');
}

function closeModalFunc() {
    expenseModal.classList.remove('active');
    expenseForm.reset();
}

// Handle Expense Submit
async function handleExpenseSubmit(e) {
    e.preventDefault();

    const expenseId = document.getElementById('expenseId').value;
    const expenseData = {
        title: document.getElementById('expenseTitle').value,
        category: document.getElementById('expenseCategory').value,
        amount: parseFloat(document.getElementById('expenseAmount').value),
        date: document.getElementById('expenseDate').value,
        notes: document.getElementById('expenseNotes').value
    };

    try {
        let response;
        if (expenseId) {
            // Update existing expense
            response = await fetch(`/api/expenses/${expenseId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expenseData)
            });
        } else {
            // Add new expense
            response = await fetch('/api/expenses', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expenseData)
            });
        }

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            closeModalFunc();
            loadExpenses();
            loadDashboardStats();
        } else {
            alert(data.error || 'An error occurred');
        }
    } catch (error) {
        console.error('Error saving expense:', error);
        alert('Failed to save expense');
    }
}

// Edit Expense
function editExpense(id) {
    const expense = allExpenses.find(exp => exp.id === id);
    if (expense) {
        openModal(expense);
    }
}

// Delete Expense
async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) {
        return;
    }

    try {
        const response = await fetch(`/api/expenses/${id}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            loadExpenses();
            loadDashboardStats();
        } else {
            alert(data.error || 'Failed to delete expense');
        }
    } catch (error) {
        console.error('Error deleting expense:', error);
        alert('Failed to delete expense');
    }
}

// Create Category Chart
function createCategoryChart(categoryTotals) {
    const ctx = document.getElementById('categoryChart').getContext('2d');

    if (categoryChart) {
        categoryChart.destroy();
    }

    const labels = Object.keys(categoryTotals);
    const data = Object.values(categoryTotals);

    if (labels.length === 0) {
        ctx.font = '16px Arial';
        ctx.fillText('No data available', 10, 50);
        return;
    }

    categoryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40',
                    '#FF6384'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + currency + context.parsed.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

// Create Monthly Chart
function createMonthlyChart(chartData) {
    const ctx = document.getElementById('monthlyChart').getContext('2d');

    if (monthlyChart) {
        monthlyChart.destroy();
    }

    if (chartData.labels.length === 0) {
        ctx.font = '16px Arial';
        ctx.fillText('No data available', 10, 50);
        return;
    }

    monthlyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Monthly Spending',
                data: chartData.data,
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Spending: ' + currency + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return currency + value;
                        }
                    }
                }
            }
        }
    });
}

// Export PDF
function exportPDF() {
    window.location.href = '/api/export/pdf';
}

// Utility Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function getCategoryColor(category) {
    const colors = {
        'Food': 'success',
        'Transport': 'info',
        'Shopping': 'warning',
        'Entertainment': 'primary',
        'Bills': 'danger',
        'Health': 'success',
        'Other': 'secondary'
    };
    return colors[category] || 'secondary';
}