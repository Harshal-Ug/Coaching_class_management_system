// script.js
// Externalized JS for the portal. Expecting backend on http://localhost:8000

let studentSession = { id: null, name: null };

/**
 * Utility: fetch JSON from backend with error handling
 * endpoint: path relative to http://localhost:8000 (or full url)
 * options: fetch options
 */
async function fetchData(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `http://localhost:8000/${endpoint}`;
    try {
        const res = await fetch(url, options);
        // If backend returns non-JSON or error, try to capture useful message
        const contentType = res.headers.get('content-type') || '';
        if (!res.ok) {
            let text = await res.text();
            console.error('Fetch error', res.status, text);
            return { error: true, status: res.status, message: text };
        }
        if (contentType.includes('application/json')) {
            return await res.json();
        } else {
            // fallback - return plain text
            return { data: await res.text() };
        }
    } catch (err) {
        console.error('Network error', err);
        return null;
    }
}

/**
 * UI helpers
 */
function showElement(id) {
    document.getElementById(id).classList.remove('hidden');
}
function hideElement(id) {
    document.getElementById(id).classList.add('hidden');
}

function showMessage(el, text, type = 'success') {
    if (!el) return;
    el.textContent = text;
    el.className = `message ${type}`;
    el.classList.remove('hidden');
}

/**
 * Navigation
 */
function showPortal() {
    hideElement('landingPage');
    showElement('portalSection');
}

function showLanding() {
    showElement('landingPage');
    hideElement('portalSection');
    showElement('roleSelection');
    hideElement('studentLogin');
    hideElement('dashboardSection');
    hideElement('resultsSection');
}

function backToRoleSelection() {
    showElement('roleSelection');
    hideElement('studentLogin');
    hideElement('dashboardSection');
    hideElement('resultsSection');
}

function logoutRedirect() {
    backToRoleSelection();
    studentSession.id = null;
    studentSession.name = null;
    const msgDiv = document.getElementById('studentLoginMsg');
    if (msgDiv) hideElement('studentLoginMsg');
}

/**
 * Role selection
 */
function selectRole(role) {
    hideElement('roleSelection');
    if (role === 'student') {
        hideElement('dashboardSection');
        showElement('studentLogin');
    } else if (role === 'teacher') {
        hideElement('studentLogin');
        showElement('dashboardSection');
        showTeacherDashboard();
    }
}

/**
 * Login (student)
 */
async function studentLogin() {
    const id = document.getElementById('studentIdInput').value.trim();
    const pwd = document.getElementById('studentPwdInput').value.trim();
    const msgDiv = document.getElementById('studentLoginMsg');

    if (!id || !pwd) {
        showMessage(msgDiv, 'Please enter both ID and password', 'error');
        return;
    }

    // Call backend (matching your previous pattern)
    const resp = await fetchData(`students/${id}/login?password=${encodeURIComponent(pwd)}`);
    if (!resp || resp.error || !resp.id) {
        const m = resp && resp.message ? resp.message : 'Invalid credentials. Please check your ID and password.';
        showMessage(msgDiv, m, 'error');
        return;
    }

    studentSession.id = parseInt(id, 10);
    studentSession.name = `${resp.first_name || ''} ${resp.last_name || ''}`.trim() || null;
    showMessage(msgDiv, `Welcome back, ${resp.first_name || 'Student'}`, 'success');

    // Small delay so user sees welcome message
    setTimeout(() => {
        hideElement('studentLogin');
        showElement('dashboardSection');
        showStudentDashboard();
    }, 700);
}

/**
 * Display query + table helper
 * rows => array of objects OR single object
 */
function displayQueryAndTable(query, rows) {
    if (!rows) rows = [];
    // normalize
    if (!Array.isArray(rows)) {
        rows = [rows];
    }

    // If there are no rows, still show query and a "no results" message
    if (!rows.length) {
        showElement('resultsSection');
        document.getElementById('queryBox').innerText = query || '';
        const tableHead = document.getElementById('tableHead');
        const tableBody = document.getElementById('tableBody');
        tableHead.innerHTML = '';
        tableBody.innerHTML = `<tr><td>No records found.</td></tr>`;
        return;
    }

    showElement('resultsSection');
    document.getElementById('queryBox').innerText = query || '';

    const tableHead = document.getElementById('tableHead');
    const tableBody = document.getElementById('tableBody');
    tableHead.innerHTML = '';
    tableBody.innerHTML = '';

    const headers = Object.keys(rows[0] || {});
    const trHead = document.createElement('tr');
    if (headers.length === 0) {
        // Data is not plain objects (maybe a string)
        const th = document.createElement('th');
        th.innerText = 'Result';
        trHead.appendChild(th);
    } else {
        headers.forEach(h => {
            const th = document.createElement('th');
            th.innerText = h;
            trHead.appendChild(th);
        });
    }
    tableHead.appendChild(trHead);

    rows.forEach(row => {
        const tr = document.createElement('tr');
        if (headers.length === 0) {
            const td = document.createElement('td');
            td.innerText = typeof row === 'object' ? JSON.stringify(row) : String(row);
            tr.appendChild(td);
        } else {
            headers.forEach(h => {
                const td = document.createElement('td');
                const val = row[h];
                td.innerText = val === null || val === undefined ? '' : String(val);
                tr.appendChild(td);
            });
        }
        tableBody.appendChild(tr);
    });
}

/**
 * Student actions
 */
async function viewProfile() {
    if (!studentSession.id) { alert('Please login first'); return; }
    const data = await fetchData(`students/${studentSession.id}/profile`);
    if (!data) return;
    const rows = data.data !== undefined ? data.data : data;
    displayQueryAndTable(data.query || `SELECT * FROM students WHERE id = ${studentSession.id}`, Array.isArray(rows) ? rows : [rows]);
}

async function viewFees() {
    if (!studentSession.id) { alert('Please login first'); return; }
    const data = await fetchData(`students/${studentSession.id}/fees`);
    if (!data) return;
    displayQueryAndTable(data.query || `SELECT * FROM fees WHERE student_id = ${studentSession.id}`, data.data || []);
}

async function viewAttendanceStudent() {
    if (!studentSession.id) { alert('Please login first'); return; }
    const data = await fetchData(`students/${studentSession.id}/attendance`);
    if (!data) return;
    displayQueryAndTable(data.query || `SELECT * FROM attendance WHERE student_id = ${studentSession.id}`, data.data || []);
}

async function viewResultsStudent() {
    if (!studentSession.id) { alert('Please login first'); return; }
    const data = await fetchData(`students/${studentSession.id}/results`);
    if (!data) return;
    displayQueryAndTable(data.query || `SELECT * FROM results WHERE student_id = ${studentSession.id}`, data.data || []);
}

async function viewEnrolledCourses() {
    if (!studentSession.id) { alert('Please login first'); return; }
    const data = await fetchData(`students/${studentSession.id}/courses`);
    if (!data) return;
    displayQueryAndTable(data.query || `SELECT c.* FROM courses c JOIN enrollments e ON c.id = e.course_id WHERE e.student_id = ${studentSession.id}`, data.data || []);
}

/**
 * Teacher/admin actions
 */
async function addStudent() {
    const first = prompt("First name:"); if (!first) return;
    const last = prompt("Last name:"); if (!last) return;
    const email = prompt("Email:"); if (!email) return;
    const age = prompt("Age:"); if (!age) return;
    const params = new URLSearchParams({ first_name: first, last_name: last, email, age });
    try {
        const res = await fetch(`http://localhost:8000/students?${params.toString()}`, { method: 'POST' });
        const data = await res.json();
        displayQueryAndTable(data.query || 'INSERT INTO students ...', [data.data]);
    } catch (err) {
        console.error(err);
        alert('Error creating student.');
    }
}

async function viewStudents() {
    const data = await fetchData("students");
    if (!data) return;
    displayQueryAndTable(data.query || 'SELECT * FROM students', data.data || []);
}

async function studentById() {
    const id = prompt("Enter Student ID:"); if (!id) return;
    const data = await fetchData(`students/${id}`);
    if (!data) return;
    displayQueryAndTable(data.query || `SELECT * FROM students WHERE id = ${id}`, data.data ? [data.data] : []);
}

async function viewBatches() {
    const data = await fetchData("batches");
    if (!data) return;
    displayQueryAndTable(data.query || 'SELECT * FROM batches', data.data || []);
}

async function viewCourses() {
    const data = await fetchData("courses");
    if (!data) return;
    displayQueryAndTable(data.query || 'SELECT * FROM courses', data.data || []);
}

async function viewAttendanceTeacher() {
    const id = prompt("Enter Student ID:"); if (!id) return;
    const data = await fetchData(`students/${id}/attendance`);
    if (!data) return;
    displayQueryAndTable(data.query || `SELECT * FROM attendance WHERE student_id = ${id}`, data.data || []);
}

async function viewResultsTeacher() {
    const id = prompt("Enter Student ID:"); if (!id) return;
    const data = await fetchData(`students/${id}/results`);
    if (!data) return;
    displayQueryAndTable(data.query || `SELECT * FROM results WHERE student_id = ${id}`, data.data || []);
}

async function viewStudentQueries() {
    const data = await fetchData("queries_list");
    if (!data) return;
    displayQueryAndTable(data.query || 'SELECT * FROM queries', data.data || []);
}

/**
 * Dashboard builders
 */
function showStudentDashboard() {
    document.getElementById('dashboardTitle').textContent = studentSession.name ? `Student Dashboard — ${studentSession.name}` : 'Student Dashboard';
    const container = document.getElementById('actionsDiv');
    container.innerHTML = '';

    const buttons = [
        { text: 'My Profile', action: viewProfile },
        { text: 'Enrolled Courses', action: viewEnrolledCourses },
        { text: 'Fee Details', action: viewFees },
        { text: 'Attendance Records', action: viewAttendanceStudent },
        { text: 'Exam Results', action: viewResultsStudent }
    ];

    buttons.forEach(b => {
        const btn = document.createElement('button');
        btn.className = 'action-item';
        btn.textContent = b.text;
        btn.onclick = b.action;
        container.appendChild(btn);
    });
}

function showTeacherDashboard() {
    document.getElementById('dashboardTitle').textContent = 'Teacher Dashboard';
    const container = document.getElementById('actionsDiv');
    container.innerHTML = '';

    const buttons = [
        { text: 'Add New Student', action: addStudent },
        { text: 'View All Students', action: viewStudents },
        { text: 'Search Student', action: studentById },
        { text: 'View Batches', action: viewBatches },
        { text: 'View Courses', action: viewCourses },
        { text: 'Student Attendance', action: viewAttendanceTeacher },
        { text: 'Student Results', action: viewResultsTeacher },
        
    ];

    buttons.forEach(b => {
        const btn = document.createElement('button');
        btn.className = 'action-item';
        btn.textContent = b.text;
        btn.onclick = b.action;
        container.appendChild(btn);
    });
}

/* Expose some functions in case inline handlers need them in global scope */
window.showPortal = showPortal;
window.showLanding = showLanding;
window.selectRole = selectRole;
window.backToRoleSelection = backToRoleSelection;
window.logoutRedirect = logoutRedirect;
window.studentLogin = studentLogin;
