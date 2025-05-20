import LogRocket from 'logrocket';

const LOGROCKET_APP_ID = '1dtbnm/trabajo_final';

// Initialize LogRocket with app ID
export function initializeLogRocket() {
    LogRocket.init(LOGROCKET_APP_ID);
}

// Identify user when logged in
export function identifyUser(userData) {
    if (userData && userData.id) {
        LogRocket.identify(userData.id, {
            name: userData.name || '',
            email: userData.email || '',
            // Add any additional user properties here
        });
    }
}

// Error handling
window.onerror = function(message, source, lineno, colno, error) {
    LogRocket.captureException(error);
};

// Custom event tracking
export function logCustomEvent(eventName, eventData) {
    LogRocket.track(eventName, eventData);
}

// Page view tracking
export function logPageView(pageName) {
    LogRocket.track('page_viewed', {
        page: pageName,
        url: window.location.href
    });
}

// Initialize by default if window.USER_DATA exists
if (typeof window !== 'undefined') {
    initializeLogRocket();
    if (window.USER_DATA) {
        identifyUser(window.USER_DATA);
    }
}
