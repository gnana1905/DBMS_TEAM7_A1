// EaseStay Hotel Management System - JavaScript
// Application State
let currentUser = null;
let rooms = [];
let currentBooking = null;
let currentFilter = 'all';

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    initializeDatePickers();
    checkExistingLogin();
    checkBackendConnection().then(isConnected => {
        if (isConnected) {
            loadRoomsFromAPI();
        }
    });
}

// Setup Event Listeners
function setupEventListeners() {
    // Login Form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Register Form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    // Payment Form
    const paymentForm = document.getElementById('paymentForm');
    if (paymentForm) {
        paymentForm.addEventListener('submit', handlePayment);
    }

    // Landing Page Booking Form
    const landingForm = document.getElementById('landingBookingForm');
    if (landingForm) {
        landingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            checkAvailability();
        });
    }

    // User Interface Booking Form
    const userForm = document.getElementById('userBookingForm');
    if (userForm) {
        userForm.addEventListener('submit', function(e) {
            e.preventDefault();
            checkAvailability();
        });
    }

    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        const modals = ['loginModal', 'registerModal', 'paymentModal', 'roomStatusModal'];
        modals.forEach(modalId => {
            const modal = document.getElementById(modalId);
            if (event.target === modal) {
                if (modalId === 'loginModal') closeLoginModal();
                if (modalId === 'registerModal') closeRegisterModal();
                if (modalId === 'paymentModal') closePaymentModal();
                if (modalId === 'roomStatusModal') closeRoomStatusModal();
            }
        });
    });
}

// API Helper Function
async function apiRequest(endpoint, method = 'GET', data = null, requiresAuth = false) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    if (requiresAuth && currentUser && currentUser.token) {
        options.headers['Authorization'] = `Bearer ${currentUser.token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        // Check if response is ok before trying to parse JSON
        if (!response.ok) {
            let errorMessage = 'API request failed';
            try {
                const errorResult = await response.json();
                errorMessage = errorResult.error || `HTTP ${response.status}: ${response.statusText}`;
            } catch (e) {
                errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API Error:', error);
        // If it's a network error, provide more helpful message
        if (error.message === 'Failed to fetch' || error.name === 'TypeError') {
            throw new Error('Cannot connect to server. Please ensure the backend server is running on http://localhost:5000');
        }
        throw error;
    }
}

// Check Backend Connection on Load
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✓ Backend server is running');
            return true;
        }
    } catch (error) {
        console.error('✗ Backend server is NOT running:', error);
        showNotification('Backend server is not running. Please start it using: cd backend && python app.py', 'error', 10000);
        return false;
    }
    return false;
}

// Initialize Date Pickers
function initializeDatePickers() {
    const today = new Date().toISOString().split('T')[0];
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowStr = tomorrow.toISOString().split('T')[0];

    // Landing page dates
    const checkin = document.getElementById('checkin');
    const checkout = document.getElementById('checkout');
    if (checkin) {
        checkin.min = today;
        checkin.value = today;
        checkin.addEventListener('change', function() {
            if (checkout) {
                checkout.min = this.value;
                if (checkout.value < this.value) {
                    checkout.value = this.value;
                }
            }
        });
    }
    if (checkout) {
        checkout.min = tomorrowStr;
        checkout.value = tomorrowStr;
    }

    // User interface dates
    const userCheckin = document.getElementById('userCheckin');
    const userCheckout = document.getElementById('userCheckout');
    if (userCheckin) {
        userCheckin.min = today;
        userCheckin.value = today;
        userCheckin.addEventListener('change', function() {
            if (userCheckout) {
                userCheckout.min = this.value;
                if (userCheckout.value < this.value) {
                    userCheckout.value = this.value;
                }
            }
            // Update available rooms count when date changes
            updateAvailableRoomsCount();
            // Save date preferences
            saveUserPreferences();
        });
    }
    if (userCheckout) {
        userCheckout.min = tomorrowStr;
        userCheckout.value = tomorrowStr;
        userCheckout.addEventListener('change', function() {
            // Update available rooms count when date changes
            updateAvailableRoomsCount();
            // Save date preferences
            saveUserPreferences();
        });
    }

    // Landing page dates - also update available rooms count
    if (checkin) {
        checkin.addEventListener('change', function() {
            updateAvailableRoomsCount();
        });
    }
    if (checkout) {
        checkout.addEventListener('change', function() {
            updateAvailableRoomsCount();
        });
    }
}

// Load Rooms from API
async function loadRoomsFromAPI() {
    try {
        const response = await apiRequest('/rooms');
        rooms = response.rooms.map(room => ({
            id: room._id,
            _id: room._id,
            name: room.name,
            type: room.type,
            price: room.price,
            image: room.image,
            description: room.description,
            capacity: room.capacity,
            amenities: room.amenities || [],
            status: room.status,
            roomNumber: room.roomNumber,
            needs_cleaning: room.needs_cleaning || false
        }));

        renderRooms();
        updateAvailableRoomsCount();
        
        // Update interfaces if they're active
        if (document.getElementById('adminInterface')?.classList.contains('active')) {
            updateAdminRooms();
            loadAdminStats();
        }
        if (document.getElementById('userInterface')?.classList.contains('active')) {
            loadUserRooms();
        }
        if (document.getElementById('staffInterface')?.classList.contains('active')) {
            loadStaffTasks();
        }
    } catch (error) {
        console.error('Failed to load rooms:', error);
        showNotification('Failed to load rooms', 'error');
    }
}

// Render Rooms on Landing Page
function renderRooms() {
    const roomsGrid = document.getElementById('roomsGrid');
    if (!roomsGrid) return;

    // Filter to show only available rooms on landing page (visible to users)
    // Available rooms are visible to users
    const availableRooms = rooms.filter(r => r.status === 'available' && !r.needs_cleaning);

    if (availableRooms.length === 0) {
        roomsGrid.innerHTML = '<div class="empty-state">No rooms available</div>';
        return;
    }

    roomsGrid.innerHTML = availableRooms.map(room => `
        <div class="room-card">
            <div class="room-image">
                <img src="${room.image || 'https://via.placeholder.com/400x250?text=Room'}" 
                     alt="${room.name}" 
                     onerror="this.src='https://via.placeholder.com/400x250?text=Room'">
                <span class="room-status-badge ${room.status}">${room.status}</span>
            </div>
            <div class="room-info">
                <h3>${room.name}</h3>
                <p>${room.description || ''}</p>
                <div class="room-meta">
                    <span><i class="fas fa-user-friends"></i> ${room.capacity} Guests</span>
                    <span><i class="fas fa-door-open"></i> Room ${room.roomNumber}</span>
                </div>
                <div class="room-features">
                    ${(room.amenities || []).slice(0, 3).map(a => `<span class="feature-tag">${a}</span>`).join('')}
                </div>
                <div class="room-footer">
                    <div class="room-price">₹${room.price} <span>/night</span></div>
                    <button class="btn-book" onclick="bookRoom('${room._id}')" 
                            ${room.status !== 'available' ? 'disabled' : ''}>
                        <i class="fas fa-calendar-check"></i> Book Now
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Handle Login
async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;

    if (!email || !password) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    try {
        const response = await apiRequest('/login', 'POST', {
            email: email,
            password: password,
            role: role
        });

        currentUser = {
            ...response.user,
            token: response.token,
            name: `${response.user.firstName} ${response.user.lastName}`
        };

        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        closeLoginModal();
        
        // Save login details
        try {
            await apiRequest('/user/login-log', 'POST', {
                login_time: new Date().toISOString(),
                email: email,
                role: role
            }, true);
        } catch (error) {
            console.error('Failed to save login log:', error);
        }
        
        redirectToInterface(role);
        showNotification(`Welcome back, ${currentUser.name}!`, 'success');
        await loadRoomsFromAPI();
    } catch (error) {
        showNotification(error.message || 'Login failed', 'error');
    }
}

// Handle Register
async function handleRegister(e) {
    e.preventDefault();

    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('regEmail').value;
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        showNotification('Passwords do not match', 'error');
        return;
    }

    try {
        const response = await apiRequest('/register', 'POST', {
            firstName: firstName,
            lastName: lastName,
            email: email,
            phone: phone,
            password: password
        });

        currentUser = {
            ...response.user,
            token: response.token,
            name: `${response.user.firstName} ${response.user.lastName}`
        };

        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        closeRegisterModal();
        redirectToInterface('guest');
        showNotification('Registration successful!', 'success');
    } catch (error) {
        showNotification(error.message || 'Registration failed', 'error');
    }
}

// Check Availability
async function checkAvailability() {
    const isUserInterface = document.getElementById('userInterface')?.classList.contains('active');
    const checkin = isUserInterface ? 
        document.getElementById('userCheckin')?.value : 
        document.getElementById('checkin')?.value;
    const checkout = isUserInterface ? 
        document.getElementById('userCheckout')?.value : 
        document.getElementById('checkout')?.value;

    if (!checkin || !checkout) {
        showNotification('Please select dates', 'error');
        return;
    }

    if (new Date(checkin) >= new Date(checkout)) {
        showNotification('Check-out must be after check-in', 'error');
        return;
    }

    try {
        const response = await apiRequest(`/rooms/available?checkin=${checkin}&checkout=${checkout}`);
        showNotification(`Found ${response.rooms.length} available rooms!`, 'success');
        
        if (isUserInterface) {
            await loadUserRooms();
        } else {
            document.getElementById('rooms')?.scrollIntoView({ behavior: 'smooth' });
        }
    } catch (error) {
        showNotification('Failed to check availability', 'error');
    }
}

// Book Room
async function bookRoom(roomId) {
    if (!currentUser) {
        showNotification('Please login to book', 'error');
        openLoginModal();
        return;
    }

    // Only guests and admins can book rooms
    if (currentUser.role !== 'guest' && currentUser.role !== 'admin') {
        showNotification('Only guests and administrators can book rooms', 'error');
        return;
    }

    const room = rooms.find(r => r._id === roomId);
    if (!room || room.status !== 'available') {
        showNotification('Room not available', 'error');
        return;
    }

    const isUserInterface = document.getElementById('userInterface')?.classList.contains('active');
    const checkin = isUserInterface ? 
        document.getElementById('userCheckin')?.value : 
        document.getElementById('checkin')?.value;
    const checkout = isUserInterface ? 
        document.getElementById('userCheckout')?.value : 
        document.getElementById('checkout')?.value;
    const guests = parseInt(isUserInterface ? 
        document.getElementById('userGuests')?.value : 
        document.getElementById('guests')?.value || '2');

    if (!checkin || !checkout) {
        showNotification('Please select dates', 'error');
        return;
    }

    try {
        const response = await apiRequest('/book', 'POST', {
            room_id: roomId,
            checkin_date: checkin,
            checkout_date: checkout,
            guests: guests,
            rooms: 1
        }, true);

        currentBooking = response.booking;
        openPaymentModal();
        await loadRoomsFromAPI();
        showNotification('Booking created! Complete payment.', 'success');
    } catch (error) {
        showNotification(error.message || 'Booking failed', 'error');
    }
}

// Handle Payment
async function handlePayment(e) {
    e.preventDefault();

    if (!currentBooking) {
        showNotification('No booking found', 'error');
        return;
    }

    try {
        const response = await apiRequest('/payment', 'POST', {
            booking_id: currentBooking._id,
            amount: currentBooking.total_price,
            payment_method: 'card'
        }, true);

        closePaymentModal();
        showNotification(response.message || 'Room booked successfully!', 'success');
        currentBooking = null;

        // Refresh rooms and bookings
        await loadRoomsFromAPI();
        if (currentUser?.role === 'guest') {
            await loadUserBookings();
            // Ensure we're on the user interface to see the bookings
            if (!document.getElementById('userInterface')?.classList.contains('active')) {
                redirectToInterface('guest');
            }
        }
        if (currentUser?.role === 'admin') {
            await loadAdminBookings();
        }
        if (currentUser?.role === 'staff') {
            await loadStaffTasks();
        }
    } catch (error) {
        showNotification(error.message || 'Payment failed', 'error');
    }
}

// Redirect to Interface
function redirectToInterface(role) {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));

    if (role === 'guest') {
        document.getElementById('userInterface').classList.add('active');
        loadUserInterface();
    } else if (role === 'admin') {
        document.getElementById('adminInterface').classList.add('active');
        loadAdminInterface();
    } else if (role === 'staff') {
        document.getElementById('staffInterface').classList.add('active');
        loadStaffInterface();
    }
}

// Load User Interface
async function loadUserInterface() {
    const userNameEl = document.getElementById('userName');
    if (userNameEl && currentUser) {
        userNameEl.textContent = currentUser.name || currentUser.firstName || 'Guest';
    }
    await loadUserBookings();
    await loadUserRooms();
}

// Load User Bookings
async function loadUserBookings() {
    const bookingsList = document.getElementById('userBookingsList');
    if (!bookingsList) return;

    try {
        const response = await apiRequest('/bookings', 'GET', null, true);
        const bookings = response.bookings || [];

        if (bookings.length === 0) {
            bookingsList.innerHTML = '<div class="empty-state">No bookings found</div>';
            return;
        }

        bookingsList.innerHTML = bookings.map(booking => `
            <div class="booking-card">
                <div class="booking-header">
                    <h4>${booking.room_name || 'Room'}</h4>
                    <span class="status-badge ${booking.status}">${booking.status}</span>
                </div>
                <div class="booking-details">
                    <p><i class="fas fa-calendar-check"></i> Check-in: ${booking.checkin_date}</p>
                    <p><i class="fas fa-calendar-times"></i> Check-out: ${booking.checkout_date}</p>
                    <p><i class="fas fa-user-friends"></i> Guests: ${booking.guests}</p>
                    <p><i class="fas fa-rupee-sign"></i> Total: ₹${booking.total_price}</p>
                </div>
                ${booking.status === 'pending' ? `
                <div class="booking-actions">
                    <button class="btn-danger btn-sm" onclick="deleteBooking('${booking._id}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
                ` : ''}
            </div>
        `).join('');
    } catch (error) {
        bookingsList.innerHTML = '<div class="error-state">Failed to load bookings</div>';
    }
}

// Update Available Rooms Count
function updateAvailableRoomsCount() {
    const countElement = document.getElementById('availableRoomsCount');
    if (!countElement) return;

    // Count only rooms visible to users (available and not needing cleaning)
    const availableRooms = rooms.filter(r => 
        r.status === 'available' && 
        !r.needs_cleaning && 
        r.status !== 'occupied' && 
        r.status !== 'maintenance'
    );
    countElement.textContent = `(${availableRooms.length})`;
}

// Scroll to User Bookings
function scrollToUserBookings() {
    const bookingsSection = document.getElementById('userBookingsList');
    if (bookingsSection) {
        bookingsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Save User Preferences (login details and dates)
async function saveUserPreferences() {
    if (!currentUser) return;

    try {
        const checkin = document.getElementById('userCheckin')?.value || document.getElementById('checkin')?.value;
        const checkout = document.getElementById('userCheckout')?.value || document.getElementById('checkout')?.value;

        if (checkin && checkout) {
            await apiRequest('/user/preferences', 'POST', {
                checkin_date: checkin,
                checkout_date: checkout,
                login_time: new Date().toISOString()
            }, true);
        }
    } catch (error) {
        console.error('Failed to save preferences:', error);
    }
}

// Load User Rooms
async function loadUserRooms() {
    const roomsGrid = document.getElementById('userRoomsGrid');
    if (!roomsGrid) return;

    // Visibility rules: Users can only see available rooms (not occupied, maintenance, or needs_cleaning)
    const availableRooms = rooms.filter(r => 
        r.status === 'available' && 
        !r.needs_cleaning && 
        r.status !== 'occupied' && 
        r.status !== 'maintenance'
    );
    
    // Update count
    updateAvailableRoomsCount();

    if (availableRooms.length === 0) {
        roomsGrid.innerHTML = '<div class="empty-state">No available rooms</div>';
        return;
    }

    roomsGrid.innerHTML = availableRooms.map(room => `
        <div class="room-card-compact">
            <img src="${room.image || 'https://via.placeholder.com/300x200?text=Room'}" 
                 alt="${room.name}"
                 onerror="this.src='https://via.placeholder.com/300x200?text=Room'">
            <div class="room-card-body">
                <h4>${room.name}</h4>
                <p>${room.description || ''}</p>
                <div class="room-meta">
                    <span><i class="fas fa-user-friends"></i> ${room.capacity}</span>
                    <span><i class="fas fa-door-open"></i> ${room.roomNumber}</span>
                </div>
                <div class="room-footer">
                    <div class="room-price">₹${room.price}/night</div>
                    <button class="btn-book" onclick="bookRoom('${room._id}')">
                        <i class="fas fa-calendar-check"></i> Book
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Load Admin Interface
async function loadAdminInterface() {
    loadAdminStats();
    updateAdminRooms();
    await loadAdminBookings();
}

// Load Admin Stats
function loadAdminStats() {
    const statsGrid = document.getElementById('adminStatsGrid');
    if (!statsGrid) return;

    const total = rooms.length;
    const available = rooms.filter(r => r.status === 'available').length;
    const occupied = rooms.filter(r => r.status === 'occupied').length;
    const maintenance = rooms.filter(r => r.status === 'maintenance').length;
    const occupancyRate = total > 0 ? Math.round((occupied / total) * 100) : 0;

    statsGrid.innerHTML = `
        <div class="stat-card">
            <div class="stat-icon primary">
                <i class="fas fa-bed"></i>
            </div>
            <div>
                <div class="stat-number">${total}</div>
                <div class="stat-label">Total Rooms</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon success">
                <i class="fas fa-check-circle"></i>
            </div>
            <div>
                <div class="stat-number">${available}</div>
                <div class="stat-label">Available</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon warning">
                <i class="fas fa-users"></i>
            </div>
            <div>
                <div class="stat-number">${occupied}</div>
                <div class="stat-label">Occupied</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon danger">
                <i class="fas fa-tools"></i>
            </div>
            <div>
                <div class="stat-number">${maintenance}</div>
                <div class="stat-label">Maintenance</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon info">
                <i class="fas fa-chart-line"></i>
            </div>
            <div>
                <div class="stat-number">${occupancyRate}%</div>
                <div class="stat-label">Occupancy Rate</div>
            </div>
        </div>
    `;
}

// Load Admin Rooms
function updateAdminRooms() {
    const roomsGrid = document.getElementById('adminRoomsGrid');
    if (!roomsGrid || !document.getElementById('adminInterface')?.classList.contains('active')) return;

    // Admin can see ALL rooms regardless of status
    const filteredRooms = currentFilter === 'all' ? rooms : rooms.filter(r => r.status === currentFilter);
    
    if (filteredRooms.length === 0) {
        roomsGrid.innerHTML = '<div class="empty-state">No rooms found</div>';
        return;
    }

    roomsGrid.innerHTML = filteredRooms.map(room => `
        <div class="room-management-card ${room.status}">
            <div class="room-header">
                <h4>${room.name}</h4>
                <span class="status-badge ${room.status}">${room.status}</span>
                ${room.needs_cleaning ? '<span class="status-badge cleaning">Needs Cleaning</span>' : ''}
            </div>
            <p><i class="fas fa-door-open"></i> Room ${room.roomNumber}</p>
            <p><i class="fas fa-user-friends"></i> ${room.capacity} guests</p>
            <p><i class="fas fa-rupee-sign"></i> ₹${room.price}/night</p>
            <div class="room-actions">
                <button class="btn-action ${room.status === 'available' ? 'active' : ''}" 
                        onclick="changeRoomStatus('${room._id}', 'available')">
                    Available
                </button>
                <button class="btn-action ${room.status === 'occupied' ? 'active' : ''}" 
                        onclick="changeRoomStatus('${room._id}', 'occupied')">
                    Occupied
                </button>
                <button class="btn-action ${room.status === 'maintenance' ? 'active' : ''}" 
                        onclick="changeRoomStatus('${room._id}', 'maintenance')">
                    Maintenance
                </button>
                <button class="btn-action btn-cleaning" 
                        onclick="markRoomForCleaning('${room._id}')">
                    <i class="fas fa-broom"></i> Mark for Cleaning
                </button>
            </div>
        </div>
    `).join('');
}

// Filter Rooms
function filterRooms(status) {
    currentFilter = status;
    // Update active tab
    document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.classList.remove('active');
        const tabText = tab.textContent.trim().toLowerCase();
        if ((status === 'all' && tabText === 'all') ||
            (status === 'available' && tabText === 'available') ||
            (status === 'occupied' && tabText === 'occupied') ||
            (status === 'maintenance' && tabText === 'maintenance')) {
            tab.classList.add('active');
        }
    });
    updateAdminRooms();
}

// Change Room Status
// Variables for room status change
let pendingRoomStatusChange = null;

async function changeRoomStatus(roomId, newStatus) {
    const room = rooms.find(r => r._id === roomId || r.id === roomId);
    if (!room) {
        showNotification('Room not found', 'error');
        return;
    }

    // Store pending change
    pendingRoomStatusChange = {
        roomId: roomId,
        roomName: room.name,
        roomNumber: room.roomNumber,
        currentStatus: room.status,
        newStatus: newStatus,
        action: 'status'
    };

    // Show popup modal
    openRoomStatusModal();
}

// Mark Room for Cleaning (Admin)
async function markRoomForCleaning(roomId) {
    const room = rooms.find(r => r._id === roomId || r.id === roomId);
    if (!room) {
        showNotification('Room not found', 'error');
        return;
    }

    // Store pending change
    pendingRoomStatusChange = {
        roomId: roomId,
        roomName: room.name,
        roomNumber: room.roomNumber,
        currentStatus: room.status,
        newStatus: 'needs_cleaning',
        action: 'cleaning'
    };

    // Show popup modal
    openRoomStatusModal();
}

// Open Room Status Modal
function openRoomStatusModal() {
    if (!pendingRoomStatusChange) return;

    const modal = document.getElementById('roomStatusModal');
    const infoDiv = document.getElementById('roomStatusInfo');
    const currentBadge = document.getElementById('currentStatusBadge');
    const newBadge = document.getElementById('newStatusBadge');

    // Set room information
    infoDiv.innerHTML = `
        <div class="room-info-item">
            <strong>Room:</strong> ${pendingRoomStatusChange.roomName}
        </div>
        <div class="room-info-item">
            <strong>Room Number:</strong> ${pendingRoomStatusChange.roomNumber}
        </div>
    `;

    // Set current status badge
    currentBadge.textContent = pendingRoomStatusChange.currentStatus;
    currentBadge.className = `status-badge ${pendingRoomStatusChange.currentStatus}`;

    // Set new status badge
    if (pendingRoomStatusChange.action === 'cleaning') {
        newBadge.textContent = 'Needs Cleaning';
        newBadge.className = 'status-badge cleaning';
    } else {
        newBadge.textContent = pendingRoomStatusChange.newStatus;
        newBadge.className = `status-badge ${pendingRoomStatusChange.newStatus}`;
    }

    modal.style.display = 'block';
}

// Close Room Status Modal
function closeRoomStatusModal() {
    const modal = document.getElementById('roomStatusModal');
    modal.style.display = 'none';
    pendingRoomStatusChange = null;
}

// Confirm Room Status Change
async function confirmRoomStatusChange() {
    if (!pendingRoomStatusChange) return;

    // Disable confirm button to prevent double clicks
    const confirmBtn = document.getElementById('confirmStatusChangeBtn');
    const originalBtnText = confirmBtn ? confirmBtn.innerHTML : '';
    if (confirmBtn) {
        confirmBtn.disabled = true;
        confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    }

    try {
        let response;
        const roomId = pendingRoomStatusChange.roomId;
        
        if (pendingRoomStatusChange.action === 'cleaning') {
            response = await apiRequest(`/room/${roomId}/cleaning`, 'PUT', {}, true);
            showNotification('Room marked for cleaning', 'success');
        } else {
            response = await apiRequest(`/room/${roomId}/status`, 'PUT', { 
                status: pendingRoomStatusChange.newStatus 
            }, true);
            showNotification(`Room status updated to ${pendingRoomStatusChange.newStatus}`, 'success');
        }

        // Refresh rooms after status change
        await loadRoomsFromAPI();
        closeRoomStatusModal();
    } catch (error) {
        console.error('Room status change error:', error);
        let errorMessage = 'Failed to update room status';
        
        if (error.message) {
            errorMessage = error.message;
        } else if (typeof error === 'string') {
            errorMessage = error;
        } else if (error.toString) {
            errorMessage = error.toString();
        }
        
        showNotification(errorMessage, 'error');
    } finally {
        // Re-enable confirm button
        if (confirmBtn) {
            confirmBtn.disabled = false;
            confirmBtn.innerHTML = originalBtnText;
        }
    }
}

// Load Admin Bookings
async function loadAdminBookings() {
    const bookingsTable = document.getElementById('adminBookingsTable');
    if (!bookingsTable) return;

    try {
        const response = await apiRequest('/bookings/all', 'GET', null, true);
        const bookings = response.bookings || [];

        if (bookings.length === 0) {
            bookingsTable.innerHTML = '<tr><td colspan="6" class="empty-state">No bookings</td></tr>';
            return;
        }

        bookingsTable.innerHTML = bookings.map(booking => {
            const userDetails = booking.user_details || {};
            const userName = userDetails.firstName && userDetails.lastName 
                ? `${userDetails.firstName} ${userDetails.lastName}` 
                : userDetails.email || (booking.user_id || '').substring(0, 8) + '...';
            return `
            <tr>
                <td>${(booking._id || '').substring(0, 8)}...</td>
                <td>${booking.room_name || booking.room_details?.name || 'N/A'} (${booking.room_number || booking.room_details?.roomNumber || ''})</td>
                <td>${userName}</td>
                <td>${booking.checkin_date || ''}</td>
                <td>${booking.checkout_date || ''}</td>
                <td><span class="status-badge ${booking.status || 'pending'}">${booking.status || 'pending'}</span></td>
            </tr>
        `;
        }).join('');
    } catch (error) {
        bookingsTable.innerHTML = '<tr><td colspan="6" class="error-state">Failed to load</td></tr>';
    }
}

// Delete Booking
async function deleteBooking(bookingId) {
    if (!confirm('Are you sure you want to delete this booking?')) {
        return;
    }

    try {
        await apiRequest(`/booking/${bookingId}`, 'DELETE', null, true);
        showNotification('Booking deleted successfully', 'success');
        
        // Refresh bookings
        await loadUserBookings();
        await loadRoomsFromAPI();
    } catch (error) {
        showNotification(error.message || 'Failed to delete booking', 'error');
    }
}

// Load Staff Interface
async function loadStaffInterface() {
    await loadStaffTasks();
}

// Load Staff Tasks
async function loadStaffTasks() {
    const tasksList = document.getElementById('staffTasksList');
    if (!tasksList) return;

    try {
        // Get only rooms that need cleaning from API
        const response = await apiRequest('/rooms/cleaning', 'GET', null, true);
        const cleaningRooms = response.rooms || [];
        
        document.getElementById('cleaningTasks').textContent = cleaningRooms.length;
        document.getElementById('occupiedRooms').textContent = cleaningRooms.length;

        if (cleaningRooms.length === 0) {
            tasksList.innerHTML = '<div class="empty-state">No cleaning tasks</div>';
            return;
        }

        tasksList.innerHTML = cleaningRooms.map(room => `
            <div class="task-card">
                <div class="task-info">
                    <h4><i class="fas fa-door-open"></i> Room ${room.roomNumber || 'N/A'}</h4>
                    <p>${room.name || 'Room'}</p>
                    <span><i class="fas fa-user-friends"></i> ${room.capacity || 0} guests</span>
                    <span class="status-badge ${room.status || 'maintenance'}">${room.status || 'maintenance'}</span>
                    ${room.needs_cleaning ? '<span class="status-badge cleaning">Needs Cleaning</span>' : ''}
                </div>
                <button class="btn-complete" onclick="markTaskComplete('${room._id}')">
                    <i class="fas fa-check"></i> Mark Clean
                </button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load cleaning tasks:', error);
        tasksList.innerHTML = `<div class="error-state">Failed to load tasks: ${error.message || 'Unknown error'}</div>`;
    }
}

// Mark Task Complete
async function markTaskComplete(roomId) {
    try {
        await apiRequest(`/room/${roomId}/clean`, 'PUT', {}, true);
        await loadRoomsFromAPI();
        await loadStaffTasks();
        showNotification('Room marked as clean', 'success');
    } catch (error) {
        showNotification(error.message || 'Failed to mark room as clean', 'error');
    }
}

// Load Staff Booked Rooms
async function loadStaffBookedRooms() {
    const bookedRoomsGrid = document.getElementById('staffBookedRooms');
    if (!bookedRoomsGrid) return;

    try {
        const response = await apiRequest('/bookings/all', 'GET', null, true);
        const bookings = response.bookings?.filter(b => b.status === 'confirmed') || [];

        if (bookings.length === 0) {
            bookedRoomsGrid.innerHTML = '<div class="empty-state">No booked rooms</div>';
            return;
        }

        bookedRoomsGrid.innerHTML = bookings.map(booking => `
            <div class="booked-room-card">
                <h4><i class="fas fa-door-open"></i> Room ${booking.room_number || ''}</h4>
                <p>${booking.room_name || 'Room'}</p>
                <div class="booking-info">
                    <p><i class="fas fa-calendar-check"></i> ${booking.checkin_date}</p>
                    <p><i class="fas fa-calendar-times"></i> ${booking.checkout_date}</p>
                    <p><i class="fas fa-user-friends"></i> ${booking.guests} guests</p>
                </div>
            </div>
        `).join('');
    } catch (error) {
        bookedRoomsGrid.innerHTML = '<div class="error-state">Failed to load</div>';
    }
}

// Show Main Page
function showMainPage() {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    document.getElementById('landingPage').classList.add('active');
    loadRoomsFromAPI();
}

// Logout
function logout() {
    currentUser = null;
    currentBooking = null;
    localStorage.removeItem('currentUser');
    showMainPage();
    showNotification('Logged out successfully', 'info');
}

// Check Existing Login
function checkExistingLogin() {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            if (currentUser && currentUser.token) {
                redirectToInterface(currentUser.role);
            }
        } catch (e) {
            localStorage.removeItem('currentUser');
        }
    }
}

// Modal Functions
function openLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

function openRegisterModal() {
    closeLoginModal();
    document.getElementById('registerModal').style.display = 'block';
}

function closeRegisterModal() {
    document.getElementById('registerModal').style.display = 'none';
}

function openPaymentModal() {
    if (!currentBooking) return;
    const modal = document.getElementById('paymentModal');
    const summary = document.getElementById('paymentSummary');
    
    const nights = Math.ceil((new Date(currentBooking.checkout_date) - new Date(currentBooking.checkin_date)) / (1000 * 60 * 60 * 24));
    
    summary.innerHTML = `
        <div class="summary-item">
            <span>Room:</span>
            <strong>${currentBooking.room_name} (${currentBooking.room_number})</strong>
        </div>
        <div class="summary-item">
            <span>Check-in:</span>
            <strong>${currentBooking.checkin_date}</strong>
        </div>
        <div class="summary-item">
            <span>Check-out:</span>
            <strong>${currentBooking.checkout_date}</strong>
        </div>
        <div class="summary-item">
            <span>Nights:</span>
            <strong>${nights}</strong>
        </div>
        <div class="summary-item total">
            <span>Total:</span>
            <strong>₹${currentBooking.total_price}</strong>
        </div>
    `;
    
    modal.style.display = 'block';
}

function closePaymentModal() {
    document.getElementById('paymentModal').style.display = 'none';
}

// Toggle Mobile Menu
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    navMenu?.classList.toggle('active');
}

// Show Notification
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), duration);
}
